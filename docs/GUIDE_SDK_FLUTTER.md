# Guide d'Intégration du SDK Dart/Flutter CoinDétude

Ce guide est destiné à l'équipe frontend **Flutter** pour consommer l'API backend officielle de **CoinDétude** via le SDK fortement typé généré (`dart-dio`).

---

## 1. Vue d'Ensemble & Architecture du SDK

Le SDK `coindetude_api` est généré automatiquement à partir de la spécification OpenAPI enrichie du backend. Il repose sur :
- **Dio** (`^5.0.0`) : Client HTTP performant avec support des interceptors, annulation de requêtes, et suivi de téléchargement/upload.
- **BuiltValue** (`built_value`) : Modèles immuables avec sérialisation/désérialisation JSON stricte et null-safety.
- **APIs modulaires par domaine** :
  - `AuthApi` : Inscription, challenge OTP (SMS / WhatsApp), connexion mot de passe, refresh tokens, logout.
  - `ReferentialApi` : Consultation publique (avec cache) des cycles, niveaux, séries, matières, chapitres et ressources.
  - `SyncApi` : Moteur de synchronisation hors-ligne avec contrôle d'idempotence (`Idempotency-Key`).
  - `UploadsApi` : Obtention d'URLs présignées S3/R2 et confirmation d'upload binaire.
  - `HealthApi` : Sondes de disponibilité (`health`, `readiness`).

---

## 2. Installation dans votre Application Flutter

### Dans votre `pubspec.yaml`

Vous pouvez consommer le SDK de deux manières :

#### Option A : Dépendance Git (recommandé en équipe)
```yaml
dependencies:
  flutter:
    sdk: flutter
  dio: ^5.7.0
  built_value: ^8.9.2
  built_collection: ^5.1.1
  coindetude_api:
    git:
      url: https://github.com/sylvainTIASSOU/coindetude-backend.git
      path: packages/coindetude_api
      ref: main # ou tag de version : v0.1.0
```

#### Option B : Dépendance de chemin local (monorepo ou développement local)
```yaml
dependencies:
  flutter:
    sdk: flutter
  dio: ^5.7.0
  built_value: ^8.9.2
  built_collection: ^5.1.1
  coindetude_api:
    path: ../coindetude-backend/packages/coindetude_api
```

Puis lancez :
```bash
flutter pub get
```

---

## 3. Initialisation du Client & Intercepteur d'Authentification

Pour gérer l'injection du token JWT et son renouvellement automatique transparent (refresh token) sur expiration (HTTP 401), créez un service d'API centralisé.

### `lib/core/api/api_client.dart`

```dart
import 'package:coindetude_api/coindetude_api.dart';
import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class ApiClient {
  static final ApiClient _instance = ApiClient._internal();
  factory ApiClient() => _instance;

  late final Dio dio;
  late final CoindetudeApi api;
  final FlutterSecureStorage _storage = const FlutterSecureStorage();

  ApiClient._internal() {
    dio = Dio(BaseOptions(
      baseUrl: _resolveBaseUrl(),
      connectTimeout: const Duration(seconds: 15),
      receiveTimeout: const Duration(seconds: 15),
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
    ));

    // Ajout de l'intercepteur de sécurité JWT
    dio.interceptors.add(_AuthInterceptor(dio: dio, storage: _storage));

    // Initialisation du SDK avec notre Dio configuré
    api = CoindetudeApi(dio: dio);
  }

  static String _resolveBaseUrl() {
    // Adapter selon la plateforme de test :
    // - Android émulateur : http://10.0.2.2:8000
    // - iOS simulateur / Desktop : http://localhost:8000
    // - Staging : https://staging-api.coindetude.tg
    // - Prod : https://api.coindetude.tg
    return const String.fromEnvironment(
      'API_BASE_URL',
      defaultValue: 'http://10.0.2.2:8000',
    );
  }
}
```

### `lib/core/api/auth_interceptor.dart`

Cet intercepteur intercepte les requêtes pour injecter le token d'accès et renouvelle automatiquement le token si le backend renvoie un code **401 Unauthorized**.

```dart
import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class _AuthInterceptor extends QueuedInterceptor {
  final Dio dio;
  final FlutterSecureStorage storage;

  _AuthInterceptor({required this.dio, required this.storage});

  @override
  Future<void> onRequest(
    RequestOptions options,
    RequestInterceptorHandler handler,
  ) async {
    final token = await storage.read(key: 'access_token');
    if (token != null && token.isNotEmpty) {
      options.headers['Authorization'] = 'Bearer $token';
    }
    handler.next(options);
  }

  @override
  Future<void> onError(DioException err, ErrorInterceptorHandler handler) async {
    if (err.response?.statusCode == 401) {
      final refreshToken = await storage.read(key: 'refresh_token');
      if (refreshToken != null) {
        try {
          // Requête directe de refresh pour éviter les boucles infinies
          final refreshDio = Dio(BaseOptions(baseUrl: dio.options.baseUrl));
          final response = await refreshDio.post(
            '/api/v1/auth/refresh',
            data: {'refresh_token': refreshToken},
          );

          final newAccessToken = response.data['access_token'];
          final newRefreshToken = response.data['refresh_token'];

          // Sauvegarde des nouveaux tokens
          await storage.write(key: 'access_token', value: newAccessToken);
          if (newRefreshToken != null) {
            await storage.write(key: 'refresh_token', value: newRefreshToken);
          }

          // Rejouer la requête d'origine avec le nouveau token
          final requestOptions = err.requestOptions;
          requestOptions.headers['Authorization'] = 'Bearer $newAccessToken';
          final retryResponse = await dio.fetch(requestOptions);
          return handler.resolve(retryResponse);
        } catch (refreshErr) {
          // Si le refresh échoue, déconnexion de l'utilisateur
          await storage.deleteAll();
          // Déclencher redirection vers la page de login
        }
      }
    }
    handler.next(err);
  }
}
```

---

## 4. Exemples Concrets d'Utilisation

### A. Authentification & Flow OTP

#### 1. Inscription initiale
```dart
final authApi = ApiClient().api.getAuthApi();

try {
  final registerBuilder = RegisterRequestBuilder()
    ..phone = '+22890123456'
    ..firstName = 'Koffi'
    ..lastName = 'Abalo'
    ..password = 'Password123'
    ..role = UserRole.student;

  final response = await authApi.register(
    registerRequest: registerBuilder.build(),
  );

  // Le serveur renvoie un code 202 avec challenge_id
  final challengeId = response.data?.challengeId;
  print('OTP envoyé via SMS/WhatsApp. Challenge: $challengeId');
} on DioException catch (e) {
  print('Erreur inscription : ${e.response?.data}');
}
```

#### 2. Validation du code OTP
```dart
try {
  final verifyBuilder = VerifyOTPRequestBuilder()
    ..challengeId = challengeId // UUID reçu précédemment
    ..code = '123456'
    ..rememberDevice = true;

  final response = await authApi.verifyOtp(
    verifyOTPRequest: verifyBuilder.build(),
  );

  final tokens = response.data?.tokens;
  final user = response.data?.user;

  // Stocker les tokens de manière sécurisée
  await storage.write(key: 'access_token', value: tokens?.accessToken);
  await storage.write(key: 'refresh_token', value: tokens?.refreshToken);

  print('Connecté avec succès ! Bienvenue ${user?.firstName}');
} on DioException catch (e) {
  print('Code OTP invalide ou expiré : ${e.response?.data}');
}
```

---

### B. Référentiel Pédagogique (Public & Caché)

Les endpoints du référentiel sont publics et optimisés avec un cache Redis côté serveur et les en-têtes `Cache-Control`.

```dart
final referentialApi = ApiClient().api.getReferentialApi();

// 1. Lister les niveaux (ex: Lycée)
final levelsResponse = await referentialApi.listLevels(
  cycle: Cycle.lyceeModerne,
  limit: 20,
);

for (final level in levelsResponse.data?.items ?? []) {
  print('Niveau : ${level.name} (ID: ${level.id})');
}

// 2. Lister les matières d'un niveau
final subjectsResponse = await referentialApi.listSubjects(
  levelId: levelId,
);

for (final subject in subjectsResponse.data?.items ?? []) {
  print('Matière : ${subject.name} - Code: ${subject.code}');
}
```

---

### C. Synchronisation Hors-ligne (Offline-First)

Pour supporter l'usage dans les zones à connectivité intermittente au Togo, les mutations d'état créées hors-ligne sont enregistrées dans une base locale (ex: Drift ou Isar) puis poussées avec le header `Idempotency-Key` (UUIDv4).

```dart
import 'package:uuid/uuid.dart';

final syncApi = ApiClient().api.getSyncApi();
final idempotencyKey = const Uuid().v4();

try {
  final eventBuilder = SyncEventRequestBuilder()
    ..entityType = SyncEntityType.planningTask
    ..operation = SyncOperation.create
    ..clientTs = DateTime.now().toUtc()
    ..payload = {
      'id': const Uuid().v4(),
      'title': 'Révision Mathématiques BEPC',
      'scheduled_for': '2026-09-25T08:00:00Z',
    };

  final response = await syncApi.applyEvent(
    idempotencyKey: idempotencyKey,
    syncEventRequest: eventBuilder.build(),
  );

  print('Événement synchronisé : ${response.data?.status}');
} on DioException catch (e) {
  if (e.response?.statusCode == 409) {
    print('Conflit détecté : résolution selon stratégie LWW.');
  }
}
```

---

### D. Upload Direct de Fichiers (S3 / Cloudflare R2)

Pour préserver les ressources du serveur backend, aucun fichier binaire ne passe par FastAPI :

```dart
import 'dart:io';

final uploadsApi = ApiClient().api.getUploadsApi();
final file = File('/chemin/vers/avatar.webp');
final fileSizeKb = (await file.length()) ~/ 1024;

// 1. Demande d'URL pré-signée
final presignBuilder = PresignRequestBuilder()
  ..fileName = 'mon_avatar.webp'
  ..fileType = 'image/webp'
  ..sizeKb = fileSizeKb
  ..purpose = UploadPurpose.avatar;

final presignResponse = await uploadsApi.presign(
  presignRequest: presignBuilder.build(),
);

final fileId = presignResponse.data!.fileId;
final uploadUrl = presignResponse.data!.uploadUrl;
final requiredHeaders = presignResponse.data!.headers.toMap();

// 2. Upload binaire direct vers le stockage Cloud avec progression
final uploadDio = Dio();
await uploadDio.put(
  uploadUrl,
  data: file.openRead(),
  options: Options(
    headers: {
      ...requiredHeaders,
      'Content-Length': await file.length(),
    },
  ),
  onSendProgress: (sent, total) {
    print('Progression : ${(sent / total * 100).toStringAsFixed(1)}%');
  },
);

// 3. Confirmation auprès du backend
final confirmResponse = await uploadsApi.confirm(fileId: fileId);
print('Fichier confirmé et disponible à : ${confirmResponse.data?.url}');
```

---

## 5. Bonnes Pratiques & Gestion des Erreurs

1. **Vérification de la Connectivité** :
   Utilisez le package `connectivity_plus` pour empiler les mutations dans votre base locale en cas d'absence de réseau avant d'appeler `SyncApi`.
2. **Gestion des Réponses 422 (Validation)** :
   Le backend renvoie les détails de validation Pydantic sous format standard `{"detail": [...]}`. Affichez les messages directement sous les champs formulaires Flutter.
3. **Mise à jour du SDK** :
   À chaque mise à jour du contrat OpenAPI, lancez `./scripts/generate_sdk.sh` ou récupérez le tag de release publié par le job CI.


import 'package:test/test.dart';
import 'package:coindetude_api/coindetude_api.dart';


/// tests for HealthApi
void main() {
  final instance = CoindetudeApi().getHealthApi();

  group(HealthApi, () {
    // Health
    //
    // Liveness : le process répond, sans dépendance externe.
    //
    //Future<BuiltMap<String, String>> health() async
    test('test health', () async {
      // TODO
    });

    // Readiness
    //
    // Readiness probe : l'app peut-elle servir du trafic ?  Vérifie : - Connexion PostgreSQL (SELECT 1) - Connexion Redis (PING)
    //
    //Future<JsonObject> readiness() async
    test('test readiness', () async {
      // TODO
    });

  });
}

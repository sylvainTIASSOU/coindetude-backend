# coindetude_api.api.HealthApi

## Load the API package
```dart
import 'package:coindetude_api/api.dart';
```

All URIs are relative to *http://localhost:8000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**health**](HealthApi.md#health) | **GET** /api/v1/health | Health
[**readiness**](HealthApi.md#readiness) | **GET** /api/v1/health/ready | Readiness


# **health**
> BuiltMap<String, String> health()

Health

Liveness : le process répond, sans dépendance externe.

### Example
```dart
import 'package:coindetude_api/api.dart';

final api = CoindetudeApi().getHealthApi();

try {
    final response = api.health();
    print(response);
} catch on DioException (e) {
    print('Exception when calling HealthApi->health: $e\n');
}
```

### Parameters
This endpoint does not need any parameter.

### Return type

**BuiltMap&lt;String, String&gt;**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **readiness**
> JsonObject readiness()

Readiness

Readiness probe : l'app peut-elle servir du trafic ?  Vérifie : - Connexion PostgreSQL (SELECT 1) - Connexion Redis (PING)

### Example
```dart
import 'package:coindetude_api/api.dart';

final api = CoindetudeApi().getHealthApi();

try {
    final response = api.readiness();
    print(response);
} catch on DioException (e) {
    print('Exception when calling HealthApi->readiness: $e\n');
}
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**JsonObject**](JsonObject.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


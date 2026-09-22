# coindetude_api.api.SyncApi

## Load the API package
```dart
import 'package:coindetude_api/api.dart';
```

All URIs are relative to *http://localhost:8000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**applyEvent**](SyncApi.md#applyevent) | **POST** /api/v1/sync/apply-event | Synchronise une mutation offline (idempotent)


# **applyEvent**
> JsonObject applyEvent(idempotencyKey, syncEventRequest)

Synchronise une mutation offline (idempotent)

Applique un événement offline avec idempotence stricte.

### Example
```dart
import 'package:coindetude_api/api.dart';
// TODO Configure OAuth2 access token for authorization: OAuth2PasswordBearer
//defaultApiClient.getAuthentication<OAuth>('OAuth2PasswordBearer').accessToken = 'YOUR_ACCESS_TOKEN';

final api = CoindetudeApi().getSyncApi();
final String idempotencyKey = idempotencyKey_example; // String | UUID v4 obligatoire. Même clé + même body = même réponse.
final SyncEventRequest syncEventRequest = ; // SyncEventRequest | 

try {
    final response = api.applyEvent(idempotencyKey, syncEventRequest);
    print(response);
} catch on DioException (e) {
    print('Exception when calling SyncApi->applyEvent: $e\n');
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **idempotencyKey** | **String**| UUID v4 obligatoire. Même clé + même body = même réponse. | 
 **syncEventRequest** | [**SyncEventRequest**](SyncEventRequest.md)|  | 

### Return type

[**JsonObject**](JsonObject.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


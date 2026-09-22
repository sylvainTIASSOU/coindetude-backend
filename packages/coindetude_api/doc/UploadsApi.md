# coindetude_api.api.UploadsApi

## Load the API package
```dart
import 'package:coindetude_api/api.dart';
```

All URIs are relative to *http://localhost:8000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**confirm**](UploadsApi.md#confirm) | **POST** /api/v1/uploads/{file_id}/confirm | Confirme l&#39;upload et valide le fichier côté serveur
[**presign**](UploadsApi.md#presign) | **POST** /api/v1/uploads/presign | Génère une URL PUT pré-signée pour upload direct


# **confirm**
> ConfirmResponse confirm(fileId)

Confirme l'upload et valide le fichier côté serveur

### Example
```dart
import 'package:coindetude_api/api.dart';
// TODO Configure OAuth2 access token for authorization: OAuth2PasswordBearer
//defaultApiClient.getAuthentication<OAuth>('OAuth2PasswordBearer').accessToken = 'YOUR_ACCESS_TOKEN';

final api = CoindetudeApi().getUploadsApi();
final String fileId = 38400000-8cf0-11bd-b23e-10b96e4ef00d; // String | 

try {
    final response = api.confirm(fileId);
    print(response);
} catch on DioException (e) {
    print('Exception when calling UploadsApi->confirm: $e\n');
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fileId** | **String**|  | 

### Return type

[**ConfirmResponse**](ConfirmResponse.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **presign**
> PresignResponse presign(presignRequest)

Génère une URL PUT pré-signée pour upload direct

### Example
```dart
import 'package:coindetude_api/api.dart';
// TODO Configure OAuth2 access token for authorization: OAuth2PasswordBearer
//defaultApiClient.getAuthentication<OAuth>('OAuth2PasswordBearer').accessToken = 'YOUR_ACCESS_TOKEN';

final api = CoindetudeApi().getUploadsApi();
final PresignRequest presignRequest = ; // PresignRequest | 

try {
    final response = api.presign(presignRequest);
    print(response);
} catch on DioException (e) {
    print('Exception when calling UploadsApi->presign: $e\n');
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **presignRequest** | [**PresignRequest**](PresignRequest.md)|  | 

### Return type

[**PresignResponse**](PresignResponse.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


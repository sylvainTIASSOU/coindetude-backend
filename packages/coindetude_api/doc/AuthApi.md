# coindetude_api.api.AuthApi

## Load the API package
```dart
import 'package:coindetude_api/api.dart';
```

All URIs are relative to *http://localhost:8000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**forgotPassword**](AuthApi.md#forgotpassword) | **POST** /api/v1/auth/forgot-password | Forgot Password
[**login**](AuthApi.md#login) | **POST** /api/v1/auth/login | Étape 1 — Login : envoie un OTP (ou skip si device de confiance)
[**logout**](AuthApi.md#logout) | **POST** /api/v1/auth/logout | Logout
[**logoutAll**](AuthApi.md#logoutall) | **POST** /api/v1/auth/logout-all | Logout All
[**refresh**](AuthApi.md#refresh) | **POST** /api/v1/auth/refresh | Refresh
[**register**](AuthApi.md#register) | **POST** /api/v1/auth/register | Étape 1 — Inscription : envoie un OTP
[**resendOtp**](AuthApi.md#resendotp) | **POST** /api/v1/auth/resend-otp | Resend Otp
[**resetPassword**](AuthApi.md#resetpassword) | **POST** /api/v1/auth/reset-password | Reset Password
[**verifyOtp**](AuthApi.md#verifyotp) | **POST** /api/v1/auth/verify-otp | Verify Otp


# **forgotPassword**
> OTPSentResponse forgotPassword(forgotPasswordRequest)

Forgot Password

### Example
```dart
import 'package:coindetude_api/api.dart';

final api = CoindetudeApi().getAuthApi();
final ForgotPasswordRequest forgotPasswordRequest = ; // ForgotPasswordRequest | 

try {
    final response = api.forgotPassword(forgotPasswordRequest);
    print(response);
} catch on DioException (e) {
    print('Exception when calling AuthApi->forgotPassword: $e\n');
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **forgotPasswordRequest** | [**ForgotPasswordRequest**](ForgotPasswordRequest.md)|  | 

### Return type

[**OTPSentResponse**](OTPSentResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **login**
> JsonObject login(loginRequest, xTrustedDevice)

Étape 1 — Login : envoie un OTP (ou skip si device de confiance)

### Example
```dart
import 'package:coindetude_api/api.dart';

final api = CoindetudeApi().getAuthApi();
final LoginRequest loginRequest = ; // LoginRequest | 
final String xTrustedDevice = xTrustedDevice_example; // String | 

try {
    final response = api.login(loginRequest, xTrustedDevice);
    print(response);
} catch on DioException (e) {
    print('Exception when calling AuthApi->login: $e\n');
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **loginRequest** | [**LoginRequest**](LoginRequest.md)|  | 
 **xTrustedDevice** | **String**|  | [optional] 

### Return type

[**JsonObject**](JsonObject.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **logout**
> logout(xRefreshToken, refreshRequest)

Logout

### Example
```dart
import 'package:coindetude_api/api.dart';
// TODO Configure OAuth2 access token for authorization: OAuth2PasswordBearer
//defaultApiClient.getAuthentication<OAuth>('OAuth2PasswordBearer').accessToken = 'YOUR_ACCESS_TOKEN';

final api = CoindetudeApi().getAuthApi();
final String xRefreshToken = xRefreshToken_example; // String | 
final RefreshRequest refreshRequest = ; // RefreshRequest | 

try {
    api.logout(xRefreshToken, refreshRequest);
} catch on DioException (e) {
    print('Exception when calling AuthApi->logout: $e\n');
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **xRefreshToken** | **String**|  | [optional] 
 **refreshRequest** | [**RefreshRequest**](RefreshRequest.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **logoutAll**
> logoutAll()

Logout All

### Example
```dart
import 'package:coindetude_api/api.dart';
// TODO Configure OAuth2 access token for authorization: OAuth2PasswordBearer
//defaultApiClient.getAuthentication<OAuth>('OAuth2PasswordBearer').accessToken = 'YOUR_ACCESS_TOKEN';

final api = CoindetudeApi().getAuthApi();

try {
    api.logoutAll();
} catch on DioException (e) {
    print('Exception when calling AuthApi->logoutAll: $e\n');
}
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **refresh**
> TokenPair refresh(xRefreshToken, refreshRequest)

Refresh

### Example
```dart
import 'package:coindetude_api/api.dart';

final api = CoindetudeApi().getAuthApi();
final String xRefreshToken = xRefreshToken_example; // String | 
final RefreshRequest refreshRequest = ; // RefreshRequest | 

try {
    final response = api.refresh(xRefreshToken, refreshRequest);
    print(response);
} catch on DioException (e) {
    print('Exception when calling AuthApi->refresh: $e\n');
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **xRefreshToken** | **String**|  | [optional] 
 **refreshRequest** | [**RefreshRequest**](RefreshRequest.md)|  | [optional] 

### Return type

[**TokenPair**](TokenPair.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **register**
> OTPSentResponse register(registerRequest)

Étape 1 — Inscription : envoie un OTP

### Example
```dart
import 'package:coindetude_api/api.dart';

final api = CoindetudeApi().getAuthApi();
final RegisterRequest registerRequest = ; // RegisterRequest | 

try {
    final response = api.register(registerRequest);
    print(response);
} catch on DioException (e) {
    print('Exception when calling AuthApi->register: $e\n');
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **registerRequest** | [**RegisterRequest**](RegisterRequest.md)|  | 

### Return type

[**OTPSentResponse**](OTPSentResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **resendOtp**
> OTPSentResponse resendOtp(resendOTPRequest)

Resend Otp

### Example
```dart
import 'package:coindetude_api/api.dart';

final api = CoindetudeApi().getAuthApi();
final ResendOTPRequest resendOTPRequest = ; // ResendOTPRequest | 

try {
    final response = api.resendOtp(resendOTPRequest);
    print(response);
} catch on DioException (e) {
    print('Exception when calling AuthApi->resendOtp: $e\n');
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **resendOTPRequest** | [**ResendOTPRequest**](ResendOTPRequest.md)|  | 

### Return type

[**OTPSentResponse**](OTPSentResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **resetPassword**
> AuthResponse resetPassword(resetPasswordRequest)

Reset Password

### Example
```dart
import 'package:coindetude_api/api.dart';

final api = CoindetudeApi().getAuthApi();
final ResetPasswordRequest resetPasswordRequest = ; // ResetPasswordRequest | 

try {
    final response = api.resetPassword(resetPasswordRequest);
    print(response);
} catch on DioException (e) {
    print('Exception when calling AuthApi->resetPassword: $e\n');
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **resetPasswordRequest** | [**ResetPasswordRequest**](ResetPasswordRequest.md)|  | 

### Return type

[**AuthResponse**](AuthResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **verifyOtp**
> AuthResponse verifyOtp(verifyOTPRequest)

Verify Otp

### Example
```dart
import 'package:coindetude_api/api.dart';

final api = CoindetudeApi().getAuthApi();
final VerifyOTPRequest verifyOTPRequest = ; // VerifyOTPRequest | 

try {
    final response = api.verifyOtp(verifyOTPRequest);
    print(response);
} catch on DioException (e) {
    print('Exception when calling AuthApi->verifyOtp: $e\n');
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **verifyOTPRequest** | [**VerifyOTPRequest**](VerifyOTPRequest.md)|  | 

### Return type

[**AuthResponse**](AuthResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


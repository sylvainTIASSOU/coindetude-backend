# coindetude_api.api.AdminreferentialApi

## Load the API package
```dart
import 'package:coindetude_api/api.dart';
```

All URIs are relative to *http://localhost:8000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**createChapter**](AdminreferentialApi.md#createchapter) | **POST** /api/v1/admin/referential/chapters | Create Chapter
[**createLevel**](AdminreferentialApi.md#createlevel) | **POST** /api/v1/admin/referential/levels | Crée un niveau scolaire
[**createResource**](AdminreferentialApi.md#createresource) | **POST** /api/v1/admin/referential/resources | Create Resource
[**createSeries**](AdminreferentialApi.md#createseries) | **POST** /api/v1/admin/referential/series | Create Series
[**createSubject**](AdminreferentialApi.md#createsubject) | **POST** /api/v1/admin/referential/subjects | Create Subject
[**deleteChapter**](AdminreferentialApi.md#deletechapter) | **DELETE** /api/v1/admin/referential/chapters/{id_} | Delete Chapter
[**deleteLevel**](AdminreferentialApi.md#deletelevel) | **DELETE** /api/v1/admin/referential/levels/{id_} | Supprime un niveau scolaire
[**deleteResource**](AdminreferentialApi.md#deleteresource) | **DELETE** /api/v1/admin/referential/resources/{id_} | Delete Resource
[**deleteSeries**](AdminreferentialApi.md#deleteseries) | **DELETE** /api/v1/admin/referential/series/{id_} | Delete Series
[**deleteSubject**](AdminreferentialApi.md#deletesubject) | **DELETE** /api/v1/admin/referential/subjects/{id_} | Delete Subject
[**updateChapter**](AdminreferentialApi.md#updatechapter) | **PUT** /api/v1/admin/referential/chapters/{id_} | Update Chapter
[**updateLevel**](AdminreferentialApi.md#updatelevel) | **PUT** /api/v1/admin/referential/levels/{id_} | Met à jour un niveau scolaire
[**updateResource**](AdminreferentialApi.md#updateresource) | **PUT** /api/v1/admin/referential/resources/{id_} | Update Resource
[**updateSeries**](AdminreferentialApi.md#updateseries) | **PUT** /api/v1/admin/referential/series/{id_} | Update Series
[**updateSubject**](AdminreferentialApi.md#updatesubject) | **PUT** /api/v1/admin/referential/subjects/{id_} | Update Subject


# **createChapter**
> ChapterRead createChapter(chapterCreate)

Create Chapter

### Example
```dart
import 'package:coindetude_api/api.dart';
// TODO Configure OAuth2 access token for authorization: OAuth2PasswordBearer
//defaultApiClient.getAuthentication<OAuth>('OAuth2PasswordBearer').accessToken = 'YOUR_ACCESS_TOKEN';

final api = CoindetudeApi().getAdminreferentialApi();
final ChapterCreate chapterCreate = ; // ChapterCreate | 

try {
    final response = api.createChapter(chapterCreate);
    print(response);
} catch on DioException (e) {
    print('Exception when calling AdminreferentialApi->createChapter: $e\n');
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **chapterCreate** | [**ChapterCreate**](ChapterCreate.md)|  | 

### Return type

[**ChapterRead**](ChapterRead.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **createLevel**
> LevelRead createLevel(levelCreate)

Crée un niveau scolaire

### Example
```dart
import 'package:coindetude_api/api.dart';
// TODO Configure OAuth2 access token for authorization: OAuth2PasswordBearer
//defaultApiClient.getAuthentication<OAuth>('OAuth2PasswordBearer').accessToken = 'YOUR_ACCESS_TOKEN';

final api = CoindetudeApi().getAdminreferentialApi();
final LevelCreate levelCreate = ; // LevelCreate | 

try {
    final response = api.createLevel(levelCreate);
    print(response);
} catch on DioException (e) {
    print('Exception when calling AdminreferentialApi->createLevel: $e\n');
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **levelCreate** | [**LevelCreate**](LevelCreate.md)|  | 

### Return type

[**LevelRead**](LevelRead.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **createResource**
> ResourceRead createResource(resourceCreate)

Create Resource

### Example
```dart
import 'package:coindetude_api/api.dart';
// TODO Configure OAuth2 access token for authorization: OAuth2PasswordBearer
//defaultApiClient.getAuthentication<OAuth>('OAuth2PasswordBearer').accessToken = 'YOUR_ACCESS_TOKEN';

final api = CoindetudeApi().getAdminreferentialApi();
final ResourceCreate resourceCreate = ; // ResourceCreate | 

try {
    final response = api.createResource(resourceCreate);
    print(response);
} catch on DioException (e) {
    print('Exception when calling AdminreferentialApi->createResource: $e\n');
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **resourceCreate** | [**ResourceCreate**](ResourceCreate.md)|  | 

### Return type

[**ResourceRead**](ResourceRead.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **createSeries**
> SeriesRead createSeries(seriesCreate)

Create Series

### Example
```dart
import 'package:coindetude_api/api.dart';
// TODO Configure OAuth2 access token for authorization: OAuth2PasswordBearer
//defaultApiClient.getAuthentication<OAuth>('OAuth2PasswordBearer').accessToken = 'YOUR_ACCESS_TOKEN';

final api = CoindetudeApi().getAdminreferentialApi();
final SeriesCreate seriesCreate = ; // SeriesCreate | 

try {
    final response = api.createSeries(seriesCreate);
    print(response);
} catch on DioException (e) {
    print('Exception when calling AdminreferentialApi->createSeries: $e\n');
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **seriesCreate** | [**SeriesCreate**](SeriesCreate.md)|  | 

### Return type

[**SeriesRead**](SeriesRead.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **createSubject**
> SubjectRead createSubject(subjectCreate)

Create Subject

### Example
```dart
import 'package:coindetude_api/api.dart';
// TODO Configure OAuth2 access token for authorization: OAuth2PasswordBearer
//defaultApiClient.getAuthentication<OAuth>('OAuth2PasswordBearer').accessToken = 'YOUR_ACCESS_TOKEN';

final api = CoindetudeApi().getAdminreferentialApi();
final SubjectCreate subjectCreate = ; // SubjectCreate | 

try {
    final response = api.createSubject(subjectCreate);
    print(response);
} catch on DioException (e) {
    print('Exception when calling AdminreferentialApi->createSubject: $e\n');
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **subjectCreate** | [**SubjectCreate**](SubjectCreate.md)|  | 

### Return type

[**SubjectRead**](SubjectRead.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **deleteChapter**
> deleteChapter(id)

Delete Chapter

### Example
```dart
import 'package:coindetude_api/api.dart';
// TODO Configure OAuth2 access token for authorization: OAuth2PasswordBearer
//defaultApiClient.getAuthentication<OAuth>('OAuth2PasswordBearer').accessToken = 'YOUR_ACCESS_TOKEN';

final api = CoindetudeApi().getAdminreferentialApi();
final String id = 38400000-8cf0-11bd-b23e-10b96e4ef00d; // String | 

try {
    api.deleteChapter(id);
} catch on DioException (e) {
    print('Exception when calling AdminreferentialApi->deleteChapter: $e\n');
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **String**|  | 

### Return type

void (empty response body)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **deleteLevel**
> deleteLevel(id)

Supprime un niveau scolaire

### Example
```dart
import 'package:coindetude_api/api.dart';
// TODO Configure OAuth2 access token for authorization: OAuth2PasswordBearer
//defaultApiClient.getAuthentication<OAuth>('OAuth2PasswordBearer').accessToken = 'YOUR_ACCESS_TOKEN';

final api = CoindetudeApi().getAdminreferentialApi();
final String id = 38400000-8cf0-11bd-b23e-10b96e4ef00d; // String | 

try {
    api.deleteLevel(id);
} catch on DioException (e) {
    print('Exception when calling AdminreferentialApi->deleteLevel: $e\n');
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **String**|  | 

### Return type

void (empty response body)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **deleteResource**
> deleteResource(id)

Delete Resource

### Example
```dart
import 'package:coindetude_api/api.dart';
// TODO Configure OAuth2 access token for authorization: OAuth2PasswordBearer
//defaultApiClient.getAuthentication<OAuth>('OAuth2PasswordBearer').accessToken = 'YOUR_ACCESS_TOKEN';

final api = CoindetudeApi().getAdminreferentialApi();
final String id = 38400000-8cf0-11bd-b23e-10b96e4ef00d; // String | 

try {
    api.deleteResource(id);
} catch on DioException (e) {
    print('Exception when calling AdminreferentialApi->deleteResource: $e\n');
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **String**|  | 

### Return type

void (empty response body)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **deleteSeries**
> deleteSeries(id)

Delete Series

### Example
```dart
import 'package:coindetude_api/api.dart';
// TODO Configure OAuth2 access token for authorization: OAuth2PasswordBearer
//defaultApiClient.getAuthentication<OAuth>('OAuth2PasswordBearer').accessToken = 'YOUR_ACCESS_TOKEN';

final api = CoindetudeApi().getAdminreferentialApi();
final String id = 38400000-8cf0-11bd-b23e-10b96e4ef00d; // String | 

try {
    api.deleteSeries(id);
} catch on DioException (e) {
    print('Exception when calling AdminreferentialApi->deleteSeries: $e\n');
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **String**|  | 

### Return type

void (empty response body)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **deleteSubject**
> deleteSubject(id)

Delete Subject

### Example
```dart
import 'package:coindetude_api/api.dart';
// TODO Configure OAuth2 access token for authorization: OAuth2PasswordBearer
//defaultApiClient.getAuthentication<OAuth>('OAuth2PasswordBearer').accessToken = 'YOUR_ACCESS_TOKEN';

final api = CoindetudeApi().getAdminreferentialApi();
final String id = 38400000-8cf0-11bd-b23e-10b96e4ef00d; // String | 

try {
    api.deleteSubject(id);
} catch on DioException (e) {
    print('Exception when calling AdminreferentialApi->deleteSubject: $e\n');
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **String**|  | 

### Return type

void (empty response body)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **updateChapter**
> ChapterRead updateChapter(id, chapterUpdate)

Update Chapter

### Example
```dart
import 'package:coindetude_api/api.dart';
// TODO Configure OAuth2 access token for authorization: OAuth2PasswordBearer
//defaultApiClient.getAuthentication<OAuth>('OAuth2PasswordBearer').accessToken = 'YOUR_ACCESS_TOKEN';

final api = CoindetudeApi().getAdminreferentialApi();
final String id = 38400000-8cf0-11bd-b23e-10b96e4ef00d; // String | 
final ChapterUpdate chapterUpdate = ; // ChapterUpdate | 

try {
    final response = api.updateChapter(id, chapterUpdate);
    print(response);
} catch on DioException (e) {
    print('Exception when calling AdminreferentialApi->updateChapter: $e\n');
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **String**|  | 
 **chapterUpdate** | [**ChapterUpdate**](ChapterUpdate.md)|  | 

### Return type

[**ChapterRead**](ChapterRead.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **updateLevel**
> LevelRead updateLevel(id, levelUpdate)

Met à jour un niveau scolaire

### Example
```dart
import 'package:coindetude_api/api.dart';
// TODO Configure OAuth2 access token for authorization: OAuth2PasswordBearer
//defaultApiClient.getAuthentication<OAuth>('OAuth2PasswordBearer').accessToken = 'YOUR_ACCESS_TOKEN';

final api = CoindetudeApi().getAdminreferentialApi();
final String id = 38400000-8cf0-11bd-b23e-10b96e4ef00d; // String | 
final LevelUpdate levelUpdate = ; // LevelUpdate | 

try {
    final response = api.updateLevel(id, levelUpdate);
    print(response);
} catch on DioException (e) {
    print('Exception when calling AdminreferentialApi->updateLevel: $e\n');
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **String**|  | 
 **levelUpdate** | [**LevelUpdate**](LevelUpdate.md)|  | 

### Return type

[**LevelRead**](LevelRead.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **updateResource**
> ResourceRead updateResource(id, resourceUpdate)

Update Resource

### Example
```dart
import 'package:coindetude_api/api.dart';
// TODO Configure OAuth2 access token for authorization: OAuth2PasswordBearer
//defaultApiClient.getAuthentication<OAuth>('OAuth2PasswordBearer').accessToken = 'YOUR_ACCESS_TOKEN';

final api = CoindetudeApi().getAdminreferentialApi();
final String id = 38400000-8cf0-11bd-b23e-10b96e4ef00d; // String | 
final ResourceUpdate resourceUpdate = ; // ResourceUpdate | 

try {
    final response = api.updateResource(id, resourceUpdate);
    print(response);
} catch on DioException (e) {
    print('Exception when calling AdminreferentialApi->updateResource: $e\n');
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **String**|  | 
 **resourceUpdate** | [**ResourceUpdate**](ResourceUpdate.md)|  | 

### Return type

[**ResourceRead**](ResourceRead.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **updateSeries**
> SeriesRead updateSeries(id, seriesUpdate)

Update Series

### Example
```dart
import 'package:coindetude_api/api.dart';
// TODO Configure OAuth2 access token for authorization: OAuth2PasswordBearer
//defaultApiClient.getAuthentication<OAuth>('OAuth2PasswordBearer').accessToken = 'YOUR_ACCESS_TOKEN';

final api = CoindetudeApi().getAdminreferentialApi();
final String id = 38400000-8cf0-11bd-b23e-10b96e4ef00d; // String | 
final SeriesUpdate seriesUpdate = ; // SeriesUpdate | 

try {
    final response = api.updateSeries(id, seriesUpdate);
    print(response);
} catch on DioException (e) {
    print('Exception when calling AdminreferentialApi->updateSeries: $e\n');
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **String**|  | 
 **seriesUpdate** | [**SeriesUpdate**](SeriesUpdate.md)|  | 

### Return type

[**SeriesRead**](SeriesRead.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **updateSubject**
> SubjectRead updateSubject(id, subjectUpdate)

Update Subject

### Example
```dart
import 'package:coindetude_api/api.dart';
// TODO Configure OAuth2 access token for authorization: OAuth2PasswordBearer
//defaultApiClient.getAuthentication<OAuth>('OAuth2PasswordBearer').accessToken = 'YOUR_ACCESS_TOKEN';

final api = CoindetudeApi().getAdminreferentialApi();
final String id = 38400000-8cf0-11bd-b23e-10b96e4ef00d; // String | 
final SubjectUpdate subjectUpdate = ; // SubjectUpdate | 

try {
    final response = api.updateSubject(id, subjectUpdate);
    print(response);
} catch on DioException (e) {
    print('Exception when calling AdminreferentialApi->updateSubject: $e\n');
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **String**|  | 
 **subjectUpdate** | [**SubjectUpdate**](SubjectUpdate.md)|  | 

### Return type

[**SubjectRead**](SubjectRead.md)

### Authorization

[OAuth2PasswordBearer](../README.md#OAuth2PasswordBearer), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


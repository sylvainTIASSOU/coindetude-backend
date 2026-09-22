# coindetude_api.api.ReferentialApi

## Load the API package
```dart
import 'package:coindetude_api/api.dart';
```

All URIs are relative to *http://localhost:8000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**getResource**](ReferentialApi.md#getresource) | **GET** /api/v1/referential/resources/{resource_id} | Détail d&#39;une ressource (avec contenu + URL fichier)
[**listChapters**](ReferentialApi.md#listchapters) | **GET** /api/v1/referential/chapters | Liste des chapitres
[**listLevels**](ReferentialApi.md#listlevels) | **GET** /api/v1/referential/levels | Liste des niveaux scolaires
[**listResources**](ReferentialApi.md#listresources) | **GET** /api/v1/referential/resources | Liste des ressources (sans contenu lourd)
[**listSeries**](ReferentialApi.md#listseries) | **GET** /api/v1/referential/series | Liste des séries (lycée)
[**listSubjects**](ReferentialApi.md#listsubjects) | **GET** /api/v1/referential/subjects | Liste des matières


# **getResource**
> ResourceReadDetail getResource(resourceId)

Détail d'une ressource (avec contenu + URL fichier)

### Example
```dart
import 'package:coindetude_api/api.dart';

final api = CoindetudeApi().getReferentialApi();
final String resourceId = 38400000-8cf0-11bd-b23e-10b96e4ef00d; // String | 

try {
    final response = api.getResource(resourceId);
    print(response);
} catch on DioException (e) {
    print('Exception when calling ReferentialApi->getResource: $e\n');
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **resourceId** | **String**|  | 

### Return type

[**ResourceReadDetail**](ResourceReadDetail.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **listChapters**
> PageResponseChapterRead listChapters(levelId, subjectId, seriesId, limit, offset)

Liste des chapitres

### Example
```dart
import 'package:coindetude_api/api.dart';

final api = CoindetudeApi().getReferentialApi();
final String levelId = 38400000-8cf0-11bd-b23e-10b96e4ef00d; // String | 
final String subjectId = 38400000-8cf0-11bd-b23e-10b96e4ef00d; // String | 
final String seriesId = 38400000-8cf0-11bd-b23e-10b96e4ef00d; // String | 
final int limit = 56; // int | 
final int offset = 56; // int | 

try {
    final response = api.listChapters(levelId, subjectId, seriesId, limit, offset);
    print(response);
} catch on DioException (e) {
    print('Exception when calling ReferentialApi->listChapters: $e\n');
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **levelId** | **String**|  | [optional] 
 **subjectId** | **String**|  | [optional] 
 **seriesId** | **String**|  | [optional] 
 **limit** | **int**|  | [optional] [default to 50]
 **offset** | **int**|  | [optional] [default to 0]

### Return type

[**PageResponseChapterRead**](PageResponseChapterRead.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **listLevels**
> PageResponseLevelRead listLevels(cycle, limit, offset)

Liste des niveaux scolaires

### Example
```dart
import 'package:coindetude_api/api.dart';

final api = CoindetudeApi().getReferentialApi();
final Cycle cycle = ; // Cycle | Filtre par cycle
final int limit = 56; // int | 
final int offset = 56; // int | 

try {
    final response = api.listLevels(cycle, limit, offset);
    print(response);
} catch on DioException (e) {
    print('Exception when calling ReferentialApi->listLevels: $e\n');
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cycle** | [**Cycle**](.md)| Filtre par cycle | [optional] 
 **limit** | **int**|  | [optional] [default to 50]
 **offset** | **int**|  | [optional] [default to 0]

### Return type

[**PageResponseLevelRead**](PageResponseLevelRead.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **listResources**
> PageResponseResourceRead listResources(chapterId, type, year, limit, offset)

Liste des ressources (sans contenu lourd)

### Example
```dart
import 'package:coindetude_api/api.dart';

final api = CoindetudeApi().getReferentialApi();
final String chapterId = 38400000-8cf0-11bd-b23e-10b96e4ef00d; // String | 
final ResourceType type = ; // ResourceType | 
final int year = 56; // int | 
final int limit = 56; // int | 
final int offset = 56; // int | 

try {
    final response = api.listResources(chapterId, type, year, limit, offset);
    print(response);
} catch on DioException (e) {
    print('Exception when calling ReferentialApi->listResources: $e\n');
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **chapterId** | **String**|  | [optional] 
 **type** | [**ResourceType**](.md)|  | [optional] 
 **year** | **int**|  | [optional] 
 **limit** | **int**|  | [optional] [default to 50]
 **offset** | **int**|  | [optional] [default to 0]

### Return type

[**PageResponseResourceRead**](PageResponseResourceRead.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **listSeries**
> PageResponseSeriesRead listSeries(cycle, limit, offset)

Liste des séries (lycée)

### Example
```dart
import 'package:coindetude_api/api.dart';

final api = CoindetudeApi().getReferentialApi();
final Cycle cycle = ; // Cycle | 
final int limit = 56; // int | 
final int offset = 56; // int | 

try {
    final response = api.listSeries(cycle, limit, offset);
    print(response);
} catch on DioException (e) {
    print('Exception when calling ReferentialApi->listSeries: $e\n');
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cycle** | [**Cycle**](.md)|  | [optional] 
 **limit** | **int**|  | [optional] [default to 50]
 **offset** | **int**|  | [optional] [default to 0]

### Return type

[**PageResponseSeriesRead**](PageResponseSeriesRead.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **listSubjects**
> PageResponseSubjectRead listSubjects(cycle, limit, offset)

Liste des matières

### Example
```dart
import 'package:coindetude_api/api.dart';

final api = CoindetudeApi().getReferentialApi();
final Cycle cycle = ; // Cycle | 
final int limit = 56; // int | 
final int offset = 56; // int | 

try {
    final response = api.listSubjects(cycle, limit, offset);
    print(response);
} catch on DioException (e) {
    print('Exception when calling ReferentialApi->listSubjects: $e\n');
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cycle** | [**Cycle**](.md)|  | [optional] 
 **limit** | **int**|  | [optional] [default to 50]
 **offset** | **int**|  | [optional] [default to 0]

### Return type

[**PageResponseSubjectRead**](PageResponseSubjectRead.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


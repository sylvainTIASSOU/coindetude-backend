# coindetude_api.model.SyncEventRequest

## Load the model package
```dart
import 'package:coindetude_api/api.dart';
```

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**entityType** | [**SyncEntityType**](SyncEntityType.md) |  | 
**operation** | [**SyncOperation**](SyncOperation.md) |  | 
**payload** | [**BuiltMap&lt;String, JsonObject&gt;**](JsonObject.md) | Contenu de l'entité (objet JSON direct) | 
**clientTs** | [**DateTime**](DateTime.md) | Horodatage client ISO 8601 UTC (tolérance ±7 jours) | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



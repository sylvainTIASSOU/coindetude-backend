//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:coindetude_api/src/model/sync_operation.dart';
import 'package:built_collection/built_collection.dart';
import 'package:coindetude_api/src/model/sync_entity_type.dart';
import 'package:built_value/json_object.dart';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';

part 'sync_event_request.g.dart';

/// Requête POST /sync/apply-event.  ⚠️ ``payload`` est un objet JSON direct (pas une string échappée). Cela réduit la taille du body (~30%) et évite les erreurs de parsing.
///
/// Properties:
/// * [entityType] 
/// * [operation] 
/// * [payload] - Contenu de l'entité (objet JSON direct)
/// * [clientTs] - Horodatage client ISO 8601 UTC (tolérance ±7 jours)
@BuiltValue()
abstract class SyncEventRequest implements Built<SyncEventRequest, SyncEventRequestBuilder> {
  @BuiltValueField(wireName: r'entity_type')
  SyncEntityType get entityType;
  // enum entityTypeEnum {  planning_task,  xp_event,  streak_event,  };

  @BuiltValueField(wireName: r'operation')
  SyncOperation get operation;
  // enum operationEnum {  create,  update,  delete,  };

  /// Contenu de l'entité (objet JSON direct)
  @BuiltValueField(wireName: r'payload')
  BuiltMap<String, JsonObject?> get payload;

  /// Horodatage client ISO 8601 UTC (tolérance ±7 jours)
  @BuiltValueField(wireName: r'client_ts')
  DateTime get clientTs;

  SyncEventRequest._();

  factory SyncEventRequest([void updates(SyncEventRequestBuilder b)]) = _$SyncEventRequest;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(SyncEventRequestBuilder b) => b;

  @BuiltValueSerializer(custom: true)
  static Serializer<SyncEventRequest> get serializer => _$SyncEventRequestSerializer();
}

class _$SyncEventRequestSerializer implements PrimitiveSerializer<SyncEventRequest> {
  @override
  final Iterable<Type> types = const [SyncEventRequest, _$SyncEventRequest];

  @override
  final String wireName = r'SyncEventRequest';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    SyncEventRequest object, {
    FullType specifiedType = FullType.unspecified,
  }) sync* {
    yield r'entity_type';
    yield serializers.serialize(
      object.entityType,
      specifiedType: const FullType(SyncEntityType),
    );
    yield r'operation';
    yield serializers.serialize(
      object.operation,
      specifiedType: const FullType(SyncOperation),
    );
    yield r'payload';
    yield serializers.serialize(
      object.payload,
      specifiedType: const FullType(BuiltMap, [FullType(String), FullType.nullable(JsonObject)]),
    );
    yield r'client_ts';
    yield serializers.serialize(
      object.clientTs,
      specifiedType: const FullType(DateTime),
    );
  }

  @override
  Object serialize(
    Serializers serializers,
    SyncEventRequest object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    return _serializeProperties(serializers, object, specifiedType: specifiedType).toList();
  }

  void _deserializeProperties(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
    required List<Object?> serializedList,
    required SyncEventRequestBuilder result,
    required List<Object?> unhandled,
  }) {
    for (var i = 0; i < serializedList.length; i += 2) {
      final key = serializedList[i] as String;
      final value = serializedList[i + 1];
      switch (key) {
        case r'entity_type':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(SyncEntityType),
          ) as SyncEntityType;
          result.entityType = valueDes;
          break;
        case r'operation':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(SyncOperation),
          ) as SyncOperation;
          result.operation = valueDes;
          break;
        case r'payload':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(BuiltMap, [FullType(String), FullType.nullable(JsonObject)]),
          ) as BuiltMap<String, JsonObject?>;
          result.payload.replace(valueDes);
          break;
        case r'client_ts':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(DateTime),
          ) as DateTime;
          result.clientTs = valueDes;
          break;
        default:
          unhandled.add(key);
          unhandled.add(value);
          break;
      }
    }
  }

  @override
  SyncEventRequest deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = SyncEventRequestBuilder();
    final serializedList = (serialized as Iterable<Object?>).toList();
    final unhandled = <Object?>[];
    _deserializeProperties(
      serializers,
      serialized,
      specifiedType: specifiedType,
      serializedList: serializedList,
      unhandled: unhandled,
      result: result,
    );
    return result.build();
  }
}


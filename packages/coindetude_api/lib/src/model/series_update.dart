//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:built_collection/built_collection.dart';
import 'package:coindetude_api/src/model/description.dart';
import 'package:coindetude_api/src/model/name1.dart';
import 'package:coindetude_api/src/model/code.dart';
import 'package:built_value/json_object.dart';
import 'package:coindetude_api/src/model/level_update_cycle.dart';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';

part 'series_update.g.dart';

/// SeriesUpdate
///
/// Properties:
/// * [code] 
/// * [name] 
/// * [cycle] 
/// * [description] 
@BuiltValue()
abstract class SeriesUpdate implements Built<SeriesUpdate, SeriesUpdateBuilder> {
  @BuiltValueField(wireName: r'code')
  Code? get code;

  @BuiltValueField(wireName: r'name')
  Name1? get name;

  @BuiltValueField(wireName: r'cycle')
  LevelUpdateCycle? get cycle;

  @BuiltValueField(wireName: r'description')
  Description? get description;

  SeriesUpdate._();

  factory SeriesUpdate([void updates(SeriesUpdateBuilder b)]) = _$SeriesUpdate;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(SeriesUpdateBuilder b) => b;

  @BuiltValueSerializer(custom: true)
  static Serializer<SeriesUpdate> get serializer => _$SeriesUpdateSerializer();
}

class _$SeriesUpdateSerializer implements PrimitiveSerializer<SeriesUpdate> {
  @override
  final Iterable<Type> types = const [SeriesUpdate, _$SeriesUpdate];

  @override
  final String wireName = r'SeriesUpdate';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    SeriesUpdate object, {
    FullType specifiedType = FullType.unspecified,
  }) sync* {
    if (object.code != null) {
      yield r'code';
      yield serializers.serialize(
        object.code,
        specifiedType: const FullType(Code),
      );
    }
    if (object.name != null) {
      yield r'name';
      yield serializers.serialize(
        object.name,
        specifiedType: const FullType(Name1),
      );
    }
    if (object.cycle != null) {
      yield r'cycle';
      yield serializers.serialize(
        object.cycle,
        specifiedType: const FullType(LevelUpdateCycle),
      );
    }
    if (object.description != null) {
      yield r'description';
      yield serializers.serialize(
        object.description,
        specifiedType: const FullType(Description),
      );
    }
  }

  @override
  Object serialize(
    Serializers serializers,
    SeriesUpdate object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    return _serializeProperties(serializers, object, specifiedType: specifiedType).toList();
  }

  void _deserializeProperties(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
    required List<Object?> serializedList,
    required SeriesUpdateBuilder result,
    required List<Object?> unhandled,
  }) {
    for (var i = 0; i < serializedList.length; i += 2) {
      final key = serializedList[i] as String;
      final value = serializedList[i + 1];
      switch (key) {
        case r'code':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(Code),
          ) as Code;
          result.code.replace(valueDes);
          break;
        case r'name':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(Name1),
          ) as Name1;
          result.name.replace(valueDes);
          break;
        case r'cycle':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(LevelUpdateCycle),
          ) as LevelUpdateCycle;
          result.cycle.replace(valueDes);
          break;
        case r'description':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(Description),
          ) as Description;
          result.description.replace(valueDes);
          break;
        default:
          unhandled.add(key);
          unhandled.add(value);
          break;
      }
    }
  }

  @override
  SeriesUpdate deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = SeriesUpdateBuilder();
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


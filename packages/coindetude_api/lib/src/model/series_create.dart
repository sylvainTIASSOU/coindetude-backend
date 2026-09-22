//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:built_collection/built_collection.dart';
import 'package:coindetude_api/src/model/description.dart';
import 'package:coindetude_api/src/model/cycle.dart';
import 'package:built_value/json_object.dart';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';

part 'series_create.g.dart';

/// SeriesCreate
///
/// Properties:
/// * [code] 
/// * [name] 
/// * [cycle] 
/// * [description] 
@BuiltValue()
abstract class SeriesCreate implements Built<SeriesCreate, SeriesCreateBuilder> {
  @BuiltValueField(wireName: r'code')
  String get code;

  @BuiltValueField(wireName: r'name')
  String get name;

  @BuiltValueField(wireName: r'cycle')
  Cycle get cycle;
  // enum cycleEnum {  college,  lycee_moderne,  lycee_technique,  };

  @BuiltValueField(wireName: r'description')
  Description? get description;

  SeriesCreate._();

  factory SeriesCreate([void updates(SeriesCreateBuilder b)]) = _$SeriesCreate;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(SeriesCreateBuilder b) => b;

  @BuiltValueSerializer(custom: true)
  static Serializer<SeriesCreate> get serializer => _$SeriesCreateSerializer();
}

class _$SeriesCreateSerializer implements PrimitiveSerializer<SeriesCreate> {
  @override
  final Iterable<Type> types = const [SeriesCreate, _$SeriesCreate];

  @override
  final String wireName = r'SeriesCreate';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    SeriesCreate object, {
    FullType specifiedType = FullType.unspecified,
  }) sync* {
    yield r'code';
    yield serializers.serialize(
      object.code,
      specifiedType: const FullType(String),
    );
    yield r'name';
    yield serializers.serialize(
      object.name,
      specifiedType: const FullType(String),
    );
    yield r'cycle';
    yield serializers.serialize(
      object.cycle,
      specifiedType: const FullType(Cycle),
    );
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
    SeriesCreate object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    return _serializeProperties(serializers, object, specifiedType: specifiedType).toList();
  }

  void _deserializeProperties(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
    required List<Object?> serializedList,
    required SeriesCreateBuilder result,
    required List<Object?> unhandled,
  }) {
    for (var i = 0; i < serializedList.length; i += 2) {
      final key = serializedList[i] as String;
      final value = serializedList[i + 1];
      switch (key) {
        case r'code':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(String),
          ) as String;
          result.code = valueDes;
          break;
        case r'name':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(String),
          ) as String;
          result.name = valueDes;
          break;
        case r'cycle':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(Cycle),
          ) as Cycle;
          result.cycle = valueDes;
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
  SeriesCreate deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = SeriesCreateBuilder();
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


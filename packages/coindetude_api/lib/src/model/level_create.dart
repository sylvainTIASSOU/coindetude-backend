//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:built_collection/built_collection.dart';
import 'package:coindetude_api/src/model/cycle.dart';
import 'package:built_value/json_object.dart';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';

part 'level_create.g.dart';

/// LevelCreate
///
/// Properties:
/// * [name] 
/// * [cycle] 
/// * [orderIndex] 
@BuiltValue()
abstract class LevelCreate implements Built<LevelCreate, LevelCreateBuilder> {
  @BuiltValueField(wireName: r'name')
  String get name;

  @BuiltValueField(wireName: r'cycle')
  Cycle get cycle;
  // enum cycleEnum {  college,  lycee_moderne,  lycee_technique,  };

  @BuiltValueField(wireName: r'order_index')
  int? get orderIndex;

  LevelCreate._();

  factory LevelCreate([void updates(LevelCreateBuilder b)]) = _$LevelCreate;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(LevelCreateBuilder b) => b
      ..orderIndex = 0;

  @BuiltValueSerializer(custom: true)
  static Serializer<LevelCreate> get serializer => _$LevelCreateSerializer();
}

class _$LevelCreateSerializer implements PrimitiveSerializer<LevelCreate> {
  @override
  final Iterable<Type> types = const [LevelCreate, _$LevelCreate];

  @override
  final String wireName = r'LevelCreate';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    LevelCreate object, {
    FullType specifiedType = FullType.unspecified,
  }) sync* {
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
    if (object.orderIndex != null) {
      yield r'order_index';
      yield serializers.serialize(
        object.orderIndex,
        specifiedType: const FullType(int),
      );
    }
  }

  @override
  Object serialize(
    Serializers serializers,
    LevelCreate object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    return _serializeProperties(serializers, object, specifiedType: specifiedType).toList();
  }

  void _deserializeProperties(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
    required List<Object?> serializedList,
    required LevelCreateBuilder result,
    required List<Object?> unhandled,
  }) {
    for (var i = 0; i < serializedList.length; i += 2) {
      final key = serializedList[i] as String;
      final value = serializedList[i + 1];
      switch (key) {
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
        case r'order_index':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(int),
          ) as int;
          result.orderIndex = valueDes;
          break;
        default:
          unhandled.add(key);
          unhandled.add(value);
          break;
      }
    }
  }

  @override
  LevelCreate deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = LevelCreateBuilder();
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


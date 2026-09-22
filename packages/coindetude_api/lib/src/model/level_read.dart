//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:coindetude_api/src/model/cycle.dart';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';

part 'level_read.g.dart';

/// LevelRead
///
/// Properties:
/// * [id] 
/// * [name] 
/// * [cycle] 
/// * [orderIndex] 
@BuiltValue()
abstract class LevelRead implements Built<LevelRead, LevelReadBuilder> {
  @BuiltValueField(wireName: r'id')
  String get id;

  @BuiltValueField(wireName: r'name')
  String get name;

  @BuiltValueField(wireName: r'cycle')
  Cycle get cycle;
  // enum cycleEnum {  college,  lycee_moderne,  lycee_technique,  };

  @BuiltValueField(wireName: r'order_index')
  int get orderIndex;

  LevelRead._();

  factory LevelRead([void updates(LevelReadBuilder b)]) = _$LevelRead;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(LevelReadBuilder b) => b;

  @BuiltValueSerializer(custom: true)
  static Serializer<LevelRead> get serializer => _$LevelReadSerializer();
}

class _$LevelReadSerializer implements PrimitiveSerializer<LevelRead> {
  @override
  final Iterable<Type> types = const [LevelRead, _$LevelRead];

  @override
  final String wireName = r'LevelRead';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    LevelRead object, {
    FullType specifiedType = FullType.unspecified,
  }) sync* {
    yield r'id';
    yield serializers.serialize(
      object.id,
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
    yield r'order_index';
    yield serializers.serialize(
      object.orderIndex,
      specifiedType: const FullType(int),
    );
  }

  @override
  Object serialize(
    Serializers serializers,
    LevelRead object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    return _serializeProperties(serializers, object, specifiedType: specifiedType).toList();
  }

  void _deserializeProperties(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
    required List<Object?> serializedList,
    required LevelReadBuilder result,
    required List<Object?> unhandled,
  }) {
    for (var i = 0; i < serializedList.length; i += 2) {
      final key = serializedList[i] as String;
      final value = serializedList[i + 1];
      switch (key) {
        case r'id':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(String),
          ) as String;
          result.id = valueDes;
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
  LevelRead deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = LevelReadBuilder();
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


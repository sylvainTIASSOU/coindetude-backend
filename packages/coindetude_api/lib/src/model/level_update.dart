//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:coindetude_api/src/model/name.dart';
import 'package:coindetude_api/src/model/order_index.dart';
import 'package:built_collection/built_collection.dart';
import 'package:built_value/json_object.dart';
import 'package:coindetude_api/src/model/level_update_cycle.dart';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';

part 'level_update.g.dart';

/// LevelUpdate
///
/// Properties:
/// * [name] 
/// * [cycle] 
/// * [orderIndex] 
@BuiltValue()
abstract class LevelUpdate implements Built<LevelUpdate, LevelUpdateBuilder> {
  @BuiltValueField(wireName: r'name')
  Name? get name;

  @BuiltValueField(wireName: r'cycle')
  LevelUpdateCycle? get cycle;

  @BuiltValueField(wireName: r'order_index')
  OrderIndex? get orderIndex;

  LevelUpdate._();

  factory LevelUpdate([void updates(LevelUpdateBuilder b)]) = _$LevelUpdate;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(LevelUpdateBuilder b) => b;

  @BuiltValueSerializer(custom: true)
  static Serializer<LevelUpdate> get serializer => _$LevelUpdateSerializer();
}

class _$LevelUpdateSerializer implements PrimitiveSerializer<LevelUpdate> {
  @override
  final Iterable<Type> types = const [LevelUpdate, _$LevelUpdate];

  @override
  final String wireName = r'LevelUpdate';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    LevelUpdate object, {
    FullType specifiedType = FullType.unspecified,
  }) sync* {
    if (object.name != null) {
      yield r'name';
      yield serializers.serialize(
        object.name,
        specifiedType: const FullType(Name),
      );
    }
    if (object.cycle != null) {
      yield r'cycle';
      yield serializers.serialize(
        object.cycle,
        specifiedType: const FullType(LevelUpdateCycle),
      );
    }
    if (object.orderIndex != null) {
      yield r'order_index';
      yield serializers.serialize(
        object.orderIndex,
        specifiedType: const FullType(OrderIndex),
      );
    }
  }

  @override
  Object serialize(
    Serializers serializers,
    LevelUpdate object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    return _serializeProperties(serializers, object, specifiedType: specifiedType).toList();
  }

  void _deserializeProperties(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
    required List<Object?> serializedList,
    required LevelUpdateBuilder result,
    required List<Object?> unhandled,
  }) {
    for (var i = 0; i < serializedList.length; i += 2) {
      final key = serializedList[i] as String;
      final value = serializedList[i + 1];
      switch (key) {
        case r'name':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(Name),
          ) as Name;
          result.name.replace(valueDes);
          break;
        case r'cycle':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(LevelUpdateCycle),
          ) as LevelUpdateCycle;
          result.cycle.replace(valueDes);
          break;
        case r'order_index':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(OrderIndex),
          ) as OrderIndex;
          result.orderIndex.replace(valueDes);
          break;
        default:
          unhandled.add(key);
          unhandled.add(value);
          break;
      }
    }
  }

  @override
  LevelUpdate deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = LevelUpdateBuilder();
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


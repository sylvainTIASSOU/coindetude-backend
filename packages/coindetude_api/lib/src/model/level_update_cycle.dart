//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:coindetude_api/src/model/model_null.dart';
import 'package:coindetude_api/src/model/cycle.dart';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';
import 'package:one_of/any_of.dart';

part 'level_update_cycle.g.dart';

/// LevelUpdateCycle
@BuiltValue()
abstract class LevelUpdateCycle implements Built<LevelUpdateCycle, LevelUpdateCycleBuilder> {
  /// Any Of [Cycle], [ModelNull]
  AnyOf get anyOf;

  LevelUpdateCycle._();

  factory LevelUpdateCycle([void updates(LevelUpdateCycleBuilder b)]) = _$LevelUpdateCycle;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(LevelUpdateCycleBuilder b) => b;

  @BuiltValueSerializer(custom: true)
  static Serializer<LevelUpdateCycle> get serializer => _$LevelUpdateCycleSerializer();
}

class _$LevelUpdateCycleSerializer implements PrimitiveSerializer<LevelUpdateCycle> {
  @override
  final Iterable<Type> types = const [LevelUpdateCycle, _$LevelUpdateCycle];

  @override
  final String wireName = r'LevelUpdateCycle';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    LevelUpdateCycle object, {
    FullType specifiedType = FullType.unspecified,
  }) sync* {
  }

  @override
  Object serialize(
    Serializers serializers,
    LevelUpdateCycle object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final anyOf = object.anyOf;
    return serializers.serialize(anyOf, specifiedType: FullType(AnyOf, anyOf.valueTypes.map((type) => FullType(type)).toList()))!;
  }

  @override
  LevelUpdateCycle deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = LevelUpdateCycleBuilder();
    Object? anyOfDataSrc;
    final targetType = const FullType(AnyOf, [FullType(Cycle), FullType(ModelNull), ]);
    anyOfDataSrc = serialized;
    result.anyOf = serializers.deserialize(anyOfDataSrc, specifiedType: targetType) as AnyOf;
    return result.build();
  }
}


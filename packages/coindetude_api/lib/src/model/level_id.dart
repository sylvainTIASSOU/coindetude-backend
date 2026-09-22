//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:coindetude_api/src/model/model_null.dart';
import 'dart:core';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';
import 'package:one_of/any_of.dart';

part 'level_id.g.dart';

/// LevelId
@BuiltValue()
abstract class LevelId implements Built<LevelId, LevelIdBuilder> {
  /// Any Of [ModelNull], [String]
  AnyOf get anyOf;

  LevelId._();

  factory LevelId([void updates(LevelIdBuilder b)]) = _$LevelId;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(LevelIdBuilder b) => b;

  @BuiltValueSerializer(custom: true)
  static Serializer<LevelId> get serializer => _$LevelIdSerializer();
}

class _$LevelIdSerializer implements PrimitiveSerializer<LevelId> {
  @override
  final Iterable<Type> types = const [LevelId, _$LevelId];

  @override
  final String wireName = r'LevelId';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    LevelId object, {
    FullType specifiedType = FullType.unspecified,
  }) sync* {
  }

  @override
  Object serialize(
    Serializers serializers,
    LevelId object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final anyOf = object.anyOf;
    return serializers.serialize(anyOf, specifiedType: FullType(AnyOf, anyOf.valueTypes.map((type) => FullType(type)).toList()))!;
  }

  @override
  LevelId deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = LevelIdBuilder();
    Object? anyOfDataSrc;
    final targetType = const FullType(AnyOf, [FullType(String), FullType(ModelNull), ]);
    anyOfDataSrc = serialized;
    result.anyOf = serializers.deserialize(anyOfDataSrc, specifiedType: targetType) as AnyOf;
    return result.build();
  }
}


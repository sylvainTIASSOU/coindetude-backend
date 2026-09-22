//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:coindetude_api/src/model/model_null.dart';
import 'dart:core';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';
import 'package:one_of/any_of.dart';

part 'series_id1.g.dart';

/// SeriesId1
@BuiltValue()
abstract class SeriesId1 implements Built<SeriesId1, SeriesId1Builder> {
  /// Any Of [ModelNull], [String]
  AnyOf get anyOf;

  SeriesId1._();

  factory SeriesId1([void updates(SeriesId1Builder b)]) = _$SeriesId1;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(SeriesId1Builder b) => b;

  @BuiltValueSerializer(custom: true)
  static Serializer<SeriesId1> get serializer => _$SeriesId1Serializer();
}

class _$SeriesId1Serializer implements PrimitiveSerializer<SeriesId1> {
  @override
  final Iterable<Type> types = const [SeriesId1, _$SeriesId1];

  @override
  final String wireName = r'SeriesId1';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    SeriesId1 object, {
    FullType specifiedType = FullType.unspecified,
  }) sync* {
  }

  @override
  Object serialize(
    Serializers serializers,
    SeriesId1 object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final anyOf = object.anyOf;
    return serializers.serialize(anyOf, specifiedType: FullType(AnyOf, anyOf.valueTypes.map((type) => FullType(type)).toList()))!;
  }

  @override
  SeriesId1 deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = SeriesId1Builder();
    Object? anyOfDataSrc;
    final targetType = const FullType(AnyOf, [FullType(String), FullType(ModelNull), ]);
    anyOfDataSrc = serialized;
    result.anyOf = serializers.deserialize(anyOfDataSrc, specifiedType: targetType) as AnyOf;
    return result.build();
  }
}


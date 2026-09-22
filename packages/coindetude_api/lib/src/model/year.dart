//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:coindetude_api/src/model/model_null.dart';
import 'dart:core';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';
import 'package:one_of/any_of.dart';

part 'year.g.dart';

/// Year
@BuiltValue()
abstract class Year implements Built<Year, YearBuilder> {
  /// Any Of [ModelNull], [int]
  AnyOf get anyOf;

  Year._();

  factory Year([void updates(YearBuilder b)]) = _$Year;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(YearBuilder b) => b;

  @BuiltValueSerializer(custom: true)
  static Serializer<Year> get serializer => _$YearSerializer();
}

class _$YearSerializer implements PrimitiveSerializer<Year> {
  @override
  final Iterable<Type> types = const [Year, _$Year];

  @override
  final String wireName = r'Year';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    Year object, {
    FullType specifiedType = FullType.unspecified,
  }) sync* {
  }

  @override
  Object serialize(
    Serializers serializers,
    Year object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final anyOf = object.anyOf;
    return serializers.serialize(anyOf, specifiedType: FullType(AnyOf, anyOf.valueTypes.map((type) => FullType(type)).toList()))!;
  }

  @override
  Year deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = YearBuilder();
    Object? anyOfDataSrc;
    final targetType = const FullType(AnyOf, [FullType(int), FullType(ModelNull), ]);
    anyOfDataSrc = serialized;
    result.anyOf = serializers.deserialize(anyOfDataSrc, specifiedType: targetType) as AnyOf;
    return result.build();
  }
}


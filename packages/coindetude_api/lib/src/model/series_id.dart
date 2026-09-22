//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:coindetude_api/src/model/model_null.dart';
import 'dart:core';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';
import 'package:one_of/any_of.dart';

part 'series_id.g.dart';

/// NULL si chapitre commun à toutes les séries
@BuiltValue()
abstract class SeriesId implements Built<SeriesId, SeriesIdBuilder> {
  /// Any Of [ModelNull], [String]
  AnyOf get anyOf;

  SeriesId._();

  factory SeriesId([void updates(SeriesIdBuilder b)]) = _$SeriesId;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(SeriesIdBuilder b) => b;

  @BuiltValueSerializer(custom: true)
  static Serializer<SeriesId> get serializer => _$SeriesIdSerializer();
}

class _$SeriesIdSerializer implements PrimitiveSerializer<SeriesId> {
  @override
  final Iterable<Type> types = const [SeriesId, _$SeriesId];

  @override
  final String wireName = r'SeriesId';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    SeriesId object, {
    FullType specifiedType = FullType.unspecified,
  }) sync* {
  }

  @override
  Object serialize(
    Serializers serializers,
    SeriesId object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final anyOf = object.anyOf;
    return serializers.serialize(anyOf, specifiedType: FullType(AnyOf, anyOf.valueTypes.map((type) => FullType(type)).toList()))!;
  }

  @override
  SeriesId deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = SeriesIdBuilder();
    Object? anyOfDataSrc;
    final targetType = const FullType(AnyOf, [FullType(String), FullType(ModelNull), ]);
    anyOfDataSrc = serialized;
    result.anyOf = serializers.deserialize(anyOfDataSrc, specifiedType: targetType) as AnyOf;
    return result.build();
  }
}


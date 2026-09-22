//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:coindetude_api/src/model/model_null.dart';
import 'dart:core';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';
import 'package:one_of/any_of.dart';

part 'content_text1.g.dart';

/// ContentText1
@BuiltValue()
abstract class ContentText1 implements Built<ContentText1, ContentText1Builder> {
  /// Any Of [ModelNull], [String]
  AnyOf get anyOf;

  ContentText1._();

  factory ContentText1([void updates(ContentText1Builder b)]) = _$ContentText1;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(ContentText1Builder b) => b;

  @BuiltValueSerializer(custom: true)
  static Serializer<ContentText1> get serializer => _$ContentText1Serializer();
}

class _$ContentText1Serializer implements PrimitiveSerializer<ContentText1> {
  @override
  final Iterable<Type> types = const [ContentText1, _$ContentText1];

  @override
  final String wireName = r'ContentText1';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    ContentText1 object, {
    FullType specifiedType = FullType.unspecified,
  }) sync* {
  }

  @override
  Object serialize(
    Serializers serializers,
    ContentText1 object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final anyOf = object.anyOf;
    return serializers.serialize(anyOf, specifiedType: FullType(AnyOf, anyOf.valueTypes.map((type) => FullType(type)).toList()))!;
  }

  @override
  ContentText1 deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = ContentText1Builder();
    Object? anyOfDataSrc;
    final targetType = const FullType(AnyOf, [FullType(String), FullType(ModelNull), ]);
    anyOfDataSrc = serialized;
    result.anyOf = serializers.deserialize(anyOfDataSrc, specifiedType: targetType) as AnyOf;
    return result.build();
  }
}


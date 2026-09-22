//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:coindetude_api/src/model/model_null.dart';
import 'dart:core';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';
import 'package:one_of/any_of.dart';

part 'title.g.dart';

/// Title
@BuiltValue()
abstract class Title implements Built<Title, TitleBuilder> {
  /// Any Of [ModelNull], [String]
  AnyOf get anyOf;

  Title._();

  factory Title([void updates(TitleBuilder b)]) = _$Title;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(TitleBuilder b) => b;

  @BuiltValueSerializer(custom: true)
  static Serializer<Title> get serializer => _$TitleSerializer();
}

class _$TitleSerializer implements PrimitiveSerializer<Title> {
  @override
  final Iterable<Type> types = const [Title, _$Title];

  @override
  final String wireName = r'Title';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    Title object, {
    FullType specifiedType = FullType.unspecified,
  }) sync* {
  }

  @override
  Object serialize(
    Serializers serializers,
    Title object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final anyOf = object.anyOf;
    return serializers.serialize(anyOf, specifiedType: FullType(AnyOf, anyOf.valueTypes.map((type) => FullType(type)).toList()))!;
  }

  @override
  Title deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = TitleBuilder();
    Object? anyOfDataSrc;
    final targetType = const FullType(AnyOf, [FullType(String), FullType(ModelNull), ]);
    anyOfDataSrc = serialized;
    result.anyOf = serializers.deserialize(anyOfDataSrc, specifiedType: targetType) as AnyOf;
    return result.build();
  }
}


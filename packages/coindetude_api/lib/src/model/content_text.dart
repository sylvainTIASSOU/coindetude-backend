//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:coindetude_api/src/model/model_null.dart';
import 'dart:core';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';
import 'package:one_of/any_of.dart';

part 'content_text.g.dart';

/// Contenu Markdown affichable directement
@BuiltValue()
abstract class ContentText implements Built<ContentText, ContentTextBuilder> {
  /// Any Of [ModelNull], [String]
  AnyOf get anyOf;

  ContentText._();

  factory ContentText([void updates(ContentTextBuilder b)]) = _$ContentText;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(ContentTextBuilder b) => b;

  @BuiltValueSerializer(custom: true)
  static Serializer<ContentText> get serializer => _$ContentTextSerializer();
}

class _$ContentTextSerializer implements PrimitiveSerializer<ContentText> {
  @override
  final Iterable<Type> types = const [ContentText, _$ContentText];

  @override
  final String wireName = r'ContentText';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    ContentText object, {
    FullType specifiedType = FullType.unspecified,
  }) sync* {
  }

  @override
  Object serialize(
    Serializers serializers,
    ContentText object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final anyOf = object.anyOf;
    return serializers.serialize(anyOf, specifiedType: FullType(AnyOf, anyOf.valueTypes.map((type) => FullType(type)).toList()))!;
  }

  @override
  ContentText deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = ContentTextBuilder();
    Object? anyOfDataSrc;
    final targetType = const FullType(AnyOf, [FullType(String), FullType(ModelNull), ]);
    anyOfDataSrc = serialized;
    result.anyOf = serializers.deserialize(anyOfDataSrc, specifiedType: targetType) as AnyOf;
    return result.build();
  }
}


//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:coindetude_api/src/model/model_null.dart';
import 'dart:core';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';
import 'package:one_of/any_of.dart';

part 'icon_url.g.dart';

/// IconUrl
@BuiltValue()
abstract class IconUrl implements Built<IconUrl, IconUrlBuilder> {
  /// Any Of [ModelNull], [String]
  AnyOf get anyOf;

  IconUrl._();

  factory IconUrl([void updates(IconUrlBuilder b)]) = _$IconUrl;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(IconUrlBuilder b) => b;

  @BuiltValueSerializer(custom: true)
  static Serializer<IconUrl> get serializer => _$IconUrlSerializer();
}

class _$IconUrlSerializer implements PrimitiveSerializer<IconUrl> {
  @override
  final Iterable<Type> types = const [IconUrl, _$IconUrl];

  @override
  final String wireName = r'IconUrl';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    IconUrl object, {
    FullType specifiedType = FullType.unspecified,
  }) sync* {
  }

  @override
  Object serialize(
    Serializers serializers,
    IconUrl object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final anyOf = object.anyOf;
    return serializers.serialize(anyOf, specifiedType: FullType(AnyOf, anyOf.valueTypes.map((type) => FullType(type)).toList()))!;
  }

  @override
  IconUrl deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = IconUrlBuilder();
    Object? anyOfDataSrc;
    final targetType = const FullType(AnyOf, [FullType(String), FullType(ModelNull), ]);
    anyOfDataSrc = serialized;
    result.anyOf = serializers.deserialize(anyOfDataSrc, specifiedType: targetType) as AnyOf;
    return result.build();
  }
}


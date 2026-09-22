//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:coindetude_api/src/model/model_null.dart';
import 'dart:core';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';
import 'package:one_of/any_of.dart';

part 'chapter_id.g.dart';

/// ChapterId
@BuiltValue()
abstract class ChapterId implements Built<ChapterId, ChapterIdBuilder> {
  /// Any Of [ModelNull], [String]
  AnyOf get anyOf;

  ChapterId._();

  factory ChapterId([void updates(ChapterIdBuilder b)]) = _$ChapterId;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(ChapterIdBuilder b) => b;

  @BuiltValueSerializer(custom: true)
  static Serializer<ChapterId> get serializer => _$ChapterIdSerializer();
}

class _$ChapterIdSerializer implements PrimitiveSerializer<ChapterId> {
  @override
  final Iterable<Type> types = const [ChapterId, _$ChapterId];

  @override
  final String wireName = r'ChapterId';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    ChapterId object, {
    FullType specifiedType = FullType.unspecified,
  }) sync* {
  }

  @override
  Object serialize(
    Serializers serializers,
    ChapterId object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final anyOf = object.anyOf;
    return serializers.serialize(anyOf, specifiedType: FullType(AnyOf, anyOf.valueTypes.map((type) => FullType(type)).toList()))!;
  }

  @override
  ChapterId deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = ChapterIdBuilder();
    Object? anyOfDataSrc;
    final targetType = const FullType(AnyOf, [FullType(String), FullType(ModelNull), ]);
    anyOfDataSrc = serialized;
    result.anyOf = serializers.deserialize(anyOfDataSrc, specifiedType: targetType) as AnyOf;
    return result.build();
  }
}


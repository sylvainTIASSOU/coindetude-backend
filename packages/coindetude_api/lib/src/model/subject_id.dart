//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:coindetude_api/src/model/model_null.dart';
import 'dart:core';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';
import 'package:one_of/any_of.dart';

part 'subject_id.g.dart';

/// SubjectId
@BuiltValue()
abstract class SubjectId implements Built<SubjectId, SubjectIdBuilder> {
  /// Any Of [ModelNull], [String]
  AnyOf get anyOf;

  SubjectId._();

  factory SubjectId([void updates(SubjectIdBuilder b)]) = _$SubjectId;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(SubjectIdBuilder b) => b;

  @BuiltValueSerializer(custom: true)
  static Serializer<SubjectId> get serializer => _$SubjectIdSerializer();
}

class _$SubjectIdSerializer implements PrimitiveSerializer<SubjectId> {
  @override
  final Iterable<Type> types = const [SubjectId, _$SubjectId];

  @override
  final String wireName = r'SubjectId';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    SubjectId object, {
    FullType specifiedType = FullType.unspecified,
  }) sync* {
  }

  @override
  Object serialize(
    Serializers serializers,
    SubjectId object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final anyOf = object.anyOf;
    return serializers.serialize(anyOf, specifiedType: FullType(AnyOf, anyOf.valueTypes.map((type) => FullType(type)).toList()))!;
  }

  @override
  SubjectId deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = SubjectIdBuilder();
    Object? anyOfDataSrc;
    final targetType = const FullType(AnyOf, [FullType(String), FullType(ModelNull), ]);
    anyOfDataSrc = serialized;
    result.anyOf = serializers.deserialize(anyOfDataSrc, specifiedType: targetType) as AnyOf;
    return result.build();
  }
}


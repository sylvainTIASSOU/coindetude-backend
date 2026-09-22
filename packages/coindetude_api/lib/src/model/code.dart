//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:coindetude_api/src/model/model_null.dart';
import 'dart:core';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';
import 'package:one_of/any_of.dart';

part 'code.g.dart';

/// Code
@BuiltValue()
abstract class Code implements Built<Code, CodeBuilder> {
  /// Any Of [ModelNull], [String]
  AnyOf get anyOf;

  Code._();

  factory Code([void updates(CodeBuilder b)]) = _$Code;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(CodeBuilder b) => b;

  @BuiltValueSerializer(custom: true)
  static Serializer<Code> get serializer => _$CodeSerializer();
}

class _$CodeSerializer implements PrimitiveSerializer<Code> {
  @override
  final Iterable<Type> types = const [Code, _$Code];

  @override
  final String wireName = r'Code';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    Code object, {
    FullType specifiedType = FullType.unspecified,
  }) sync* {
  }

  @override
  Object serialize(
    Serializers serializers,
    Code object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final anyOf = object.anyOf;
    return serializers.serialize(anyOf, specifiedType: FullType(AnyOf, anyOf.valueTypes.map((type) => FullType(type)).toList()))!;
  }

  @override
  Code deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = CodeBuilder();
    Object? anyOfDataSrc;
    final targetType = const FullType(AnyOf, [FullType(String), FullType(ModelNull), ]);
    anyOfDataSrc = serialized;
    result.anyOf = serializers.deserialize(anyOfDataSrc, specifiedType: targetType) as AnyOf;
    return result.build();
  }
}


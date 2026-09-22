//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:coindetude_api/src/model/model_null.dart';
import 'dart:core';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';
import 'package:one_of/any_of.dart';

part 'name1.g.dart';

/// Name1
@BuiltValue()
abstract class Name1 implements Built<Name1, Name1Builder> {
  /// Any Of [ModelNull], [String]
  AnyOf get anyOf;

  Name1._();

  factory Name1([void updates(Name1Builder b)]) = _$Name1;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(Name1Builder b) => b;

  @BuiltValueSerializer(custom: true)
  static Serializer<Name1> get serializer => _$Name1Serializer();
}

class _$Name1Serializer implements PrimitiveSerializer<Name1> {
  @override
  final Iterable<Type> types = const [Name1, _$Name1];

  @override
  final String wireName = r'Name1';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    Name1 object, {
    FullType specifiedType = FullType.unspecified,
  }) sync* {
  }

  @override
  Object serialize(
    Serializers serializers,
    Name1 object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final anyOf = object.anyOf;
    return serializers.serialize(anyOf, specifiedType: FullType(AnyOf, anyOf.valueTypes.map((type) => FullType(type)).toList()))!;
  }

  @override
  Name1 deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = Name1Builder();
    Object? anyOfDataSrc;
    final targetType = const FullType(AnyOf, [FullType(String), FullType(ModelNull), ]);
    anyOfDataSrc = serialized;
    result.anyOf = serializers.deserialize(anyOfDataSrc, specifiedType: targetType) as AnyOf;
    return result.build();
  }
}


//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:coindetude_api/src/model/model_null.dart';
import 'dart:core';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';
import 'package:one_of/any_of.dart';

part 'name2.g.dart';

/// Name2
@BuiltValue()
abstract class Name2 implements Built<Name2, Name2Builder> {
  /// Any Of [ModelNull], [String]
  AnyOf get anyOf;

  Name2._();

  factory Name2([void updates(Name2Builder b)]) = _$Name2;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(Name2Builder b) => b;

  @BuiltValueSerializer(custom: true)
  static Serializer<Name2> get serializer => _$Name2Serializer();
}

class _$Name2Serializer implements PrimitiveSerializer<Name2> {
  @override
  final Iterable<Type> types = const [Name2, _$Name2];

  @override
  final String wireName = r'Name2';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    Name2 object, {
    FullType specifiedType = FullType.unspecified,
  }) sync* {
  }

  @override
  Object serialize(
    Serializers serializers,
    Name2 object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final anyOf = object.anyOf;
    return serializers.serialize(anyOf, specifiedType: FullType(AnyOf, anyOf.valueTypes.map((type) => FullType(type)).toList()))!;
  }

  @override
  Name2 deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = Name2Builder();
    Object? anyOfDataSrc;
    final targetType = const FullType(AnyOf, [FullType(String), FullType(ModelNull), ]);
    anyOfDataSrc = serialized;
    result.anyOf = serializers.deserialize(anyOfDataSrc, specifiedType: targetType) as AnyOf;
    return result.build();
  }
}


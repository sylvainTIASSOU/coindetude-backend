//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:coindetude_api/src/model/model_null.dart';
import 'dart:core';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';
import 'package:one_of/any_of.dart';

part 'name.g.dart';

/// Name
@BuiltValue()
abstract class Name implements Built<Name, NameBuilder> {
  /// Any Of [ModelNull], [String]
  AnyOf get anyOf;

  Name._();

  factory Name([void updates(NameBuilder b)]) = _$Name;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(NameBuilder b) => b;

  @BuiltValueSerializer(custom: true)
  static Serializer<Name> get serializer => _$NameSerializer();
}

class _$NameSerializer implements PrimitiveSerializer<Name> {
  @override
  final Iterable<Type> types = const [Name, _$Name];

  @override
  final String wireName = r'Name';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    Name object, {
    FullType specifiedType = FullType.unspecified,
  }) sync* {
  }

  @override
  Object serialize(
    Serializers serializers,
    Name object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final anyOf = object.anyOf;
    return serializers.serialize(anyOf, specifiedType: FullType(AnyOf, anyOf.valueTypes.map((type) => FullType(type)).toList()))!;
  }

  @override
  Name deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = NameBuilder();
    Object? anyOfDataSrc;
    final targetType = const FullType(AnyOf, [FullType(String), FullType(ModelNull), ]);
    anyOfDataSrc = serialized;
    result.anyOf = serializers.deserialize(anyOfDataSrc, specifiedType: targetType) as AnyOf;
    return result.build();
  }
}


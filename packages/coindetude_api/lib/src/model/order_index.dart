//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:coindetude_api/src/model/model_null.dart';
import 'dart:core';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';
import 'package:one_of/any_of.dart';

part 'order_index.g.dart';

/// OrderIndex
@BuiltValue()
abstract class OrderIndex implements Built<OrderIndex, OrderIndexBuilder> {
  /// Any Of [ModelNull], [int]
  AnyOf get anyOf;

  OrderIndex._();

  factory OrderIndex([void updates(OrderIndexBuilder b)]) = _$OrderIndex;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(OrderIndexBuilder b) => b;

  @BuiltValueSerializer(custom: true)
  static Serializer<OrderIndex> get serializer => _$OrderIndexSerializer();
}

class _$OrderIndexSerializer implements PrimitiveSerializer<OrderIndex> {
  @override
  final Iterable<Type> types = const [OrderIndex, _$OrderIndex];

  @override
  final String wireName = r'OrderIndex';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    OrderIndex object, {
    FullType specifiedType = FullType.unspecified,
  }) sync* {
  }

  @override
  Object serialize(
    Serializers serializers,
    OrderIndex object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final anyOf = object.anyOf;
    return serializers.serialize(anyOf, specifiedType: FullType(AnyOf, anyOf.valueTypes.map((type) => FullType(type)).toList()))!;
  }

  @override
  OrderIndex deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = OrderIndexBuilder();
    Object? anyOfDataSrc;
    final targetType = const FullType(AnyOf, [FullType(int), FullType(ModelNull), ]);
    anyOfDataSrc = serialized;
    result.anyOf = serializers.deserialize(anyOfDataSrc, specifiedType: targetType) as AnyOf;
    return result.build();
  }
}


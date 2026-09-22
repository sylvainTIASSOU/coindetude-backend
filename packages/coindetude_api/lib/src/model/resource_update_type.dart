//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:coindetude_api/src/model/model_null.dart';
import 'package:coindetude_api/src/model/resource_type.dart';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';
import 'package:one_of/any_of.dart';

part 'resource_update_type.g.dart';

/// ResourceUpdateType
@BuiltValue()
abstract class ResourceUpdateType implements Built<ResourceUpdateType, ResourceUpdateTypeBuilder> {
  /// Any Of [ModelNull], [ResourceType]
  AnyOf get anyOf;

  ResourceUpdateType._();

  factory ResourceUpdateType([void updates(ResourceUpdateTypeBuilder b)]) = _$ResourceUpdateType;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(ResourceUpdateTypeBuilder b) => b;

  @BuiltValueSerializer(custom: true)
  static Serializer<ResourceUpdateType> get serializer => _$ResourceUpdateTypeSerializer();
}

class _$ResourceUpdateTypeSerializer implements PrimitiveSerializer<ResourceUpdateType> {
  @override
  final Iterable<Type> types = const [ResourceUpdateType, _$ResourceUpdateType];

  @override
  final String wireName = r'ResourceUpdateType';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    ResourceUpdateType object, {
    FullType specifiedType = FullType.unspecified,
  }) sync* {
  }

  @override
  Object serialize(
    Serializers serializers,
    ResourceUpdateType object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final anyOf = object.anyOf;
    return serializers.serialize(anyOf, specifiedType: FullType(AnyOf, anyOf.valueTypes.map((type) => FullType(type)).toList()))!;
  }

  @override
  ResourceUpdateType deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = ResourceUpdateTypeBuilder();
    Object? anyOfDataSrc;
    final targetType = const FullType(AnyOf, [FullType(ResourceType), FullType(ModelNull), ]);
    anyOfDataSrc = serialized;
    result.anyOf = serializers.deserialize(anyOfDataSrc, specifiedType: targetType) as AnyOf;
    return result.build();
  }
}


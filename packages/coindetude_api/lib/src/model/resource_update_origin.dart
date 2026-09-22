//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:coindetude_api/src/model/model_null.dart';
import 'package:coindetude_api/src/model/resource_origin.dart';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';
import 'package:one_of/any_of.dart';

part 'resource_update_origin.g.dart';

/// ResourceUpdateOrigin
@BuiltValue()
abstract class ResourceUpdateOrigin implements Built<ResourceUpdateOrigin, ResourceUpdateOriginBuilder> {
  /// Any Of [ModelNull], [ResourceOrigin]
  AnyOf get anyOf;

  ResourceUpdateOrigin._();

  factory ResourceUpdateOrigin([void updates(ResourceUpdateOriginBuilder b)]) = _$ResourceUpdateOrigin;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(ResourceUpdateOriginBuilder b) => b;

  @BuiltValueSerializer(custom: true)
  static Serializer<ResourceUpdateOrigin> get serializer => _$ResourceUpdateOriginSerializer();
}

class _$ResourceUpdateOriginSerializer implements PrimitiveSerializer<ResourceUpdateOrigin> {
  @override
  final Iterable<Type> types = const [ResourceUpdateOrigin, _$ResourceUpdateOrigin];

  @override
  final String wireName = r'ResourceUpdateOrigin';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    ResourceUpdateOrigin object, {
    FullType specifiedType = FullType.unspecified,
  }) sync* {
  }

  @override
  Object serialize(
    Serializers serializers,
    ResourceUpdateOrigin object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final anyOf = object.anyOf;
    return serializers.serialize(anyOf, specifiedType: FullType(AnyOf, anyOf.valueTypes.map((type) => FullType(type)).toList()))!;
  }

  @override
  ResourceUpdateOrigin deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = ResourceUpdateOriginBuilder();
    Object? anyOfDataSrc;
    final targetType = const FullType(AnyOf, [FullType(ResourceOrigin), FullType(ModelNull), ]);
    anyOfDataSrc = serialized;
    result.anyOf = serializers.deserialize(anyOfDataSrc, specifiedType: targetType) as AnyOf;
    return result.build();
  }
}


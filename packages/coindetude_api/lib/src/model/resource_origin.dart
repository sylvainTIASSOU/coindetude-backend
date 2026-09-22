//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:built_collection/built_collection.dart';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';

part 'resource_origin.g.dart';

class ResourceOrigin extends EnumClass {

  /// Source d'une ressource pédagogique.
  @BuiltValueEnumConst(wireName: r'admin')
  static const ResourceOrigin admin = _$admin;
  /// Source d'une ressource pédagogique.
  @BuiltValueEnumConst(wireName: r'teacher')
  static const ResourceOrigin teacher = _$teacher;
  /// Source d'une ressource pédagogique.
  @BuiltValueEnumConst(wireName: r'ia')
  static const ResourceOrigin ia = _$ia;

  static Serializer<ResourceOrigin> get serializer => _$resourceOriginSerializer;

  const ResourceOrigin._(String name): super(name);

  static BuiltSet<ResourceOrigin> get values => _$values;
  static ResourceOrigin valueOf(String name) => _$valueOf(name);
}

/// Optionally, enum_class can generate a mixin to go with your enum for use
/// with Angular. It exposes your enum constants as getters. So, if you mix it
/// in to your Dart component class, the values become available to the
/// corresponding Angular template.
///
/// Trigger mixin generation by writing a line like this one next to your enum.
abstract class ResourceOriginMixin = Object with _$ResourceOriginMixin;


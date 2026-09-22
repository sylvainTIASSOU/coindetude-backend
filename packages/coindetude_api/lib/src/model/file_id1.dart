//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:coindetude_api/src/model/model_null.dart';
import 'dart:core';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';
import 'package:one_of/any_of.dart';

part 'file_id1.g.dart';

/// FileId1
@BuiltValue()
abstract class FileId1 implements Built<FileId1, FileId1Builder> {
  /// Any Of [ModelNull], [String]
  AnyOf get anyOf;

  FileId1._();

  factory FileId1([void updates(FileId1Builder b)]) = _$FileId1;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(FileId1Builder b) => b;

  @BuiltValueSerializer(custom: true)
  static Serializer<FileId1> get serializer => _$FileId1Serializer();
}

class _$FileId1Serializer implements PrimitiveSerializer<FileId1> {
  @override
  final Iterable<Type> types = const [FileId1, _$FileId1];

  @override
  final String wireName = r'FileId1';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    FileId1 object, {
    FullType specifiedType = FullType.unspecified,
  }) sync* {
  }

  @override
  Object serialize(
    Serializers serializers,
    FileId1 object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final anyOf = object.anyOf;
    return serializers.serialize(anyOf, specifiedType: FullType(AnyOf, anyOf.valueTypes.map((type) => FullType(type)).toList()))!;
  }

  @override
  FileId1 deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = FileId1Builder();
    Object? anyOfDataSrc;
    final targetType = const FullType(AnyOf, [FullType(String), FullType(ModelNull), ]);
    anyOfDataSrc = serialized;
    result.anyOf = serializers.deserialize(anyOfDataSrc, specifiedType: targetType) as AnyOf;
    return result.build();
  }
}


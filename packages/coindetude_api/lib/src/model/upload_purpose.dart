//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:built_collection/built_collection.dart';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';

part 'upload_purpose.g.dart';

class UploadPurpose extends EnumClass {

  /// Purpose déclaré par le client au presign.
  @BuiltValueEnumConst(wireName: r'avatar')
  static const UploadPurpose avatar = _$avatar;
  /// Purpose déclaré par le client au presign.
  @BuiltValueEnumConst(wireName: r'homework_scan')
  static const UploadPurpose homeworkScan = _$homeworkScan;
  /// Purpose déclaré par le client au presign.
  @BuiltValueEnumConst(wireName: r'resource_pdf')
  static const UploadPurpose resourcePdf = _$resourcePdf;

  static Serializer<UploadPurpose> get serializer => _$uploadPurposeSerializer;

  const UploadPurpose._(String name): super(name);

  static BuiltSet<UploadPurpose> get values => _$values;
  static UploadPurpose valueOf(String name) => _$valueOf(name);
}

/// Optionally, enum_class can generate a mixin to go with your enum for use
/// with Angular. It exposes your enum constants as getters. So, if you mix it
/// in to your Dart component class, the values become available to the
/// corresponding Angular template.
///
/// Trigger mixin generation by writing a line like this one next to your enum.
abstract class UploadPurposeMixin = Object with _$UploadPurposeMixin;


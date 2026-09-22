//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:built_collection/built_collection.dart';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';

part 'file_status.g.dart';

class FileStatus extends EnumClass {

  /// Statut d'un fichier dans son cycle de vie.
  @BuiltValueEnumConst(wireName: r'pending')
  static const FileStatus pending = _$pending;
  /// Statut d'un fichier dans son cycle de vie.
  @BuiltValueEnumConst(wireName: r'uploaded')
  static const FileStatus uploaded = _$uploaded;
  /// Statut d'un fichier dans son cycle de vie.
  @BuiltValueEnumConst(wireName: r'failed')
  static const FileStatus failed = _$failed;

  static Serializer<FileStatus> get serializer => _$fileStatusSerializer;

  const FileStatus._(String name): super(name);

  static BuiltSet<FileStatus> get values => _$values;
  static FileStatus valueOf(String name) => _$valueOf(name);
}

/// Optionally, enum_class can generate a mixin to go with your enum for use
/// with Angular. It exposes your enum constants as getters. So, if you mix it
/// in to your Dart component class, the values become available to the
/// corresponding Angular template.
///
/// Trigger mixin generation by writing a line like this one next to your enum.
abstract class FileStatusMixin = Object with _$FileStatusMixin;


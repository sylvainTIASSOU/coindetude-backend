//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:built_collection/built_collection.dart';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';

part 'sync_operation.g.dart';

class SyncOperation extends EnumClass {

  /// Opération CRDT envoyée par un client offline-first.
  @BuiltValueEnumConst(wireName: r'create')
  static const SyncOperation create = _$create;
  /// Opération CRDT envoyée par un client offline-first.
  @BuiltValueEnumConst(wireName: r'update')
  static const SyncOperation update = _$update;
  /// Opération CRDT envoyée par un client offline-first.
  @BuiltValueEnumConst(wireName: r'delete')
  static const SyncOperation delete = _$delete;

  static Serializer<SyncOperation> get serializer => _$syncOperationSerializer;

  const SyncOperation._(String name): super(name);

  static BuiltSet<SyncOperation> get values => _$values;
  static SyncOperation valueOf(String name) => _$valueOf(name);
}

/// Optionally, enum_class can generate a mixin to go with your enum for use
/// with Angular. It exposes your enum constants as getters. So, if you mix it
/// in to your Dart component class, the values become available to the
/// corresponding Angular template.
///
/// Trigger mixin generation by writing a line like this one next to your enum.
abstract class SyncOperationMixin = Object with _$SyncOperationMixin;


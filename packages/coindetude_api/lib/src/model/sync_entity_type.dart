//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:built_collection/built_collection.dart';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';

part 'sync_entity_type.g.dart';

class SyncEntityType extends EnumClass {

  /// Types d'entités supportés par /sync/apply-event.
  @BuiltValueEnumConst(wireName: r'planning_task')
  static const SyncEntityType planningTask = _$planningTask;
  /// Types d'entités supportés par /sync/apply-event.
  @BuiltValueEnumConst(wireName: r'xp_event')
  static const SyncEntityType xpEvent = _$xpEvent;
  /// Types d'entités supportés par /sync/apply-event.
  @BuiltValueEnumConst(wireName: r'streak_event')
  static const SyncEntityType streakEvent = _$streakEvent;

  static Serializer<SyncEntityType> get serializer => _$syncEntityTypeSerializer;

  const SyncEntityType._(String name): super(name);

  static BuiltSet<SyncEntityType> get values => _$values;
  static SyncEntityType valueOf(String name) => _$valueOf(name);
}

/// Optionally, enum_class can generate a mixin to go with your enum for use
/// with Angular. It exposes your enum constants as getters. So, if you mix it
/// in to your Dart component class, the values become available to the
/// corresponding Angular template.
///
/// Trigger mixin generation by writing a line like this one next to your enum.
abstract class SyncEntityTypeMixin = Object with _$SyncEntityTypeMixin;


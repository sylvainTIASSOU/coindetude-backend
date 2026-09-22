//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:built_collection/built_collection.dart';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';

part 'cycle.g.dart';

class Cycle extends EnumClass {

  /// Cycle d'enseignement au Togo.  Le lycée est scindé en deux types car les séries, les programmes et les examens diffèrent : - ``lycee_moderne`` : séries générales (A4, C, D, E...) - ``lycee_technique`` : séries techniques (F1, F2, F3, F4...)
  @BuiltValueEnumConst(wireName: r'college')
  static const Cycle college = _$college;
  /// Cycle d'enseignement au Togo.  Le lycée est scindé en deux types car les séries, les programmes et les examens diffèrent : - ``lycee_moderne`` : séries générales (A4, C, D, E...) - ``lycee_technique`` : séries techniques (F1, F2, F3, F4...)
  @BuiltValueEnumConst(wireName: r'lycee_moderne')
  static const Cycle lyceeModerne = _$lyceeModerne;
  /// Cycle d'enseignement au Togo.  Le lycée est scindé en deux types car les séries, les programmes et les examens diffèrent : - ``lycee_moderne`` : séries générales (A4, C, D, E...) - ``lycee_technique`` : séries techniques (F1, F2, F3, F4...)
  @BuiltValueEnumConst(wireName: r'lycee_technique')
  static const Cycle lyceeTechnique = _$lyceeTechnique;

  static Serializer<Cycle> get serializer => _$cycleSerializer;

  const Cycle._(String name): super(name);

  static BuiltSet<Cycle> get values => _$values;
  static Cycle valueOf(String name) => _$valueOf(name);
}

/// Optionally, enum_class can generate a mixin to go with your enum for use
/// with Angular. It exposes your enum constants as getters. So, if you mix it
/// in to your Dart component class, the values become available to the
/// corresponding Angular template.
///
/// Trigger mixin generation by writing a line like this one next to your enum.
abstract class CycleMixin = Object with _$CycleMixin;


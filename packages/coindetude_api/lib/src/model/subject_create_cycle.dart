//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:coindetude_api/src/model/model_null.dart';
import 'package:coindetude_api/src/model/cycle.dart';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';
import 'package:one_of/any_of.dart';

part 'subject_create_cycle.g.dart';

/// NULL = matière transverse à tous les cycles
@BuiltValue()
abstract class SubjectCreateCycle implements Built<SubjectCreateCycle, SubjectCreateCycleBuilder> {
  /// Any Of [Cycle], [ModelNull]
  AnyOf get anyOf;

  SubjectCreateCycle._();

  factory SubjectCreateCycle([void updates(SubjectCreateCycleBuilder b)]) = _$SubjectCreateCycle;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(SubjectCreateCycleBuilder b) => b;

  @BuiltValueSerializer(custom: true)
  static Serializer<SubjectCreateCycle> get serializer => _$SubjectCreateCycleSerializer();
}

class _$SubjectCreateCycleSerializer implements PrimitiveSerializer<SubjectCreateCycle> {
  @override
  final Iterable<Type> types = const [SubjectCreateCycle, _$SubjectCreateCycle];

  @override
  final String wireName = r'SubjectCreateCycle';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    SubjectCreateCycle object, {
    FullType specifiedType = FullType.unspecified,
  }) sync* {
  }

  @override
  Object serialize(
    Serializers serializers,
    SubjectCreateCycle object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final anyOf = object.anyOf;
    return serializers.serialize(anyOf, specifiedType: FullType(AnyOf, anyOf.valueTypes.map((type) => FullType(type)).toList()))!;
  }

  @override
  SubjectCreateCycle deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = SubjectCreateCycleBuilder();
    Object? anyOfDataSrc;
    final targetType = const FullType(AnyOf, [FullType(Cycle), FullType(ModelNull), ]);
    anyOfDataSrc = serialized;
    result.anyOf = serializers.deserialize(anyOfDataSrc, specifiedType: targetType) as AnyOf;
    return result.build();
  }
}


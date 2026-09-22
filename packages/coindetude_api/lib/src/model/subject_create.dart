//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:built_collection/built_collection.dart';
import 'package:coindetude_api/src/model/icon_url.dart';
import 'package:coindetude_api/src/model/subject_create_cycle.dart';
import 'package:built_value/json_object.dart';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';

part 'subject_create.g.dart';

/// SubjectCreate
///
/// Properties:
/// * [name] 
/// * [iconUrl] 
/// * [cycle] 
@BuiltValue()
abstract class SubjectCreate implements Built<SubjectCreate, SubjectCreateBuilder> {
  @BuiltValueField(wireName: r'name')
  String get name;

  @BuiltValueField(wireName: r'icon_url')
  IconUrl? get iconUrl;

  @BuiltValueField(wireName: r'cycle')
  SubjectCreateCycle? get cycle;

  SubjectCreate._();

  factory SubjectCreate([void updates(SubjectCreateBuilder b)]) = _$SubjectCreate;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(SubjectCreateBuilder b) => b;

  @BuiltValueSerializer(custom: true)
  static Serializer<SubjectCreate> get serializer => _$SubjectCreateSerializer();
}

class _$SubjectCreateSerializer implements PrimitiveSerializer<SubjectCreate> {
  @override
  final Iterable<Type> types = const [SubjectCreate, _$SubjectCreate];

  @override
  final String wireName = r'SubjectCreate';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    SubjectCreate object, {
    FullType specifiedType = FullType.unspecified,
  }) sync* {
    yield r'name';
    yield serializers.serialize(
      object.name,
      specifiedType: const FullType(String),
    );
    if (object.iconUrl != null) {
      yield r'icon_url';
      yield serializers.serialize(
        object.iconUrl,
        specifiedType: const FullType(IconUrl),
      );
    }
    if (object.cycle != null) {
      yield r'cycle';
      yield serializers.serialize(
        object.cycle,
        specifiedType: const FullType(SubjectCreateCycle),
      );
    }
  }

  @override
  Object serialize(
    Serializers serializers,
    SubjectCreate object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    return _serializeProperties(serializers, object, specifiedType: specifiedType).toList();
  }

  void _deserializeProperties(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
    required List<Object?> serializedList,
    required SubjectCreateBuilder result,
    required List<Object?> unhandled,
  }) {
    for (var i = 0; i < serializedList.length; i += 2) {
      final key = serializedList[i] as String;
      final value = serializedList[i + 1];
      switch (key) {
        case r'name':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(String),
          ) as String;
          result.name = valueDes;
          break;
        case r'icon_url':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(IconUrl),
          ) as IconUrl;
          result.iconUrl.replace(valueDes);
          break;
        case r'cycle':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(SubjectCreateCycle),
          ) as SubjectCreateCycle;
          result.cycle.replace(valueDes);
          break;
        default:
          unhandled.add(key);
          unhandled.add(value);
          break;
      }
    }
  }

  @override
  SubjectCreate deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = SubjectCreateBuilder();
    final serializedList = (serialized as Iterable<Object?>).toList();
    final unhandled = <Object?>[];
    _deserializeProperties(
      serializers,
      serialized,
      specifiedType: specifiedType,
      serializedList: serializedList,
      unhandled: unhandled,
      result: result,
    );
    return result.build();
  }
}


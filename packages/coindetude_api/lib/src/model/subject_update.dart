//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:coindetude_api/src/model/name2.dart';
import 'package:built_collection/built_collection.dart';
import 'package:coindetude_api/src/model/icon_url.dart';
import 'package:built_value/json_object.dart';
import 'package:coindetude_api/src/model/level_update_cycle.dart';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';

part 'subject_update.g.dart';

/// SubjectUpdate
///
/// Properties:
/// * [name] 
/// * [iconUrl] 
/// * [cycle] 
@BuiltValue()
abstract class SubjectUpdate implements Built<SubjectUpdate, SubjectUpdateBuilder> {
  @BuiltValueField(wireName: r'name')
  Name2? get name;

  @BuiltValueField(wireName: r'icon_url')
  IconUrl? get iconUrl;

  @BuiltValueField(wireName: r'cycle')
  LevelUpdateCycle? get cycle;

  SubjectUpdate._();

  factory SubjectUpdate([void updates(SubjectUpdateBuilder b)]) = _$SubjectUpdate;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(SubjectUpdateBuilder b) => b;

  @BuiltValueSerializer(custom: true)
  static Serializer<SubjectUpdate> get serializer => _$SubjectUpdateSerializer();
}

class _$SubjectUpdateSerializer implements PrimitiveSerializer<SubjectUpdate> {
  @override
  final Iterable<Type> types = const [SubjectUpdate, _$SubjectUpdate];

  @override
  final String wireName = r'SubjectUpdate';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    SubjectUpdate object, {
    FullType specifiedType = FullType.unspecified,
  }) sync* {
    if (object.name != null) {
      yield r'name';
      yield serializers.serialize(
        object.name,
        specifiedType: const FullType(Name2),
      );
    }
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
        specifiedType: const FullType(LevelUpdateCycle),
      );
    }
  }

  @override
  Object serialize(
    Serializers serializers,
    SubjectUpdate object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    return _serializeProperties(serializers, object, specifiedType: specifiedType).toList();
  }

  void _deserializeProperties(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
    required List<Object?> serializedList,
    required SubjectUpdateBuilder result,
    required List<Object?> unhandled,
  }) {
    for (var i = 0; i < serializedList.length; i += 2) {
      final key = serializedList[i] as String;
      final value = serializedList[i + 1];
      switch (key) {
        case r'name':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(Name2),
          ) as Name2;
          result.name.replace(valueDes);
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
            specifiedType: const FullType(LevelUpdateCycle),
          ) as LevelUpdateCycle;
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
  SubjectUpdate deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = SubjectUpdateBuilder();
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


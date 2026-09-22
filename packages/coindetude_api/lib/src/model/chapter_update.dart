//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:coindetude_api/src/model/order_index.dart';
import 'package:built_collection/built_collection.dart';
import 'package:coindetude_api/src/model/description.dart';
import 'package:coindetude_api/src/model/title.dart';
import 'package:coindetude_api/src/model/subject_id.dart';
import 'package:built_value/json_object.dart';
import 'package:coindetude_api/src/model/level_id.dart';
import 'package:coindetude_api/src/model/series_id1.dart';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';

part 'chapter_update.g.dart';

/// ChapterUpdate
///
/// Properties:
/// * [levelId] 
/// * [subjectId] 
/// * [seriesId] 
/// * [title] 
/// * [description] 
/// * [orderIndex] 
@BuiltValue()
abstract class ChapterUpdate implements Built<ChapterUpdate, ChapterUpdateBuilder> {
  @BuiltValueField(wireName: r'level_id')
  LevelId? get levelId;

  @BuiltValueField(wireName: r'subject_id')
  SubjectId? get subjectId;

  @BuiltValueField(wireName: r'series_id')
  SeriesId1? get seriesId;

  @BuiltValueField(wireName: r'title')
  Title? get title;

  @BuiltValueField(wireName: r'description')
  Description? get description;

  @BuiltValueField(wireName: r'order_index')
  OrderIndex? get orderIndex;

  ChapterUpdate._();

  factory ChapterUpdate([void updates(ChapterUpdateBuilder b)]) = _$ChapterUpdate;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(ChapterUpdateBuilder b) => b;

  @BuiltValueSerializer(custom: true)
  static Serializer<ChapterUpdate> get serializer => _$ChapterUpdateSerializer();
}

class _$ChapterUpdateSerializer implements PrimitiveSerializer<ChapterUpdate> {
  @override
  final Iterable<Type> types = const [ChapterUpdate, _$ChapterUpdate];

  @override
  final String wireName = r'ChapterUpdate';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    ChapterUpdate object, {
    FullType specifiedType = FullType.unspecified,
  }) sync* {
    if (object.levelId != null) {
      yield r'level_id';
      yield serializers.serialize(
        object.levelId,
        specifiedType: const FullType(LevelId),
      );
    }
    if (object.subjectId != null) {
      yield r'subject_id';
      yield serializers.serialize(
        object.subjectId,
        specifiedType: const FullType(SubjectId),
      );
    }
    if (object.seriesId != null) {
      yield r'series_id';
      yield serializers.serialize(
        object.seriesId,
        specifiedType: const FullType(SeriesId1),
      );
    }
    if (object.title != null) {
      yield r'title';
      yield serializers.serialize(
        object.title,
        specifiedType: const FullType(Title),
      );
    }
    if (object.description != null) {
      yield r'description';
      yield serializers.serialize(
        object.description,
        specifiedType: const FullType(Description),
      );
    }
    if (object.orderIndex != null) {
      yield r'order_index';
      yield serializers.serialize(
        object.orderIndex,
        specifiedType: const FullType(OrderIndex),
      );
    }
  }

  @override
  Object serialize(
    Serializers serializers,
    ChapterUpdate object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    return _serializeProperties(serializers, object, specifiedType: specifiedType).toList();
  }

  void _deserializeProperties(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
    required List<Object?> serializedList,
    required ChapterUpdateBuilder result,
    required List<Object?> unhandled,
  }) {
    for (var i = 0; i < serializedList.length; i += 2) {
      final key = serializedList[i] as String;
      final value = serializedList[i + 1];
      switch (key) {
        case r'level_id':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(LevelId),
          ) as LevelId;
          result.levelId.replace(valueDes);
          break;
        case r'subject_id':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(SubjectId),
          ) as SubjectId;
          result.subjectId.replace(valueDes);
          break;
        case r'series_id':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(SeriesId1),
          ) as SeriesId1;
          result.seriesId.replace(valueDes);
          break;
        case r'title':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(Title),
          ) as Title;
          result.title.replace(valueDes);
          break;
        case r'description':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(Description),
          ) as Description;
          result.description.replace(valueDes);
          break;
        case r'order_index':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(OrderIndex),
          ) as OrderIndex;
          result.orderIndex.replace(valueDes);
          break;
        default:
          unhandled.add(key);
          unhandled.add(value);
          break;
      }
    }
  }

  @override
  ChapterUpdate deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = ChapterUpdateBuilder();
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


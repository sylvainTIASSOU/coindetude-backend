//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:coindetude_api/src/model/series_id.dart';
import 'package:built_collection/built_collection.dart';
import 'package:coindetude_api/src/model/description.dart';
import 'package:built_value/json_object.dart';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';

part 'chapter_create.g.dart';

/// ChapterCreate
///
/// Properties:
/// * [levelId] 
/// * [subjectId] 
/// * [title] 
/// * [orderIndex] 
/// * [seriesId] 
/// * [description] 
@BuiltValue()
abstract class ChapterCreate implements Built<ChapterCreate, ChapterCreateBuilder> {
  @BuiltValueField(wireName: r'level_id')
  String get levelId;

  @BuiltValueField(wireName: r'subject_id')
  String get subjectId;

  @BuiltValueField(wireName: r'title')
  String get title;

  @BuiltValueField(wireName: r'order_index')
  int get orderIndex;

  @BuiltValueField(wireName: r'series_id')
  SeriesId? get seriesId;

  @BuiltValueField(wireName: r'description')
  Description? get description;

  ChapterCreate._();

  factory ChapterCreate([void updates(ChapterCreateBuilder b)]) = _$ChapterCreate;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(ChapterCreateBuilder b) => b;

  @BuiltValueSerializer(custom: true)
  static Serializer<ChapterCreate> get serializer => _$ChapterCreateSerializer();
}

class _$ChapterCreateSerializer implements PrimitiveSerializer<ChapterCreate> {
  @override
  final Iterable<Type> types = const [ChapterCreate, _$ChapterCreate];

  @override
  final String wireName = r'ChapterCreate';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    ChapterCreate object, {
    FullType specifiedType = FullType.unspecified,
  }) sync* {
    yield r'level_id';
    yield serializers.serialize(
      object.levelId,
      specifiedType: const FullType(String),
    );
    yield r'subject_id';
    yield serializers.serialize(
      object.subjectId,
      specifiedType: const FullType(String),
    );
    yield r'title';
    yield serializers.serialize(
      object.title,
      specifiedType: const FullType(String),
    );
    yield r'order_index';
    yield serializers.serialize(
      object.orderIndex,
      specifiedType: const FullType(int),
    );
    if (object.seriesId != null) {
      yield r'series_id';
      yield serializers.serialize(
        object.seriesId,
        specifiedType: const FullType(SeriesId),
      );
    }
    if (object.description != null) {
      yield r'description';
      yield serializers.serialize(
        object.description,
        specifiedType: const FullType(Description),
      );
    }
  }

  @override
  Object serialize(
    Serializers serializers,
    ChapterCreate object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    return _serializeProperties(serializers, object, specifiedType: specifiedType).toList();
  }

  void _deserializeProperties(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
    required List<Object?> serializedList,
    required ChapterCreateBuilder result,
    required List<Object?> unhandled,
  }) {
    for (var i = 0; i < serializedList.length; i += 2) {
      final key = serializedList[i] as String;
      final value = serializedList[i + 1];
      switch (key) {
        case r'level_id':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(String),
          ) as String;
          result.levelId = valueDes;
          break;
        case r'subject_id':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(String),
          ) as String;
          result.subjectId = valueDes;
          break;
        case r'title':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(String),
          ) as String;
          result.title = valueDes;
          break;
        case r'order_index':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(int),
          ) as int;
          result.orderIndex = valueDes;
          break;
        case r'series_id':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(SeriesId),
          ) as SeriesId;
          result.seriesId.replace(valueDes);
          break;
        case r'description':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(Description),
          ) as Description;
          result.description.replace(valueDes);
          break;
        default:
          unhandled.add(key);
          unhandled.add(value);
          break;
      }
    }
  }

  @override
  ChapterCreate deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = ChapterCreateBuilder();
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


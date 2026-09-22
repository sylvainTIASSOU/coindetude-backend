//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:coindetude_api/src/model/content_text1.dart';
import 'package:coindetude_api/src/model/resource_update_type.dart';
import 'package:coindetude_api/src/model/year.dart';
import 'package:built_collection/built_collection.dart';
import 'package:coindetude_api/src/model/title.dart';
import 'package:coindetude_api/src/model/chapter_id.dart';
import 'package:coindetude_api/src/model/resource_update_origin.dart';
import 'package:coindetude_api/src/model/file_id1.dart';
import 'package:built_value/json_object.dart';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';

part 'resource_update.g.dart';

/// ResourceUpdate
///
/// Properties:
/// * [chapterId] 
/// * [type] 
/// * [title] 
/// * [contentText] 
/// * [fileId] 
/// * [year] 
/// * [origin] 
@BuiltValue()
abstract class ResourceUpdate implements Built<ResourceUpdate, ResourceUpdateBuilder> {
  @BuiltValueField(wireName: r'chapter_id')
  ChapterId? get chapterId;

  @BuiltValueField(wireName: r'type')
  ResourceUpdateType? get type;

  @BuiltValueField(wireName: r'title')
  Title? get title;

  @BuiltValueField(wireName: r'content_text')
  ContentText1? get contentText;

  @BuiltValueField(wireName: r'file_id')
  FileId1? get fileId;

  @BuiltValueField(wireName: r'year')
  Year? get year;

  @BuiltValueField(wireName: r'origin')
  ResourceUpdateOrigin? get origin;

  ResourceUpdate._();

  factory ResourceUpdate([void updates(ResourceUpdateBuilder b)]) = _$ResourceUpdate;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(ResourceUpdateBuilder b) => b;

  @BuiltValueSerializer(custom: true)
  static Serializer<ResourceUpdate> get serializer => _$ResourceUpdateSerializer();
}

class _$ResourceUpdateSerializer implements PrimitiveSerializer<ResourceUpdate> {
  @override
  final Iterable<Type> types = const [ResourceUpdate, _$ResourceUpdate];

  @override
  final String wireName = r'ResourceUpdate';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    ResourceUpdate object, {
    FullType specifiedType = FullType.unspecified,
  }) sync* {
    if (object.chapterId != null) {
      yield r'chapter_id';
      yield serializers.serialize(
        object.chapterId,
        specifiedType: const FullType(ChapterId),
      );
    }
    if (object.type != null) {
      yield r'type';
      yield serializers.serialize(
        object.type,
        specifiedType: const FullType(ResourceUpdateType),
      );
    }
    if (object.title != null) {
      yield r'title';
      yield serializers.serialize(
        object.title,
        specifiedType: const FullType(Title),
      );
    }
    if (object.contentText != null) {
      yield r'content_text';
      yield serializers.serialize(
        object.contentText,
        specifiedType: const FullType(ContentText1),
      );
    }
    if (object.fileId != null) {
      yield r'file_id';
      yield serializers.serialize(
        object.fileId,
        specifiedType: const FullType(FileId1),
      );
    }
    if (object.year != null) {
      yield r'year';
      yield serializers.serialize(
        object.year,
        specifiedType: const FullType(Year),
      );
    }
    if (object.origin != null) {
      yield r'origin';
      yield serializers.serialize(
        object.origin,
        specifiedType: const FullType(ResourceUpdateOrigin),
      );
    }
  }

  @override
  Object serialize(
    Serializers serializers,
    ResourceUpdate object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    return _serializeProperties(serializers, object, specifiedType: specifiedType).toList();
  }

  void _deserializeProperties(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
    required List<Object?> serializedList,
    required ResourceUpdateBuilder result,
    required List<Object?> unhandled,
  }) {
    for (var i = 0; i < serializedList.length; i += 2) {
      final key = serializedList[i] as String;
      final value = serializedList[i + 1];
      switch (key) {
        case r'chapter_id':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(ChapterId),
          ) as ChapterId;
          result.chapterId.replace(valueDes);
          break;
        case r'type':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(ResourceUpdateType),
          ) as ResourceUpdateType;
          result.type.replace(valueDes);
          break;
        case r'title':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(Title),
          ) as Title;
          result.title.replace(valueDes);
          break;
        case r'content_text':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(ContentText1),
          ) as ContentText1;
          result.contentText.replace(valueDes);
          break;
        case r'file_id':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(FileId1),
          ) as FileId1;
          result.fileId.replace(valueDes);
          break;
        case r'year':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(Year),
          ) as Year;
          result.year.replace(valueDes);
          break;
        case r'origin':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(ResourceUpdateOrigin),
          ) as ResourceUpdateOrigin;
          result.origin.replace(valueDes);
          break;
        default:
          unhandled.add(key);
          unhandled.add(value);
          break;
      }
    }
  }

  @override
  ResourceUpdate deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = ResourceUpdateBuilder();
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


//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:coindetude_api/src/model/file_id.dart';
import 'package:coindetude_api/src/model/year.dart';
import 'package:built_collection/built_collection.dart';
import 'package:coindetude_api/src/model/content_text.dart';
import 'package:coindetude_api/src/model/chapter_id.dart';
import 'package:coindetude_api/src/model/resource_origin.dart';
import 'package:built_value/json_object.dart';
import 'package:coindetude_api/src/model/resource_type.dart';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';

part 'resource_create.g.dart';

/// ResourceCreate
///
/// Properties:
/// * [type] 
/// * [title] 
/// * [chapterId] 
/// * [contentText] 
/// * [fileId] 
/// * [year] 
/// * [origin] 
@BuiltValue()
abstract class ResourceCreate implements Built<ResourceCreate, ResourceCreateBuilder> {
  @BuiltValueField(wireName: r'type')
  ResourceType get type;
  // enum typeEnum {  cours,  exercice,  annale,  corrige,  };

  @BuiltValueField(wireName: r'title')
  String get title;

  @BuiltValueField(wireName: r'chapter_id')
  ChapterId? get chapterId;

  @BuiltValueField(wireName: r'content_text')
  ContentText? get contentText;

  @BuiltValueField(wireName: r'file_id')
  FileId? get fileId;

  @BuiltValueField(wireName: r'year')
  Year? get year;

  @BuiltValueField(wireName: r'origin')
  ResourceOrigin? get origin;
  // enum originEnum {  admin,  teacher,  ia,  };

  ResourceCreate._();

  factory ResourceCreate([void updates(ResourceCreateBuilder b)]) = _$ResourceCreate;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(ResourceCreateBuilder b) => b
      ..origin = const ._(ResourceOrigin.admin);

  @BuiltValueSerializer(custom: true)
  static Serializer<ResourceCreate> get serializer => _$ResourceCreateSerializer();
}

class _$ResourceCreateSerializer implements PrimitiveSerializer<ResourceCreate> {
  @override
  final Iterable<Type> types = const [ResourceCreate, _$ResourceCreate];

  @override
  final String wireName = r'ResourceCreate';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    ResourceCreate object, {
    FullType specifiedType = FullType.unspecified,
  }) sync* {
    yield r'type';
    yield serializers.serialize(
      object.type,
      specifiedType: const FullType(ResourceType),
    );
    yield r'title';
    yield serializers.serialize(
      object.title,
      specifiedType: const FullType(String),
    );
    if (object.chapterId != null) {
      yield r'chapter_id';
      yield serializers.serialize(
        object.chapterId,
        specifiedType: const FullType(ChapterId),
      );
    }
    if (object.contentText != null) {
      yield r'content_text';
      yield serializers.serialize(
        object.contentText,
        specifiedType: const FullType(ContentText),
      );
    }
    if (object.fileId != null) {
      yield r'file_id';
      yield serializers.serialize(
        object.fileId,
        specifiedType: const FullType(FileId),
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
        specifiedType: const FullType(ResourceOrigin),
      );
    }
  }

  @override
  Object serialize(
    Serializers serializers,
    ResourceCreate object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    return _serializeProperties(serializers, object, specifiedType: specifiedType).toList();
  }

  void _deserializeProperties(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
    required List<Object?> serializedList,
    required ResourceCreateBuilder result,
    required List<Object?> unhandled,
  }) {
    for (var i = 0; i < serializedList.length; i += 2) {
      final key = serializedList[i] as String;
      final value = serializedList[i + 1];
      switch (key) {
        case r'type':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(ResourceType),
          ) as ResourceType;
          result.type = valueDes;
          break;
        case r'title':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(String),
          ) as String;
          result.title = valueDes;
          break;
        case r'chapter_id':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(ChapterId),
          ) as ChapterId;
          result.chapterId.replace(valueDes);
          break;
        case r'content_text':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(ContentText),
          ) as ContentText;
          result.contentText.replace(valueDes);
          break;
        case r'file_id':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(FileId),
          ) as FileId;
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
            specifiedType: const FullType(ResourceOrigin),
          ) as ResourceOrigin;
          result.origin = valueDes;
          break;
        default:
          unhandled.add(key);
          unhandled.add(value);
          break;
      }
    }
  }

  @override
  ResourceCreate deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = ResourceCreateBuilder();
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


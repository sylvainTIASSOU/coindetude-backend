//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:coindetude_api/src/model/resource_origin.dart';
import 'package:coindetude_api/src/model/resource_type.dart';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';

part 'resource_read_detail.g.dart';

/// Vue détaillée avec ``content_text`` + URL S3 presign si file.
///
/// Properties:
/// * [id] 
/// * [chapterId] 
/// * [type] 
/// * [title] 
/// * [fileId] 
/// * [year] 
/// * [origin] 
/// * [contentText] 
/// * [fileUrl] 
@BuiltValue()
abstract class ResourceReadDetail implements Built<ResourceReadDetail, ResourceReadDetailBuilder> {
  @BuiltValueField(wireName: r'id')
  String get id;

  @BuiltValueField(wireName: r'chapter_id')
  String? get chapterId;

  @BuiltValueField(wireName: r'type')
  ResourceType get type;
  // enum typeEnum {  cours,  exercice,  annale,  corrige,  };

  @BuiltValueField(wireName: r'title')
  String get title;

  @BuiltValueField(wireName: r'file_id')
  String? get fileId;

  @BuiltValueField(wireName: r'year')
  int? get year;

  @BuiltValueField(wireName: r'origin')
  ResourceOrigin get origin;
  // enum originEnum {  admin,  teacher,  ia,  };

  @BuiltValueField(wireName: r'content_text')
  String? get contentText;

  @BuiltValueField(wireName: r'file_url')
  String? get fileUrl;

  ResourceReadDetail._();

  factory ResourceReadDetail([void updates(ResourceReadDetailBuilder b)]) = _$ResourceReadDetail;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(ResourceReadDetailBuilder b) => b;

  @BuiltValueSerializer(custom: true)
  static Serializer<ResourceReadDetail> get serializer => _$ResourceReadDetailSerializer();
}

class _$ResourceReadDetailSerializer implements PrimitiveSerializer<ResourceReadDetail> {
  @override
  final Iterable<Type> types = const [ResourceReadDetail, _$ResourceReadDetail];

  @override
  final String wireName = r'ResourceReadDetail';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    ResourceReadDetail object, {
    FullType specifiedType = FullType.unspecified,
  }) sync* {
    yield r'id';
    yield serializers.serialize(
      object.id,
      specifiedType: const FullType(String),
    );
    yield r'chapter_id';
    yield object.chapterId == null ? null : serializers.serialize(
      object.chapterId,
      specifiedType: const FullType.nullable(String),
    );
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
    yield r'file_id';
    yield object.fileId == null ? null : serializers.serialize(
      object.fileId,
      specifiedType: const FullType.nullable(String),
    );
    yield r'year';
    yield object.year == null ? null : serializers.serialize(
      object.year,
      specifiedType: const FullType.nullable(int),
    );
    yield r'origin';
    yield serializers.serialize(
      object.origin,
      specifiedType: const FullType(ResourceOrigin),
    );
    if (object.contentText != null) {
      yield r'content_text';
      yield serializers.serialize(
        object.contentText,
        specifiedType: const FullType.nullable(String),
      );
    }
    if (object.fileUrl != null) {
      yield r'file_url';
      yield serializers.serialize(
        object.fileUrl,
        specifiedType: const FullType.nullable(String),
      );
    }
  }

  @override
  Object serialize(
    Serializers serializers,
    ResourceReadDetail object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    return _serializeProperties(serializers, object, specifiedType: specifiedType).toList();
  }

  void _deserializeProperties(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
    required List<Object?> serializedList,
    required ResourceReadDetailBuilder result,
    required List<Object?> unhandled,
  }) {
    for (var i = 0; i < serializedList.length; i += 2) {
      final key = serializedList[i] as String;
      final value = serializedList[i + 1];
      switch (key) {
        case r'id':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(String),
          ) as String;
          result.id = valueDes;
          break;
        case r'chapter_id':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType.nullable(String),
          ) as String?;
          if (valueDes == null) continue;
          result.chapterId = valueDes;
          break;
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
        case r'file_id':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType.nullable(String),
          ) as String?;
          if (valueDes == null) continue;
          result.fileId = valueDes;
          break;
        case r'year':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType.nullable(int),
          ) as int?;
          if (valueDes == null) continue;
          result.year = valueDes;
          break;
        case r'origin':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(ResourceOrigin),
          ) as ResourceOrigin;
          result.origin = valueDes;
          break;
        case r'content_text':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType.nullable(String),
          ) as String?;
          if (valueDes == null) continue;
          result.contentText = valueDes;
          break;
        case r'file_url':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType.nullable(String),
          ) as String?;
          if (valueDes == null) continue;
          result.fileUrl = valueDes;
          break;
        default:
          unhandled.add(key);
          unhandled.add(value);
          break;
      }
    }
  }

  @override
  ResourceReadDetail deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = ResourceReadDetailBuilder();
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


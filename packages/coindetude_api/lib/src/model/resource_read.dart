//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:coindetude_api/src/model/resource_origin.dart';
import 'package:coindetude_api/src/model/resource_type.dart';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';

part 'resource_read.g.dart';

/// Vue allégée (pas de ``content_text``) pour les listes.
///
/// Properties:
/// * [id] 
/// * [chapterId] 
/// * [type] 
/// * [title] 
/// * [fileId] 
/// * [year] 
/// * [origin] 
@BuiltValue()
abstract class ResourceRead implements Built<ResourceRead, ResourceReadBuilder> {
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

  ResourceRead._();

  factory ResourceRead([void updates(ResourceReadBuilder b)]) = _$ResourceRead;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(ResourceReadBuilder b) => b;

  @BuiltValueSerializer(custom: true)
  static Serializer<ResourceRead> get serializer => _$ResourceReadSerializer();
}

class _$ResourceReadSerializer implements PrimitiveSerializer<ResourceRead> {
  @override
  final Iterable<Type> types = const [ResourceRead, _$ResourceRead];

  @override
  final String wireName = r'ResourceRead';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    ResourceRead object, {
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
  }

  @override
  Object serialize(
    Serializers serializers,
    ResourceRead object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    return _serializeProperties(serializers, object, specifiedType: specifiedType).toList();
  }

  void _deserializeProperties(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
    required List<Object?> serializedList,
    required ResourceReadBuilder result,
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
        default:
          unhandled.add(key);
          unhandled.add(value);
          break;
      }
    }
  }

  @override
  ResourceRead deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = ResourceReadBuilder();
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


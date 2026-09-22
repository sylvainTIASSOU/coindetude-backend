//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:built_collection/built_collection.dart';
import 'package:coindetude_api/src/model/chapter_read.dart';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';

part 'page_response_chapter_read.g.dart';

/// PageResponseChapterRead
///
/// Properties:
/// * [items] 
/// * [total] - Nombre total d'éléments (toutes pages)
/// * [limit] 
/// * [offset] 
/// * [hasMore] - True s'il reste des éléments après cette page
@BuiltValue()
abstract class PageResponseChapterRead implements Built<PageResponseChapterRead, PageResponseChapterReadBuilder> {
  @BuiltValueField(wireName: r'items')
  BuiltList<ChapterRead> get items;

  /// Nombre total d'éléments (toutes pages)
  @BuiltValueField(wireName: r'total')
  int get total;

  @BuiltValueField(wireName: r'limit')
  int get limit;

  @BuiltValueField(wireName: r'offset')
  int get offset;

  /// True s'il reste des éléments après cette page
  @BuiltValueField(wireName: r'has_more')
  bool get hasMore;

  PageResponseChapterRead._();

  factory PageResponseChapterRead([void updates(PageResponseChapterReadBuilder b)]) = _$PageResponseChapterRead;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(PageResponseChapterReadBuilder b) => b;

  @BuiltValueSerializer(custom: true)
  static Serializer<PageResponseChapterRead> get serializer => _$PageResponseChapterReadSerializer();
}

class _$PageResponseChapterReadSerializer implements PrimitiveSerializer<PageResponseChapterRead> {
  @override
  final Iterable<Type> types = const [PageResponseChapterRead, _$PageResponseChapterRead];

  @override
  final String wireName = r'PageResponseChapterRead';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    PageResponseChapterRead object, {
    FullType specifiedType = FullType.unspecified,
  }) sync* {
    yield r'items';
    yield serializers.serialize(
      object.items,
      specifiedType: const FullType(BuiltList, [FullType(ChapterRead)]),
    );
    yield r'total';
    yield serializers.serialize(
      object.total,
      specifiedType: const FullType(int),
    );
    yield r'limit';
    yield serializers.serialize(
      object.limit,
      specifiedType: const FullType(int),
    );
    yield r'offset';
    yield serializers.serialize(
      object.offset,
      specifiedType: const FullType(int),
    );
    yield r'has_more';
    yield serializers.serialize(
      object.hasMore,
      specifiedType: const FullType(bool),
    );
  }

  @override
  Object serialize(
    Serializers serializers,
    PageResponseChapterRead object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    return _serializeProperties(serializers, object, specifiedType: specifiedType).toList();
  }

  void _deserializeProperties(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
    required List<Object?> serializedList,
    required PageResponseChapterReadBuilder result,
    required List<Object?> unhandled,
  }) {
    for (var i = 0; i < serializedList.length; i += 2) {
      final key = serializedList[i] as String;
      final value = serializedList[i + 1];
      switch (key) {
        case r'items':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(BuiltList, [FullType(ChapterRead)]),
          ) as BuiltList<ChapterRead>;
          result.items.replace(valueDes);
          break;
        case r'total':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(int),
          ) as int;
          result.total = valueDes;
          break;
        case r'limit':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(int),
          ) as int;
          result.limit = valueDes;
          break;
        case r'offset':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(int),
          ) as int;
          result.offset = valueDes;
          break;
        case r'has_more':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(bool),
          ) as bool;
          result.hasMore = valueDes;
          break;
        default:
          unhandled.add(key);
          unhandled.add(value);
          break;
      }
    }
  }

  @override
  PageResponseChapterRead deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = PageResponseChapterReadBuilder();
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


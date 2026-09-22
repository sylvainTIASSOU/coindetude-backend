//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:coindetude_api/src/model/level_read.dart';
import 'package:built_collection/built_collection.dart';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';

part 'page_response_level_read.g.dart';

/// PageResponseLevelRead
///
/// Properties:
/// * [items] 
/// * [total] - Nombre total d'éléments (toutes pages)
/// * [limit] 
/// * [offset] 
/// * [hasMore] - True s'il reste des éléments après cette page
@BuiltValue()
abstract class PageResponseLevelRead implements Built<PageResponseLevelRead, PageResponseLevelReadBuilder> {
  @BuiltValueField(wireName: r'items')
  BuiltList<LevelRead> get items;

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

  PageResponseLevelRead._();

  factory PageResponseLevelRead([void updates(PageResponseLevelReadBuilder b)]) = _$PageResponseLevelRead;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(PageResponseLevelReadBuilder b) => b;

  @BuiltValueSerializer(custom: true)
  static Serializer<PageResponseLevelRead> get serializer => _$PageResponseLevelReadSerializer();
}

class _$PageResponseLevelReadSerializer implements PrimitiveSerializer<PageResponseLevelRead> {
  @override
  final Iterable<Type> types = const [PageResponseLevelRead, _$PageResponseLevelRead];

  @override
  final String wireName = r'PageResponseLevelRead';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    PageResponseLevelRead object, {
    FullType specifiedType = FullType.unspecified,
  }) sync* {
    yield r'items';
    yield serializers.serialize(
      object.items,
      specifiedType: const FullType(BuiltList, [FullType(LevelRead)]),
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
    PageResponseLevelRead object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    return _serializeProperties(serializers, object, specifiedType: specifiedType).toList();
  }

  void _deserializeProperties(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
    required List<Object?> serializedList,
    required PageResponseLevelReadBuilder result,
    required List<Object?> unhandled,
  }) {
    for (var i = 0; i < serializedList.length; i += 2) {
      final key = serializedList[i] as String;
      final value = serializedList[i + 1];
      switch (key) {
        case r'items':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(BuiltList, [FullType(LevelRead)]),
          ) as BuiltList<LevelRead>;
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
  PageResponseLevelRead deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = PageResponseLevelReadBuilder();
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


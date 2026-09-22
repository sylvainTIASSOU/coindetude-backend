//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:coindetude_api/src/model/series_read.dart';
import 'package:built_collection/built_collection.dart';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';

part 'page_response_series_read.g.dart';

/// PageResponseSeriesRead
///
/// Properties:
/// * [items] 
/// * [total] - Nombre total d'éléments (toutes pages)
/// * [limit] 
/// * [offset] 
/// * [hasMore] - True s'il reste des éléments après cette page
@BuiltValue()
abstract class PageResponseSeriesRead implements Built<PageResponseSeriesRead, PageResponseSeriesReadBuilder> {
  @BuiltValueField(wireName: r'items')
  BuiltList<SeriesRead> get items;

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

  PageResponseSeriesRead._();

  factory PageResponseSeriesRead([void updates(PageResponseSeriesReadBuilder b)]) = _$PageResponseSeriesRead;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(PageResponseSeriesReadBuilder b) => b;

  @BuiltValueSerializer(custom: true)
  static Serializer<PageResponseSeriesRead> get serializer => _$PageResponseSeriesReadSerializer();
}

class _$PageResponseSeriesReadSerializer implements PrimitiveSerializer<PageResponseSeriesRead> {
  @override
  final Iterable<Type> types = const [PageResponseSeriesRead, _$PageResponseSeriesRead];

  @override
  final String wireName = r'PageResponseSeriesRead';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    PageResponseSeriesRead object, {
    FullType specifiedType = FullType.unspecified,
  }) sync* {
    yield r'items';
    yield serializers.serialize(
      object.items,
      specifiedType: const FullType(BuiltList, [FullType(SeriesRead)]),
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
    PageResponseSeriesRead object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    return _serializeProperties(serializers, object, specifiedType: specifiedType).toList();
  }

  void _deserializeProperties(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
    required List<Object?> serializedList,
    required PageResponseSeriesReadBuilder result,
    required List<Object?> unhandled,
  }) {
    for (var i = 0; i < serializedList.length; i += 2) {
      final key = serializedList[i] as String;
      final value = serializedList[i + 1];
      switch (key) {
        case r'items':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(BuiltList, [FullType(SeriesRead)]),
          ) as BuiltList<SeriesRead>;
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
  PageResponseSeriesRead deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = PageResponseSeriesReadBuilder();
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


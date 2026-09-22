//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:built_collection/built_collection.dart';
import 'package:coindetude_api/src/model/resource_read.dart';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';

part 'page_response_resource_read.g.dart';

/// PageResponseResourceRead
///
/// Properties:
/// * [items] 
/// * [total] - Nombre total d'éléments (toutes pages)
/// * [limit] 
/// * [offset] 
/// * [hasMore] - True s'il reste des éléments après cette page
@BuiltValue()
abstract class PageResponseResourceRead implements Built<PageResponseResourceRead, PageResponseResourceReadBuilder> {
  @BuiltValueField(wireName: r'items')
  BuiltList<ResourceRead> get items;

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

  PageResponseResourceRead._();

  factory PageResponseResourceRead([void updates(PageResponseResourceReadBuilder b)]) = _$PageResponseResourceRead;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(PageResponseResourceReadBuilder b) => b;

  @BuiltValueSerializer(custom: true)
  static Serializer<PageResponseResourceRead> get serializer => _$PageResponseResourceReadSerializer();
}

class _$PageResponseResourceReadSerializer implements PrimitiveSerializer<PageResponseResourceRead> {
  @override
  final Iterable<Type> types = const [PageResponseResourceRead, _$PageResponseResourceRead];

  @override
  final String wireName = r'PageResponseResourceRead';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    PageResponseResourceRead object, {
    FullType specifiedType = FullType.unspecified,
  }) sync* {
    yield r'items';
    yield serializers.serialize(
      object.items,
      specifiedType: const FullType(BuiltList, [FullType(ResourceRead)]),
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
    PageResponseResourceRead object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    return _serializeProperties(serializers, object, specifiedType: specifiedType).toList();
  }

  void _deserializeProperties(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
    required List<Object?> serializedList,
    required PageResponseResourceReadBuilder result,
    required List<Object?> unhandled,
  }) {
    for (var i = 0; i < serializedList.length; i += 2) {
      final key = serializedList[i] as String;
      final value = serializedList[i + 1];
      switch (key) {
        case r'items':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(BuiltList, [FullType(ResourceRead)]),
          ) as BuiltList<ResourceRead>;
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
  PageResponseResourceRead deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = PageResponseResourceReadBuilder();
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


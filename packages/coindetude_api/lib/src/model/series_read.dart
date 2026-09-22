//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:coindetude_api/src/model/cycle.dart';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';

part 'series_read.g.dart';

/// SeriesRead
///
/// Properties:
/// * [id] 
/// * [code] 
/// * [name] 
/// * [cycle] 
/// * [description] 
@BuiltValue()
abstract class SeriesRead implements Built<SeriesRead, SeriesReadBuilder> {
  @BuiltValueField(wireName: r'id')
  String get id;

  @BuiltValueField(wireName: r'code')
  String get code;

  @BuiltValueField(wireName: r'name')
  String get name;

  @BuiltValueField(wireName: r'cycle')
  Cycle get cycle;
  // enum cycleEnum {  college,  lycee_moderne,  lycee_technique,  };

  @BuiltValueField(wireName: r'description')
  String? get description;

  SeriesRead._();

  factory SeriesRead([void updates(SeriesReadBuilder b)]) = _$SeriesRead;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(SeriesReadBuilder b) => b;

  @BuiltValueSerializer(custom: true)
  static Serializer<SeriesRead> get serializer => _$SeriesReadSerializer();
}

class _$SeriesReadSerializer implements PrimitiveSerializer<SeriesRead> {
  @override
  final Iterable<Type> types = const [SeriesRead, _$SeriesRead];

  @override
  final String wireName = r'SeriesRead';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    SeriesRead object, {
    FullType specifiedType = FullType.unspecified,
  }) sync* {
    yield r'id';
    yield serializers.serialize(
      object.id,
      specifiedType: const FullType(String),
    );
    yield r'code';
    yield serializers.serialize(
      object.code,
      specifiedType: const FullType(String),
    );
    yield r'name';
    yield serializers.serialize(
      object.name,
      specifiedType: const FullType(String),
    );
    yield r'cycle';
    yield serializers.serialize(
      object.cycle,
      specifiedType: const FullType(Cycle),
    );
    yield r'description';
    yield object.description == null ? null : serializers.serialize(
      object.description,
      specifiedType: const FullType.nullable(String),
    );
  }

  @override
  Object serialize(
    Serializers serializers,
    SeriesRead object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    return _serializeProperties(serializers, object, specifiedType: specifiedType).toList();
  }

  void _deserializeProperties(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
    required List<Object?> serializedList,
    required SeriesReadBuilder result,
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
        case r'code':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(String),
          ) as String;
          result.code = valueDes;
          break;
        case r'name':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(String),
          ) as String;
          result.name = valueDes;
          break;
        case r'cycle':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(Cycle),
          ) as Cycle;
          result.cycle = valueDes;
          break;
        case r'description':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType.nullable(String),
          ) as String?;
          if (valueDes == null) continue;
          result.description = valueDes;
          break;
        default:
          unhandled.add(key);
          unhandled.add(value);
          break;
      }
    }
  }

  @override
  SeriesRead deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = SeriesReadBuilder();
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


//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:coindetude_api/src/model/cycle.dart';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';

part 'subject_read.g.dart';

/// SubjectRead
///
/// Properties:
/// * [id] 
/// * [name] 
/// * [iconUrl] 
/// * [cycle] 
@BuiltValue()
abstract class SubjectRead implements Built<SubjectRead, SubjectReadBuilder> {
  @BuiltValueField(wireName: r'id')
  String get id;

  @BuiltValueField(wireName: r'name')
  String get name;

  @BuiltValueField(wireName: r'icon_url')
  String? get iconUrl;

  @BuiltValueField(wireName: r'cycle')
  Cycle? get cycle;
  // enum cycleEnum {  college,  lycee_moderne,  lycee_technique,  };

  SubjectRead._();

  factory SubjectRead([void updates(SubjectReadBuilder b)]) = _$SubjectRead;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(SubjectReadBuilder b) => b;

  @BuiltValueSerializer(custom: true)
  static Serializer<SubjectRead> get serializer => _$SubjectReadSerializer();
}

class _$SubjectReadSerializer implements PrimitiveSerializer<SubjectRead> {
  @override
  final Iterable<Type> types = const [SubjectRead, _$SubjectRead];

  @override
  final String wireName = r'SubjectRead';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    SubjectRead object, {
    FullType specifiedType = FullType.unspecified,
  }) sync* {
    yield r'id';
    yield serializers.serialize(
      object.id,
      specifiedType: const FullType(String),
    );
    yield r'name';
    yield serializers.serialize(
      object.name,
      specifiedType: const FullType(String),
    );
    yield r'icon_url';
    yield object.iconUrl == null ? null : serializers.serialize(
      object.iconUrl,
      specifiedType: const FullType.nullable(String),
    );
    yield r'cycle';
    yield object.cycle == null ? null : serializers.serialize(
      object.cycle,
      specifiedType: const FullType.nullable(Cycle),
    );
  }

  @override
  Object serialize(
    Serializers serializers,
    SubjectRead object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    return _serializeProperties(serializers, object, specifiedType: specifiedType).toList();
  }

  void _deserializeProperties(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
    required List<Object?> serializedList,
    required SubjectReadBuilder result,
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
        case r'name':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(String),
          ) as String;
          result.name = valueDes;
          break;
        case r'icon_url':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType.nullable(String),
          ) as String?;
          if (valueDes == null) continue;
          result.iconUrl = valueDes;
          break;
        case r'cycle':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType.nullable(Cycle),
          ) as Cycle?;
          if (valueDes == null) continue;
          result.cycle = valueDes;
          break;
        default:
          unhandled.add(key);
          unhandled.add(value);
          break;
      }
    }
  }

  @override
  SubjectRead deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = SubjectReadBuilder();
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


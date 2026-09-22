//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:coindetude_api/src/model/file_status.dart';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';

part 'confirm_response.g.dart';

/// ConfirmResponse
///
/// Properties:
/// * [fileId] 
/// * [status] 
/// * [sizeKb] 
/// * [mimeType] 
/// * [url] 
/// * [uploadedAt] 
@BuiltValue()
abstract class ConfirmResponse implements Built<ConfirmResponse, ConfirmResponseBuilder> {
  @BuiltValueField(wireName: r'file_id')
  String get fileId;

  @BuiltValueField(wireName: r'status')
  FileStatus get status;
  // enum statusEnum {  pending,  uploaded,  failed,  };

  @BuiltValueField(wireName: r'size_kb')
  int get sizeKb;

  @BuiltValueField(wireName: r'mime_type')
  String get mimeType;

  @BuiltValueField(wireName: r'url')
  String get url;

  @BuiltValueField(wireName: r'uploaded_at')
  DateTime get uploadedAt;

  ConfirmResponse._();

  factory ConfirmResponse([void updates(ConfirmResponseBuilder b)]) = _$ConfirmResponse;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(ConfirmResponseBuilder b) => b;

  @BuiltValueSerializer(custom: true)
  static Serializer<ConfirmResponse> get serializer => _$ConfirmResponseSerializer();
}

class _$ConfirmResponseSerializer implements PrimitiveSerializer<ConfirmResponse> {
  @override
  final Iterable<Type> types = const [ConfirmResponse, _$ConfirmResponse];

  @override
  final String wireName = r'ConfirmResponse';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    ConfirmResponse object, {
    FullType specifiedType = FullType.unspecified,
  }) sync* {
    yield r'file_id';
    yield serializers.serialize(
      object.fileId,
      specifiedType: const FullType(String),
    );
    yield r'status';
    yield serializers.serialize(
      object.status,
      specifiedType: const FullType(FileStatus),
    );
    yield r'size_kb';
    yield serializers.serialize(
      object.sizeKb,
      specifiedType: const FullType(int),
    );
    yield r'mime_type';
    yield serializers.serialize(
      object.mimeType,
      specifiedType: const FullType(String),
    );
    yield r'url';
    yield serializers.serialize(
      object.url,
      specifiedType: const FullType(String),
    );
    yield r'uploaded_at';
    yield serializers.serialize(
      object.uploadedAt,
      specifiedType: const FullType(DateTime),
    );
  }

  @override
  Object serialize(
    Serializers serializers,
    ConfirmResponse object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    return _serializeProperties(serializers, object, specifiedType: specifiedType).toList();
  }

  void _deserializeProperties(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
    required List<Object?> serializedList,
    required ConfirmResponseBuilder result,
    required List<Object?> unhandled,
  }) {
    for (var i = 0; i < serializedList.length; i += 2) {
      final key = serializedList[i] as String;
      final value = serializedList[i + 1];
      switch (key) {
        case r'file_id':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(String),
          ) as String;
          result.fileId = valueDes;
          break;
        case r'status':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(FileStatus),
          ) as FileStatus;
          result.status = valueDes;
          break;
        case r'size_kb':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(int),
          ) as int;
          result.sizeKb = valueDes;
          break;
        case r'mime_type':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(String),
          ) as String;
          result.mimeType = valueDes;
          break;
        case r'url':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(String),
          ) as String;
          result.url = valueDes;
          break;
        case r'uploaded_at':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(DateTime),
          ) as DateTime;
          result.uploadedAt = valueDes;
          break;
        default:
          unhandled.add(key);
          unhandled.add(value);
          break;
      }
    }
  }

  @override
  ConfirmResponse deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = ConfirmResponseBuilder();
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


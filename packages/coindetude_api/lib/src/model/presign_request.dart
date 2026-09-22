//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:coindetude_api/src/model/upload_purpose.dart';
import 'package:built_collection/built_collection.dart';
import 'package:coindetude_api/src/model/file_name.dart';
import 'package:built_value/json_object.dart';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';

part 'presign_request.g.dart';

/// Corps de POST /uploads/presign.
///
/// Properties:
/// * [fileType] - MIME type (whitelist : image/webp, image/jpeg, application/pdf)
/// * [sizeKb] 
/// * [purpose] 
/// * [fileName] 
@BuiltValue()
abstract class PresignRequest implements Built<PresignRequest, PresignRequestBuilder> {
  /// MIME type (whitelist : image/webp, image/jpeg, application/pdf)
  @BuiltValueField(wireName: r'file_type')
  String get fileType;

  @BuiltValueField(wireName: r'size_kb')
  int get sizeKb;

  @BuiltValueField(wireName: r'purpose')
  UploadPurpose get purpose;
  // enum purposeEnum {  avatar,  homework_scan,  resource_pdf,  };

  @BuiltValueField(wireName: r'file_name')
  FileName? get fileName;

  PresignRequest._();

  factory PresignRequest([void updates(PresignRequestBuilder b)]) = _$PresignRequest;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(PresignRequestBuilder b) => b;

  @BuiltValueSerializer(custom: true)
  static Serializer<PresignRequest> get serializer => _$PresignRequestSerializer();
}

class _$PresignRequestSerializer implements PrimitiveSerializer<PresignRequest> {
  @override
  final Iterable<Type> types = const [PresignRequest, _$PresignRequest];

  @override
  final String wireName = r'PresignRequest';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    PresignRequest object, {
    FullType specifiedType = FullType.unspecified,
  }) sync* {
    yield r'file_type';
    yield serializers.serialize(
      object.fileType,
      specifiedType: const FullType(String),
    );
    yield r'size_kb';
    yield serializers.serialize(
      object.sizeKb,
      specifiedType: const FullType(int),
    );
    yield r'purpose';
    yield serializers.serialize(
      object.purpose,
      specifiedType: const FullType(UploadPurpose),
    );
    if (object.fileName != null) {
      yield r'file_name';
      yield serializers.serialize(
        object.fileName,
        specifiedType: const FullType(FileName),
      );
    }
  }

  @override
  Object serialize(
    Serializers serializers,
    PresignRequest object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    return _serializeProperties(serializers, object, specifiedType: specifiedType).toList();
  }

  void _deserializeProperties(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
    required List<Object?> serializedList,
    required PresignRequestBuilder result,
    required List<Object?> unhandled,
  }) {
    for (var i = 0; i < serializedList.length; i += 2) {
      final key = serializedList[i] as String;
      final value = serializedList[i + 1];
      switch (key) {
        case r'file_type':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(String),
          ) as String;
          result.fileType = valueDes;
          break;
        case r'size_kb':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(int),
          ) as int;
          result.sizeKb = valueDes;
          break;
        case r'purpose':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(UploadPurpose),
          ) as UploadPurpose;
          result.purpose = valueDes;
          break;
        case r'file_name':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(FileName),
          ) as FileName;
          result.fileName.replace(valueDes);
          break;
        default:
          unhandled.add(key);
          unhandled.add(value);
          break;
      }
    }
  }

  @override
  PresignRequest deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = PresignRequestBuilder();
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


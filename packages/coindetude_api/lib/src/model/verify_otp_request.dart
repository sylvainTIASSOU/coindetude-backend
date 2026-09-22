//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';

part 'verify_otp_request.g.dart';

/// VerifyOTPRequest
///
/// Properties:
/// * [challengeId] 
/// * [code] 
/// * [rememberDevice] 
@BuiltValue()
abstract class VerifyOTPRequest implements Built<VerifyOTPRequest, VerifyOTPRequestBuilder> {
  @BuiltValueField(wireName: r'challenge_id')
  String get challengeId;

  @BuiltValueField(wireName: r'code')
  String get code;

  @BuiltValueField(wireName: r'remember_device')
  bool? get rememberDevice;

  VerifyOTPRequest._();

  factory VerifyOTPRequest([void updates(VerifyOTPRequestBuilder b)]) = _$VerifyOTPRequest;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(VerifyOTPRequestBuilder b) => b
      ..rememberDevice = false;

  @BuiltValueSerializer(custom: true)
  static Serializer<VerifyOTPRequest> get serializer => _$VerifyOTPRequestSerializer();
}

class _$VerifyOTPRequestSerializer implements PrimitiveSerializer<VerifyOTPRequest> {
  @override
  final Iterable<Type> types = const [VerifyOTPRequest, _$VerifyOTPRequest];

  @override
  final String wireName = r'VerifyOTPRequest';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    VerifyOTPRequest object, {
    FullType specifiedType = FullType.unspecified,
  }) sync* {
    yield r'challenge_id';
    yield serializers.serialize(
      object.challengeId,
      specifiedType: const FullType(String),
    );
    yield r'code';
    yield serializers.serialize(
      object.code,
      specifiedType: const FullType(String),
    );
    if (object.rememberDevice != null) {
      yield r'remember_device';
      yield serializers.serialize(
        object.rememberDevice,
        specifiedType: const FullType(bool),
      );
    }
  }

  @override
  Object serialize(
    Serializers serializers,
    VerifyOTPRequest object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    return _serializeProperties(serializers, object, specifiedType: specifiedType).toList();
  }

  void _deserializeProperties(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
    required List<Object?> serializedList,
    required VerifyOTPRequestBuilder result,
    required List<Object?> unhandled,
  }) {
    for (var i = 0; i < serializedList.length; i += 2) {
      final key = serializedList[i] as String;
      final value = serializedList[i + 1];
      switch (key) {
        case r'challenge_id':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(String),
          ) as String;
          result.challengeId = valueDes;
          break;
        case r'code':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(String),
          ) as String;
          result.code = valueDes;
          break;
        case r'remember_device':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(bool),
          ) as bool;
          result.rememberDevice = valueDes;
          break;
        default:
          unhandled.add(key);
          unhandled.add(value);
          break;
      }
    }
  }

  @override
  VerifyOTPRequest deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = VerifyOTPRequestBuilder();
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


//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';

part 'resend_otp_request.g.dart';

/// ResendOTPRequest
///
/// Properties:
/// * [challengeId] 
@BuiltValue()
abstract class ResendOTPRequest implements Built<ResendOTPRequest, ResendOTPRequestBuilder> {
  @BuiltValueField(wireName: r'challenge_id')
  String get challengeId;

  ResendOTPRequest._();

  factory ResendOTPRequest([void updates(ResendOTPRequestBuilder b)]) = _$ResendOTPRequest;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(ResendOTPRequestBuilder b) => b;

  @BuiltValueSerializer(custom: true)
  static Serializer<ResendOTPRequest> get serializer => _$ResendOTPRequestSerializer();
}

class _$ResendOTPRequestSerializer implements PrimitiveSerializer<ResendOTPRequest> {
  @override
  final Iterable<Type> types = const [ResendOTPRequest, _$ResendOTPRequest];

  @override
  final String wireName = r'ResendOTPRequest';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    ResendOTPRequest object, {
    FullType specifiedType = FullType.unspecified,
  }) sync* {
    yield r'challenge_id';
    yield serializers.serialize(
      object.challengeId,
      specifiedType: const FullType(String),
    );
  }

  @override
  Object serialize(
    Serializers serializers,
    ResendOTPRequest object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    return _serializeProperties(serializers, object, specifiedType: specifiedType).toList();
  }

  void _deserializeProperties(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
    required List<Object?> serializedList,
    required ResendOTPRequestBuilder result,
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
        default:
          unhandled.add(key);
          unhandled.add(value);
          break;
      }
    }
  }

  @override
  ResendOTPRequest deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = ResendOTPRequestBuilder();
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


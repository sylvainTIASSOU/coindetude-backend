//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:coindetude_api/src/model/otp_channel.dart';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';

part 'otp_sent_response.g.dart';

/// Réponse des étapes 1 (register, login, forgot, resend).
///
/// Properties:
/// * [challengeId] 
/// * [expiresIn] 
/// * [channel] 
/// * [maskedPhone] 
/// * [devCode] 
@BuiltValue()
abstract class OTPSentResponse implements Built<OTPSentResponse, OTPSentResponseBuilder> {
  @BuiltValueField(wireName: r'challenge_id')
  String get challengeId;

  @BuiltValueField(wireName: r'expires_in')
  int get expiresIn;

  @BuiltValueField(wireName: r'channel')
  OTPChannel get channel;
  // enum channelEnum {  whatsapp,  sms,  };

  @BuiltValueField(wireName: r'masked_phone')
  String get maskedPhone;

  @BuiltValueField(wireName: r'dev_code')
  String? get devCode;

  OTPSentResponse._();

  factory OTPSentResponse([void updates(OTPSentResponseBuilder b)]) = _$OTPSentResponse;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(OTPSentResponseBuilder b) => b;

  @BuiltValueSerializer(custom: true)
  static Serializer<OTPSentResponse> get serializer => _$OTPSentResponseSerializer();
}

class _$OTPSentResponseSerializer implements PrimitiveSerializer<OTPSentResponse> {
  @override
  final Iterable<Type> types = const [OTPSentResponse, _$OTPSentResponse];

  @override
  final String wireName = r'OTPSentResponse';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    OTPSentResponse object, {
    FullType specifiedType = FullType.unspecified,
  }) sync* {
    yield r'challenge_id';
    yield serializers.serialize(
      object.challengeId,
      specifiedType: const FullType(String),
    );
    yield r'expires_in';
    yield serializers.serialize(
      object.expiresIn,
      specifiedType: const FullType(int),
    );
    yield r'channel';
    yield serializers.serialize(
      object.channel,
      specifiedType: const FullType(OTPChannel),
    );
    yield r'masked_phone';
    yield serializers.serialize(
      object.maskedPhone,
      specifiedType: const FullType(String),
    );
    if (object.devCode != null) {
      yield r'dev_code';
      yield serializers.serialize(
        object.devCode,
        specifiedType: const FullType.nullable(String),
      );
    }
  }

  @override
  Object serialize(
    Serializers serializers,
    OTPSentResponse object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    return _serializeProperties(serializers, object, specifiedType: specifiedType).toList();
  }

  void _deserializeProperties(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
    required List<Object?> serializedList,
    required OTPSentResponseBuilder result,
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
        case r'expires_in':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(int),
          ) as int;
          result.expiresIn = valueDes;
          break;
        case r'channel':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(OTPChannel),
          ) as OTPChannel;
          result.channel = valueDes;
          break;
        case r'masked_phone':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(String),
          ) as String;
          result.maskedPhone = valueDes;
          break;
        case r'dev_code':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType.nullable(String),
          ) as String?;
          if (valueDes == null) continue;
          result.devCode = valueDes;
          break;
        default:
          unhandled.add(key);
          unhandled.add(value);
          break;
      }
    }
  }

  @override
  OTPSentResponse deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = OTPSentResponseBuilder();
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


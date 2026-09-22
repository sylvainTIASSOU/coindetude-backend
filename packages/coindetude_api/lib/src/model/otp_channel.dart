//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:built_collection/built_collection.dart';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';

part 'otp_channel.g.dart';

class OTPChannel extends EnumClass {

  /// Canal de livraison du code OTP.
  @BuiltValueEnumConst(wireName: r'whatsapp')
  static const OTPChannel whatsapp = _$whatsapp;
  /// Canal de livraison du code OTP.
  @BuiltValueEnumConst(wireName: r'sms')
  static const OTPChannel sms = _$sms;

  static Serializer<OTPChannel> get serializer => _$oTPChannelSerializer;

  const OTPChannel._(String name): super(name);

  static BuiltSet<OTPChannel> get values => _$values;
  static OTPChannel valueOf(String name) => _$valueOf(name);
}

/// Optionally, enum_class can generate a mixin to go with your enum for use
/// with Angular. It exposes your enum constants as getters. So, if you mix it
/// in to your Dart component class, the values become available to the
/// corresponding Angular template.
///
/// Trigger mixin generation by writing a line like this one next to your enum.
abstract class OTPChannelMixin = Object with _$OTPChannelMixin;


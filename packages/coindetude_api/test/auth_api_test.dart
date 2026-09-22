import 'package:test/test.dart';
import 'package:coindetude_api/coindetude_api.dart';


/// tests for AuthApi
void main() {
  final instance = CoindetudeApi().getAuthApi();

  group(AuthApi, () {
    // Forgot Password
    //
    //Future<OTPSentResponse> forgotPassword(ForgotPasswordRequest forgotPasswordRequest) async
    test('test forgotPassword', () async {
      // TODO
    });

    // Étape 1 — Login : envoie un OTP (ou skip si device de confiance)
    //
    //Future<JsonObject> login(LoginRequest loginRequest, { String xTrustedDevice }) async
    test('test login', () async {
      // TODO
    });

    // Logout
    //
    //Future logout({ String xRefreshToken, RefreshRequest refreshRequest }) async
    test('test logout', () async {
      // TODO
    });

    // Logout All
    //
    //Future logoutAll() async
    test('test logoutAll', () async {
      // TODO
    });

    // Refresh
    //
    //Future<TokenPair> refresh({ String xRefreshToken, RefreshRequest refreshRequest }) async
    test('test refresh', () async {
      // TODO
    });

    // Étape 1 — Inscription : envoie un OTP
    //
    //Future<OTPSentResponse> register(RegisterRequest registerRequest) async
    test('test register', () async {
      // TODO
    });

    // Resend Otp
    //
    //Future<OTPSentResponse> resendOtp(ResendOTPRequest resendOTPRequest) async
    test('test resendOtp', () async {
      // TODO
    });

    // Reset Password
    //
    //Future<AuthResponse> resetPassword(ResetPasswordRequest resetPasswordRequest) async
    test('test resetPassword', () async {
      // TODO
    });

    // Verify Otp
    //
    //Future<AuthResponse> verifyOtp(VerifyOTPRequest verifyOTPRequest) async
    test('test verifyOtp', () async {
      // TODO
    });

  });
}

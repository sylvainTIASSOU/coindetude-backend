import 'package:test/test.dart';
import 'package:coindetude_api/coindetude_api.dart';


/// tests for UploadsApi
void main() {
  final instance = CoindetudeApi().getUploadsApi();

  group(UploadsApi, () {
    // Confirme l'upload et valide le fichier côté serveur
    //
    //Future<ConfirmResponse> confirm(String fileId) async
    test('test confirm', () async {
      // TODO
    });

    // Génère une URL PUT pré-signée pour upload direct
    //
    //Future<PresignResponse> presign(PresignRequest presignRequest) async
    test('test presign', () async {
      // TODO
    });

  });
}

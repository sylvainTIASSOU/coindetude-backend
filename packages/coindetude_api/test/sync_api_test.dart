import 'package:test/test.dart';
import 'package:coindetude_api/coindetude_api.dart';


/// tests for SyncApi
void main() {
  final instance = CoindetudeApi().getSyncApi();

  group(SyncApi, () {
    // Synchronise une mutation offline (idempotent)
    //
    // Applique un événement offline avec idempotence stricte.
    //
    //Future<JsonObject> applyEvent(String idempotencyKey, SyncEventRequest syncEventRequest) async
    test('test applyEvent', () async {
      // TODO
    });

  });
}

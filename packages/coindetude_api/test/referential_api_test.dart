import 'package:test/test.dart';
import 'package:coindetude_api/coindetude_api.dart';


/// tests for ReferentialApi
void main() {
  final instance = CoindetudeApi().getReferentialApi();

  group(ReferentialApi, () {
    // Détail d'une ressource (avec contenu + URL fichier)
    //
    //Future<ResourceReadDetail> getResource(String resourceId) async
    test('test getResource', () async {
      // TODO
    });

    // Liste des chapitres
    //
    //Future<PageResponseChapterRead> listChapters({ String levelId, String subjectId, String seriesId, int limit, int offset }) async
    test('test listChapters', () async {
      // TODO
    });

    // Liste des niveaux scolaires
    //
    //Future<PageResponseLevelRead> listLevels({ Cycle cycle, int limit, int offset }) async
    test('test listLevels', () async {
      // TODO
    });

    // Liste des ressources (sans contenu lourd)
    //
    //Future<PageResponseResourceRead> listResources({ String chapterId, ResourceType type, int year, int limit, int offset }) async
    test('test listResources', () async {
      // TODO
    });

    // Liste des séries (lycée)
    //
    //Future<PageResponseSeriesRead> listSeries({ Cycle cycle, int limit, int offset }) async
    test('test listSeries', () async {
      // TODO
    });

    // Liste des matières
    //
    //Future<PageResponseSubjectRead> listSubjects({ Cycle cycle, int limit, int offset }) async
    test('test listSubjects', () async {
      // TODO
    });

  });
}

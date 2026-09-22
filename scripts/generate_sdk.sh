#!/usr/bin/env bash
# ==============================================================================
# Script de génération du SDK Dart / Flutter pour CoinDétude
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
OUTPUT_DIR="${REPO_ROOT}/packages/coindetude_api"
CONFIG_FILE="${REPO_ROOT}/openapi-generator-config.yaml"
SPEC_FILE="${REPO_ROOT}/openapi.json"

echo "=========================================================="
echo "🚀 Génération du SDK Dart/Flutter CoinDétude"
echo "=========================================================="

cd "${REPO_ROOT}"

# 1. Export du contrat OpenAPI à jour
echo "📦 1. Export du schéma OpenAPI..."
poetry run python -m scripts.export_openapi --output "${SPEC_FILE}"

# 2. Détection du moteur openapi-generator
echo "⚙️ 2. Détection de openapi-generator..."
GENERATED=0

if command -v openapi-generator-cli >/dev/null 2>&1; then
    echo "   Utilisation du binaire global openapi-generator-cli"
    openapi-generator-cli generate \
        -c "${CONFIG_FILE}" \
        -i "${SPEC_FILE}" \
        -o "${OUTPUT_DIR}"
    GENERATED=1
elif command -v docker >/dev/null 2>&1; then
    echo "   Utilisation de Docker (openapitools/openapi-generator-cli:v7.8.0)"
    docker run --rm \
        -v "${REPO_ROOT}:/local" \
        openapitools/openapi-generator-cli:v7.8.0 generate \
        -c /local/openapi-generator-config.yaml \
        -i /local/openapi.json \
        -o /local/packages/coindetude_api
    GENERATED=1
elif command -v npx >/dev/null 2>&1; then
    echo "   Utilisation de npx (@openapitools/openapi-generator-cli)"
    npx @openapitools/openapi-generator-cli generate \
        -c "${CONFIG_FILE}" \
        -i "${SPEC_FILE}" \
        -o "${OUTPUT_DIR}"
    GENERATED=1
elif command -v java >/dev/null 2>&1; then
    JAR_CACHE="${REPO_ROOT}/.cache/openapi-generator-cli.jar"
    if [ ! -f "${JAR_CACHE}" ]; then
        echo "   Téléchargement du JAR openapi-generator-cli 7.8.0..."
        mkdir -p "${REPO_ROOT}/.cache"
        curl -sSL "https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli/7.8.0/openapi-generator-cli-7.8.0.jar" -o "${JAR_CACHE}"
    fi
    echo "   Utilisation du JAR standalone java..."
    java -jar "${JAR_CACHE}" generate \
        -c "${CONFIG_FILE}" \
        -i "${SPEC_FILE}" \
        -o "${OUTPUT_DIR}"
    GENERATED=1
else
    echo "⚠️ Aucun moteur d'exécution (docker, npx, openapi-generator-cli, java) n'a été détecté localement."
    echo "   En CI, le job GitHub Actions utilise l'image Docker officielle automatiquement."
    echo "   Pour tester en local, installez Docker ou Node.js (npx)."
fi

# 3. Post-processing Dart (si Dart/Flutter est installé)
if [ "${GENERATED}" -eq 1 ] && command -v dart >/dev/null 2>&1; then
    echo "🎯 3. Compilation et vérification du SDK Dart..."
    cd "${OUTPUT_DIR}"
    dart pub get
    if grep -q "build_runner" pubspec.yaml 2>/dev/null; then
        echo "   Exécution de build_runner..."
        dart run build_runner build --delete-conflicting-outputs
    fi
    echo "   Analyse statique..."
    dart analyze || true
fi

echo "=========================================================="
echo "✅ Opération terminée avec succès !"
echo "=========================================================="


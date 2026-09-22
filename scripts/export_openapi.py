"""Script d'export et de validation du contrat OpenAPI de CoinDétude.

Usage :
    # Exporter le schéma dans openapi.json
    poetry run python -m scripts.export_openapi

    # Spécifier un chemin de sortie alternatif
    poetry run python -m scripts.export_openapi --output custom_path.json

    # Vérifier si le schéma committé est à jour (idéal en CI / pre-commit)
    poetry run python -m scripts.export_openapi --check
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

# Assurer que le répertoire racine est dans le sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from app.main import app  # noqa: E402


def generate_openapi_dict() -> dict[str, Any]:
    """Génère le dictionnaire OpenAPI enrichi."""
    return app.openapi()


def export_openapi(output_path: Path) -> None:
    """Écrit le schéma OpenAPI formaté dans le fichier cible."""
    schema = generate_openapi_dict()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    content = json.dumps(schema, indent=2, ensure_ascii=False) + "\n"
    output_path.write_text(content, encoding="utf-8")

    paths_count = len(schema.get("paths", {}))
    schemas_count = len(schema.get("components", {}).get("schemas", {}))
    tags_count = len(schema.get("tags", []))

    print(
        f"✅ Contrat OpenAPI exporté avec succès dans '{output_path}'\n"
        f"   - Endpoints : {paths_count}\n"
        f"   - Schémas : {schemas_count}\n"
        f"   - Tags thématiques : {tags_count}\n"
        f"   - Taille : {len(content.encode('utf-8')) / 1024:.1f} KB"
    )


def check_openapi_drift(target_path: Path) -> bool:
    """Vérifie si le fichier existant est identique au schéma actuel."""
    if not target_path.exists():
        print(f"❌ Erreur : Le fichier '{target_path}' n'existe pas. Lancez l'export.")
        return False

    try:
        existing_content = target_path.read_text(encoding="utf-8")
        existing_schema = json.loads(existing_content)
    except Exception as exc:
        print(f"❌ Erreur de lecture du fichier existant '{target_path}' : {exc}")
        return False

    current_schema = generate_openapi_dict()

    if existing_schema == current_schema:
        print(f"✅ Le contrat OpenAPI '{target_path}' est parfaitement à jour.")
        return True

    print(
        f"❌ Dérive détectée ! Le fichier '{target_path}' ne correspond pas "
        "au code actuel de l'API.\n"
        "👉 Veuillez régénérer le schéma avec : poetry run python -m scripts.export_openapi"
    )
    return False


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Outil d'export et vérification du schéma OpenAPI CoinDétude"
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=REPO_ROOT / "openapi.json",
        help="Chemin du fichier OpenAPI de sortie (défaut: openapi.json à la racine)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Vérifie la dérive par rapport au fichier existant sans le modifier (code 0 si OK)",
    )

    args = parser.parse_args()

    if args.check:
        is_synced = check_openapi_drift(args.output)
        sys.exit(0 if is_synced else 1)
    else:
        export_openapi(args.output)


if __name__ == "__main__":
    main()

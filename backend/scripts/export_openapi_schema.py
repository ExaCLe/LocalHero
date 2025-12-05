import json
from pathlib import Path

from dotenv import load_dotenv

from app.main import app

load_dotenv()


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    output_path = project_root / "openapi.json"

    schema = app.openapi()
    output_path.write_text(json.dumps(schema, indent=2))
    print(f"Wrote OpenAPI schema to {output_path}")


if __name__ == "__main__":
    main()

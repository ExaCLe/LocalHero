"""
Generate OpenAPI schema from FastAPI and TypeScript types for the frontend.

- Writes backend/openapi.json
- Runs `openapi-typescript` to update frontend/src/lib/openapi-types.ts

Intended to be run via pre-commit and manually.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv


def main() -> int:
    project_root = Path(__file__).resolve().parents[2]  # project-root/
    backend_dir = project_root / "backend"
    frontend_dir = project_root / "frontend"

    # 1) Load env so app.main can import cleanly (DB URL etc. if needed)
    env_path = backend_dir / ".env"
    if env_path.exists():
        load_dotenv(env_path)

    # 2) Import FastAPI app and generate OpenAPI schema
    sys.path.insert(0, str(backend_dir))
    try:
        from app.main import app  # type: ignore[import]
    except Exception as exc:  # noqa: BLE001
        print(f"[sync-openapi] Failed to import app.main: {exc}", file=sys.stderr)
        return 1

    schema = app.openapi()
    openapi_path = backend_dir / "openapi.json"
    openapi_path.write_text(json.dumps(schema, indent=2))
    print(f"[sync-openapi] Wrote OpenAPI schema to {openapi_path}")

    # 3) Run openapi-typescript in the frontend
    output_path = frontend_dir / "src" / "lib" / "openapi-types.ts"
    try:
        subprocess.run(
            [
                "npx",
                "openapi-typescript",
                str(openapi_path),
                "--output",
                str(output_path),
            ],
            cwd=str(frontend_dir),
            check=True,
        )
    except FileNotFoundError:
        print(
            "[sync-openapi] `npx` not found. "
            "Make sure Node.js is installed and `openapi-typescript` is added as a dev dependency "
            "(npm install --save-dev openapi-typescript).",
            file=sys.stderr,
        )
        return 1
    except subprocess.CalledProcessError as exc:  # noqa: BLE001
        print(
            f"[sync-openapi] openapi-typescript failed with exit code {exc.returncode}",
            file=sys.stderr,
        )
        return exc.returncode

    print(f"[sync-openapi] Wrote TypeScript types to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

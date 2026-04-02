import argparse
import os

import httpx


DEFAULT_API = "http://localhost:8000"


def get_token(api_url: str, username: str, password: str) -> str:
    response = httpx.post(
        f"{api_url}/auth/token",
        data={"username": username, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=30.0,
    )
    response.raise_for_status()
    return response.json()["access_token"]


def upload_file(api_url: str, token: str, file_path: str) -> dict:
    with open(file_path, "rb") as f:
        files = {"file": (os.path.basename(file_path), f, "application/octet-stream")}
        response = httpx.post(
            f"{api_url}/backups/upload",
            files=files,
            headers={"Authorization": f"Bearer {token}"},
            timeout=120.0,
        )
    response.raise_for_status()
    return response.json()


def main() -> None:
    parser = argparse.ArgumentParser(description="Upload backup to OpenBackup API")
    parser.add_argument("file", help="Path to file to upload")
    parser.add_argument("--api", default=DEFAULT_API)
    parser.add_argument("--username", default="admin")
    parser.add_argument("--password", default="admin123")
    args = parser.parse_args()

    token = get_token(args.api, args.username, args.password)
    result = upload_file(args.api, token, args.file)
    print(result)


if __name__ == "__main__":
    main()

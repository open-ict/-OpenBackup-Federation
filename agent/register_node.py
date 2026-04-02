import argparse

import httpx


def get_token(api_url: str, username: str, password: str) -> str:
    response = httpx.post(
        f"{api_url}/auth/token",
        data={"username": username, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=30.0,
    )
    response.raise_for_status()
    return response.json()["access_token"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Register a federation node")
    parser.add_argument("--api", default="http://localhost:8000")
    parser.add_argument("--username", default="admin")
    parser.add_argument("--password", default="admin123")
    parser.add_argument("--name", required=True)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--region", default="EU")
    parser.add_argument("--description", default="")
    args = parser.parse_args()

    token = get_token(args.api, args.username, args.password)
    response = httpx.post(
        f"{args.api}/nodes/register",
        json={
            "name": args.name,
            "base_url": args.base_url,
            "region": args.region,
            "description": args.description,
        },
        headers={"Authorization": f"Bearer {token}"},
        timeout=30.0,
    )
    response.raise_for_status()
    print(response.json())


if __name__ == "__main__":
    main()

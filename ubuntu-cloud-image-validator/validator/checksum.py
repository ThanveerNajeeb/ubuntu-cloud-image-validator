import hashlib
import requests

def compute_sha256(file_path: str) -> str:
    """Compute SHA256 checksum of a local file."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def verify_remote_checksum(url: str, expected_sha256: str) -> dict:
    """Download a file from URL and verify its SHA256 checksum."""
    try:
        response = requests.get(url, timeout=30, stream=True)
        response.raise_for_status()
        sha256 = hashlib.sha256()
        for chunk in response.iter_content(chunk_size=8192):
            sha256.update(chunk)
        actual = sha256.hexdigest()
        return {"url": url, "expected": expected_sha256, "actual": actual, "valid": actual == expected_sha256}
    except Exception as e:
        return {"url": url, "error": str(e), "valid": False}

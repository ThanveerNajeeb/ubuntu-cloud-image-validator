import os
import tempfile
import hashlib
from validator.checksum import compute_sha256

def test_sha256_correct():
    content = b"ubuntu cloud image test content"
    expected = hashlib.sha256(content).hexdigest()
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(content)
        tmp_path = f.name
    try:
        result = compute_sha256(tmp_path)
        assert result == expected
    finally:
        os.unlink(tmp_path)

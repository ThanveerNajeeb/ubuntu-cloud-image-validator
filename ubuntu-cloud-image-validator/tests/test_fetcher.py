from validator.fetcher import get_images_by_release

MOCK_INDEX = {
    "products": {
        "com.ubuntu.cloud:server:22.04:amd64": {
            "release": "jammy", "arch": "amd64", "label": "release",
            "versions": {
                "20240101": {
                    "items": {
                        "disk1.img": {
                            "ftype": "disk1.img", "sha256": "abc123def456",
                            "size": 500000000, "endpoint": "https://ec2.amazonaws.com",
                            "path": "server/releases/jammy/release-20240101/ubuntu-22.04.img"
                        }
                    }
                }
            }
        }
    }
}

def test_filter_by_release():
    results = get_images_by_release(MOCK_INDEX, release="jammy")
    assert len(results) == 1
    assert results[0]["release"] == "jammy"

def test_filter_by_cloud():
    results = get_images_by_release(MOCK_INDEX, cloud="amazonaws")
    assert len(results) == 1

def test_filter_no_match():
    results = get_images_by_release(MOCK_INDEX, release="focal")
    assert len(results) == 0

def test_no_filter_returns_all():
    results = get_images_by_release(MOCK_INDEX)
    assert len(results) >= 1

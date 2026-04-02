import requests

SIMPLESTREAMS_URL = (
    "https://cloud-images.ubuntu.com/releases/streams/v1/com.ubuntu.cloud:released:download.json"
)

def fetch_image_index():
    """Fetch the Ubuntu cloud image index from Canonical's simplestreams."""
    response = requests.get(SIMPLESTREAMS_URL, timeout=15)
    response.raise_for_status()
    return response.json()

def get_images_by_release(index, release=None, cloud=None):
    """Filter images from the index by Ubuntu release name and/or cloud provider."""
    results = []
    products = index.get("products", {})
    for product_key, product in products.items():
        versions = product.get("versions", {})
        for version_key, version in versions.items():
            items = version.get("items", {})
            for item_key, item in items.items():
                entry = {
                    "product": product_key,
                    "release": product.get("release", ""),
                    "version": version_key,
                    "label": product.get("label", ""),
                    "arch": product.get("arch", ""),
                    "cloud": item.get("endpoint", ""),
                    "sha256": item.get("sha256", ""),
                    "size": item.get("size", 0),
                    "ftype": item.get("ftype", ""),
                    "path": item.get("path", ""),
                }
                if release and release.lower() not in entry["release"].lower():
                    continue
                if cloud and cloud.lower() not in entry["cloud"].lower():
                    continue
                results.append(entry)
    return results

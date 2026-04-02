import json
from datetime import datetime

def format_human(images: list, title: str = "Ubuntu Cloud Image Report") -> str:
    """Format image list as a human-readable report."""
    lines = []
    lines.append("=" * 60)
    lines.append(f"  {title}")
    lines.append(f"  Generated: {datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append("=" * 60)
    if not images:
        lines.append("  No images found matching the criteria.")
        return "\n".join(lines)
    for i, img in enumerate(images, 1):
        lines.append(f"\n[{i}] Release : {img.get('release', 'N/A')}")
        lines.append(f"    Version : {img.get('version', 'N/A')}")
        lines.append(f"    Arch    : {img.get('arch', 'N/A')}")
        lines.append(f"    Type    : {img.get('ftype', 'N/A')}")
        lines.append(f"    Cloud   : {img.get('cloud', 'N/A')}")
        sha = img.get("sha256", "")
        lines.append(f"    SHA256  : {sha[:24]}..." if sha else "    SHA256  : N/A")
        size = img.get("size", 0)
        lines.append(f"    Size    : {round(size / 1024 / 1024, 1)} MB" if size else "    Size    : N/A")
    lines.append("\n" + "=" * 60)
    lines.append(f"  Total images found: {len(images)}")
    lines.append("=" * 60)
    return "\n".join(lines)

def format_json(images: list) -> str:
    """Format image list as structured JSON."""
    return json.dumps(images, indent=2)

import argparse
import sys
from validator.fetcher import fetch_image_index, get_images_by_release
from validator.reporter import format_human, format_json

def main():
    parser = argparse.ArgumentParser(
        description="Ubuntu Cloud Image Validator — inspect and validate Ubuntu cloud images",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m validator.cli --release jammy
  python -m validator.cli --release noble --cloud aws
  python -m validator.cli --release focal --output json
        """
    )
    parser.add_argument("--release", help="Ubuntu release name (e.g. jammy, noble, focal)")
    parser.add_argument("--cloud", help="Filter by cloud provider keyword (e.g. aws, azure, google)")
    parser.add_argument("--output", choices=["human", "json"], default="human", help="Output format")
    parser.add_argument("--limit", type=int, default=10, help="Max results to show (default: 10)")
    args = parser.parse_args()
    print("Fetching Ubuntu cloud image index from Canonical...")
    try:
        index = fetch_image_index()
    except Exception as e:
        print(f"ERROR: Could not fetch image index — {e}")
        sys.exit(1)
    images = get_images_by_release(index, release=args.release, cloud=args.cloud)
    images = images[:args.limit]
    if args.output == "json":
        print(format_json(images))
    else:
        print(format_human(images))

if __name__ == "__main__":
    main()

# Ubuntu Cloud Image Validator

A Python CLI tool for validating and inspecting Ubuntu cloud images across AWS, Azure, and GCP — built to mirror real-world workflows used by Canonical's cloud image team.

---

## What It Does

Ubuntu publishes cloud images for every major public cloud platform. This tool queries Canonical's official [Simplestreams](https://cloud-images.ubuntu.com) metadata index to:

- **Inspect** available Ubuntu cloud images by release (e.g. `jammy`, `noble`, `focal`)
- **Filter** by cloud provider (AWS, Azure, GCP)
- **Verify** SHA256 checksums to confirm image integrity
- **Report** results in human-readable or structured JSON format

---

## Why I Built This

I built this project to deepen my understanding of how Canonical manages Ubuntu cloud images — specifically the Simplestreams metadata format, `cloud-init` integration, and Debian packaging. It directly reflects the kind of Python tooling used in Ubuntu cloud image workflows.

---

## Installation

**Requirements:** Python 3.8+, pip
```bash
git clone https://github.com/ThanveerNajeeb/ubuntu-cloud-image-validator.git
cd ubuntu-cloud-image-validator
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

---

## Usage
```bash
# List latest Ubuntu Jammy (22.04) images
python -m validator.cli --release jammy

# Filter by cloud provider
python -m validator.cli --release noble --cloud aws

# Output as JSON
python -m validator.cli --release focal --output json

# Limit results
python -m validator.cli --release jammy --limit 5
```

---

## Running Tests
```bash
pytest tests/ -v
```

All 9 tests cover checksum computation, image filtering, and report formatting.

---

## Project Structure
```
ubuntu-cloud-image-validator/
├── validator/
│   ├── cli.py          # Argparse CLI entry point
│   ├── fetcher.py      # Queries Canonical Simplestreams index
│   ├── checksum.py     # SHA256 verification logic
│   └── reporter.py     # Human-readable and JSON formatters
├── tests/
├── requirements.txt
├── setup.py
└── README.md
```

---

## Author

**Thanveer Najeeb** — Cloud & DevOps Engineer
[LinkedIn](https://www.linkedin.com/in/thanveer-najeeb-0984a61a0) · [GitHub](https://github.com/ThanveerNajeeb)

---

## License

MIT License

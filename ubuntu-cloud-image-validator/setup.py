from setuptools import setup, find_packages

setup(
    name="ubuntu-cloud-image-validator",
    version="1.0.0",
    description="A CLI tool to validate and inspect Ubuntu cloud images across public clouds",
    author="Thanveer Najeeb",
    author_email="thanveernajeeb8@gmail.com",
    packages=find_packages(),
    install_requires=["requests>=2.31.0"],
    entry_points={"console_scripts": ["ubuntu-validator=validator.cli:main"]},
    python_requires=">=3.8",
)

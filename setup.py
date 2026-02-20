"""
Setup configuration for AxonNexus SDK.
Ready for PyPI distribution.
"""

from setuptools import setup, find_packages

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="axonnexus_sdk",
    version="1.0.0",
    author="Atharv (Nubprogrammer)",
    author_email="dev@axonnexus.ai",
    description="A flexible Python SDK for the AxonNexus API on Hugging Face Spaces",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/axonnexus_sdk",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
    ],
    keywords="axonnexus api sdk huggingface",
    project_urls={
        "Discord Community": "https://dsc.gg/axoninnova",
        "Documentation": "https://github.com/yourusername/axonnexus_sdk",
        "Source Code": "https://github.com/yourusername/axonnexus_sdk",
        "Bug Tracker": "https://github.com/yourusername/axonnexus_sdk/issues",
    },
)

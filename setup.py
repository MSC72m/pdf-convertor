from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="file-converter",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A versatile file format converter with async support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/file-converter",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pdf2docx",
        "aiopath",
        "PyMuPDF",
        "img2pdf",
        "python-pptx",
        "pandas",
        "weasyprint",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-asyncio",
            "black",
            "isort",
        ],
    },
) 
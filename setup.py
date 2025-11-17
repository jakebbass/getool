#!/usr/bin/env python3
"""Setup script for getool."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="getool",
    version="0.1.0",
    author="jakebbass",
    description="Generate ElevenLabs Twilio Outbound Integration Blueprint",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jakebbass/getool",
    py_modules=["getool"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "getool=getool:main",
        ],
    },
)

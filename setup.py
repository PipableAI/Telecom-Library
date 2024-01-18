from setuptools import setup, find_packages

setup(
    name="telecom_library",
    version="0.1.0",
    description="A Python library for telecom-related functions",
    packages=find_packages(),
    install_requires=[
        "psycopg2-binary",
        "psycopg2",
        "slack_sdk",
    ],
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
)

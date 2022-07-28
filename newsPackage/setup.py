from setuptools import setup, find_packages

setup(
    name="KnewsScraper",
    version="0.1",
    description="ccpy",
    author="limetree06",
    author_email="limetree0006@gmail.com",
    url="https://github.com/limetree06",
    download_url="https://github.com/limetree06/Knews-Scraper/archive/0.0.tar.gz",
    install_requires=[],
    packages=find_packages(exclude=[]),
    keywords=["kornewsscraper"],
    python_requires=">=3",
    package_data={},
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)

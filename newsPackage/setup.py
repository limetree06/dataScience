from setuptools import setup, find_packages

INSTALL_REQUIRES = [
    "pandas >= 0.14",
    "requests >= 2.7.0",
    "beautifulsoup4 >= 4.9.3",
]

KEYWORDS = [
    "news",
    "scraping",
]

setup(
    name="Knews-Scraper",
    version="0.0.1",
    description="Scrape news titles from DAUM",
    author="limetree06",
    author_email="limetree0006@gmail.com",
    url="https://github.com/limetree06",
    license="MIT",
    install_requires=INSTALL_REQUIRES,
    packages=find_packages(),
    keywords=KEYWORDS,
    python_requires=">=3",
)

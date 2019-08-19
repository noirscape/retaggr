from setuptools import setup, find_packages

setup(
    name="retaggr",
    version="0.1.0a",
    url="https://github.com/booru-utils/reverse-search",
    license="LGPLv3",
    description="Reverse image searching utility for images.",
    long_description=open("README.md").read(),
    author="Valentijn 'noirscape' V.",
    author_email="neko@catgirlsin.space",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
    ],
    keywords="reverse image search booru",
    project_urls={
        "Source": "https://github.com/booru-utils/reverse-search",
        "Tracker": "https://github.com/booru-utils/reverse-search/issues",
    },
    packages=find_packages(exclude=['docs', 'tests*'])
)
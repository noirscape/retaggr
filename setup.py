from setuptools import setup, find_packages
import subprocess

setup(
    name="retaggr",
    version="3.1.0",
    url="https://github.com/noirscape/retaggr",
    license="LGPLv3",
    description="Reverse image searching utility for images.",
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    author="Valentijn 'noirscape' V.",
    author_email="neko@catgirlsin.space",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Programming Language :: Python :: 3",
    ],
    keywords="reverse image search booru",
    project_urls={
        "Source": "https://github.com/noirscape/retaggr",
        "Tracker": "https://github.com/noirscape/retaggr/issues",
        "Documentation": "https://retaggr.rtfd.org"
    },
    packages=find_packages('src'),
    package_dir={'':'src',},
    install_requires=[
        "lxml",
        "fake-useragent",
        "requests",
        "aiohttp"
    ]
)

from setuptools import setup, find_packages
import subprocess

def get_version():
    out_val = subprocess.getoutput("git describe --long | sed 's/-/-r/;'")
    if len(subprocess.getoutput("git status -s")) != 0:
        out_val += "-dirty"
    return out_val

setup(
    name="retaggr",
    version=get_version(),
    url="https://github.com/booru-utils/reverse-search",
    license="LGPLv3",
    description="Reverse image searching utility for images.",
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    author="Valentijn 'noirscape' V.",
    author_email="neko@catgirlsin.space",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
    ],
    keywords="reverse image search booru",
    project_urls={
        "Source": "https://github.com/booru-utils/retaggr",
        "Tracker": "https://github.com/booru-utils/retaggr/issues",
        "Documentation": "https://retaggr.rtfd.org"
    },
    packages=find_packages('src'),
    package_dir={'':'src',},
    install_requires=[
        "aiohttp-requests",
        "lxml",
        "fake-useragent",
        "requests",
    ]
)

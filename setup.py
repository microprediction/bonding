import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="bonding",
    version="0.0.1",
    description="Bonding curve market makers",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/microprediction/bonding",
    author="microprediction",
    author_email="peter.cotton@microprediction.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
    ],
    packages=["bonding",
              "bonding.builtin"
              ],
    test_suite='pytest',
    tests_require=['pytest'],
    include_package_data=True,
    install_requires=['scipy'],
    entry_points={
        "console_scripts": [
            "bonding=bonding.__main__:main",
        ]
    },
)
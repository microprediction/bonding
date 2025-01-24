import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="amms",
    version="0.0.3",
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
    packages=["amms",
              ],
    test_suite='pytest',
    tests_require=['pytest'],
    include_package_data=True,
    install_requires=['scipy'],
    entry_points={
        "console_scripts": [
            "amms=amms.__main__:main",
        ]
    },
)
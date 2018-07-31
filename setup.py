import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="configfy",
    version="1.0.7",
    author="Manuel Pasieka",
    author_email="manuel.pasieka@protonmail.ch",
    description="Decorator library to expose keyword arguments through config files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mapa17/configfy",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)

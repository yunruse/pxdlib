import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

packages = setuptools.find_packages()

setuptools.setup(
    name="pxdlib",
    description="Pixelmator Pro file (.pxd) library",
    version="0.0.1",
    author="Mia yun Ruse",
    author_email="mia@yunru.se",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yunruse/pxdlib",
    packages=packages,
    classifiers=[
        # TODO: add classifier, keywords
    ],
    keywords="?",
    python_requires='>=3.6',
    install_requires=[],
)

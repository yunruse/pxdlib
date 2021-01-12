import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

packages = setuptools.find_packages()

setuptools.setup(
    name="pxdlib",
    description="Pixelmator Pro file (.pxd) library",
    version="0.0.3",
    author="Mia yun Ruse",
    author_email="mia@yunru.se",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yunruse/pxdlib",
    packages=packages,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Multimedia :: Graphics :: Editors",
    ],
    keywords="Pixelmator pxd file image raster vector",
    python_requires='>=3.6',
    install_requires=[],
)

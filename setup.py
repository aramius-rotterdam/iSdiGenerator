import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="iSdiGenerator",
    version="0.0.1",
    author="ArAmIuS de Rotterdam",
    author_email="bchowa@gmail.com",
    description="iSdiGenerator is a tool to generate a C++ class which represents an interface.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aramius-rotterdam/iSdiGenerator",
    project_urls={
        "Bug Tracker": "https://github.com/aramius-rotterdam/iSdiGenerator/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL-3.0 License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
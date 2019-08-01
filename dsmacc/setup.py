import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dsmacc",
    version="0.0.1",
    author="Daniel Ellis",
    author_email="danielellisscience@googlemail.com",
    description="An initator / processor of the DSMACC box model",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wolfiex/DSMACC",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

print 'go into obs and compile f90'

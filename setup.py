import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="deregress",
    version="0.0.1",
    author="Diego Jesus",
    author_email="diego.a.r.jz@gmail.com",
    description="A lightweight regression testing system.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/diegoarjz/deregress.git",
    packages=setuptools.find_packages()
)

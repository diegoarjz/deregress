import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="deregress",
    version="0.0.1",
    author="Diego Jesus",
    author_email="diego.a.r.jz@gmail.com",
    description="Regression testing external programs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="to_be_defined",
    packages=setuptools.find_packages()
)

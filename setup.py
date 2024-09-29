from setuptools import setup, find_packages


setup(
    name="Astro",
    version="1.0",
    packages=find_packages(),

    # Top level, single-file modules
    py_modules=["src/log",
                "src/astro_db"]
)

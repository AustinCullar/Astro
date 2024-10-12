from setuptools import setup, find_packages


setup(
    name="Astro",
    version="1.0",
    packages=find_packages(),

    # Top level, single-file modules
    py_modules=[
        "src/log",
        "src/astro_db",
        "src/progress"],

    # Packages required to run the app
    install_requires=[
        "python-dotenv>=1.0.1",
        "google-api-python-client>=2.146.0",
        "nltk>=3.9.1",
        "pandas>=2.2.3"],

    # Packages required to test/develop the app
    extras_require={
        "dev": [
            "pytest>=8.3.3",
            "coverage>=7.6.1",
            "flake8>=7.1.1"
        ]
    },
)

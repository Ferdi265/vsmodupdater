from setuptools import setup

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name = "vsmodupdater",
    description = "a mod updater for VintageStory",
    version = "0.3.0",
    author = "Ferdinand Bachmann",
    author_email = "theferdi265@gmail.com",
    packages = [
        "vsmodupdater",
    ],
    entry_points = {
        "console_scripts": [
            "vsmodupdater=vsmodupdater.cli:main",
        ]
    },
    package_data = {
        "vsmodupdater": ["py.typed"]
    },
    python_requires = ">=3.7",
    install_requires = requirements
)

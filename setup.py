from setuptools import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='wordlbot',
    version='1.0.1',
    packages=['wordlbot'],
    url='https://github.com/kimvais/wordlbot/',
    license='BSD',
    author='Kimmo Parviainen-Jalanko',
    author_email='kimvais@kimva.is',
    description="A tool to help solve The New Your Times' World -game",
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={
        "console_scripts": ['wordlbot = wordlbot.__main__:main'],
    },
    package_data={
        "wordlbot": ["*.xz", ]
    }
)

from setuptools import setup

setup(
    name='wordlbot',
    version='1.0',
    packages=['wordlbot'],
    url='https://github.com/kimvais/wordlbot/',
    license='BSD',
    author='Kimmo Parviainen-Jalanko',
    author_email='kimvais@kimva.is',
    description="A tool to help solve The New Your Times' World -game",
    entry_points={
        "console_scripts": ['wordlbot = wordlbot.__main__:main'],
    },
    package_data={
        "wordlbot": ["*.xz", ]
    }
)

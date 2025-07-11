from setuptools import setup, find_packages

setup(
    name='Pridey',
    version='0.1.0',
    description='Beautiful color and plotting utilities for matplotlib',
    author='Barton Muller',
    packages=find_packages(),
    install_requires=[
        'matplotlib',
        'seaborn',
        'numpy',
        'colorspacious',
        'scipy'
    ],
    include_package_data=True,
    package_data={
        'Pridey': ['colorsheet.csv']
    },
    python_requires='>=3.7',
)

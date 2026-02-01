from setuptools import find_packages, setup

setup(
    name='plotfair',
    version='0.1.0',
    description='Beautiful color and plotting utilities using matplotlib & plotly',
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
        'plotfair': ['colorsheet.csv']
    },
    python_requires='>=3.7',
)

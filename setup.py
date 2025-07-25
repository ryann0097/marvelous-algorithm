from setuptools import setup, find_packages

long_description = """
# SAGA
*S*cheduling *A*lgorithms *GA*thered

Read more about SAGA on [GitHub](https://github.com/ANRGUSC/saga)
"""

setup(
    name='saga',
    version='0.0.11',
    description='Collection of schedulers for distributed computing',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ANRGUSC/saga',
    author='Jared Coleman',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    install_requires=[
        'networkx',
        'numpy',
        'matplotlib',
        'scipy',
        'pandas',
        'plotly',
        'kaleido',
        'pysmt',
        'wfcommons',
        'streamlit',
        'dill',
        'pygraphviz',
        'joblib==1.3.2',
        'statsmodels==0.14.1',
        'seaborn==0.13.2',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'saga_exp_parametric = saga.experiment.benchmarking.parametric:main',
        ],
    },
)

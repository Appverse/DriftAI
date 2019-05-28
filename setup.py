"""Setup module"""
from setuptools import setup, find_packages

setup(
    name='driftai',
    version='0.1',
    description='Framework to automate hyperparameter optimization',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    python_requires='>=3.6, <4',
    install_requires=[
        'numpy', 
        'pandas', 
        'scikit-learn', 
        "click",
        "tinydb",
        "pillow",
    ],
    include_package_data=True,
    keywords='machine-learning ml framework automatization optimization',
    packages=find_packages(exclude=['test', 'test.*']),
    entry_points='''
        [console_scripts]
        dai=driftai.cli:main
    ''',
)
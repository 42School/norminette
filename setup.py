from setuptools import setup, find_namespace_packages

import os
import setuptools
import subprocess

subprocess.call("pip install -r requirements.txt", shell=True)
exec(open("norminette/version.py").read())
setup(
    name="norminette",
    version=__version__,
    author="42",
    author_email="pedago@42.fr",
    description="Open source norminette",
    package_dir={'lexer':'norminette/lexer', 'rules':'norminette/rules', 'tools':'norminette/tools'},
    packages=find_namespace_packages(),
    entry_points={
        'console_scripts': [
            'norminette = norminette.__main__:main',
        ],
    },
)

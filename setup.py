from setuptools import setup, find_namespace_packages

setup(
    name="norminette",
    version="2.0.5",
    author="42",
    author_email="pedago@42.fr",
    description="Open source norminette",
    package_dir={'lexer':'norminette/lexer', 'rules':'norminette/rules', 'tools':'norminette/tools'},
    packages=find_namespace_packages(),#['norminette', 'norminette.lexer', 'norminette.rules'],
    entry_points={
        'console_scripts': [
            'norminette = norminette.__main__:main',
        ],
    },
)
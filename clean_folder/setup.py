from setuptools import setup, find_namespace_packages

setup(
    name='clean_folder',
    version='0.0.1',
    description='Very useful code',
    url='https://github.com/Dmytro9513/first.git',
    author='Dimasta',
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['clean-folder = clean_folder.clean:main']}
)

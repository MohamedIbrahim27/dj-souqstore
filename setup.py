from setuptools import setup, find_packages

setup(
    name='myproject',
    version='0.1',
    description='My Django project',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/MohamedIbrahim27/souqstore.git',
    packages=find_packages(),
    install_requires=[
        'Django==4.1.5',
        'requests',
        # add any other dependencies here
    ],
)
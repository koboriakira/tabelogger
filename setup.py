from setuptools import setup, find_packages

setup(
    name="tabelogger",
    version='1.0',
    description='食べログの管理アプリ',
    author='Kobori Akira',
    author_email='private.beats@gmail.com',
    url='https://github.com/koboriakira/tabelogger',
    packages=find_packages(),
    install_requires=open('requirements.txt').read().splitlines(),
    license='MIT',
)

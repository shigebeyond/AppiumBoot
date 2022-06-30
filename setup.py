# coding=utf-8
import re
import ast
from setuptools import setup, find_packages
from os.path import dirname, join, abspath
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# 读元数据：author/version/description
with open('AppiumBoot/__init__.py', 'rb') as f:
    text = f.read().decode('utf-8')
    items = re.findall(r'__(\w+)__ = "(.+)"', text)
    meta = dict(items)

setup(
    name='AppiumBoot',
    version=meta['version'],
    url='https://github.com/shigebeyond/AppiumBoot',
    license='BSD',
    author=meta['author'],
    author_email='772910474@qq.com',
    description=meta['description'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.6",
    install_requires=[
        'PyYAML>=6.0',
        'selenium==4.1.5',
        'selenium-requests==1.4.1',
        'jsonpath>=0.82',
        'lxml==4.3.2',
        'Appium-Python-Client==2.3.0'
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Operating System :: POSIX :: Linux",
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    entry_points='''
        [console_scripts]
        AppiumBoot=AppiumBoot.boot:main
    '''
)

import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='pyravepay',
    version='0.2.6',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',  # example license
    description='A reusable app for making online payments with ravepay',
    long_description=README,
    url='https://www.example.com/',
    author='Biola Oyeniyi',
    author_email='gbozee@gmail.com',
    install_requires=[
        "requests==2.23.0",
        "Paperboy==1.0.1",
        "python-dateutil==2.8.1",
    ],
    # extras_require={"django": ["django>=2.0"], "starlette": ["starlette==0.12.13"]},
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: X.Y',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)

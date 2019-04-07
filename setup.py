import os

from setuptools import find_packages, setup

from drf_simple_invite import VERSION

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='drf_simple_invite',
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    description='An extension of django rest framework that allows to invite user via email',
    long_description=README,
    long_description_content_type='text/markdown',  # This is important for README.md in markdown format
    url='https://github.com/thapabishwa/drf-simple-invite/',
    author='Bishwa Thapa',
    author_email='thapabishwa@aol.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)

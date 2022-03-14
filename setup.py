import setuptools
import gqylpy_datastruct as g

setuptools.setup(
    name=g.__name__,
    version='.'.join(str(v) for v in g.__version__),
    author='竹永康',
    author_email='gqylpy@outlook.com',
    license='Apache 2.0',
    long_description='',
    url='',
    packages=[g.__name__],
    install_requires=[],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Text Processing :: Indexing',
        'Topic :: Utilities',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ]
)

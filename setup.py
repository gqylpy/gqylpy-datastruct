import setuptools
import pkg_resources
import gqylpy_datastruct as g

with open(g.__file__, encoding='utf8') as f:
    for line in f:
        if line.startswith('@version: ', 4):
            version = line.split()[-1]
            break
    author, email = f.readline().split(maxsplit=1)[-1].rstrip().split()
    source = f.readline().split()[-1]

with open('README.md', encoding='utf8') as f:
    long_description = f.read()

with open('requirements.txt', encoding='utf8') as f:
    requires = [str(x) for x in pkg_resources.parse_requirements(f)]

setuptools.setup(
    name=g.__name__,
    version=version,
    author=author,
    author_email=email,
    license='Apache 2.0',
    url='http://gqylpy.com',
    project_urls={'Source': source},
    description='创建一张蓝图来规划好程序需要的数据结构，并在之后使用该蓝图去校验到来的数据是'
                '否如期。',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=[g.__name__],
    python_requires='>=3.6, <4',
    install_requires=requires,
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
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11'
    ]
)

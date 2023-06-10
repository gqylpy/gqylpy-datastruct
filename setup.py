import re
import setuptools
import pkg_resources
import gqylpy_datastruct as g

version, author, email, source = re.search(
    ' {4}@version: ([1-9]\d*\.\d+(?:\.(?:alpha|beta)?\d+)?)\n'
    ' {4}@author: ([\u4e00-\u9fa5]{2,4}|[A-Z][a-z]+(?: [A-Z][a-z]+)?) (<.+?>)\n'
    ' {4}@source: (https?://.+)',
    g.__doc__,
).groups()

setuptools.setup(
    name=g.__name__,
    version=version,
    author=author,
    author_email=email,
    license='Apache 2.0',
    url='http://gqylpy.com',
    project_urls={'Source': source},
    description='创建一张蓝图来规划好程序需要的数据结构，并在之后使用该蓝图去校验到来的数'
                '据是否如期。',
    long_description=open('README.md', encoding='utf8').read(),
    long_description_content_type='text/markdown',
    packages=[g.__name__],
    python_requires='>=3.8, <4',
    install_requires=[str(x) for x in pkg_resources.parse_requirements(
        open('requirements.txt', encoding='utf8')
    )],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: Chinese (Simplified)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Object Brokering',
        'Topic :: Software Development :: Pre-processors',
        'Topic :: Software Development :: Quality Assurance',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12'
    ]
)

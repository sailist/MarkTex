from setuptools import setup, find_packages

long_description = ""  # 这里可以导入外部的README.md

setup(
    name='marktex',
    version='0.9.8',
    description='convert markdown 2 latex code perfactly,support Chinese Language',
    long_description=long_description,
    url='https://github.com/sailist/MarkTex',
    author='hzYang',
    author_email='sailist@outlook.com',
    license='MIT',
    include_package_data=True,
    install_requires=[
        "pylatex", "matplotlib", 'requests'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',  # 自 3.5 开始支持 typehint
        'Programming Language :: Python :: 3.6',
    ],
    keywords='markdown latex convert',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'marktex = marktex.cli:main'
        ]
    },
)

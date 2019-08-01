from setuptools import setup,find_packages

setup(
    name='marktex',
    version='0.7.0.dev1',
    description='convert markdown 2 latex code perfactly,support Chinese Language',
    url='https://github.com/sailist/MarkTex',
    author='hzYang',
    author_email='sailist@outlook.com',
    license='MIT',
    include_package_data = True,
    install_requires = [
      "pylatex",
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='markdown latex convert',
    packages=find_packages(),
    entry_points={
        'console_scripts':[
            'marktex = marktex.marktex:main'
        ]
      },
)
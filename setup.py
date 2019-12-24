from setuptools import setup, find_packages

setup(
    name="masonite-validation",
    packages=[
        'masonite.validation',
        'masonite.validation.commands',
        'masonite.validation.providers',
    ],
    package_dir = {'': 'src'},
    include_package_data=True,
    version='2.2.14',
    install_requires=[
        'masonite-dot'
    ],
    description="Validation Package",
    author="Joseph Mancuso",
    author_email='joe@masoniteproject.com',
    url='https://github.com/MasoniteFramework/masonite',
    keywords=['masonite', 'python web framework', 'python3'],
    license='MIT',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        'Operating System :: OS Independent',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',

        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities'
    ]
)

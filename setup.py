import setuptools

setuptools.setup(
    name = 'saturn',
    version = '0.1.0',
    packages = setuptools.find_packages(),
    entry_points = {
        'console_scripts': [
            'saturn = saturn.cli:main'
        ]
    }
)

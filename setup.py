from setuptools import setup, find_namespace_packages

setup(
    name="hparams",
    version="0.3",
    packages=['hparams', 'hparams.localconfig'],
    include_package_data=True,
    install_requires=['gcsfs'],
    zip_safe=False
)

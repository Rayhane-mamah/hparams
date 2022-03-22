from setuptools import setup, find_namespace_packages

setup(
    name="hparams",
    version="0.1",
    packages=['hparams', 'hparams.localconfig'],
    include_package_data=True,
    zip_safe=False
)

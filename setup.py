from setuptools import setup, find_packages

setup(
    name="huobi_client",
    version="0.3.0",
    description="a client library for huobi",
    author="czheo",
    license="LGPL",
    keywords="bitcoin huobi huobi.com",
    packages=find_packages(),
    scripts=[
        'bin/huobi'
    ],
    install_requires=[
        'requests',
        'six',
        'websocket-client',
    ],
)

from setuptools import setup

setup(
    name="huobi_client",
    version="0.2.0",
    description="a client library for huobi",
    author="czheo",
    license="LGPL",
    keywords="bitcoin huobi huobi.com",
    packages=[
        "huobi_client"
    ],
    scripts=[
        'bin/huobi'
    ],
    install_requires=[
        'requests',
        'six',
        'websocket-client',
    ],
)

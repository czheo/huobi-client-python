from setuptools import setup

setup(
    name="huobi_client",
    version="0.1.0",
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
        'socketIO-client==0.5.7.2',
        'requests',
    ],
)

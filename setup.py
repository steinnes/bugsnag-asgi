import os
from setuptools import setup, find_packages


def get_version():
    __version__ = None
    with open(os.path.join(os.path.dirname(__file__), 'bugsnag_asgi/_version.py')) as version_src:
        namespace = {}
        exec(version_src.read(), namespace)
        __version__ = namespace.get('__version__')
    return __version__


setup(
    name='bugsnag_asgi',
    version=get_version(),
    description='Bugsnag integration for asgi frameworks',
    url='https://github.com/steinnes/bugsnag-asgi',
    author='Steinn Eldjarn Sigurdarson',
    author_email='steinnes@gmail.com',
    keywords=['bugsnag', 'asgi', 'exceptions'],
    install_requires=['bugsnag'],
    packages=find_packages(),
)

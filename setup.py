from distutils.core import setup

setup(
    name='lurker',
    version='0.1',
    packages=['lurker', 'lurker.cache', 'lurker.cache.backends'],
    url='http://www.github.com/emre/lurker',
    license='MIT',
    author='Emre Yilmaz',
    author_email='mail@emreyilmaz.me',
    description='a tiny wrapper for mysqldb',
)

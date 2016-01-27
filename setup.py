from setuptools import setup

setup(
    name='filepusher',
    version='0.1',
    description='Embedded web server for sending large mail attatchments',
    url='http://github.com/thomashn/filepusher',
    author='Thomas Hanssen Nornes',
    author_email='thomas.nornes@gmail.com',
    license='MIT',
    packages=['app'],
    install_requires=['cherrypy'],
    zip_safe=False)

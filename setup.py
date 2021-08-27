from setuptools import setup

setup(
    name='rlrdecoder',
    version='1.0.0',
    description='Python 3 library for decoding Rocket League replays',
    url='https://github.com/Zacks7348/RLRDecoder',
    author='Zackary Schreiner',
    author_email='zacks7348@gmail.com',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Rocket League Replay',
        'License :: MIT  License',
        'Programming Language :: Python :: 3',
    ],
    keywords='Rocket League, replay, decoding',
    package_dir={'': 'rlrdecoder'},
    packages=['rlrdecoder'],
    python_requires='>=3.6',
    install_requires=['bitstring'],
)
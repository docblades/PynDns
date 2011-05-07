from setuptools import setup

setup(name='Pyndns',
      version='0.1.0a',
      description='A Python DynDns update client',
      author='Christian Blades',
      author_email='christian.blades@docblades.com',
      url='http://docblades.com',
      packages=['pyndns'],
      classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Natural Language :: English',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Programming Language :: Python',
        'Operating System :: OS Independent'
        ],
      requires=['BeautifulSoup(>=3.0)', 'dnslib', 'argparse']
      )

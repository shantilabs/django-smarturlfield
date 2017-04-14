from distutils.core import setup


setup(
    name='django-smarturlfield',
    version='1.0.0',
    author='Maxim Oransky',
    author_email='maxim.oransky@gmail.com',
    description="Django model and form fields that performs URL normalization. For example it adds 'http://' prefix and forces punicode encoding.",
    long_description=open('README.rst').read(),
    url='https://github.com/shantilabs/django-smarturlfield',
    packages=[
        'smarturlfield'
    ],
    keywords=[
        'django', 'django-fields', 'url'
    ],
)

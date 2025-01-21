from setuptools import setup, find_packages

setup(
    name="DEV_BLOG",
    version="1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-login',
        'flask-mail',
        'flask-bcrypt',
        'flask-wtf',
        'pymongo',
        'pillow',
        'python-dotenv',
        'gunicorn'
    ]
) 
from setuptools import setup, find_packages
import os

dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

requires = [
    'Pillow',
    'docx2txt'
]

setup(name='handwritten_image',
    version='0.14',
    description='Convert plain text into the handwritten text',
    packages=find_packages(),
    author='Vadim Mukhametgareev',
    author_email='townhor@mail.ru',
    url='https://github.com/xcapt0/handwritten',
    zip_safe=False,
    long_description_content_type='text/markdown',
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
    ],
    keywords='handwrite, handwritten',
    install_requires=requires
)
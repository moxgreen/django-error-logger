from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="django-error-logger",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Django application that logs HTTP 500 errors with detailed context",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/django-error-logger",
    packages=["error_logger", "error_logger.migrations"],
    include_package_data=True,
    package_data={
        "error_logger": [
            "templates/error_logger/*.html",
            "migrations/*.py",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "Django>=3.2",
    ],
    extras_require={
        "impersonation": ["django-su>=1.0.0"],
    },
)

from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()

setup(
    name="surgishop_reports",
    version="0.0.1",
    description="Custom ERPNext reports for Surgishop",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Surgishop",
    author_email="support@surgishop.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        "frappe"
    ]
)

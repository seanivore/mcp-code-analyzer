from setuptools import setup, find_packages

setup(
    name="mcp-code-analyzer",
    version="0.1.0",
    description="A Model Context Protocol server for Python code analysis",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="seanivore",
    url="https://github.com/seanivore/mcp-code-analyzer",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "asyncio",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
    ],
    keywords="mcp, code analysis, static analysis, claude, anthropic",
)
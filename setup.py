from setuptools import find_packages, setup

setup(
    name="acma-dashboard",
    version="0.1.0",
    packages=find_packages(where="app"),
    package_dir={"": "app"},
    install_requires=[
        "streamlit>=1.32.0",
        "plotly>=5.18.0",
        "pandas>=2.2.0",
        "redis>=5.0.1",
        "python-dotenv>=1.0.0",
    ],
    python_requires=">=3.8",
)

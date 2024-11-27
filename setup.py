from setuptools import find_packages, setup

setup(
    name="acma-dashboard",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "streamlit>=1.32.0",
        "plotly>=5.18.0",
        "pandas>=2.2.0",
        "redis>=5.0.1",
        "python-dotenv>=1.0.0",
        "psycopg2-binary>=2.9.9",
    ],
    python_requires=">=3.8",
)

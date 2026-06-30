from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="investment-intelligence-system",
    version="4.0.0",
    author="Investment Intelligence Team",
    author_email="info@iis.ir",
    description="سیستم هوشمند مدیریت سرمایه‌گذاری برای بورس ایران",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/investment-system",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    extras_require={
        "dev": [
            "black==23.11.0",
            "flake8==6.1.0",
            "mypy==1.7.1",
            "isort==5.12.0",
        ],
        "docs": [
            "sphinx==7.2.6",
            "sphinx-rtd-theme==2.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "iis-update=scripts.daily_update:main",
            "iis-retrain=scripts.retrain_model:main",
            "iis-api=uvicorn.src.api.app:app",
        ],
    },
)

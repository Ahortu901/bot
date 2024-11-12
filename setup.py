from setuptools import setup, find_packages

setup(
    name="TradingBot",
    version="0.1.0",
    description="An AI-powered trading bot for crypto/stock market analysis and automated trading",
    author="Your Name",
    author_email="ahortuderrick0@gmail.com",
    packages=find_packages(),
    install_requires=[
        # Data handling and manipulation
        "pandas>=1.1.5",
        "numpy>=1.19.5",
        
        # API requests
        "requests>=2.25.1",
        
        # Visualization
        "matplotlib>=3.3.4",
        "seaborn>=0.11.1",
        
        # Machine learning
        "scikit-learn>=0.24.1",
        
        # Deep learning (optional, if you use it)
        "tensorflow>=2.4.1",  # OR
        "torch>=1.7.1",
        
        # Technical analysis for trading indicators
        "ta-lib>=0.4.0",
        
        # Crypto exchange APIs
        "ccxt>=1.42.5",
        
        # Backtesting library (optional, for backtesting strategies)
        "backtrader>=1.9.76.123",

        # Logging and monitoring (optional)
        "loguru>=0.5.3",

        "forex-python>=1.5",
        "ta-lib>=0.4.0",
        "keras",
        "yfinance",
        "logging",
        "logging",
        
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)

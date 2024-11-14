from setuptools import setup, find_packages

setup(
    name='ForexTradingBot',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'numpy==1.24.0',
        'pandas==1.5.3',
        'matplotlib==3.7.0',
        'scikit-learn==1.2.0',
        'tensorflow==2.13.0',
        'keras==2.13.0',
        'requests==2.28.1',
        'aiohttp==3.8.1',
        'joblib',
        'ta-lib'
    ],
    author='Ahortu Derrick',
    description='A deep learning-based Forex trading bot with backtesting and risk management.',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],

)
print ("[+] Installation done")

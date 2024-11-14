from setuptools import setup, find_packages

setup(
    name="AITradingBot",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'tensorflow==2.14.0',
        'numpy==1.24.2',
        'pandas==2.1.0',
        'matplotlib==3.7.1',
        'requests==2.31.0',
        'scikit-learn==1.3.0',
        'ta-lib==0.4.0',
    ],
    entry_points={
        'console_scripts': [
            'start-bot=main:run_bot',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)



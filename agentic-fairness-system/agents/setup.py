from setuptools import setup, find_packages

setup(
    name="agentic-fairness-agents",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.104.1",
        "uvicorn==0.24.0",
        "kafka-python==2.0.2",
        "pandas==2.1.3",
        "numpy==1.24.3",
        "scipy==1.11.4",
        "aif360==0.5.0",
    ],
    entry_points={
        "console_scripts": [
            "agent-bias-detection=agent_1_bias_detection.main:app",
        ],
    },
)

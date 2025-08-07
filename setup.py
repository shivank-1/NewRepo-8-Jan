from setuptools import setup, find_packages

setup(
    name="ai-calling-agent-rupeeq",
    version="1.0.0",
    description="Agentic AI Solution for Financial Services Customer Calling",
    author="Shivank",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "livekit-agents>=1.2.3",
        "livekit-plugins-openai>=0.6.0",
        "livekit-plugins-elevenlabs>=0.5.0",
        "livekit-plugins-deepgram>=0.6.0",
        "livekit-plugins-silero>=0.5.0",
        "python-dotenv>=1.0.0",
        "aiohttp>=3.8.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial Services",
        "Programming Language :: Python :: 3.8",
        "Topic :: Communications :: Telephony",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
from setuptools import setup

setup(
    name="connectboxcontrol",
    version="1.0.0",
    description="Turn the WiFi of your Connect Box router on/off",
    packages=['connectboxcontrol'],
    include_package_data=True,
    install_requires=['flask', 'gunicorn', 'pycryptodome', 'requests']
)

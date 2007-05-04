from setuptools import setup, find_packages

setup(
    name="666 Luftballons",
    version="1.0",
    description="Puzzle/action game in which you try to stomp devils in "
                "balloons.",
    author="Thijs Jonkman & Jeroen Vloothuis",
    packages=find_packages(),
    install_requires=[
       'setuptools',
       'Pygame',
    ],
    entry_points={
        'console_scripts': [
            '666luftballons = 666luftballons.main:main',
        ]
    },
)

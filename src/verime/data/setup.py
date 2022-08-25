
from setuptools import Extension, setup, find_packages

print(find_packages())
setup(
        name = "$package",
        version = "0.1",
        packages=find_packages(),
        ext_modules=[
            Extension(
                name="$package.simu",
                sources=["pymod.cpp"],
                extra_objects=["simu.a"],
                ),
            ]
)


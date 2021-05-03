import setuptools

setuptools.setup(
    name="streamlit-text-label",
    version="0.0.1",
    author="Basis AI",
    author_email="developers@basis-ai.com",
    description="Components for labelling text document",
    long_description="",
    long_description_content_type="text/plain",
    url="https://github.com/basisai/streamlit-text-label",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.6",
    install_requires=[
        # By definition, a Custom Component depends on Streamlit.
        # If your component has other Python dependencies, list
        # them here.
        "streamlit >= 0.63",
    ],
)

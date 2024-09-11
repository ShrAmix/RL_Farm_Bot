from cx_Freeze import setup, Executable

setup(
    name="YourApp",
    version="0.1",
    description="Description of your app",
    executables=[Executable("main.py")]
)

from cx_Freeze import setup, Executable

build_exe_options = {
    "optimize":2
}

target=Executable(
    script="server.py",
    icon="discord.ico"
)

# On appelle la fonction setup
setup(
    name = "dicsord server",
    version = "1",
    description = "Votre programme",
    options={"build_exe": build_exe_options},
    executables = [target],
)

#build an .exe by running the "python setup.py build" command in local powershell
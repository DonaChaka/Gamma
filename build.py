import subprocess
import sys
import os

"""
Final executable in dist directory.

 We can use UPX, a powerful executable packer, to compress the executable file. It can significantly reduce the file size.

Install UPX: You can download UPX from here
, and make sure it's installed.

Use the --upx-dir Flag: After installing UPX, you can tell PyInstaller to use it during the build process to compress the final executable:

--upx-dir="path_to_upx"  # Provide path to the UPX folder

"""

# Path to the Python script you want to convert into an executable
script_name = "main.py"
executable_name = "Gamma"

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(current_dir, "build")
dist_dir = os.path.join(current_dir, "dist")
icon_path = os.path.join(current_dir, "icons", "gamma.ico")
templates_path = os.path.join(current_dir, "gui", "flask_ui", "templates")
static_path = os.path.join(current_dir, "gui", "flask_ui", "static")

spec_path = build_dir

# Ensure the build and dist folder exists
if not os.path.exists(build_dir):
    os.makedirs(build_dir)

if not os.path.exists(dist_dir):
    os.makedirs(dist_dir)

# PyInstaller command to convert the Python script into an executable
# -F: Bundle everything into a single executable
# -w: Disable the terminal window (use -c for console apps)
command = [
    "pyinstaller",
    "--onefile",
    "--distpath", dist_dir,
    "--workpath", build_dir,
    "--specpath", spec_path,
    "--name", executable_name,
    "--windowed",
    "--strip",
    "--icon", icon_path,
    "--add-data", f"{templates_path};gui/flask_ui/templates",
    "--add-data", f"{static_path};gui/flask_ui/static",
    script_name
]


# Run the PyInstaller command
try:
    subprocess.run(command, check=True)
    print(f"Executable created successfully in '{build_dir}' folder.")
except subprocess.CalledProcessError as e:
    print(f"Error during PyInstaller execution: {e}")
    sys.exit(1)

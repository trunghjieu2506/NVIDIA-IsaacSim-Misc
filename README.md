# NVIDIA-IsaacSim-Misc
Collection of scripts and notes when running Isaac Sim on the cloud

## pythonscript.py
This is an example of a standalone Python Script to run Iteractive Scripting on Visual Studio Code with Nvidia Isaac Sim. This script spawns a Franka Manipulator to conduct pick and place action. It is important to note that this implementation of Nivida Isaac Sim library in standalone python script is different from the documentation example. 

Asynchronous workflow is essential for the standalone script to work. 

## Import External Packages 
To import external packages, for example openai package, you need to run the script on the Nvidia Isaac Sim built-in Python Editor. Download it from Visual Studio Code does not work.
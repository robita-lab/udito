# UDITO - a Social Robotics Platform for HRI Researching (UNDER CONSTRUCTION)
This repository includes the development of robotic skills for HRI research.




## Found Issues

- 10/03/2025 - ERROR: "No module named 'em'" al hacer colcon build --packages-select tutorial_interfaces
Solution: https://robotics.stackexchange.com/questions/79663/python-module-empy-missing-tutorials
pip uninstall em
pip install empy

O tambien:
pip uninstall em
pip install empy==3.3.4

- ERROR: "No module named catkin_pkg"
pip install catkin_pkg lark

- 11/03/2025 - Errores varios debido a utilizar ROS con Python3.9.
A traves de chatGPT se borra esta versión de Python y se compila todo en 3.10.12
Algunas cosas que se hicieron:
Borrar los enlaces simbólidos de python y rehacerlos:

sudo ln -sf /usr/bin/python3.10 /usr/bin/python
sudo ln -sf /usr/bin/python3.10 /usr/bin/python3

Comprobar versiones

which python
which python3
ls -l /usr/bin/python*

python --version
python3 --version
python3 -c "import sys; print(sys.executable)"

Gestionar las alternativas:
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.10 2
sudo update-alternatives --set python /usr/bin/python3.10
sudo update-alternatives --config python

Compilar poniendo explícitamente 
colcon build --symlink-install --cmake-args -DPYTHON_EXECUTABLE=/usr/bin/python3.10
pip install catkin_pkg lark

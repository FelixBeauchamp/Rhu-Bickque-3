# Rhu-Bickque-3
Projet S4 de la meilleure équipe

After importing this code in your IDE it is important to add some libraries. We used PyCharm for this project, so the explanation will be based on that IDE.

### Import Packages ###

There are two ways to import the packages on PyCharm. The first one is through the requirements.txt file:

1. When you open requirements.txt or a Python file on a project that contains requirements.txt, PyCharm checks whether all the packages specified in requirements.txt are installed for the current Python interpreter.

2. Notification on the requirements
If any packages are missing, a notification bar is displayed at the top of the editor. Click Install requirements.

The other method is to do it manuallly like so:

  The libraries that have to be included are :
  
    numpy
    
    opencv-python
    
    dynamixel-sdk
    
    Adafruit-PCA9865
    
  
  To add those Packages on Pycharm, go to Settings-> Project:NameofProject-> Python Interpreter-> click the + symbole (Install)->search for the Package to add-> Select it-> Install Package
  
  Do those steps for each package, then the project is ready to go and it will build and execute.

Those libraries will be in the External Libraries-> site-packages

There the documentation on each librairy and funciton will be available.


### Use Pycharm as ArduinoIDE ###

The link explains very well how to set up PyCharm to use .ino files :
https://samclane.dev/Pycharm-Arduino/#:~:text=This%20can%20be%20accomplished%20through,done%20this%20correctly%2C%20then%20your%20.


### Main ###
The code is pretty much plug and play. Once all the connection are made, it is only neccesary to change the ports for the Arduino, Open-Rb and camera in the main depending on the computer used to solve the cube.


### 3-D model and assembly of the Rhu-Bickque-3 ###

To print and change the design of the Rhu-Bickque-3, the Modélisation directory contains all the neccessary information to do so.




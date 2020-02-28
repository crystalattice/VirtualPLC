# VirtualPLC
Emulated PLC equipment for virtual systems

Simulates a liquid storage and transfer system. Utilizes real-world physics modeling for things like valve pressure drop, pump laws, liquid viscosity, etc.

To run HMI graphical interface, change hmilayout.py to have correct path of VirtualPLC directory (line 2). Then run "python <path>/hmi/hmilayout.py". 
You should see a schematic with blue buttons. Clicking the buttons open/closes valves and turns pumps on or off. 
Dragging the right side of the screen to the left opens the table. Click the button to populate the table with system parameters; reclick every time changes are made to the schematic.

Python Experiment: Mayan Doom 

(Rendering, Raycasting, QT UI with Maya)



[Warnings] Make sure you are in a blank scene as this will erase other existing objects in the scene upon startup


Demonstration: https://youtu.be/1MBP1x0osU4?si=VkE39Q1Pa7fwQjw6


Requirements:

-If Qt is not installed in your mayapy env, you will need to install it first in order to use this ("PathToMayaFolder\bin\mayapy.exe" -m pip install Qt.py==1.3.6)
-In MayanDoom_01.py you'll need to change the file path variable to the location you placed this programs folder here:
dirpathstr = r'\path_to_folder\RayCaster_A'



Project Desicription:

This project is a Python experiment I had a lot of fun with. My goal was that I challenged myself to use my general knowledge of Python, my tool creation with QT UIs, Maya CMDS, and old fashioned game rendering math techniques to see if it is indeed possible to shoehorn an entire video game into Maya. Now it would seem that its totally possible, despite the fact its an incredibly inefficient way of running games due to the large overhead of having to run Maya, in order to run Python, in order to run (wrapped) MEL, in order to create and interact with 3D objects in a Maya scene... But thats besides the point of why I started this.
It was a bit of complex project trying to think of everything I needed to make a smooth experience, and keep everythign as modular as possible by moving all callable actions into custom methods within the class. It certainly helped down the road when I had to switch around the order of certain operations, as all these complex repeatable tasks had been abstracted. This project is a demonstration of my knowledge of Python tool creation and integration with Maya, as well as my knowledge of QT UI creation, Maya API interaction, and a little bit of creativity! 
I hope this has answered a question you possibly may have never asked, "Can Maya run (Mayan)Doom?". Well now you know!



Instructions:

Once you have all the files in a folder and the directory path variable has been changed to match, run the script and a UI should pop up.

The UI has 6 basic movement controls, forward/backward./left/right/turn left/turn right.
There are 3 Menu buttons, start/interact/reset, 1 spinner for FOV limit, and 2 additional spinners for distance shading tweaks

->Start: Initalize the game
->Interact: Interact with green doors to proceed to the next level.
->Reset: Resets the game to the current levels start position, also used for enacting FOV changes.
->FOV: Field of View (FOV) will determine the amount of scanlines to render, each scanline = 1 degree of vision, higher FOV. will be slower to render but provide better visual presence. (You should run this upon startup)
->Additional Spinners, these 2 ont he top right will adjust the distance shading, see what you like most.


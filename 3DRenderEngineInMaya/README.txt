Python Experiment: 3D Render Engine

(Rendering, Raycasting, QT UI with Maya)



[Warnings] Make sure you are in a blank scene as this will erase other existing objects in the scene upon starting the tool's setup



Requirements:

-If Qt is not installed in your mayapy env, you will need to install it first in order to use this ("PathToMayaFolder\bin\mayapy.exe" -m pip install Qt.py==1.3.6)
-In 3DRenderEngineTool.py you'll need to change the file path variable to the location you placed this programs folder here:
dirpathstr = r'\path_to_folder\3DRenderEngineInMaya'



Project Desicription:

This project is an experiment in Python that originally started off outside of Maya as a learning exercise for exploring how 3D rendering works. The first iterations were using a simple graph module to give me some basic visualization ability, in this case it was MatPlotLib. It worked for what I needed at the time, eventually I saw the limitations and oddities of MatPlotLib, and decided to try another relatively light one, GASP. GASP worked much better, I went on to incrementally upgrade the render engine, once it got vertices looking nice, I tried edges, once edges were working I ventured into rasterization. Which is where I hit a roadblock. I eventually got face rasterization working, however GASP would noticiably slow down when the faces started to encompass a lot of on-screen pixel space. In the future I intend to work on this in something more apt, like PyGame or even OpenGL to allow for more performance.
I wanted to run this in Maya simply to see if it can be done, and of course it can. Anywhere you can access a 2D array of 'pixel' like objects, and have a Python API, theres potential to make a screen and therefore render ojects on it. Running this in Maya has a significant overhead toll, so I left this as just vertex projection for a proof of concept. Although I'm dedicated to building this from scratch and all the math/functions that are needed, it would be notably more tedious in Maya, since if you are interacting with abritary objects as 'pixels' theres no such functions as "clear screen". The "screen doesn really exist, meaning you have to keep track of every pixel and its address in this non-visual array in the code. Its fascinating to me how I can render shapes with just a bunch numbers in Python, because thats all it really is at the end of the day.
Hope you enjoy seeing this proof of concept.


Instructions:

Once you have all the files in a folder and the directory path variable has been changed to match, run the script and a UI should pop up.

The tool's UI has a number of buttons. the right side displays directional controls for the object that tool is currently storing and rendering, a cube by default.
The buttons on the left side are used for setup and rendering changes

Left Side:

->Copy Points: Select an object in the viewport and click this to make the tool copy those vertices for rendering (object needs to be at origin, the obejcts scale and position being off centre may cause problems)
->Screen Setup: Click this to start the initalize the 20x20 cube pixel screen
->Draw: Draws the tool's currently stored object onto the screen (by default, a cube)
->Reset: Clears all drawn pixels on the pixel screen
->Run Animation: Runs a short rotation animation on the currently stored object

Right Side:
->Position: Thin arrow buttons at the tips of each XYZ axis
->Rotation: Circular arrow buttons under the tips of each XYZ axis
->Scale: Wide Up/Down arrows buttons a bit left of the XYZ axis

Note: Objects with more pixels will cause slower render performance, depending on your computer specs.

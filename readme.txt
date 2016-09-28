

Mirra
2D OpenGL graphics Python framework by www.ixi-software.net
version alpha 0.4b - Sept 2016.


*** NOTICE *** 
This library is not under active development. We update it every now and then to fulfill our needs.

 

Description:

Mirra is a 2D OpenGL graphics library based on Python. Mirra allows for the creation of 2D interfaces, games or applications. It defines a set of classes to render primitive shapes (Text, Pixel, Line, Circle, Rect, Bitmap, BitmapPolygon), it manages rendering and user input (mouse and keyboard). Mirra focuses on interaction and implements an event managing system and classes that capture mouse events (in a way like Macromedia Director or Flash do).

Mirra can send and receive OpenSoundControl messages via the OSC module (altought this scripts are based on a pretty old implementation of OPSC for Python)

Mirra uses PyOPenGL and PyQT

 

License :

This library is free software; you can redistribute it and/or modify it under the terms of the Lesser GNU, Lesser General Public License as published by the Free Software Foundation.

This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more details.
You should have received a copy of the GNU Lesser General Public License along with this library; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

Mirra contains small parts by others such as OSC.py by Daniel Holth under Lesser GPL. Licence and credits are included on those parts from others.

 

System requirements:

Python - www.python.org
PyOpenGL - pyopengl.sourceforge.net
PyQT

(*) Under some versions of Windows you might need to install as well GLUT32.dll to get OpenGL running. This can be downloaded from http://www.xmission.com/%7Enate/glut.html . Just copy the glut32.dll into your c:\windows\system32 folder



 

Installation

Uncompress the zip cd to the mirra folder and on the terminal type : 'python setup.py install'. Windows users can use the exe installer provided.

 

Changes:

0.4b : 
- Complete removed Pygame and WxPython in favor of PyQT. This means that some old features are drop. Sound functionality is removed (better use Pyo library)

0.3.5 :
- Engine class from graphics.py converted to module engine.py with functions this allows to avoid having to pass the reference to engine on each render. Drawing functions are now accesed by importing engine. (First step towards moving this part of code into C)
- removed visible property

0.3.2 :
- killMe() renamed to end()
- implement properties for the Base class like rect or quad that update on the fly when you change location, etc...
- added preferences system (check example provided)
- removed pygame from main,py and events.py this disables self.env and should slightly improve performance on event handling
- added end() function to App

0.3.1 :
- fullscreen overwrites pos and size properties to fit display's size
- added self.width and self.height to main app. they return same as self.size[0] and self.size[1]
- fixed data folder problem on export.py for windows. need to be checked yet on mac

0.3 :
- (finally!) Fixed basic integration with wxPython
- fixed error in some linux system with sound from externals sound engines colliding with pygame audio. From now on audio needs to be initalised manually with self.initAudio()
- tested ChucK and SuperCollider as external sound engines.
- fixed mayor errors with wxpython
- fixed export.py module errors under windows
- added startup preferences system. Check example 16 and prefs.txt files

0.2.8.2 (Piksel):
- added rect class as property of graphical objects. This allows to have x,y,loc properties connected to a rect left,top,right,bottom, quad properties.
- trying experimental 3D mode
- added draw styles to Circles, Arcs, Lines, Rects and Polygons
- changes on rendering stack system
- added Arc drawing primitive class
- added end() method to primitive classes
- massive changes on render engine to optimise performance: reduced amount of code executed on the render loop, optimised loops, optimised drawing methods
- improving documentation files to include a better API description
- improving documentation and comments on the code

0.2.8.1 :
- fixed errors on setup.py installer script, exe installer provided for windows users - fixed bugs on Bitmap instances when calling tile() and setImage() - Implemented support for images with transparencies - graphics.py cleaned, there where some old lines of code not used anymore.

0.2.8 :
- Using py2exe / py2app now it can easily be created self executables (mac and win, linux users dont need this) non dependent from Python interpreter or library dependencies. Check 15export.py example.
- added mouseVisible property to App. self.mouseVisible = 0 will hide the mouse (but itwill keep active!)
- end() happends now just before quiting pygame and not after
- Bitmap and tmapPolygon images can be changed on the fly with setImage(pathtoimage) method, check examples related to textures
- several changes to optimise performance
- more extendingclasses examples added
- modified opengl setup suggested by tom betts to get rid of unnecesary coordinate and angle translations.
- finally fixed wx problems with refresh thanks to tip from robin dunn. Currently reconstructing wx support and creating examples. gui.py added back.
- fixed bug on mouse click that caused some mouse clicks not to be recognised properly.
- top app's mouseLoc implemented as a python property on pygame
- small changes on events.py to add mouseLoc to wx

0.2.7 :
- added pong.py to examples
- changed resources importing method to allow mirra to work as a proper python library
- added start method to Base class to avoid having to extend __init__ always when extending bult-in classes
- solved bug with start() on main.App class - added more examples

0.2.6.1 :
- changed tabs to spaces in all files to avoid problems in some editors.
- bug fixed, property blend was not active.
- bug fixed, killMe() method was not working properly. Thanks to Dan Law.
- bug fixed, instances where added twice to rendering stack because of new z property system. Thanks to Dan Law.
- bug fixed, setting the loc now work on Line class. Thanks to Dan Law.

0.2.6 :
- removed setters and getters for a more pythonic Mirra. This causes mayor changes on the API, check 'Short tutorial' section for more details.
- added visible property to all shapes
- small optimisation changes and code clean up
- license changed to LGPL to allow for commercial use of Mirra

0.2.5.7 :
- wxPython frames (with menus, status bars etc..) can be defined in a custom module. Before it was hard wired (just for testing) inside the mirra package. Check example6wxPython.py for usage
- render stack performance improved. Before it was a bidimensional array a 'bucket' for each Z depth(and they where 1000!), every time it rendered it had to go through each bucket rendering its shapes. Now it is one dimensional array where objects are shorted depending on their Z when created. The work is done on creation time and not every time it renders! . We are tying to improve...
- small changes to improve performance here and there ...
- joystick support added (only under pygame at the moment). Example provided.
- added keyUp() event to event manager. Modified KeyDown() now it only receives an argument with the pressed key code. (many thanks to Peter Goode for pointing this out)
- added render() method to MirraApp. This feature has been added just for completenes, it is handy to test drawing methods. Check example11directdrawing.py
- added end() method to MirraApp. It is called just before the application is closed. Good place to kill processes, write preferences to disk, etc...

0.2.5.6 :
- added basic audio functionality using pygame (to be extended and improved over next releases).
- fixed bug on setColor(). Alpha was default to 0 instead of 1 causing shapes to disapear if no alpha was passed.
- fixed bug on intersection with rotated Rects.
- hard-coded wxPython dependency removed and coded proper system exits if PyOpenGL or Pygame are not found.
- improved documentation and examples
- circles diameter argument is now called width.

0.2.5.5 :
- GLUT dropped in favor of Pygame. This way dependency from PIL library has been removed.
- support for more image file types added thanks to pygame
- mayor changes on graphics.py module to make class structure more clear and simple trying to avoid using multiple inheritance too much.
- added constrain to dragged shapes --> self.setConstrainRect(left, top, right, bottom). To reset do self.setConstrainRect(0,0,0,0)
- All shapes have now (inherited from Base) a built it self.getMouseLoc() method
- Base class keeps now a reference to the main App instance so that all objects inheriting from Base can comunicate back. This makes for example the access to mouseLoc more easy and clear to implement. Because main App knows about the mouseLoc it can be asked for its value using that reference. A class called Test could do Test.app.getMouseLoc() and would get a tupple containing x and y of current mouseloc. The previous system was more obscure than this one.

0.2.5.4 :
- bug fixed : eventhandler instance didnt receive the MirraApp instance so it couldnt pass back events to it.
- small changes in documentation and examples
- added to MirraApp class a method to access the mouse location --> getMouseLoc()

0.2.5 :
- optimised bitmap handling system (images are stored as static property of graphics engine class)
- WxPython and Pygame support added.
- new examples added and documentation improved
- small changes on rendering method to improve performance and some z location errors.
- bug fixed : when shape.setInteractiveState(1) and draggged there was a weird behavior
- Text class implements now setText(string) and getText()
- Text class implements default GLUT fonts
- Rects have now height and width allowing to create rectangles as well as squares
- small changes and cleanup on utilities.py module
- Base object implents :
self.mouseLoc --> gives access to mouse location
self.blend = float --> sets alpha component of instance's color
self.blend --> returns alpha component of instance's color

0.2.2 : solved flickering when two shapes are in the same z location
0.2.1 : solved bug with flipH() and flipV() in Rects

 


 

Contents of Mirra:

> /examples
mirratemplate.py --> Application example
+ other examples ...
> /mirra package folder:
main.py --> main application class
graphics.py --> main drawing classes and graphicsStack instance
events.py --> event handling classes
utilities.py --> a handy bunch of functions (collisions, random nums and colors, rotations, some triginometry and maths) and utility classes such as the Stack class.
> /mirra/OSC package folder: (this is a pretty old implementation)
OSC.py --> Open Sound Control library by daniel Holth
oscAPI.py --> simple interface to OSC.py by ixi

 

Aknowledgements :

Currently Mirra is made thanks to the support and help of:
- The Digital Research Unit / Center for Excelence on Digital Design at the University of Huddersfield. http://www.druh.co.uk
- Goto10 collective www.goto10.org

Some parts of the development of Mirra were developed with the support from different institutions :
- The Digital Research Unit at the University of Huddersfield. http://www.druh.co.uk
- The Lansdown Center for Electronic Arts at Middlesex University who helped providing expertise and support for developing the early versions of Mirra. http://www.cea.mdx.ac.uk/
- Bizkaiko Diputazioa, Basque Country.
- Buchsenhausen Kunstlerhaus, Innsbruck, Austria.

Tom Schoulten, John Cox, Daniel Holth and Tom Betts for the technical help.


Feedback:

We would more than happy to hear your comments, suggestions or to incorporte any improvement you might do to our code. Contact us on www.ixi-software.net 
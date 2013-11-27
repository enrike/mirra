#!/usr/bin/env python

# please report errors to info@ixi-audio.net
# to install :
# python setup.py install

# create a distribution :
# python setup.py sdist

#create win exe installer :
# python setup.py bdist_wininst




from distutils.core import setup

import os, sys


try: # check
    import wx
except ImportError:
    print "some features of mirra use wxPython library, you might want to install it"

if sys.platform == 'win32' : # windows
    try :
        import py2exe
    except ImportError:
        print 'no py2exe installed in your system, you wont be able to export mirra scripts'
elif sys.platform == 'darwin': # OSX
    try :
        import py2app as whatever # just try
    except ImportError:
        print 'no py2app installed in your system, you wont be able to export mirra scripts'

try: # check
    import OpenGL
    import pygame
except ImportError:
    print "instalation error : you MUST have both pygame and pyOpenGL installed to run mirra"
    raise sys.exit() # do not do it






setup(name = 'Mirra',
    version = '0.3.5',
    description = '2D interaction focused OpenGL graphics library',
    license = 'LGPL',
    author = 'ixi software',
    author_email = 'info@ixi-audio.net',
    url = 'http://www.ixi-audio.net/mirra',

    packages = ['mirra', 'mirra.osc'],
    data_files = [ ]
)





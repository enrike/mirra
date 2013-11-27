#!/usr/bin/env python


##########################################################
main_file_name = '' # main file
packages = [] # any packages you might have created
icon_path = '' # on mac the icon file type is .icns on win is .ico
extra_files = []
##
##
### extra files & folders you might want to include
### ** by default this script takes anything included in a folder called 'data' in the
### ** applications folder so you dont really need to use this
### the format is -> str destination folder name , list with str relative path to files
## extra_files = [
####    ("", []), # "" means root dir, the one where main_file_name lives
####    ("data", ["data/slicer_pd.pd",
####        "data/sampler.pd",
####        "data/flower2.wav"]
####    )
##] # end extra_files
############################################################################




import os, sys, shutil
from distutils.core import setup

##import sys,os, string
##from distutils.sysconfig import *
##from distutils.core import setup,Extension
##from distutils.command.build_ext import build_ext
##from distutils.command.install import install
##from distutils.command.install_data import install_data
	

# if os.name == 'nt' : # windows
if sys.platform == 'win32':
    try :
        import py2exe
    except ImportError:
        print 'no py2app installed in your system'
elif sys.platform == 'darwin':
    try :
        import py2app as ppp
    except ImportError:
        print 'no py2app installed in your system'






def pack( mainFile='', extraPackages=[], extraFiles=[], iconPath='', winconsole=0 ) : 
    """ to run this module from within python
    """
    if sys.platform != 'win32' :
        if os.uname()[0] == 'Linux' :
            print 'no need to pack on Linux'
            return # OFF
##        elif os.uname()[0] == 'Darwin' :
##            os.chdir(os.path.dirname(mainFile)) # change to current file directory on mac
    
        
    import utilities
    if utilities.run_as_app() : return # running as exe > escape!
    
    global main_file_name, packages, icon_path # declare them!!
    main_file_name = mainFile # get users input into globals
    packages = extraPackages
    icon_path = iconPath
    extra_files = extraFiles
    packit(winconsole) # do it now!



def recursive_copy(src='', dst='', foldBlackList=(),extBlackList=()):
    """ copies tree excluding blacklisted extension files and folders
    """
    if os.path.isdir(dst) :
        shutil.rmtree(dst) # just try get rid of the old version
    for root, dirs, files in os.walk(src):
        if not len([ i for i in root.split(os.sep) if i in foldBlackList ]):
            rel = root.replace(src, '', 1) # get the relative path from dst folder downwards
            if not os.path.isdir(dst + os.sep + rel): # only if not there already
                os.mkdir(dst + os.sep + rel)
            for i in files:
                if not len([ i for j in extBlackList if i.endswith(j) ]):
                    shutil.copyfile(root + os.sep + i, dst + os.sep + rel + os.sep + i)



def proofcheck(dic):
    # now check for errors in user files
    if not os.path.isfile(main_file_name) : 
        print 'error : main file %s does not seem to exist' % main_file_name
        raise sys.exit() # OFF

    if len(icon_path) == 0 or not os.path.isfile(icon_path) :
        print 'error : icon %s does not seem to exist' % icon_path
        if sys.platform == 'win32':
            dic[0].pop('icon_resources') # this is why we do this after declaring windows
        else :
            try :
                dic['py2app'].pop('iconfile')
            except KeyError:
                print 'no icon specified'
    print ".. done checking user's files .........."

    return dic




def packit( winconsole=0 ):
    global main_file_name, packages, icon_path, extra_files

    print '** exporting process started **'

    # If run without args (doubleclick on win), build executable in quiet mode.
    if len(sys.argv) == 1:
        if sys.platform == 'win32':
            sys.argv.append("py2exe")
            sys.argv.append("--excludes=OpenGL") # avoid error from opengl on win
            sys.argv.append("--includes=ctypes,ctypes.util,weakref,new,distutils.util,logging") # avoid error from opengl on win
        elif sys.platform == 'darwin':
            sys.argv.append("py2app")
            sys.argv.append("--no-strip")

        sys.argv.append("-q") # for both plats

    # in case they havent been declared #
    try :
        main_file_name
    except NameError :
        print 'you did not specifly any main file in first argument for export.pack()'
        raise sys.exit() # off

    try :
        packages
    except NameError :
        packages = [] # any packages you might have created

    try :
        icon_path
    except NameError :
        icon_path = ''

    try :
        extra_files
    except NameError :
        extra_files = [] 

    ###################################

    # get all files and folders in subfolder 'data' and put it on the data list.
    for c, d, f in os.walk('data'):
        rel = c.replace(os.getcwd(), '', 1) # get the relative path
        if not '.svn' in rel : # in case there are hidden svn folders
            for n in range(len(f)):
                f[n] = os.path.join(rel, f[n]) # make up new tupple ('data', ['fe.wav','as.pd'])
            extra_files.append((rel, f)) #

    # checking validity for all files in extra_files
    for sub in extra_files :
##        if len(sub[1]) > 0 : # files specified
        if len(sub) > 0 : # files specified
            for res in sub[1]:
                if not os.path.isfile(res) :
                    i = extra_files.index(sub)
                    z = extra_files[i][1].index(res)
                    extra_files[i][1].pop(z) # remove invalid file addresses
                    print 'invalid path %s especified, ignoring'%res
        else :
            extra_files.pop(sub) # remove empty dirs
            print 'empty directory %s especified, ignoring'%res

    # make sure mirra is included
    if not 'mirra' in packages : packages.append('mirra')


    
    ## WINDOWS ###################
    if sys.platform == 'win32': # details for windows exe
        windows = [ dict(
            script = main_file_name,
            packages = packages,
            icon_resources = [(1, icon_path)], # id_num, file
            )
        ]

        windows = proofcheck(windows)

        # main options
        options =  dict( py2exe = dict(
            compressed = 1,
            optimize = 2,
            bundle_files = 1, # added new
            )
        )
        # running setup
        if winconsole :
            setup(
                options = options,
                console = windows,
                zipfile =  r"lib\shardlib.zip", # This dir contains everything except the executables and the python dll.
                data_files = extra_files # resources -> str folder name , list str relative_path_to_files
            )
        else : 
            setup(
                options = options,
                windows = windows,
                zipfile =  r"lib\shardlib.zip", # This dir contains everything except the executables and the python dll.
                data_files = extra_files # resources -> str folder name , list str relative_path_to_files
            )
##########
        # copy glut32.dll and site-packages\OpenGL manually
        dist = os.path.join(os.getcwd(), 'dist') # destination
        
        pathtopengl = os.path.join(sys.exec_prefix, 'Lib\site-packages\OpenGL') # get python folder plus sitepackages

        # now manually copy /site-packages/OpenGL to /dist folder
        try :
            assert(os.path.isdir(pathtopengl)), 'could not find Python\Lib\site-packages\OpenGL directory'
            print '\n' ; print 'copying OpenGL folder to dist, this might take some time ...'
            recursive_copy(pathtopengl, os.path.join(dist, 'OpenGL'),
                ('Demo', 'doc', 'Tk', 'WGL', 'scripts'), ('.pyo', '.pyc'))
        except : 
            print 'error : could not find Python\Lib\site-packages\OpenGL directory, trying to find the egg...'
            packsfolder = os.path.join(sys.exec_prefix, 'Lib\site-packages' )
            print 'you must manually copy the PyOpenGL and setuptools eggs to dis/lib and insert then into the path in your script ...'
            # here i need to find the .eggs for PyOpenGL and setuptools
            # and copy them into the /Lib folder
##            for c, d, f in os.walk( packsfolder ):
##                print f
##                if 'PyOpenGL' in f or 'setuptools' in f :
##                    print 'copying', f 
##                    shutil.copy('c:\windows\system32\glut32.dll', os.path.join(dist, 'lib'))
##                    print f            

        # now glut32.dll as well from c:\windows\system32\glut32.dll to /dist
        assert(os.path.isfile('c:\windows\system32\glut32.dll')), 'could not find glut32.dll in your windows\system32 directory, check mirra documentation'
        shutil.copy('c:\windows\system32\glut32.dll', dist) # copy glut32.dll

    ### MAC ######################
    elif sys.platform == 'darwin':
        print 'deleting previous dist ...'
        try :
            shutil.rmtree(os.path.join(os.getcwd(), 'dist'))
        except :
            print 'no previous dist to delete'
    ##  files.append(('../Frameworks', ['/usr/local/lib/libwx_mac-2.4.0.rsrc'])) # for wx

        options = dict( py2app = dict(
            # includes = 'blah.py' # modules to include
            packages = packages,
        ##          # This is a shortcut that will place MyApplication.icns
        ##          # in the Contents/Resources folder of the application bundle,
        ##          # and make sure the CFBundleIcon plist key is set appropriately.
            iconfile = icon_path,
            resources = extra_files,
            argv_emulation = 1, # do i need this?
        ))

        options = proofcheck(options)

        # running setup
        setup(
            # details for app
            app = [ main_file_name ],
            setup_requires=["py2app"],
            options = options
        ) # end setup



    # FOR both mac and win now :

    # now delete build dir for all platforms
    print 'deleting build dir'
    shutil.rmtree(os.path.join(os.getcwd(), 'build')) # just get rid of the old version

    print '\n'; print 'Looks like everyting went right so you should have your app in the dist folder'#%os.path.basename(main_file_name)
    print 'Do you want to quit this console or continue launching %s?' % os.path.basename(main_file_name)
    a = raw_input("yes or no to quit? : ")
    if a == 'yes' or a == 'y':
        raise sys.exit() # off

    

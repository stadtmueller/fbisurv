#! /usr/bin/python3

import os
import time
import hashlib
import subprocess

class Instance( object ):
    def __init__( self,  filename ):
        self.filename = filename
        self.instance = None
        self.firstStart = True
        
    def setFilename( self,  filename ):
        self.filename = filename
        
    def start( self ):
        realname = os.path.realpath( self.filename )

        while not self.firstStart:
            sum1 = md5( realname )
            time.sleep( 0.1 )
            sum2 = md5( realname )

            if sum1 == sum2:
                break

        self.instance = subprocess.Popen( [ "fbi", "-a", "-T", "1", realname ] )
        self.firstStart = False
        
    def stop( self ):
        self.instance.terminate()
        # Remove following line if program doesnt start twice( fckng fbi! )
        os.system( "killall fbi" )
        
    def restart( self ):
        self.stop()
        self.start()

def md5( filename ):
    gen = hashlib.md5()
    with open( filename, "rb" ) as f:
        for chunk in iter( lambda: f.read( 4096 ), b"" ):
            gen.update( chunk )
    return gen.hexdigest()

def listFiles():
    retFiles = []

    for root, dirs, files in os.walk( "/home/pi/FTP/" ):
        for filename in files:
            if filename != "mesg.txt":
                retFiles.append( os.path.join( root, filename ) )

    retFiles.sort()
    return retFiles

files = listFiles()
oldCount = len( files )

ins = Instance( files[ -1 ] )
ins.start()

try:
    while True:
        files = listFiles()
        newCount = len( files )
        
        if oldCount < newCount:
            oldCount = newCount
            ins.setFilename( files[ -1 ] )
            ins.restart()
        else:
            time.sleep( 1 )
except KeyboardInterrupt:
    ins.stop()

import os
import shutil
import struct
import imghdr

def get_image_size(fname):
    with open(fname, 'rb') as fhandle:
        head = fhandle.read(24)
        if len(head) != 24:
        	return -1, -1
        if imghdr.what(fname) == 'png':
            check = struct.unpack('>i', head[4:8])[0]
            if check != 0x0d0a1a0a:
            	return -1, -1
            width, height = struct.unpack('>ii', head[16:24])
        elif imghdr.what(fname) == 'gif':
            width, height = struct.unpack('<HH', head[6:10])
        elif imghdr.what(fname) == 'jpeg':
            try:
                fhandle.seek(0) # Read 0xff next
                size = 2
                ftype = 0
                while not 0xc0 <= ftype <= 0xcf:
                    fhandle.seek(size, 1)
                    byte = fhandle.read(1)
                    while ord(byte) == 0xff:
                        byte = fhandle.read(1)
                    ftype = ord(byte)
                    size = struct.unpack('>H', fhandle.read(2))[0] - 2
                # We are at a SOFn block
                fhandle.seek(1, 1)  # Skip 'precision' byte.
                height, width = struct.unpack('>HH', fhandle.read(4))
            except Exception: #IGNORE:W0703
            	return -1, -1
        else:
        	return -1, -1
        return width, height

def fetch_spotlight():
	if not os.path.exists(destFolder):
	    os.makedirs(destFolder)

	destFileNames = [ os.path.splitext(f)[0] for f in os.listdir(destFolder)]
	copiedFiles = []

	for fileName in os.listdir(sourceFolder):
		filePath = os.path.join(sourceFolder, fileName)
		root, ext = os.path.splitext(filePath)
		if ext == '' and fileName not in destFileNames:
			width, height = get_image_size(filePath)
			if width >= minImageWidth and height >=minImageHeight:
				shutil.copy(filePath, destFolder)
				copiedFilePath = os.path.join(destFolder, fileName)
				os.rename(copiedFilePath, "%s.jpg" % (copiedFilePath))

minImageWidth = 1920
minImageHeight = 1080
sourceFolder = "C:/Users/%s/AppData/Local/Packages/Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy/LocalState/Assets" % (os.getlogin())
destFolder = "C:/Users/%s/Pictures/Spotlight" % (os.getlogin())

fetch_spotlight()
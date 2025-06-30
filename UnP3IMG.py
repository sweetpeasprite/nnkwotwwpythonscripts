print("    +*%@@@#=                  "
+ "\n          +%@#           #@@  "
+ "\n             #@%      *@@*    "
+ "\n               #@+ #@@*       "
+ "\n                %@@*          "
+ "\n             *@@+#@           "
+ "\n          #@@+    @=          "
+ "\n       *@@*       @=          "
+ "\n         *@#     =@           "
+ "\n            *@*  %*           "
+ "\n               *@%            "
+ "\n               @* *#=         "
+ "\n             ##      #*       "
+ "\n          =%+           #+    "
+ "\n       +#=                =*= ")
print("Tool for unpacking .p3igg texture packages in Ni no Kuni: Wrath of the White Witch.\nCreated by sweetpea-sprite.\nPossibly only works on textures that come from .pkchr files...\n")

# imports
import os.path
from pathlib import Path
import struct

while 1 == 1:
    print('Type "unpack" to unpack a file and "repack" to repack a file.')
    choicer = input("")
    if choicer.lower() == "unpack" or choicer.lower() == "repack":
        break
    else:
        print("Invalid input.")
		
if choicer.lower() == "unpack":

    pathToFile = input("Input .p3img (not .p3igg!) header file to unpack: ")

    if os.path.isfile(pathToFile) == True: # checks that the file exists
        
        # get raw data from the header file
        rawHeaderData = Path(pathToFile).read_bytes()
        
        # check magic number + extension
        if struct.unpack_from("I", rawHeaderData, 0)[0] != 6778217 or not pathToFile.endswith(".p3img"):
            if pathToFile.endswith(".p3igg"):
                print("Input .p3img, not .p3igg!")
            else:
                print("File doesn't look like a .p3img!\nIf you think this is a bug, report it!")
            input("Press enter to exit.")
            quit()
        
        if os.path.isfile(pathToFile[:-6] + ".p3igg") == False:
            print("Couldn't find accompanying .p3igg file.\nMake sure it's in the same place as the .p3img, and has the same name.")
            input("Press enter to exit.")
            quit()
        
        # get raw data from the actual file
        rawFileData = Path(pathToFile[:-6] + ".p3igg").read_bytes()
        
        # get info from header
        numFiles = struct.unpack_from("I", rawHeaderData, 40)[0]
        fileStart = struct.unpack_from("I", rawHeaderData, 16)[0]
        sect1Length = struct.unpack_from("I", rawHeaderData, 48)[0]
        listStart = fileStart + sect1Length + (numFiles * 48)
        
        # file name list
        fileNameList = []
        offs = listStart
        currChr = rawHeaderData[offs]
        currName = ""
        for i in range(numFiles):
            while currChr == 0:
                offs += 1
                currChr = rawHeaderData[offs]
            while currChr != 0:
                currName += str(struct.unpack_from("c", rawHeaderData, offs)[0], "utf-8")
                offs += 1
                currChr = rawHeaderData[offs]
            offs += 1
            currChr = rawHeaderData[offs]
            fileNameList.append(currName)
            currName = ""
        
        # make directory if it doesn't exist
        if not os.path.exists(pathToFile[:-6]):
            os.makedirs(pathToFile[:-6])
            
        DDSheaderBytes = b'DDS |\x00\x00\x00\x07\x10\x00\x00\x80\x00\x00\x00\x80\x00\x00\x00\x00D\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 \x00\x00\x00\x04\x00\x00\x00DX10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00b\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00'
        DDSheader = bytearray(DDSheaderBytes)
        
        offs = fileStart + sect1Length
        for i in range(numFiles):
            currentFileHead = struct.unpack_from("4I", rawHeaderData, offs)
            offs += 24
            currentFileWidth = struct.unpack_from("H", rawHeaderData, offs)[0]
            currentFileHeight = struct.unpack_from("H", rawHeaderData, offs + 2)[0]
            offs += 24
            struct.pack_into("I", DDSheader, 12, currentFileHeight)
            struct.pack_into("I", DDSheader, 16, currentFileWidth)
            struct.pack_into("I", DDSheader, 20, currentFileHead[2])
            currFileContent = rawFileData[currentFileHead[1]:currentFileHead[1] + currentFileHead[2]]
            with open(pathToFile[:-6] + "/" + fileNameList[i] + ".dds", "wb") as binary_file:
                binary_file.write(DDSheader + currFileContent)
            print("File " + fileNameList[i] + ".dds" + " written.")
        
    else:
        print("File doesn't exist.")

if choicer.lower() == "repack":
    
    pathToFile = input("Input .p3img (not .p3igg!) header file to repack: ")

    if os.path.isfile(pathToFile) == True: # checks that the file exists
    
    # get raw data from the header file
        rawHeaderData = Path(pathToFile).read_bytes()
    
    # check magic number + extension
        if struct.unpack_from("I", rawHeaderData, 0)[0] != 6778217 or not pathToFile.endswith(".p3img"):
            if pathToFile.endswith(".p3igg"):
                print("Input .p3img, not .p3igg!")
            else:
                print("File doesn't look like a .p3img!\nIf you think this is a bug, report it!")
            input("Press enter to exit.")
            quit()
        
        if os.path.isfile(pathToFile[:-6] + ".p3igg") == False:
            print("Couldn't find accompanying .p3igg file.\nMake sure it's in the same place as the .p3img, and has the same name.")
            input("Press enter to exit.")
            quit()
        
        # get raw data from the actual file
        rawFileData = Path(pathToFile[:-6] + ".p3igg").read_bytes()
        
        # get info from header
        numFiles = struct.unpack_from("I", rawHeaderData, 40)[0]
        fileStart = struct.unpack_from("I", rawHeaderData, 16)[0]
        sect1Length = struct.unpack_from("I", rawHeaderData, 48)[0]
        listStart = fileStart + sect1Length + (numFiles * 48)
        
        # file name list
        fileNameList = []
        offs = listStart
        currChr = rawHeaderData[offs]
        currName = ""
        for i in range(numFiles):
            while currChr == 0:
                offs += 1
                currChr = rawHeaderData[offs]
            while currChr != 0:
                currName += str(struct.unpack_from("c", rawHeaderData, offs)[0], "utf-8")
                offs += 1
                currChr = rawHeaderData[offs]
            offs += 1
            currChr = rawHeaderData[offs]
            fileNameList.append(currName)
            currName = ""
        
        # file selector
        print("\nList of files:")
        for i in fileNameList:
            print(i + ".dds")
        fileToReplace = input("\nInput name of file to replace (from the list!): ")
        
        fileID = -1
        for i in range(numFiles):
            if fileToReplace == fileNameList[i] + ".dds":
                fileID = i
                break
        if fileID == -1:
            print("Couldn't find dds file. Check you spelled it correctly!")
            input("\nPress enter to exit.")
            quit()
        
        fileToAdd = input("\nInput file to replace it with (your new file): ")
        
        if os.path.isfile(fileToAdd) == False:
            print("File doesn't exist.")
            input("\nPress enter to exit.")
            quit()
        
        # get data for new file
        rawNewData = Path(fileToAdd).read_bytes()
        
        # check magic number + extension
        if struct.unpack_from("I", rawNewData, 0)[0] != 542327876 or not fileToAdd.endswith(".dds"):
            print("File doesn't look like a .dds!\nIf you think this is a bug, report it!")
            input("Press enter to exit.")
            quit()
        
        # make sure it's the correct KIND of dds
        if struct.unpack_from("I", rawNewData, 84)[0] != 808540228:
            print("Wrong DDS format.\nTry using BC7/DXT10, and don't generate mipmaps.")
            input("Press enter to exit.")
            quit()
            
        # get rid of dds header
        rawNewData = rawNewData[148:]
        
        # get info for original file from .p3img
        ogFileStart = struct.unpack_from("I", rawHeaderData, fileStart + sect1Length + 4 + (fileID * 48))[0]
        ogFileLength = struct.unpack_from("I", rawHeaderData, fileStart + sect1Length + 8 + (fileID * 48))[0]
        # new file length
        newFileLength = len(rawNewData)
        
        # create new p3igg file
        newIggBytes = rawFileData[:ogFileStart] + rawNewData + rawFileData[ogFileStart+ogFileLength:]
        newIggByteArray = bytearray(newIggBytes)
        
        # editable header
        newImgByteArray = bytearray(rawHeaderData)
        
        # edit header parameters
        # edited file length:
        struct.pack_into("I", newImgByteArray, fileStart + sect1Length + 8 + (fileID * 48), newFileLength)
        # rest of the file starts:
        i = fileID + 1
        while i < numFiles:
            currFileStart = struct.unpack_from("I", rawHeaderData, fileStart + sect1Length + 4 + (fileID * 48))[0]
            struct.pack_into("I", newImgByteArray, fileStart + sect1Length + 4 + (fileID * 48), (currFileStart - ogFileLength) + newFileLength)
            i += 1
        
        # write to new files
        with open(pathToFile[:-6] + " edited.p3img", "wb") as binary_file:
            binary_file.write(newImgByteArray)
        print("Successfully written file to " + pathToFile[:-6] + " edited.p3img.")
        with open(pathToFile[:-6] + " edited.p3igg", "wb") as binary_file:
            binary_file.write(newIggByteArray)
        print("Successfully written file to " + pathToFile[:-6] + " edited.p3igg.")
        
    else:
        print("File doesn't exist.")

input("\nPress enter to exit.")
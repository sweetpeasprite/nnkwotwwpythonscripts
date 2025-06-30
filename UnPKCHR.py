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
print("Tool for unpacking .pkchr package files in Ni no Kuni: Wrath of the White Witch.\nCreated by sweetpea-sprite.\n")

print("Usage instructions:\nInput file name to unpack into data folder in the same place as this .py.\nFile name can optionally include a path; default path is the same directory as this .py.\n")

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

    pathToFile = input("Input file to unpack: ")

    if os.path.isfile(pathToFile) == True: # checks that the file exists
        
        # get raw data
        rawData = Path(pathToFile).read_bytes()
        
        # check magic number + extension
        if struct.unpack_from("I", rawData, 0)[0] != 808538184 or not pathToFile.endswith(".pkchr"):
            print("File doesn't look like a .pkchr!\nIf you think this is a bug, report it!")
            input("Press enter to exit.")
            quit()
        
        # get info from the header
        numFiles = struct.unpack_from("I", rawData, 4)[0] # number of files in the pkchr
        listStart = struct.unpack_from("I", rawData, 16)[0] # start of file list text
        filesStart = struct.unpack_from("I", rawData, 20)[0] # start of where files actually begin
        
        # file name list
        fileNameList = []
        offs = listStart
        currChr = rawData[offs]
        currName = ""
        for i in range(numFiles):
            while currChr != 0:
                if currChr == 47:
                    currName += "."
                else:
                    currName += str(struct.unpack_from("c", rawData, offs)[0], "utf-8")
                offs += 1
                currChr = rawData[offs]
            offs += 1
            currChr = rawData[offs]
            fileNameList.append(currName)
            currName = ""
        
        # make directory if it doesn't exist
        if not os.path.exists(pathToFile[:-6]):
            os.makedirs(pathToFile[:-6])
        
        offs = 32
        for i in range(numFiles):
            currentFileHead = struct.unpack_from("8I", rawData, offs)
            offs += 32
            currFileContent = rawData[(filesStart + currentFileHead[4]):(filesStart + currentFileHead[4] + currentFileHead[5])]
            with open(pathToFile[:-6] + "/" + fileNameList[i], "wb") as binary_file:
                binary_file.write(currFileContent)
            print("File " + fileNameList[i] + " written.")
        
    else:
        print("File doesn't exist.")

if choicer.lower() == "repack":
    
    pathToFile = input("Input file to edit: ")
    
    if os.path.isfile(pathToFile) == True: # checks that the file exists
        
        # get raw data
        rawData = Path(pathToFile).read_bytes()
        
        # check magic number + extension
        if struct.unpack_from("I", rawData, 0)[0] != 808538184 or not pathToFile.endswith(".pkchr"):
            print("File doesn't look like a .pkchr!\nIf you think this is a bug, report it!")
            input("Press enter to exit.")
            quit()
        
        # get info from the header
        numFiles = struct.unpack_from("I", rawData, 4)[0] # number of files in the pkchr
        listStart = struct.unpack_from("I", rawData, 16)[0] # start of file list text
        filesStart = struct.unpack_from("I", rawData, 20)[0] # start of where files actually begin
        
        # file name list
        fileNameList = []
        offs = listStart
        currChr = rawData[offs]
        currName = ""
        for i in range(numFiles):
            while currChr != 0:
                if currChr == 47:
                    currName += "."
                else:
                    currName += str(struct.unpack_from("c", rawData, offs)[0], "utf-8")
                offs += 1
                currChr = rawData[offs]
            offs += 1
            currChr = rawData[offs]
            fileNameList.append(currName)
            currName = ""
        
        # file selector
        print("\nList of files:")
        for i in fileNameList:
            print(i)
        fileToReplace = input("\nInput name of file to replace (from the list!): ")
        
        fileID = -1
        for i in range(numFiles):
            if fileToReplace == fileNameList[i]:
                fileID = i
                break
        if fileID == -1:
            print("Couldn't find file. Check you spelled it correctly!")
            input("\nPress enter to exit.")
            quit()
        
        fileToAdd = input("\nInput file to replace it with (your new file): ")
        
        if os.path.isfile(fileToAdd) == False:
            print("File doesn't exist.")
            input("\nPress enter to exit.")
            quit()
        
        # get data for new file
        rawNewData = Path(fileToAdd).read_bytes()
        # can't check the file for this one because it could be truly anything...
        
        # get info for original file from .pkchr
        ogFileStart = struct.unpack_from("I", rawData, (48 + (32 * fileID)))[0] + filesStart
        ogFileLength = struct.unpack_from("I", rawData, (52 + (32 * fileID)))[0]
        # new file length
        newFileLength = len(rawNewData)
        
        # create new pkchr file
        
        newPkchrBytes = rawData[:ogFileStart] + rawNewData + rawData[ogFileStart+ogFileLength:]
        newPkchrByteArray = bytearray(newPkchrBytes)
        
        # edit header parameters
        # edited file length:
        struct.pack_into("I", newPkchrByteArray, 52 + (32 * fileID), newFileLength)
        # rest of the file starts:
        i = fileID + 1
        while i < numFiles:
            currFileStart = struct.unpack_from("I", rawData, (48 + (32 * i)))[0]
            struct.pack_into("I", newPkchrByteArray, 48 + (32 * i), (currFileStart - ogFileLength) + newFileLength)
            i += 1
        
        # write to new file
        with open(pathToFile[:-6] + " edited.pkchr", "wb") as binary_file:
            binary_file.write(newPkchrByteArray)
        print("Successfully written file to " + pathToFile[:-6] + " edited.pkchr.")
        
    else:
        print("File doesn't exist.")

input("\nPress enter to exit.")
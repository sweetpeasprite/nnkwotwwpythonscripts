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
print("Tool for unpacking .img packages in Ni no Kuni: Wrath of the White Witch.\nCreated by sweetpea-sprite.\n")

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
        if struct.unpack_from("I", rawData, 0)[0] != 3362121 or not pathToFile.endswith(".img"):
            print("File doesn't look like a .img!\nIf you think this is a bug, report it!")
            input("Press enter to exit.")
            quit()
        
        # get info from header
        listStart = struct.unpack_from("I", rawData, 4)[0]
        numFiles = struct.unpack_from("I", rawData, 8)[0]
        
        # file name list
        fileNameList = []
        offs = listStart
        currChr = rawData[offs]
        currName = ""
        for i in range(numFiles):
            for x in range(16):
                if currChr == 0:
                    currName += ""
                else:
                    currName += str(struct.unpack_from("c", rawData, offs)[0], "utf-8")
                offs += 1
                currChr = rawData[offs]
            offs += 48
            currChr = rawData[offs]
            fileNameList.append(currName)
            currName = ""
        
        # make directory if it doesn't exist
        if not os.path.exists(pathToFile[:-4]):
            os.makedirs(pathToFile[:-4])
        
        offs = listStart + 32
        for i in range(numFiles):
            currentFileHead = struct.unpack_from("8I", rawData, offs)
            offs += 64
            currFileContent = rawData[currentFileHead[1]:(currentFileHead[1] + currentFileHead[5])]
            with open(pathToFile[:-4] + "/" + fileNameList[i] + ".dds", "wb") as binary_file:
                binary_file.write(currFileContent)
            print("File " + fileNameList[i] + ".dds" + " written.")
        
    else:
        print("File doesn't exist.")

if choicer.lower() == "repack":
    
    pathToFile = input("Input file to edit: ")
    
    if os.path.isfile(pathToFile) == True: # checks that the file exists
        
        # get raw data
        rawData = Path(pathToFile).read_bytes()
        
        # check magic number + extension
        if struct.unpack_from("I", rawData, 0)[0] != 3362121 or not pathToFile.endswith(".img"):
            print("File doesn't look like a .img!\nIf you think this is a bug, report it!")
            input("Press enter to exit.")
            quit()
        
        # get info from header
        listStart = struct.unpack_from("I", rawData, 4)[0]
        numFiles = struct.unpack_from("I", rawData, 8)[0]
        
        # file name list
        fileNameList = []
        offs = listStart
        currChr = rawData[offs]
        currName = ""
        for i in range(numFiles):
            for x in range(16):
                if currChr == 0:
                    currName += ""
                else:
                    currName += str(struct.unpack_from("c", rawData, offs)[0], "utf-8")
                offs += 1
                currChr = rawData[offs]
            offs += 48
            currChr = rawData[offs]
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
        
        # get info for original file from .img
        ogFileStart = struct.unpack_from("I", rawData, (52 + (64 * fileID)))[0]
        ogFileLength = struct.unpack_from("I", rawData, (68 + (64 * fileID)))[0]
        # new file length
        newFileLength = len(rawNewData)
        
        # create new img file
        
        newImgBytes = rawData[:ogFileStart] + rawNewData + rawData[ogFileStart+ogFileLength:]
        newImgByteArray = bytearray(newImgBytes)
        
        # edit header parameters
        # edited file length:
        struct.pack_into("I", newImgByteArray, 68 + (64 * fileID), newFileLength)
        # rest of the file starts:
        i = fileID + 1
        while i < numFiles:
            currFileStart = struct.unpack_from("I", rawData, (52 + (64 * i)))[0]
            struct.pack_into("I", newImgByteArray, 52 + (64 * i), (currFileStart - ogFileLength) + newFileLength)
            i += 1
        
        # write to new file
        with open(pathToFile[:-4] + " edited.img", "wb") as binary_file:
            binary_file.write(newImgByteArray)
        print("Successfully written file to " + pathToFile[:-4] + " edited.img.")
        
    else:
        print("File doesn't exist.")

input("\nPress enter to exit.")
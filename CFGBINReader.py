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
print("Tool for editing .cfg.bin dialogue files in Ni no Kuni: Wrath of the White Witch.\nCreated by sweetpea-sprite.\n")

print("Usage instructions:\nInput file name (either a compiled .cfg.bin or a decompiled .json) to decompile/recompile.\nFile name can optionally include a path; default path is the same directory as this .py.")

# imports
import os.path
from pathlib import Path
import struct
import json

# get input file from user
pathToFile = input("File: ")

if os.path.isfile(pathToFile) == True: # checks that the file exists
    if pathToFile.lower().endswith(".cfg.bin"):
        
        # get the binary data
        rawData = Path(pathToFile).read_bytes()
        
        # HEADER
        
        # declare header tuple
        header = ()
        # log bytes until we hit section 1's header (which always starts with 3766650362 (I HOPE))
        offs = 0
        currentByte = struct.unpack_from("I", rawData, offs)
        i = 0
        while currentByte[0] != 3766650362 and i != 10:
            header += struct.unpack_from("IIII", rawData, offs)
            offs += 16
            currentByte = struct.unpack_from("I", rawData, offs)
            i += 1
        if i == 10: # hey don't think about this error check too hard, ok?
            print("This doesn't look like a dialogue file!\nIf you think this is a bug, please contact sweetpea-sprite.")
            input("Press enter to exit.")
            quit()
        # adds the sect 1 header to the header
        header = header + struct.unpack_from("IIII", rawData, offs)
        # set offset to post sect 1 header
        offs += 16
        # grab the number of dialogues + sections from the header
        numDialogues = header[3]
        numSects = header[-2]
        
        # SECTION 1
        
        section1 = []
        i = 0
        for i in range(numSects):
            current = struct.unpack_from("iiiiiiii", rawData, offs)
            section1.append(current)
            offs += 32
        
        # skip section break
        offs += 16
        
        # SECTION 2
        
        section2 = []
        i = 0
        for i in range(numSects):
            current = struct.unpack_from("iiiiiiii", rawData, offs)
            section2.append(current)
            offs += 32
        
        # skip section break
        offs += 16
        
        # finally. the actual dialogue
        # DIALOGUE
        
        dialogueContent = []
        i = 0
        currentChar = rawData[offs]
        charCheck3 = rawData[offs-1:offs+2]
        charCheck2 = rawData[offs-1:offs+1]
        message = ""
        for i in range(numDialogues):
            while currentChar != 0:
                if charCheck3 == b'\xe2\x80\x94': # em dash
                    message += "[em]"
                    offs += 3
                elif charCheck3 == b'\xe2\x80\x99': # those stupid fucking fake apostrophes
                    message += "'"
                    offs += 3
                elif currentChar in range(194, 196): # accented letters
                    if charCheck2 == b'\xc3\xa4': # ä
                        message += "[a:]"
                    if charCheck2 == b'\xc3\xa2': # â
                        message += "[a^]"
                    if charCheck2 == b'\xc3\x85': # Å
                        message += "[Ao]"
                    if charCheck2 == b'\xc2\xbf': # ¿
                        message += "[qu]"
                    if charCheck2 == b'\xc3\xa9': # é
                        message += "[e<]"
                    if charCheck2 == b'\xc3\xb1': # ñ
                        message += "[n~]"
                    offs += 2
                else:
                    message += str(struct.unpack_from("c", rawData, offs)[0], "utf-8")
                    offs += 1
                currentChar = rawData[offs]
                charCheck3 = rawData[offs:offs+3]
                charCheck2 = rawData[offs:offs+2]
            offs += 1
            currentChar = rawData[offs]
            if not message.startswith("201") and message != "default" and message != "IDK591-1064" and message != "Marcin Kdzierski":
                dialogueContent.append(message)
            message = ""
        
        # skip padding
        while currentChar == 255:
            offs += 1
            currentChar = rawData[offs]
        
        # ENDING SECTION
        
        endSect = ()
        while offs != len(rawData):
            endSect += struct.unpack_from("IIII", rawData, offs)
            offs += 16
        
        
        ### WRITING TO JSON ###
        
        # puts the first two sections with their corresponding message
        messageList = []
        i = 0
        for i in range(numSects):
            currentObject = {
                "Section1": section1[i],
                "Section2": section2[i],
                "Message": ""
                }
            if i < numDialogues:
                currentObject["Message"] = dialogueContent[i]
            messageList.append(currentObject)
        
        # first json (over-formatted)
        jsonData = json.dumps({"Header": header, "MessageList": messageList, "Footer": endSect}, indent = 4)
        
        # less formatted json
        jsonFinal = ''
        skip = 0
        for char in jsonData:
            if (skip == 1) and ((char == '\n') or (char == ' ')) :
                pass
            elif (char == '[') :
                skip = 1
                jsonFinal += char
            elif (char == ']') :
                skip = 0
                jsonFinal += char
            else :
                jsonFinal += char
        
        # creates + writes to file
        with open(pathToFile + ".json", mode="w", encoding="utf-8") as write_file:
            print(jsonFinal, file = write_file)
        
        # success message :]
        print("Successfully wrote file to " + pathToFile + ".json")
        
    elif pathToFile.lower().endswith(".json"):
        
        # import file
        with open(pathToFile, mode="r", encoding="utf-8") as read_file:
            jsonFile = json.load(read_file)
        
        offsJson = 0
        offsFile = 0
        
        # writing the header
        header = bytearray(len(jsonFile["Header"]) * 4)
        while offsJson != len(jsonFile["Header"]):
            struct.pack_into("I", header, offsFile, jsonFile["Header"][offsJson])
            offsJson += 1
            offsFile += 4
        
        offsJson = 0
        sectNum = jsonFile["Header"][-2]
        diaNum = jsonFile["Header"][3]
        
        # section 1
        
        offsFile = 0
        
        section1 = bytearray(sectNum * 32)
        for i in range(sectNum):
            for x in range(8):
                struct.pack_into("i", section1, offsFile, jsonFile["MessageList"][i]["Section1"][x])
                offsFile += 4
        
        # section 2
        
        offsFile = 0
        
        section2 = bytearray(sectNum * 32)
        for i in range(sectNum):
            for x in range(8):
                struct.pack_into("i", section2, offsFile, jsonFile["MessageList"][i]["Section2"][x])
                offsFile += 4
        
        # dialogue
        
        msgList = []
        msgLen = 0
        accList = ["[a:]", "[a^]", "[Ao]", "[qu]", "[e<]", "[n~]"]
        accCount = 0
        a = 0
        for i in range(sectNum):
            msgList.append(jsonFile["MessageList"][i]["Message"])
            msgLen += len(msgList[i]) + 1
            emdCount = jsonFile["MessageList"][i]["Message"].count("[em]")
            for x in range(emdCount):
                msgLen -= 1
            while a < len(accList):
                accCount += jsonFile["MessageList"][i]["Message"].count(accList[a])
                a += 1
            a = 0
            for x in range(accCount):
                msgLen -= 2
            accCount = 0
            # section 1 dialogue start byte:
            if i < sectNum - 1:
                struct.pack_into("i", section1, ((32 * (i + 1)) + 24), msgLen)
        # sect 1 first one (always has to be 0...)
        struct.pack_into("i", section1, 24, 0)
        # header dialogue length:
        struct.pack_into("I", header, 8, msgLen)
        
        # actual dialogue bytes
        offsFile = 0
        trueMsgLen = msgLen
        while trueMsgLen % 16 != 0:
            trueMsgLen += 1
        dialogueContent = bytearray(trueMsgLen)
        for i in range(len(msgList)):
            x = 0
            while x < len(msgList[i]):
                if msgList[i][x:x+4] == "[em]":
                    struct.pack_into("BBB", dialogueContent, offsFile, 226, 128, 148)
                    x += 4
                    offsFile += 3
                elif msgList[i][x:x+4] == "[a:]":
                    struct.pack_into("BB", dialogueContent, offsFile, 195, 164)
                    x += 4
                    offsFile += 2
                elif msgList[i][x:x+4] == "[a^]":
                    struct.pack_into("BB", dialogueContent, offsFile, 195, 162)
                    x += 4
                    offsFile += 2
                elif msgList[i][x:x+4] == "[Ao]":
                    struct.pack_into("BB", dialogueContent, offsFile, 195, 133)
                    x += 4
                    offsFile += 2
                elif msgList[i][x:x+4] == "[qu]":
                    struct.pack_into("BB", dialogueContent, offsFile, 194, 191)
                    x += 4
                    offsFile += 2
                elif msgList[i][x:x+4] == "[e<]":
                    struct.pack_into("BB", dialogueContent, offsFile, 195, 169)
                    x += 4
                    offsFile += 2
                elif msgList[i][x:x+4] == "[n~]":
                    struct.pack_into("BB", dialogueContent, offsFile, 195, 177)
                    x += 4
                    offsFile += 2
                else:
                    struct.pack_into("c", dialogueContent, offsFile, bytes(msgList[i][x], "utf-8"))
                    offsFile += 1
                    x += 1
            struct.pack_into("x", dialogueContent, offsFile)
            offsFile += 1
        
        # add padding
        while trueMsgLen != msgLen:
            struct.pack_into("B", dialogueContent, offsFile, 255)
            offsFile += 1
            msgLen += 1
        
        # writing the footer
        offsJson = 0
        offsFile = 0
        footer = bytearray(len(jsonFile["Footer"]) * 4)
        while offsJson != len(jsonFile["Footer"]):
            struct.pack_into("I", footer, offsFile, jsonFile["Footer"][offsJson])
            offsJson += 1
            offsFile += 4
        
        # calculate + check the size of the final file
        fileSize = len(header) + len(section1) + len(section2) + msgLen + len(footer) + 32
        if fileSize % 16 != 0:
            print("Something went wrong!\nCalculated file size invalid. Please report this bug!")
            input("Press enter to exit.")
            quit()
        
        # the breaks
        firstBreak = b'\xc9\xff\xe3{\x00\xff\xff\xff\xc3A\xc3T\x00\xff\xff\xff'
        secondBreak = b'\xadBH\xde\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
        
        # WRITE !!!
        
        with open(pathToFile + ".cfg.bin", "wb") as binary_file:
            binary_file.write(header + section1 + firstBreak + section2 + secondBreak + dialogueContent + footer)
        
        print("Successfully wrote file to " + pathToFile + ".cfg.bin")
        
    else:
        print("Invalid file.")
else:
    print("Couldn't find file.")



input("Press enter to exit.")
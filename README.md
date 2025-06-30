A collection of Python 3 scripts for modding Ni no Kuni: Wrath of the White Witch Remastered.  
**All scripts require Python 3 to be installed.**  
Usage instructions are included in the .py, see below for more details.  

---

## CFGBINReader
**Doesn't work all the time.** I'm working on this... Will hopefully work with most English dialogue files for now.  
Used for editing dialogue *.cfg.bin* files. Open the script and enter a file name to decompile into a *.json* file that you can then edit the dialogue in. Once you're done, open the script and enter the name of the *.json* to recompile into a *.cfg.bin*.  
Tags list in the editor:  
ä: \[a:]  
â: \[a^]  
Å: \[Ao]  
¿: \[qu]  
é: \[e<]  
ñ: \[n~]  
emdash: \[em]  
There are more built-in tags (i.e. Nazcaan letters, button icons) that will also work; these aren't documented just yet...  
This is still a work-in-progress.  

## UnPKCHR
Used for unpacking/repacking *.pkchr* files. These files are commonly used for models (i.e. in data\character).

## UnIMGPAK
Used for unpacking/repacking *.imgpak* files. These files are commonly used for icons and menus.

## UnP3IMG
Used for unpacking/repacking *.p3img* and *.p3igg* files. These files always have the other next to them; the *.p3img* is the header for the DDS files contained in the *.p3igg*. Commonly used for textures.  
There are two variants of this program: *UnP3IMG.py* and *UnP3IMG-PKCHR.py*. The first uses BC7/DXT10 encoding for the DDS files, which is (as far as I can tell) the most common format outside of *.pkchr* files. The second uses BC1/DXT1 encoding, which is used for model textures inside *.pkchr*s.  
If you come up against a file that looks like a colourful mess when unpacked, try using the other program.  
**Please note you have to use the same encoding when saving your new DDS file to replace the old one.**  

## UnIMG
Used for unpacking/repacking *.img* files (sometimes found in .pkchr files). I don't actually know if these files are used... but if they ever are, you can use this to edit them.  
DDS format is BC1/DXT1.  

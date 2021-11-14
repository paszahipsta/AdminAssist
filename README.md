# AdminAssist

AdminAssist uses WMI to help you extract information from any windows computer in domain or workgroup

For now it can display information like:
- hardware you're running on
- Ip settings and route table

Plan for next updates:
- domain information display
- last logins in the domain
- computers in the domain
- users in the domain

## Requirements:

The script is based on WMI, so it will run only on Windows.

To obtain information about remote computer you need to be sure that you can connect to the WMI. 

Enable WMI in WORKGROUP:

https://support.rapidfiretools.com/hc/en-us/articles/360007604558-Allowing-Remote-WMI-Access-in-a-WORKGROUP

Enable WMI in Domain:  

From what I know domain Administrator have enough priviliges to query remote machines through WMI (if I'm wrong please let me know)

Library requirements are available in requirements.txt .

## Syntax 

####  AdminRookie supports command line menu (just double click on exe file):  

<img title="a title" src="https://i.ibb.co/zsbdvDx/menu.png">

#### You can also use the powershell and cmd to specify more advanced settings:  
  
```
options:
  -h, --help            show this help message and exit
  -target TARGET        AdminRookie.exe <computer_name> - run the program for remote machine
  -hardware             Display hardware information, don't run menu
  -network              Display network information, don't run menu

authentication:
  -credentials USERNAME:PASSWORD
                        Supply username and password
```

## Example 
```
AdminAssist.exe -hardware -target MY_COMPUTER -credentials me:mypass
```

This will display hardware of MY_COMPUTER machine. Credentials are only neccesary if on your current account you don't have priviliges to access target machine.

## False-positive windows defender

Windows defender is sometimes blocking the executable file. However the python script itself seems to work without these issues. If you don't trust the executable you can easily use pyinstaller to create your own executable file: 

```
py -m pip install pyinstaller
pyinstaller --onefile main.py
```


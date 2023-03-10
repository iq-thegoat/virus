import aiohttp,asyncio,time,math
import colorama,random,datetime,os,threading
import tkinter.filedialog as fd
colorama.init()
colors = [colorama.Fore.RED,colorama.Fore.YELLOW,  colorama.Fore.MAGENTA, colorama.Fore.CYAN]
rc = random.choice(colors)
res = colorama.Fore.RESET


def center(var:str, space:int=None): # From Pycenter
    if not space:
        space = (os.get_terminal_size().columns - len(var.splitlines()[int(len(var.splitlines())/2)])) / 2
    
    return "\n".join((' ' * int(space)) + var for var in var.splitlines())


def get_elapsed_time(start_time):
    end_time = datetime.datetime.now()
    elapsed_time = end_time - start_time
    hours, remainder = divmod(elapsed_time.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    return [int(hours), int(minutes), int(seconds)]


hits = []
MySql = []
MsSql = []
PostGress = []
Oracle = []
MariaDb = []
AllSqls = []
Errors = []
start = datetime.datetime.now()
start_math = time.time()
tries = []
waf = []
BadUrls = []

def cli():
    global hits
    global MariaDb
    global MySql
    global MsSql
    global AllSqls
    global Errors
    global Oracle
    global PostGress
    global waf
    global BadUrls
    global combosize
    while True:
        time.sleep(1)
        os.system("cls")
        name = """
        
 :::::::: ::::::::::: ::::::::::: ::::::::::       ::::::::       :::::::::  :::    ::: ::::::::::: :::        :::::::::: 
:+:    :+:    :+:         :+:     :+:             :+:    :+:      :+:    :+: :+:    :+:     :+:     :+:        :+:        
+:+           +:+         +:+     +:+             +:+    +:+      +:+    +:+ +:+    +:+     +:+     +:+        +:+        
+#++:++#++    +#+         +#+     +#++:++#        +#+    +:+      +#++:++#+  +#++:++#++     +#+     +#+        +#++:++#   
       +#+    +#+         +#+     +#+             +#+    +#+      +#+        +#+    +#+     +#+     +#+        +#+        
#+#    #+#    #+#         #+#     #+#             #+#    #+#      #+#        #+#    #+#     #+#     #+#        #+#        
 ######## ###########     ###     ##########       ########       ###        ###    ### ########### ########## ########## 
                                                                                                                          
"""

        print(center(rc+name))
        Mysql_str = str(len(MySql))
        MariaDb_str = str(len(MariaDb))
        Oracle_str = str(len(Oracle))
        PostGress_str  = str(len(PostGress))
        MsSql_str = str(len(MsSql))
        WAF_str = str(len(waf))
        Errors_str = "4000000"
        elapsedmath = time.time() - start_math
        CPM = int(len(tries) / elapsedmath) * 60
        elapsed_str = get_elapsed_time(start)
        elapsed_show = f"{str(elapsed_str[0])}:{str(elapsed_str[1])}:{str(elapsed_str[2])}" 
        searchedShow = f"{40"
        def centeer(text):
            return f"{text:^100}"
        
        print(res)
        print(center('--------------------------------------------------'))
        print(center(f'|{res}     Database      {res}|{rc:^5}Status{res}'))
        print(center('--------------------------------------------------'))
        print(center(f'|{rc}MySql{res}    |{Mysql_str:<17}            '))
        print(center(f'|{rc:^5}MariaDb{res}  |{MariaDb_str:<20}        '))
        print(center(f'|{rc:^5}Oracle{res}   |{Oracle_str:<20}         '))
        print(center(f'|{rc:^5}PostGress{res}|{PostGress_str:<22}      '))
        print(center(f'|{rc:^5}MsSql{res}    |{MsSql_str:<19}          '))
        print(center(f'|{rc:^5}WAF{res}      |{WAF_str:<17}            '))
        print(center('--------------------------------------------------'))
        print(center(f'|{rc:<5}Elapsed{res} |{elapsed_show}|{rc:>18}{res}'))
        print(center(f'|{rc:<5}Errors{res}  |{Errors_str}|{rc:>22}{res}'))
        print(center(f'|{rc:<5}Checked{res} |{searchedShow}|{rc:>20}{res}'))
        print(center('--------------------------------------------------'))
        os._exit()


cli()
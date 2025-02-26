# coding=utf-8


from rich import console,table
import subprocess
from time import strftime,localtime
import os
import requests
import threading

console = console.Console()
# 日志输出函数
def log(level, message,WriteToLog=True,print=True):
    if level == "info" or level == 1:
        log = f"[{strftime('%H:%M:%S',localtime())} INFO] {message}"
        if print:    
            console.print(f"[bold white]{log}")
        if WriteToLog == True:
            with open("latest.log","a+",encoding="utf-8") as file:
                file.write(f"{log}\n")
    elif level == "warning" or level == 2:
        log = f"[{strftime('%H:%M:%S',localtime())} WARNING] {message}"
        if print:
            console.print(f"[bold yellow]{log}")
        if WriteToLog == True:
            with open("latest.log","a+",encoding="utf-8") as file:
                file.write(f"{log}\n")
    elif level == "error" or level == 3:
        log = f"[{strftime('%H:%M:%S',localtime())} ERROR] {message}"
        if print:    
            console.print(f"[bold red]{log}")
        if WriteToLog == True:
            with open("latest.log","a+",encoding="utf-8") as file:
                file.write(f"{log}\n")


# 初始化
class init():
    
    if(os.path.isfile("latest.log")):
        os.remove("latest.log")

    def CheckJava():
        try:
            output = subprocess.check_output("java -version", stderr=subprocess.STDOUT, shell=True).decode('utf-8')
            if "java version" in output:
                log(1,"成功发现JAVA环境")
                import re
                match = re.search(r"version \"(.*?)\"",output)
                if match:
                    java_version = match.group(1)
                    log("info", f"Java版本: {java_version}")
                else:
                    log("warning", "无法解析Java版本号")
        except OSError:
            log(2,"未发现java环境！请检查环境变量或重新安装Java！")
        except subprocess.CalledProcessError as e:
            log(3,f"发生错误:{e.output}")
    CheckJava()
    console.print("[bold blue]   _   _   _       _____             ")
    console.print("[bold blue]  | | | | | |     |_   _|            ")
    console.print("[bold blue]  | |_| | | |       | |      [bold yellow]HrotonLauncher-Terminal        ")
    console.print("[bold blue]  |  _  | | |___    | |       [bright_cyan]Version 1.1.0")
    console.print("[bold blue]  |_| |_| |_____|   |_|              \n")
    console.print("初始化成功！开始进入主菜单")

class Main():
    def Menu(self):
        console.print("[bold] 欢迎来到HLT主页面！")
        console.print("[bold] 请选择您要进行的操作：")
        console.print("[bold] 1-新建服务器")
        # console.print("[bold] 2-运行现有的服务器")
        console.print("[bold] 2-下载服务端")
        console.print("[bold] 3-关于")
        console.print("[bold] 0-退出程序")
        choice = input("请输入您的选择：")
        if choice == "1":
            global MaximumMemory,MinimumMemory,name
            name = input("请输入服务器名称：")
            if name == "":
                log("error", "服务器名称不能为空！")
                Main.Menu(Main)
            MaximumMemory = input("请输入服务器最大内存（单位为MB）：")
            MinimumMemory = input("请输入服务器最小内存（单位为MB）：")

            try:
                intMaximumMemory = int(MaximumMemory)
                intMinimumMemory = int(MinimumMemory)
            except ValueError:
                log("error", "内存必须为整数！")
                Main.Menu(Main)
            if intMaximumMemory > intMinimumMemory:

                    self.DownloadCore(self)

 
                
            else:
                log("warning", "最大内存必须大于最小内存！")
                Main.Menu(Main)
            
        if choice == "2":
            self.DownloadCore(self,False)
        if choice == "3":
            console.print("[bold] HrtonLauncher-Terminal由HrotonStudio开发，用于在终端中运行Minecraft服务器")
            console.print("[bold] 作者：HanWen_lu")
            console.print("[bold] 官方网站: https://hroton.cn/")
            console.print("[bold] 遇到问题? 请联系我们: support@hroton.cn或help@hroton.cn")
            Main.Menu(Main)
        if choice == "0":
            log("info", "程序退出，代码为0",print=False)
            exit(0)
        else:
            log("error", "输入错误！")
            Main.Menu(Main)


    def getcorelist(self):
        response = requests.get("https://hroton.cn/api/servercore/CoreList.json")
        if response.status_code != 200:
            response = response = requests.get("http://api.hroton.cn:16680/api/servercore/CoreList.json")
        response.encoding = "utf-8"
        corelist_json = response.text
        import json
        corelist_json_data = json.loads(corelist_json)
        files_list = corelist_json_data.get("files", [])

        links = []
        filenames = []
        for file_info in files_list:
            file_link = file_info.get("link")
            file_name = file_info.get("filename")
            if file_link:
                links.append(file_link)
            else:
                log("warning", "文件不存在")
            if file_name:
                filenames.append(file_name)
                print(file_name)
        return filenames
    


    def read_stream(stream, callback):
        with stream:
            for line in iter(stream.readline, ''):
                callback(line.strip('\n'))


    def DownloadCore(self,check=True):
        self.getcorelist(self)
        import tqdm
        global corename
        corename = input("请输入您要下载的服务端名称(与文件名保持一致)：")
        
        if corename in self.getcorelist(self):
            log("info", "正在下载服务端")
            corelink = f"http://hroton.cn/api/servercore/{corename}"
            response = requests.get(corelink, stream=True)
            if response.status_code != 200:
                response = response = requests.get(f"http://api.hroton.cn:16680/api/servercore/{corename}")
            content_size = int(response.headers['Content-Length'])/1024
            if os.path.exists(f"./{name}") == False:
                os.mkdir(name)
            else:
                log(3, "服务器文件夹已存在！")
                Main.Menu(Main)
            with open(f"./{name}/{corename}", "wb") as file:
               for data in tqdm.tqdm(iterable=response.iter_content(chunk_size=1024), total=content_size, unit='KB',desc="正在下载服务端"):
                   file.write(data)
            log("info", "下载完成！")
            if check:
                self.CheckServer(self)
            else:
                Main.Menu(Main)
        else:
            log("warning", "未找到该服务端！")
            Main.Menu(self)


    def CheckServer(self):
        Table = table.Table(show_header=True, header_style="bold magenta")
        Table.add_column("服务器名称", style="cyan", width=12)
        Table.add_column("最小内存", style="yellow", width=12)
        Table.add_column("最大内存", style="green", width=12)

        Table.add_row(name,MinimumMemory,MaximumMemory)
        console.print(Table)
        Choose = console.input("[blod blue]请确定以上信息是否无误，确认即代表您同意Minecraft的最终用户协议(Y/N):")
        if Choose == "Y" or Choose == "y":
            log("info", "正在启动服务器")
            self.StartServer(self)
        elif Choose == "N" or Choose == "n":
            log("info", "正在回到主菜单")
            Main.Menu(self)
        elif Choose == "0":
            Main.Menu(self)
        else:
            log("warning", "无效的字符！")
            self.CheckServer(self)

    def StartServer(self):
        if os.path.exists(f"./{name}/eula.txt"):
            os.remove(f"./{name}/eula.txt")
        with open("eula.txt","w",encoding="utf-8") as file:
            file.write("# By changing the setting below to TRUE you are indicating your agreement to our EULA (https://account.mojang.com/documents/minecraft_eula).\n #Change By HrotonLauncher-Terminal\neula=true") 
        log("info", "正在启动服务器")
        command = (f"java -Xmx{MaximumMemory}M -Xms{MinimumMemory}M -jar ./{name}/{corename} nogui")
        global stdout,stderr
        try:   

            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True,encoding="utf-8",errors='ignore')
            log("info", f"已执行命令:{command}")
            log("info", f"进程ID:{process.pid}")

            def read_stream(stream, callback):
                with stream:
                    for line in iter(stream.readline, ''):
                        callback(line.strip('\n'))
                    
            def log_stdout(line):
                console.print(f"{line.strip()}")
                if "Done" in line:
                    word = corename.split("-")
                    log("info", "服务器启动成功！")
                    log("info", f"端口默认为25565,已在127.0.0.1上运行")
                    log("info", f"最大内存已经设置为{MaximumMemory}MB，最小内存已经设置为{MinimumMemory}MB")
                    log("info", f"版本为{word[1]}")
                    log("info", f"服务器服务端为{word[0]}")

 
            def log_stderr(line):
                console.print(f"{line.strip()}")


            stdout_thread = threading.Thread(target=read_stream, args=(process.stdout, log_stdout)).start()
            stderr_thread = threading.Thread(target=read_stream, args=(process.stderr, log_stderr)).start()
            process.wait()



            stdout, stderr = process.communicate()

            if process.returncode != 0:
                        log("error", f"进程退出，返回值为{process.returncode}")
                        log("error", f"标准错误：{stderr}")
                        log("error", "正在退出")
                        Main.Menu(Main)

        except subprocess.CalledProcessError as e:
            log("error", f"启动时发生错误")
            Main.Menu(Main)

if __name__ == "__main__":
    init()
    Main.Menu(Main)

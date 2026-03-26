import tkinter as tk
from tkinter import ttk, messagebox
import threading
import os
import subprocess
import zipfile
import shutil
from datetime import datetime

class SoundCloudApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("SoundCloud Playlist Downloader")
        self.window.geometry("600x400")
        self.window.configure(bg='#2b2b2b')
        self.window.resizable(False, False)
        
        style = ttk.Style()
        style.configure('TFrame', background='#2b2b2b')
        style.configure('TLabel', background='#2b2b2b', foreground='white')
        style.configure('TButton', background='#404040', foreground='white')
        
        main_frame = tk.Frame(self.window, bg='#2b2b2b')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(main_frame, text="SoundCloud Playlist Downloader", 
                font=('Arial', 16, 'bold'), bg='#2b2b2b', fg='#ff6b35').pack(pady=(0, 20))
        
        tk.Label(main_frame, text="Paste Playlist URL:", 
                font=('Arial', 10), bg='#2b2b2b', fg='white').pack(anchor='w')
        
        self.url_entry = tk.Entry(main_frame, font=('Arial', 12), bg='#1a1a1a', 
                                  fg='white', insertbackground='white', bd=0)
        self.url_entry.pack(fill='x', pady=(5, 15))
        
        self.download_btn = tk.Button(main_frame, text="FETCH & DOWNLOAD", 
                                     font=('Arial', 12, 'bold'), bg='#ff6b35', fg='white',
                                     activebackground='#ff8c5a', activeforeground='white',
                                     bd=0, padx=20, pady=10, cursor='hand2',
                                     command=self.start_download)
        self.download_btn.pack(pady=(0, 10))
        
        self.status_label = tk.Label(main_frame, text="", font=('Arial', 10),
                                     bg='#2b2b2b', fg='#888888')
        self.status_label.pack()
        
        self.progress_label = tk.Label(main_frame, text="", font=('Arial', 10),
                                       bg='#2b2b2b', fg='#ff6b35')
        self.progress_label.pack(pady=(10, 0))
        
        self.text_area = tk.Text(main_frame, font=('Courier', 9), bg='#1a1a1a',
                                  fg='#00ff00', bd=0, state='disabled', height=12)
        self.text_area.pack(fill='both', expand=True, pady=(15, 0))
        
        scrollbar = tk.Scrollbar(self.text_area, command=self.text_area.yview)
        scrollbar.pack(side='right', fill='y')
        self.text_area.config(yscrollcommand=scrollbar.set)
        
        self.download_dir = os.path.join(os.path.expanduser("~"), "SoundCloudDownloads")
        os.makedirs(self.download_dir, exist_ok=True)
        
        self.log(f"Download folder: {self.download_dir}")
        
        self.window.mainloop()
    
    def log(self, message):
        self.text_area.config(state='normal')
        self.text_area.insert('end', message + '\n')
        self.text_area.see('end')
        self.text_area.config(state='disabled')
        self.text_area.update()
    
    def set_status(self, message, color='#888888'):
        self.status_label.config(text=message, fg=color)
    
    def set_progress(self, message):
        self.progress_label.config(text=message)
        self.progress_label.update()
    
    def start_download(self):
        url = self.url_entry.get().strip()
        
        if not url or 'soundcloud.com' not in url:
            messagebox.showerror("Error", "Please enter a valid SoundCloud playlist URL")
            return
        
        self.download_btn.config(state='disabled', text="DOWNLOADING...")
        self.url_entry.config(state='disabled')
        
        thread = threading.Thread(target=self.download_playlist, args=(url,))
        thread.daemon = True
        thread.start()
    
    def download_playlist(self, url):
        try:
            self.log("=" * 50)
            self.log(f"Download folder: {self.download_dir}")
            self.log("=" * 50)
            self.log(f"Starting download at {datetime.now().strftime('%H:%M:%S')}")
            self.log("=" * 50)
            
            self.set_status("Fetching playlist info...")
            self.set_progress("Step 1/3: Analyzing playlist...")
            
            yt_dlp_path = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Python", "Python314", "Scripts", "yt-dlp.exe")
            
            result = subprocess.run(
                [yt_dlp_path, '--flat-playlist', '-J', url],
                capture_output=True, text=True, timeout=60
            )
            
            import json
            info = json.loads(result.stdout)
            playlist_title = info.get('title', 'Unknown_Playlist')
            entries = info.get('entries') or []
            total = len(entries)
            
            self.log(f"\nPlaylist: {playlist_title}")
            self.log(f"Total tracks: {total}")
            self.log("-" * 50)
            
            safe_title = "".join(c if c.isalnum() or c in ' -_' else '_' for c in playlist_title)
            session_dir = os.path.join(self.download_dir, safe_title)
            os.makedirs(session_dir, exist_ok=True)
            
            self.set_status(f"Found {total} tracks", '#00ff00')
            self.set_progress(f"Step 2/3: Downloading {total} tracks...")
            
            self.log("\nDownloading tracks...")
            
            download_cmd = [
                yt_dlp_path,
                '-x', '--audio-format', 'mp3',
                '--audio-quality', '0',
                '-o', os.path.join(session_dir, '%(playlist_index)03d - %(title)s.%(ext)s'),
                url
            ]
            
            process = subprocess.Popen(download_cmd, stdout=subprocess.PIPE, 
                                       stderr=subprocess.STDOUT, text=True)
            
            if process.stdout:
                for line in process.stdout:
                    line = line.strip()
                    if line:
                        self.log(line)
            
            process.wait()
            
            if process.returncode != 0:
                self.log(f"Download process returned: {process.returncode}")
            
            all_files = os.listdir(session_dir)
            self.log(f"\nAll files in folder: {all_files}")
            mp3_files = [f for f in all_files if f.endswith('.mp3') or f.endswith('.m4a') or f.endswith('.wav')]
            self.log(f"Downloaded: {len(mp3_files)} files")
            
            if mp3_files:
                self.set_progress("Step 3/3: Creating ZIP file...")
                self.log("\nCreating ZIP archive...")
                
                zip_path = os.path.join(self.download_dir, f"{safe_title}.zip")
                try:
                    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                        for f in mp3_files:
                            file_path = os.path.join(session_dir, f)
                            arcname = f
                            zipf.write(file_path, arcname)
                    
                    zip_size = os.path.getsize(zip_path) / (1024 * 1024)
                    self.log(f"ZIP created: {zip_path}")
                    self.log(f"ZIP size: {zip_size:.2f} MB")
                    
                    self.log("\nCleaning up temp files...")
                    shutil.rmtree(session_dir)
                    
                    self.log(f"\nZIP saved to: {zip_path}")
                    self.set_status(f"Done! {zip_path}", '#00ff00')
                except Exception as zip_err:
                    self.log(f"ZIP error: {zip_err}")
                    self.set_status(f"ZIP failed, files in folder", '#ffaa00')
            else:
                self.log("No files downloaded - check logs above")
                self.set_status("Download failed", '#ff4444')
            
            self.log("\n" + "=" * 50)
            self.log("COMPLETE")
            self.log("=" * 50)
            
        except subprocess.TimeoutExpired:
            self.log("ERROR: Operation timed out")
            self.set_status("Timeout error", '#ff4444')
        except Exception as e:
            self.log(f"ERROR: {str(e)}")
            self.set_status(f"Error: {str(e)}", '#ff4444')
        finally:
            self.download_btn.config(state='normal', text="FETCH & DOWNLOAD")
            self.url_entry.config(state='normal')

if __name__ == "__main__":
    SoundCloudApp()

import tkinter as tk
from tkinter import ttk, simpledialog
from pypresence import Presence
import time
from urllib.request import urlopen
from PIL import Image, ImageTk  
import pystray
from pystray import MenuItem as item
import os
import json

class DiscordCustomActivity:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  

        self.client_id = simpledialog.askstring("Client ID", "Enter your Discord application client ID:")
        if not self.client_id:
            self.root.destroy()
            return

        self.RPC = Presence(self.client_id)
        self.RPC.connect()

        self.root.deiconify() 
        self.root.title("Discord Custom Activity")
        self.root.attributes('-fullscreen', True) 

        self.root.configure(bg="#2C2F33")  

        icon_url = "https://www.amwp.website/image/logo.png"
        icon_image = Image.open(urlopen(icon_url))
        icon_photo = ImageTk.PhotoImage(icon_image)
        self.root.iconphoto(False, icon_photo)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", background="#2C2F33", foreground="#FFFFFF", font=("Segoe UI", 10))
        style.configure("TEntry", fieldbackground="#23272A", foreground="#FFFFFF", insertcolor="#FFFFFF", padding=5, relief="flat", font=("Segoe UI", 10))
        style.configure("TCombobox", fieldbackground="#23272A", foreground="#FFFFFF", background="#23272A", arrowcolor="#FFFFFF", font=("Segoe UI", 10))
        style.configure("TButton", background="#7289DA", foreground="#FFFFFF", padding=5, relief="flat", font=("Segoe UI", 10, "bold"))
        style.map("TButton", background=[("active", "#99AAB5")])

        self.activity_type = tk.StringVar(value="Playing")
        self.activity_text = tk.StringVar(value="彼女を取り戻すために、どんな壁でも乗り越える")
        self.activity_name = tk.StringVar(value="僕は誰にも負けたくない")
        self.button_label1 = tk.StringVar(value="GitHub")
        self.button_url1 = tk.StringVar(value="https://github.com/ItzApipAjalah")
        self.button_label2 = tk.StringVar(value="Website")
        self.button_url2 = tk.StringVar(value="https://example.com")
        self.timestamp = tk.BooleanVar(value=True) 
        self.large_image_url = tk.StringVar(value="")
        self.large_image_text = tk.StringVar(value="") 
        self.small_image_url = tk.StringVar(value="") 
        self.small_image_text = tk.StringVar(value="")  

        self.load_config()

        self.create_widgets()
        self.create_tray_icon()

    def create_widgets(self):
        ttk.Label(self.root, text="Activity Type:").pack(pady=5)
        ttk.Combobox(self.root, textvariable=self.activity_type, 
                     values=["Playing", "Listening to", "Watching"]).pack(pady=5)

        ttk.Label(self.root, text="Activity Text:").pack(pady=5)
        ttk.Entry(self.root, textvariable=self.activity_text).pack(pady=5, fill=tk.X)

        ttk.Label(self.root, text="Description:").pack(pady=5)
        ttk.Entry(self.root, textvariable=self.activity_name).pack(pady=5, fill=tk.X)

        ttk.Label(self.root, text="Large Image URL:").pack(pady=5)
        ttk.Entry(self.root, textvariable=self.large_image_url).pack(pady=5, fill=tk.X)

        ttk.Label(self.root, text="Large Image Description:").pack(pady=5)
        ttk.Entry(self.root, textvariable=self.large_image_text).pack(pady=5, fill=tk.X)

        ttk.Label(self.root, text="Small Image URL:").pack(pady=5)
        ttk.Entry(self.root, textvariable=self.small_image_url).pack(pady=5, fill=tk.X)

        ttk.Label(self.root, text="Small Image Description:").pack(pady=5)
        ttk.Entry(self.root, textvariable=self.small_image_text).pack(pady=5, fill=tk.X)

        ttk.Label(self.root, text="Button 1 Label:").pack(pady=5)
        ttk.Entry(self.root, textvariable=self.button_label1).pack(pady=5, fill=tk.X)

        ttk.Label(self.root, text="Button 1 URL:").pack(pady=5)
        ttk.Entry(self.root, textvariable=self.button_url1).pack(pady=5, fill=tk.X)

        ttk.Label(self.root, text="Button 2 Label:").pack(pady=5)
        ttk.Entry(self.root, textvariable=self.button_label2).pack(pady=5, fill=tk.X)

        ttk.Label(self.root, text="Button 2 URL:").pack(pady=5)
        ttk.Entry(self.root, textvariable=self.button_url2).pack(pady=5, fill=tk.X)

        ttk.Checkbutton(self.root, text="Include Timestamp", variable=self.timestamp).pack(pady=5)

        ttk.Button(self.root, text="Set Activity", command=self.set_activity).pack(pady=10, fill=tk.X)
        ttk.Button(self.root, text="Clear Activity", command=self.clear_activity).pack(pady=5, fill=tk.X)

        ttk.Button(self.root, text="Hide to Tray", command=self.hide_to_tray).pack(pady=5, fill=tk.X)
        
        ttk.Button(self.root, text="Exit", command=self.exit_app).pack(pady=5, fill=tk.X)

        ttk.Label(self.root, text="Status:").pack(pady=5)
        self.status_label = ttk.Label(self.root, text="Connected")
        self.status_label.pack(pady=5, fill=tk.X)

    def set_activity(self):
        activity_type = self.activity_type.get()
        text = self.activity_text.get()
        name = self.activity_name.get()
        button_label1 = self.button_label1.get()
        button_url1 = self.button_url1.get()
        button_label2 = self.button_label2.get()
        button_url2 = self.button_url2.get()
        include_timestamp = self.timestamp.get()
        large_image = self.large_image_url.get()
        large_text = self.large_image_text.get()
        small_image = self.small_image_url.get()
        small_text = self.small_image_text.get()

        if len(text) < 2:
            self.status_label.config(text="Error: Activity text must be at least 2 characters long")
            return

        if (button_url1 and not button_url1.startswith("https://")) or (button_url2 and not button_url2.startswith("https://")):
            self.status_label.config(text="Error: URLs must start with 'https://'")
            return

        buttons = []
        if button_label1 and button_url1:
            buttons.append({"label": button_label1, "url": button_url1})
        if button_label2 and button_url2:
            buttons.append({"label": button_label2, "url": button_url2})

        timestamp = int(time.time()) if include_timestamp else None

        try:
            if activity_type == "Playing":
                self.RPC.update(state=text, details=name, large_image=large_image, large_text=large_text,
                                small_image=small_image, small_text=small_text, buttons=buttons if buttons else None, start=timestamp)
            elif activity_type == "Listening to":
                self.RPC.update(state=text, details=f"Listening to {name}", large_image=large_image, large_text=large_text,
                                small_image=small_image, small_text=small_text, buttons=buttons if buttons else None, start=timestamp)
            elif activity_type == "Watching":
                self.RPC.update(state=text, details=f"Watching {name}", large_image=large_image, large_text=large_text,
                                small_image=small_image, small_text=small_text, buttons=buttons if buttons else None, start=timestamp)

            self.status_label.config(text=f"Activity set: {name} {activity_type} {text}")
            self.save_config()
        except Exception as e:
            self.status_label.config(text=f"Error: {e}")

    def clear_activity(self):
        self.RPC.clear()
        self.status_label.config(text="Activity cleared")

    def hide_to_tray(self):
        self.root.withdraw()
        self.tray_icon.run()

    def exit_app(self):
        self.root.quit()

    def show_window(self, icon, item):
        self.root.deiconify()
        self.tray_icon.stop()

    def quit_app(self, icon, item):
        self.tray_icon.stop()
        self.root.quit()

    def create_tray_icon(self):
        image = Image.open(urlopen("https://www.amwp.website/image/logo.png"))
        menu = (item('Show', self.show_window), item('Quit', self.quit_app))
        self.tray_icon = pystray.Icon("DiscordCustomActivity", image, "Discord Custom Activity", menu)

    def save_config(self):
        config = {
            "activity_type": self.activity_type.get(),
            "activity_text": self.activity_text.get(),
            "activity_name": self.activity_name.get(),
            "button_label1": self.button_label1.get(),
            "button_url1": self.button_url1.get(),
            "button_label2": self.button_label2.get(),
            "button_url2": self.button_url2.get(),
            "timestamp": self.timestamp.get(),
            "large_image_url": self.large_image_url.get(),
            "large_image_text": self.large_image_text.get(),
            "small_image_url": self.small_image_url.get(),
            "small_image_text": self.small_image_text.get()
        }
        appdata_path = os.getenv('APPDATA')
        config_path = os.path.join(appdata_path, 'discord_custom_activity_config.json')
        with open(config_path, 'w') as config_file:
            json.dump(config, config_file)

    def load_config(self):
        appdata_path = os.getenv('APPDATA')
        config_path = os.path.join(appdata_path, 'discord_custom_activity_config.json')
        if os.path.exists(config_path):
            with open(config_path, 'r') as config_file:
                config = json.load(config_file)
                self.activity_type.set(config.get("activity_type", "Playing"))
                self.activity_text.set(config.get("activity_text", "彼女を取り戻すために、どんな壁でも乗り越える"))
                self.activity_name.set(config.get("activity_name", "僕は誰にも負けたくない"))
                self.button_label1.set(config.get("button_label1", "GitHub"))
                self.button_url1.set(config.get("button_url1", "https://github.com/ItzApipAjalah"))
                self.button_label2.set(config.get("button_label2", "Website"))
                self.button_url2.set(config.get("button_url2", "https://example.com"))
                self.timestamp.set(config.get("timestamp", True))
                self.large_image_url.set(config.get("large_image_url", ""))
                self.large_image_text.set(config.get("large_image_text", ""))
                self.small_image_url.set(config.get("small_image_url", ""))
                self.small_image_text.set(config.get("small_image_text", ""))

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = DiscordCustomActivity()
    app.run()

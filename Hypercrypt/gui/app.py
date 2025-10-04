import customtkinter as ctk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
from customtkinter import CTkImage
import numpy as np
import os
import json
import random
from datetime import datetime

from core.encryptor import ImageEncryptor
from core.metrics import ImageMetrics

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("HyperCrypt GUI - Samir AMODE MALL")
        self.geometry("1100x700")
        self.resizable(False, False)
        self.configure(bg="#1B2E4B")

        self.image_np = None
        self.displayed_image_np = None
        self.encrypted_image = None
        self.key_info = None
        self.custom_params = None

        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(expand=True, fill="both", padx=10, pady=10)

        self.tab_image = self.tabs.add("📁 Image")
        self.tab_key = self.tabs.add("🔑 Clé")
        self.tab_encrypt = self.tabs.add("🔐 Chiffrement")
        self.tab_decrypt = self.tabs.add("🔓 Déchiffrement")
        self.tab_metrics = self.tabs.add("📊 Analyse")

        self.build_tab_image()
        self.build_tab_key()
        self.build_tab_encrypt()
        self.build_tab_decrypt()
        self.build_tab_metrics()

        # Footer
        footer = ctk.CTkFrame(self, fg_color="#2D2D2D")
        footer.pack(side="bottom", fill="x", pady=5)

        logo1_path = os.path.join(os.path.dirname(__file__), "logo_ecole1.png")
        logo2_path = os.path.join(os.path.dirname(__file__), "logo_ecole2.jpeg")

        img1 = CTkImage(light_image=Image.open(logo1_path), size=(60, 60))
        img2 = CTkImage(light_image=Image.open(logo2_path), size=(60, 60))

        logo_frame = ctk.CTkFrame(footer, fg_color="transparent")
        logo_frame.pack(pady=5, fill="x")

        ctk.CTkLabel(logo_frame, image=img1, text="").pack(side="left", padx=20)
        ctk.CTkLabel(logo_frame, text="Fait par AMODE MALL Samir", font=("Helvetica", 12, "italic"),
                     text_color="#F4F4F4").pack(side="left", expand=True)
        ctk.CTkLabel(logo_frame, image=img2, text="").pack(side="right", padx=20)

        self.footer_images = img1, img2

    def build_tab_image(self):
        ctk.CTkLabel(self.tab_image, text="Glissez une image ici ou utilisez le bouton ci-dessous", font=("Arial", 16)).pack(pady=10)
        drop_sim_frame = ctk.CTkFrame(self.tab_image, height=180, fg_color="#2D2D2D", corner_radius=12)
        drop_sim_frame.pack(padx=30, pady=10, fill="x")
        ctk.CTkLabel(drop_sim_frame, text="🖼️ Glissez une image ici", font=("Arial", 14, "italic"), text_color="#F4F4F4").pack(pady=40)
        ctk.CTkButton(self.tab_image, text="📂 Charger une image", command=self.load_image).pack(pady=10)
        ctk.CTkButton(self.tab_image, text="💾 Sauvegarder l'image affichée", command=self.save_displayed_image).pack(pady=10)
        self.image_display = ctk.CTkLabel(self.tab_image, text="")
        self.image_display.pack(pady=10)
        self.image_encrypt_preview = ctk.CTkLabel(self.tab_encrypt, text="")
        self.image_encrypt_preview.pack(pady=10)
        self.image_decrypt_preview = ctk.CTkLabel(self.tab_decrypt, text="")
        self.image_decrypt_preview.pack(pady=10)

    def build_tab_key(self):
        ctk.CTkButton(self.tab_key, text="📁 Charger clé", command=self.load_key).pack(pady=10)
        ctk.CTkButton(self.tab_key, text="🔄 Générer et sauvegarder", command=self.generate_and_save_key).pack(pady=10)
        self.key_box = ctk.CTkTextbox(self.tab_key, height=180)
        self.key_box.pack(padx=20, pady=10, fill="both")
        self.key_box.configure(state="disabled")

    def build_tab_encrypt(self):
        ctk.CTkButton(self.tab_encrypt, text="🔐 Chiffrer l'image", command=self.encrypt_image).pack(pady=20)

    def build_tab_decrypt(self):
        ctk.CTkButton(self.tab_decrypt, text="🔓 Déchiffrer avec session", command=self.decrypt_image).pack(pady=10)
        ctk.CTkButton(self.tab_decrypt, text="🔑 Déchiffrer depuis clé", command=self.decrypt_from_key).pack(pady=10)

    def build_tab_metrics(self):
        ctk.CTkButton(self.tab_metrics, text="📊 Afficher métriques", command=self.show_metrics).pack(pady=10)
        ctk.CTkButton(self.tab_metrics, text="🖼️ Comparer visuellement", command=self.compare_images).pack(pady=10)
        ctk.CTkButton(self.tab_metrics, text="💾 Sauvegarder comparaison", command=self.save_comparison_images).pack(pady=10)

    def load_image(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg")])
        if path:
            self.load_image_from_path(path)

    def load_image_from_path(self, path):
        image = Image.open(path).convert("RGB")
        self.image_np = np.array(image)
        self.encrypted_image = self.image_np
        self.display_image(self.image_np)

    def display_image(self, img_np):
        self.displayed_image_np = img_np
        image = Image.fromarray(img_np)
        image.thumbnail((400, 400))
        tk_img = ImageTk.PhotoImage(image)
        self.image_display.configure(image=tk_img, text="")
        self.image_display.image = tk_img
        self.image_encrypt_preview.configure(image=tk_img, text="")
        self.image_encrypt_preview.image = tk_img
        self.image_decrypt_preview.configure(image=tk_img, text="")
        self.image_decrypt_preview.image = tk_img

    def save_displayed_image(self):
        if self.displayed_image_np is None:
            return
        path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if path:
            Image.fromarray(self.displayed_image_np).save(path)

    def load_key(self):
        path = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if path:
            with open(path, 'r') as f:
                data = json.load(f)
                # Compatible avec anciennes et nouvelles clés
                if "params" in data:
                    self.custom_params = data["params"]
                else:
                    self.custom_params = data
            self.display_key(self.custom_params)

    def generate_and_save_key(self):
        params = {
            "a": round(random.uniform(20, 40), 6),
            "b": round(random.uniform(1, 5), 6),
            "c": round(random.uniform(10, 30), 6),
            "d": round(random.uniform(0.1, 1.0), 6),
            "e": round(random.uniform(1.0, 3.0), 6),
            "f": round(random.uniform(1.0, 2.0), 6),
            "x0": round(random.uniform(0.01, 0.5), 6),
            "y0": round(random.uniform(0.01, 0.5), 6),
            "z0": round(random.uniform(0.01, 0.5), 6),
            "u0": round(random.uniform(0.01, 0.5), 6),
            "v0": round(random.uniform(0.01, 0.5), 6),
            "w0": round(random.uniform(0.01, 0.5), 6),
            "h": 0.001,
            "quant_seed": random.randint(10000, 99999)  # Ajout d'une graine quantique
        }
        path = filedialog.asksaveasfilename(defaultextension=".json")
        if path:
            with open(path, 'w') as f:
                json.dump(params, f, indent=4)
            self.custom_params = params
            self.display_key(params)

    def display_key(self, params):
        self.key_box.configure(state="normal")
        self.key_box.delete("1.0", "end")
        for k, v in params.items():
            self.key_box.insert("end", f"{k} = {v}\n")
        if "quant_seed" in params:
            self.key_box.insert("end", "\n🔬 Clé quantique activée\n")
        self.key_box.configure(state="disabled")

    def encrypt_image(self):
        if self.image_np is None or self.custom_params is None:
            return
        encryptor = ImageEncryptor(self.custom_params)
        self.encrypted_image, self.key_info = encryptor.encrypt(self.image_np)
        self.display_image(self.encrypted_image)

    def decrypt_image(self):
        if self.encrypted_image is None or self.key_info is None:
            return
        decryptor = ImageEncryptor(self.custom_params)
        decrypted = decryptor.decrypt(self.encrypted_image, **self.key_info)
        self.display_image(decrypted)

    def decrypt_from_key(self):
        if self.encrypted_image is None or self.custom_params is None:
            return
        decryptor = ImageEncryptor(self.custom_params)
        decrypted = decryptor.decrypt(self.encrypted_image, auto_recompute=True)
        self.display_image(decrypted)

    def show_metrics(self):
        if self.image_np is None or self.encrypted_image is None:
            return

        npcr = ImageMetrics.npcr(self.image_np, self.encrypted_image)
        uaci = ImageMetrics.uaci(self.image_np, self.encrypted_image)
        entropy = ImageMetrics.entropy(self.encrypted_image)

        win = ctk.CTkToplevel(self)
        win.title("Métriques de sécurité")
        win.geometry("400x220")
        win.resizable(False, False)

        ctk.CTkLabel(win, text="📊 Résultats des métriques", font=("Arial", 18, "bold"), text_color="#FFA726").pack(pady=15)
        ctk.CTkLabel(win, text=f"NPCR : {npcr:.2f}%", font=("Arial", 14)).pack(pady=5)
        ctk.CTkLabel(win, text=f"UACI : {uaci:.2f}%", font=("Arial", 14)).pack(pady=5)
        ctk.CTkLabel(win, text=f"Entropie R : {entropy[0]:.2f}", font=("Arial", 14)).pack(pady=2)
        ctk.CTkLabel(win, text=f"Entropie G : {entropy[1]:.2f}", font=("Arial", 14)).pack(pady=2)
        ctk.CTkLabel(win, text=f"Entropie B : {entropy[2]:.2f}", font=("Arial", 14)).pack(pady=2)
        ctk.CTkButton(win, text="Fermer", command=win.destroy).pack(pady=10)

    def compare_images(self):
        if self.image_np is None or self.encrypted_image is None or self.key_info is None:
            return
        decrypted = ImageEncryptor(self.custom_params).decrypt(self.encrypted_image, **self.key_info)
        win = ctk.CTkToplevel(self)
        win.geometry("850x300")
        win.title("Comparaison visuelle")

        def resize(img_np):
            img = Image.fromarray(img_np)
            img.thumbnail((250, 250))
            return ImageTk.PhotoImage(img)

        img1 = resize(self.image_np)
        img2 = resize(self.encrypted_image)
        img3 = resize(decrypted)

        ctk.CTkLabel(win, text="Originale").grid(row=0, column=0)
        ctk.CTkLabel(win, text="Chiffrée").grid(row=0, column=1)
        ctk.CTkLabel(win, text="Déchiffrée").grid(row=0, column=2)
        ctk.CTkLabel(win, image=img1, text="").grid(row=1, column=0)
        ctk.CTkLabel(win, image=img2, text="").grid(row=1, column=1)
        ctk.CTkLabel(win, image=img3, text="").grid(row=1, column=2)
        win.img1, win.img2, win.img3 = img1, img2, img3

    def save_comparison_images(self):
        if self.image_np is None or self.encrypted_image is None or self.key_info is None:
            return
        base = filedialog.askdirectory(title="Choisir un dossier")
        if not base:
            return
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        decrypted = ImageEncryptor(self.custom_params).decrypt(self.encrypted_image, **self.key_info)
        Image.fromarray(self.image_np).save(os.path.join(base, f"original_{now}.png"))
        Image.fromarray(self.encrypted_image).save(os.path.join(base, f"chiffree_{now}.png"))
        Image.fromarray(decrypted).save(os.path.join(base, f"dechiffree_{now}.png"))


if __name__ == "__main__":
    app = App()
    app.mainloop()

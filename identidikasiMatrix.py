import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import csv


class ImageMatrixApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Identifikasi Nilai Matriks Citra Grayscale")

        # Frame tombol
        frame_buttons = tk.Frame(root)
        frame_buttons.pack(pady=10)

        btn_open = tk.Button(frame_buttons, text="Buka Gambar", command=self.open_image)
        btn_open.pack(side=tk.LEFT, padx=5)

        btn_show_matrix = tk.Button(frame_buttons, text="Tampilkan Matriks", command=self.show_matrix)
        btn_show_matrix.pack(side=tk.LEFT, padx=5)

        btn_save_csv = tk.Button(frame_buttons, text="Simpan CSV", command=self.save_csv)
        btn_save_csv.pack(side=tk.LEFT, padx=5)

        # Canvas untuk gambar
        self.canvas = tk.Label(root)
        self.canvas.pack()

        # Textbox matriks
        self.text_matrix = tk.Text(root, width=80, height=20)
        self.text_matrix.pack(pady=10)

        self.img_array = None

    def open_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg;*.png;*.bmp;*.jpeg")]
        )
        if not file_path:
            return

        try:
            img = Image.open(file_path).convert("L")  # konversi grayscale
            self.img_array = np.array(img)

            # Resize agar pas ditampilkan
            img_resized = img.resize((250, 250))
            self.tk_img = ImageTk.PhotoImage(img_resized)
            self.canvas.config(image=self.tk_img)

            self.text_matrix.delete(1.0, tk.END)
            self.text_matrix.insert(tk.END, "Gambar berhasil dimuat.\nKlik 'Tampilkan Matriks' atau 'Simpan CSV'.")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal membuka gambar: {e}")

    def show_matrix(self):
        if self.img_array is None:
            messagebox.showwarning("Peringatan", "Silakan buka gambar terlebih dahulu.")
            return

        self.text_matrix.delete(1.0, tk.END)
        for row in self.img_array:
            row_str = " ".join([f"{val:3}" for val in row])
            self.text_matrix.insert(tk.END, row_str + "\n")

    def save_csv(self):
        if self.img_array is None:
            messagebox.showwarning("Peringatan", "Silakan buka gambar terlebih dahulu.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")]
        )
        if not file_path:
            return

        try:
            with open(file_path, mode="w", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(self.img_array)
            messagebox.showinfo("Sukses", f"Matriks berhasil disimpan ke {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan CSV: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageMatrixApp(root)
    root.mainloop()

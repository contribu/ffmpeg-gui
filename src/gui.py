import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from .converter import convert_files

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("音楽ファイル変換アプリ")

        self.input_dir_label = tk.Label(self.root, text="入力ディレクトリ:")
        self.input_dir_label.pack()
        self.input_dir_entry = tk.Entry(self.root, width=50)
        self.input_dir_entry.pack()
        self.input_dir_button = tk.Button(self.root, text="参照", command=self.select_input_dir)
        self.input_dir_button.pack()

        self.output_dir_label = tk.Label(self.root, text="出力ディレクトリ:")
        self.output_dir_label.pack()
        self.output_dir_entry = tk.Entry(self.root, width=50)
        self.output_dir_entry.pack()
        self.output_dir_button = tk.Button(self.root, text="参照", command=self.select_output_dir)
        self.output_dir_button.pack()

        self.run_button = tk.Button(self.root, text="実行", command=self.start_conversion)
        self.run_button.pack()

        self.progress = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.root, variable=self.progress, maximum=100)
        self.progress_bar.pack(fill=tk.X, padx=10, pady=10)

        self.log_text = tk.Text(self.root, height=10, state="disabled")
        self.log_text.pack(fill=tk.BOTH, padx=10, pady=10)

    def select_input_dir(self):
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.input_dir_entry.delete(0, tk.END)
            self.input_dir_entry.insert(0, dir_path)

    def select_output_dir(self):
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.output_dir_entry.delete(0, tk.END)
            self.output_dir_entry.insert(0, dir_path)

    def start_conversion(self):
        input_dir = self.input_dir_entry.get()
        output_dir = self.output_dir_entry.get()
        if not input_dir or not output_dir:
            messagebox.showerror("エラー", "入力と出力ディレクトリを指定してください。")
            return

        self.log_message("変換を開始します...")
        self.run_button.config(state="disabled")

        try:
            convert_files(input_dir, output_dir, progress_callback=self.update_progress, log_callback=self.log_message)
        except subprocess.CalledProcessError:
            messagebox.showerror("変換エラー", "変換中にエラーが発生しました。詳細はログを確認してください。")

        self.run_button.config(state="normal")


    def update_progress(self, progress):
        self.progress.set(progress * 100)
        self.root.update_idletasks()

    def log_message(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")

    def run(self):
        self.root.mainloop()

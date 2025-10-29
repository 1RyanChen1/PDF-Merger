import os
import tkinter as tk
from tkinter import filedialog, messagebox
from pypdf import PdfWriter

class PDFMergerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Meregr")
        self.root.geometry("500x400")

        self.file_list = []

        # File List
        self.listbox = tk.Listbox(root, selectmode=tk.SINGLE, width=60, height=15)
        self.listbox.pack(pady=10)

        #buttons
        btn = tk.Frame(root)
        btn.pack()

        tk.Button(btn, text="Add", command=self.add_files).grid(row=0, column=0, padx=5)
        tk.Button(btn, text="Remove", command=self.remove).grid(row=0, column=1, padx=5)
        tk.Button(btn, text="Move Up", command=self.move_up).grid(row=0, column=2, padx=5)
        tk.Button(btn, text="Move Down", command=self.move_down).grid(row=0, column=3, padx=5)
        tk.Button(btn, text="Merge PDF", command=self.merge).grid(row=0, column=4, padx=5)

    def add_files(self):
        files = filedialog.askopenfilenames(
            title="Choose Files",
            filetypes=[("PDF file", "*.pdf"),("PDF文件", "*.pdf")]
        )
        for f in files:
            if f not in self.file_list:
                self.file_list.append(f)
                self.listbox.insert(tk.END, f)

    def remove(self):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            self.file_list.pop(index)
            self.listbox.delete(index)

    def move_up(self):
        selection = self.listbox.curselection()
        if not selection or selection[0] == 0:
            return
        index = selection[0]
        self.file_list[index-1], self.file_list[index] = self.file_list[index], self.file_list[index-1]
        self.refresh(index-1)

    def move_down(self):
        selection = self.listbox.curselection()
        if not selection or selection[0] == len(self.file_list)-1:
            return
        index = selection[0]
        self.file_list[index+1], self.file_list[index] = self.file_list[index], self.file_list[index+1]
        self.refresh(index+1)

    def refresh(self, new_index=None):
        self.listbox.delete(0, tk.END)
        for f in self.file_list:
            self.listbox.insert(tk.END, f)
        if new_index is not None:
            self.listbox.select_set(new_index)

    def merge(self):
        if not self.file_list:
            messagebox.showwarning("Warning", "Please Add PDF File First")
            return

        output_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF file", "*.pdf"),("PDF文件", "*.pdf")],
            title="Merged PDF Save as"
        )
        if not output_path:
            return

        merger = PdfWriter()
        for pdf in self.file_list:
            merger.append(pdf)

        try:
            with open(output_path, "wb") as f_out:
                merger.write(f_out)
            messagebox.showinfo("Success", f"PDF Merged!\nSaved to\n{output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Fail to Merge{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFMergerGUI(root)
    root.mainloop()

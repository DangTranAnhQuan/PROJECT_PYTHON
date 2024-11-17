import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import numpy as np
def search_data():
    search_term = simpledialog.askstring("Tìm kiếm", "Nhập từ khóa tìm kiếm:")
    if search_term:
        filtered_df = df[df.apply(lambda row: search_term.lower() in row.astype(str).str.lower().values, axis=1)]
        if filtered_df.empty:
            messagebox.showinfo("Kết quả tìm kiếm", "Không tìm thấy dữ liệu phù hợp.")
        else:
            display_filtered_data(filtered_df)

def display_filtered_data(filtered_df):
    for row in tree.get_children():
        tree.delete(row)
    
    for _, row in filtered_df.iterrows():
        tree.insert("", tk.END, values=list(row))
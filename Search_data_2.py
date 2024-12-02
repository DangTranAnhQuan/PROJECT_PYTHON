import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import numpy as np
from datetime import datetime
def search_data2():
    def apply_search():
        try:
            # Lấy thông tin từ các ô nhập liệu
            column1 = column1_choice.get()
            value1 = value1_entry.get()
            column2 = column2_choice.get()
            value2 = value2_entry.get()

            # Lọc dữ liệu dựa trên điều kiện nhập
            filtered_df = df

            if column1 and value1:
                if column1 in df.columns:
                    filtered_df = filtered_df[filtered_df[column1].astype(str).str.contains(value1, case=False, na=False)]

            if column2 and value2:
                if column2 in df.columns:
                    filtered_df = filtered_df[filtered_df[column2].astype(str).str.contains(value2, case=False, na=False)]

            if filtered_df.empty:
                messagebox.showinfo("Kết quả", "Không có dữ liệu thỏa mãn điều kiện tìm kiếm.")
            else:
                # Hiển thị kết quả tìm kiếm
                display_search_results(filtered_df)
                messagebox.showinfo("Kết quả", "Tìm kiếm thành công.")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")

    # Tạo cửa sổ tìm kiếm
    search_window = tk.Toplevel(root)
    search_window.title("Tìm kiếm dữ liệu")
    search_window.geometry("500x300")

    tk.Label(search_window, text="Chọn cột 1:").pack(pady=5)
    column1_choice = ttk.Combobox(search_window, values=[col for col in df.columns if col not in ["Amount", "Quantity", "Profit"]], state="readonly")
    column1_choice.pack(pady=5)

    tk.Label(search_window, text="Nhập giá trị 1:").pack(pady=5)
    value1_entry = tk.Entry(search_window)
    value1_entry.pack(pady=5)

    tk.Label(search_window, text="Chọn cột 2:").pack(pady=5)
    column2_choice = ttk.Combobox(search_window, values=[col for col in df.columns if col not in ["Amount", "Quantity", "Profit"]], state="readonly")
    column2_choice.pack(pady=5)

    tk.Label(search_window, text="Nhập giá trị 2:").pack(pady=5)
    value2_entry = tk.Entry(search_window)
    value2_entry.pack(pady=5)

    tk.Button(search_window, text="Áp dụng tìm kiếm", command=apply_search).pack(pady=20)

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
from typing import Optional, Callable
from datetime import date, datetime
import os
import sys
import csv

from controllers.users import get_user_by_email
from controllers.listing import listing

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class MainWindow:
    def __init__(self, root: tk.Tk, **kwargs):
        """
        Initialize the login GUI
        
        Args:
            root (tk.Tk): Main tkinter window
        """
        self.root = root
        self.root.title("Buyma 出品 / ホーム")
        try:
            icon_path = resource_path("assets/images/favicon.ico")
            self.root.iconbitmap(icon_path)
        except tk.TclError:
            print("Warning: Could not load application icon.")
        # self.root.iconphoto(False, tk.PhotoImage(file="assets/images/buyma.png"))
        self.root.geometry("800x450")
        self.root.resizable(False, False)
        self.db = kwargs.get('database')  # Store database reference
        self.parent = kwargs.get('parent')
        self.products = self.parent.products
        self.user = self.parent.user
        self.auto_listing = self.parent.auto_listing
        # self.products = []
        # self.user = {
        #     "email": "youdan55@yahoo.co.jp",
        #     "password": "15791579aA"
        # }
        
        # Center the window
        self.center_window()
        
        # Create GUI elements
        self.create_widgets()
        
        # Store callback for successful login
        self.on_login_success: Optional[Callable] = None
        
        self.draw_table()
        
    def center_window(self):
        """Center the window on screen"""
        try:
            # Check if root window still exists and is valid
            if not hasattr(self, 'root') or not self.root or not self.root.winfo_exists():
                print("Warning: Root window not available for centering")
                return
                
            self.root.update_idletasks()
            
            # Get window dimensions safely
            try:
                width = self.root.winfo_width()
                height = self.root.winfo_height()
            except tk.TclError as e:
                print(f"Error getting window dimensions: {e}")
                return
                
            # Get screen dimensions safely
            try:
                screen_width = self.root.winfo_screenwidth()
                screen_height = self.root.winfo_screenheight()
            except tk.TclError as e:
                print(f"Error getting screen dimensions: {e}")
                return
                
            # Calculate position
            x = (screen_width // 2) - (width // 2)
            y = (screen_height // 2) - (height // 2)
            
            # Set geometry safely
            try:
                self.root.geometry(f'{width}x{height}+{x}+{y}')
                print("MainWindow centered successfully")
            except tk.TclError as e:
                print(f"Error setting window geometry: {e}")
                
        except Exception as e:
            print(f"Error in MainWindow center_window: {e}")
            import traceback
            traceback.print_exc()
    
    def create_widgets(self):
        """Create and arrange GUI widgets"""
        # Main Frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # # --- Top Input Fields ---
        # ttk.Label(main_frame, text="BUYMAメールアドレス:").grid(row=0, column=0, sticky="w")
        # self.email_var = tk.StringVar()
        # ttk.Entry(main_frame, textvariable=self.email_var, width=30).grid(row=0, column=1, sticky="ew")

        # ttk.Label(main_frame, text="アクセスコード:").grid(row=1, column=0, sticky="w")
        # self.access_code_var = tk.StringVar()
        # ttk.Entry(main_frame, textvariable=self.access_code_var, width=30).grid(row=1, column=1, sticky="ew")

        # --- CSV Select ---
        ttk.Button(main_frame, text="出品シートを選択", command=self.select_csv).grid(row=0, column=0, pady=5)
        self.csv_file_label = ttk.Label(main_frame, text="未選択")
        self.csv_file_label.grid(row=0, column=1, sticky="w")

        # # --- Table Area ---
        # self.table = ttk.Treeview(main_frame, columns=[], show="headings", height=8)
        # self.table.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=10)
        
         # --- Table Area ---
        table_frame = ttk.Frame(main_frame)
        table_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=10)
        
        # Create Treeview
        self.table = ttk.Treeview(table_frame, columns=[], show="headings", height=8)
        # Map of row_id -> detail message for error rows
        self.row_detail_map = {}
        
        # Create Scrollbars
        y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        x_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=self.table.xview)
        
        self.table.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        # Bind double-click to show detail of error rows
        self.table.bind("<Double-1>", self.on_row_double_click)
        
        # Grid placement
        self.table.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")
        
        # Configure resizing
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        # --- Log Area ---
        self.log_text = tk.Text(main_frame, height=5)
        self.log_text.grid(row=2, column=0, columnspan=2, sticky="ew")
        # Configure tags for colored log messages
        self.log_text.tag_configure("info", foreground="black")
        self.log_text.tag_configure("success", foreground="green")
        self.log_text.tag_configure("error", foreground="red")

        # --- Bottom Buttons ---
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")

        ttk.Button(button_frame, text="エラーを確認", command=self.check_errors).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Q&A", command=self.open_help).pack(side="left", padx=5)
        self.days_var = tk.StringVar(value="30")
        ttk.Entry(button_frame, width=5, textvariable=self.days_var).pack(side="left")
        ttk.Label(button_frame, text="日以内に出した商品は除外する").pack(side="left")

        # self.hide_mode = tk.BooleanVar()
        # ttk.Checkbutton(button_frame, text="非表示モード", variable=self.hide_mode).pack(side="left", padx=5)

        # self.mode = tk.StringVar(value="出品")
        # ttk.Radiobutton(button_frame, text="下書き", variable=self.mode, value="下書き").pack(side="left")
        # ttk.Radiobutton(button_frame, text="出品", variable=self.mode, value="出品").pack(side="left")

        ttk.Button(button_frame, text="開始", command=self.start_process).pack(side="right", padx=10)
        # Add Clear Log button
        ttk.Button(button_frame, text="ログをクリア", command=lambda: self.log_text.delete("1.0", "end")).pack(side="right", padx=5)

        # Padding and resizing
        for i in range(6):
            main_frame.rowconfigure(i, weight=1)

    def select_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.csv_file_label.config(text=file_path.split("/")[-1])
            self.load_csv_to_table(file_path)

    def load_csv_to_table(self, file_path):
        import csv

        # Clear existing rows and columns
        for row in self.table.get_children():
            self.table.delete(row)
        self.table["columns"] = ()
        self.table["show"] = "headings"

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)
            if not rows:
                return  # Empty file

            headers = rows[1]
            self.table["columns"] = headers

            # Set new headings
            for col in headers:
                self.table.heading(col, text=col)
                self.table.column(col, width=120, anchor="center")

            # Insert the rest of the rows
            for row in rows[2:]:
                # Pad row if it's shorter than headers
                if len(row) < len(headers):
                    row += [""] * (len(headers) - len(row))
                self.table.insert("", "end", values=row)
                
    def draw_table(self):
        headers = ["フォルダ名","商品名","ブランド","モデル・ライン","カテゴリ","商品コメント","色・サイズ補足情報","購入期限","仕入先URL","買付地","ショップ名","発送地","仕入先保存","カラー系統","サイズ","シーズン","タグ","テーマ","価格","参考価格","配送方法名","在庫","型番,メモ","関税負担","出品メモ"]
        self.table["columns"] = headers

        # Set new headings
        for col in headers:
            self.table.heading(col, text=col)
            self.table.column(col, width=120, anchor="center")

        # Insert the rest of the rows
        if len(self.products):
            for row in self.products:
                # Pad row if it's shorter than headers
                if len(row) < len(headers):
                    row += [""] * (len(headers) - len(row))
                self.table.insert("", "end", values=row)
        # self.save_list()
        if self.auto_listing:
            self.start_process()
            
    # def save_list(self):
    #     csv_file = "product_list.csv"
        
    #     for product in self.products:
    #         product_id = product[8].split("product-")[-1]
    #         current_date = date.today()
            
    #         # Check if file exists to determine whether to write headers
    #         file_exists = os.path.exists(csv_file)
            
    #         # Open file in append mode ('a') to add new rows
    #         with open(csv_file, 'a', newline='', encoding='utf-8') as file:
    #             writer = csv.writer(file)
                
    #             # Write headers only if file doesn't exist
    #             if not file_exists:
    #                 writer.writerow(['Product ID', 'Date'])
                
    #             # Write the product data
    #             writer.writerow([product_id, current_date])
        
    #     self.log_info(f"Product data saved to {csv_file}")

    
    def log_info(self, message):
        self.log_text.insert("end", message + "\n", "info")
        self.log_text.see("end")

    def log_success(self, message):
        self.log_text.insert("end", message + "\n", "success")
        self.log_text.see("end")

    def log_error(self, message):
        self.log_text.insert("end", message + "\n", "error")
        self.log_text.see("end")

    def check_errors(self):
        self.log_error("Error check not implemented yet")

    def start_process(self):
        self.log_info("Start clicked")
        result = listing(self.products, self.user, logging=self.log_info)
        for index, res in enumerate(result):
            if res["status"] == "error":
                # Color the corresponding row background as yellow
                try:
                    row_ids = self.table.get_children()
                    if 0 <= index < len(row_ids):
                        target_row_id = row_ids[index]
                        # Configure a tag for yellow background (idempotent)
                        self.table.tag_configure("yellow_bg", background="yellow")
                        # Apply the tag to the specific row
                        self.table.item(target_row_id, tags=("yellow_bg",))
                        # Store the detail for this row to show on double-click
                        self.row_detail_map[target_row_id] = res.get("detail", "")
                except Exception as e:
                    print(f"Failed to color row {index}: {e}")

    def on_row_double_click(self, event):
        try:
            # Identify the row under mouse or use current selection
            row_id = self.table.identify_row(event.y)
            if not row_id:
                sel = self.table.selection()
                if sel:
                    row_id = sel[0]
            if not row_id:
                return
            # If this row has an associated detail, show it
            if row_id in self.row_detail_map:
                detail = self.row_detail_map.get(row_id, "")
                if detail:
                    messagebox.showinfo("詳細", detail)
        except Exception as e:
            print(f"Failed to handle double click: {e}")


    def open_help(self):
        messagebox.showinfo("ヘルプ", "Q&A will be added here.")
    
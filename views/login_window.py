import tkinter as tk
from tkinter import ttk, messagebox
import threading
import os
import sys
from typing import Optional, Callable

from controllers.users import get_user_by_email

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class LoginWindow:
    def __init__(self, root: tk.Tk, **kwargs):
        """
        Initialize the login GUI
        
        Args:
            root (tk.Tk): Main tkinter window
        """
        self.root = root
        self.root.title("Buyma 出品 / ログイン")
        try:
            icon_path = resource_path("assets/images/favicon.ico")
            self.root.iconbitmap(icon_path)
        except tk.TclError:
            print("Warning: Could not load application icon.")
        # self.root.iconphoto(False, tk.PhotoImage(file="assets/images/buyma.png"))
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        self.db = kwargs.get('database')  # Store database reference
        self.parent = kwargs.get('parent')
        
        # Center the window
        self.center_window()
        
        # Create GUI elements
        self.create_widgets()
        
        # Store callback for successful login
        self.on_login_success: Optional[Callable] = None
        
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
                print("LoginWindow centered successfully")
            except tk.TclError as e:
                print(f"Error setting window geometry: {e}")
                
        except Exception as e:
            print(f"Error in LoginWindow center_window: {e}")
            import traceback
            traceback.print_exc()
    
    def create_widgets(self):
        """Create and arrange GUI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="ようこそ!", font=("Arial", 24, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        subtitle_label = ttk.Label(main_frame, text="アカウントにログイン", font=("Arial", 12))
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 30))
        
        # Email field
        ttk.Label(main_frame, text="メール:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.email_var = tk.StringVar(value="youdan55@yahoo.co.jp")
        self.email_entry = ttk.Entry(main_frame, textvariable=self.email_var, width=35, font=("Arial", 11))
        self.email_entry.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Password field
        ttk.Label(main_frame, text="パスワード:", font=("Arial", 10, "bold")).grid(row=4, column=0, sticky=tk.W, pady=(0, 5))
        self.password_var = tk.StringVar(value="15791579aA")
        self.password_entry = ttk.Entry(main_frame, textvariable=self.password_var, show="*", width=35, font=("Arial", 11))
        self.password_entry.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Show/Hide password checkbox
        self.show_password_var = tk.BooleanVar()
        show_password_cb = ttk.Checkbutton(main_frame, text="パスワードを表示", variable=self.show_password_var, 
                                          command=self.toggle_password_visibility)
        show_password_cb.grid(row=6, column=0, columnspan=2, pady=(0, 20))
        
        # Login button
        self.login_button = ttk.Button(main_frame, text="ログイン", command=self.login, style="Accent.TButton")
        self.login_button.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=9, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="", font=("Arial", 9))
        self.status_label.grid(row=10, column=0, columnspan=2)
        
        # Bind Enter key to login
        self.root.bind('<Return>', lambda event: self.login())
        
        # Focus on email entry
        self.email_entry.focus()
        
    
    def toggle_password_visibility(self):
        """Toggle password field visibility"""
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")
    
    def login(self):
        """Handle login process"""
        email = self.email_var.get().strip()
        password = self.password_var.get()
        
        # Validation
        if not email or not password:
            messagebox.showerror("エラー", "メールアドレスとパスワードの両方を入力してください.")
            return
        
        if not self.is_valid_email(email):
            messagebox.showerror("エラー", "有効なメールアドレスを入力してください.")
            return
        
        # Start login process in separate thread
        self.set_loading_state(True)

        threading.Thread(target=self.perform_login, args=(email, password), daemon=True).start()
    
    def perform_login(self, email: str, password: str):
        """Perform actual login with Firebase Auth"""
        try:
            # Note: Firebase Admin SDK doesn't support email/password authentication directly
            # You would need to use Firebase Auth REST API or Firebase Auth client SDK
            # For now, we'll simulate the login process
            
            # Simulate API call delay
            import time
            time.sleep(1)

            curUser = get_user_by_email(self.db, email)
            if curUser is None:
                self.root.after(0, self.login_failed, "ユーザーが見つかりません")
                return
            elif curUser['password'] != password:
                self.root.after(0, self.login_failed, "メールアドレスまたはパスワードが無効です")
                return
            elif curUser['status'] != 'active':
                self.root.after(0, self.login_failed, "ユーザーはアクティブではありません")
                return
            else:
                # Simulate successful login
                user_data = {
                    "email": email,
                    "uid": curUser['name'],  # Assuming uid is stored in user document
                    "password": password
                }
                self.root.after(0, self.login_success, user_data)
                
        except Exception as e:
            self.root.after(0, self.login_failed, f"ログイン エラー: {str(e)}")
    
    def login_success(self, user_data: dict):
        """Handle successful login"""
        self.set_loading_state(False)
        messagebox.showinfo("Success", f"ようこそ!, {user_data['uid']}様.")
        
        # Call success callback if provided
        if self.on_login_success:
            self.on_login_success(user_data)
        
        print("LoginWindow: calling parent.show_main_page()")
        # Don't destroy the root window - let the parent handle the transition
        if self.parent:
            print("LoginWindow: calling parent.show_main_page()")
            if user_data['email'] == "admin@gmail.com":
                self.parent.show_register()  # Admin should go to main page, not register
            else:
                self.parent.show_initial_option_window(user_data)
    
    def login_failed(self, error_message: str):
        """Handle failed login"""
        self.set_loading_state(False)
        messagebox.showerror("ログインに失敗しました", error_message)
    
    def set_loading_state(self, loading: bool):
        """Set loading state for UI elements"""
        if loading:
            self.login_button.config(state="disabled")
            self.progress.start()
            self.status_label.config(text="ログインしています...")
        else:
            self.login_button.config(state="normal")
            self.progress.stop()
            self.status_label.config(text="")
    
    def is_valid_email(self, email: str) -> bool:
        """Validate email format"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def set_login_success_callback(self, callback: Callable):
        """Set callback function to be called on successful login"""
        self.on_login_success = callback
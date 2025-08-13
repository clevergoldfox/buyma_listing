import tkinter as tk
from tkinter import ttk, messagebox
import firebase_admin
from firebase_admin import credentials, auth
import threading
import os
import sys
from typing import Optional, Callable

from controllers.users import create_user
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class RegisterWindow:
    def __init__(self, root: tk.Tk, parent, **kwargs):
        """
        Initialize the registration GUI
        
        Args:
            root (tk.Tk): Registration window
            login_window (tk.Tk): Login window to return to
        """
        self.root = root
        self.root.title("Buyma 出品 / ユーザー管理")
        try:
            icon_path = resource_path("assets/images/favicon.ico")
            self.root.iconbitmap(icon_path)
        except tk.TclError:
            print("Warning: Could not load application icon.")
        self.root.geometry("1200x700")
        self.root.resizable(True, True)
        self.db = kwargs.get('database')  # Store database reference
        self.parent = parent
        
        # Edit mode variables
        self.edit_mode = False
        self.current_edit_user_id = None
        
        # Center the window
        self.center_window()
        
        # Create GUI elements
        self.create_widgets()
        
        # Load user data
        self.load_users()
    
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
                print("RegisterWindow centered successfully")
            except tk.TclError as e:
                print(f"Error setting window geometry: {e}")
                
        except Exception as e:
            print(f"Error in RegisterWindow center_window: {e}")
            import traceback
            traceback.print_exc()
    
    def create_widgets(self):
        """Create and arrange GUI widgets"""
        # Main container with two panels
        main_container = ttk.Frame(self.root)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configure grid weights for the container
        main_container.columnconfigure(0, weight=1)  # Left panel (register form)
        main_container.columnconfigure(1, weight=2)  # Right panel (user table)
        main_container.rowconfigure(0, weight=1)
        
        # Left Panel - Registration Form
        left_panel = ttk.LabelFrame(main_container, text="新規ユーザー登録", padding="20")
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Right Panel - User Management Table
        right_panel = ttk.LabelFrame(main_container, text="ユーザー管理", padding="20")
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        # Configure panel weights
        left_panel.columnconfigure(0, weight=1)
        right_panel.columnconfigure(0, weight=1)
        right_panel.rowconfigure(1, weight=1)
        
        # Create registration form widgets
        self.create_register_form(left_panel)
        
        # Create user management table
        self.create_user_table(right_panel)
        
    def create_register_form(self, parent):
        """Create the registration form widgets"""
        # Title
        title_label = ttk.Label(parent, text="新規登録", font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Edit mode status label
        self.edit_status_label = ttk.Label(parent, text="", font=("Arial", 10), foreground="blue")
        self.edit_status_label.grid(row=0, column=1, pady=(0, 10), sticky="e")
        
        subtitle_label = ttk.Label(parent, text="今すぐ参加しましょう!", font=("Arial", 10))
        subtitle_label.grid(row=1, column=0, pady=(0, 20))
        
        # Name field
        ttk.Label(parent, text="フルネーム：", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(parent, textvariable=self.name_var, width=30, font=("Arial", 11))
        self.name_entry.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Email field
        ttk.Label(parent, text="メール:", font=("Arial", 10, "bold")).grid(row=4, column=0, sticky=tk.W, pady=(0, 5))
        self.email_var = tk.StringVar()
        self.email_entry = ttk.Entry(parent, textvariable=self.email_var, width=30, font=("Arial", 11))
        self.email_entry.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Password field
        ttk.Label(parent, text="パスワード:", font=("Arial", 10, "bold")).grid(row=6, column=0, sticky=tk.W, pady=(0, 5))
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(parent, textvariable=self.password_var, show="*", width=30, font=("Arial", 11))
        self.password_entry.grid(row=7, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Confirm Password field
        ttk.Label(parent, text="パスワードを認証する:", font=("Arial", 10, "bold")).grid(row=8, column=0, sticky=tk.W, pady=(0, 5))
        self.confirm_password_var = tk.StringVar()
        self.confirm_password_entry = ttk.Entry(parent, textvariable=self.confirm_password_var, show="*", width=30, font=("Arial", 11))
        self.confirm_password_entry.grid(row=9, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Show/Hide password checkbox
        self.show_password_var = tk.BooleanVar()
        show_password_cb = ttk.Checkbutton(parent, text="パスワードを表示", variable=self.show_password_var, 
                                          command=self.toggle_password_visibility)
        show_password_cb.grid(row=10, column=0, pady=(0, 20))
        
        # Status radio buttons
        ttk.Label(parent, text="ステータス:", font=("Arial", 10, "bold")).grid(row=11, column=0, sticky=tk.W, pady=(0, 5))
        self.status_var = tk.StringVar(value="active")
        
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=12, column=0, sticky="w", pady=(0, 20))
        
        active_radio = ttk.Radiobutton(status_frame, text="アクティブ", variable=self.status_var, value="active")
        active_radio.pack(side="left", padx=(0, 20))
        
        inactive_radio = ttk.Radiobutton(status_frame, text="非アクティブ", variable=self.status_var, value="inactive")
        inactive_radio.pack(side="left")
        
        # Register button
        self.register_button = ttk.Button(parent, text="登録", command=self.register, style="Accent.TButton")
        self.register_button.grid(row=13, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Cancel button (initially hidden)
        self.cancel_button = ttk.Button(parent, text="キャンセル", command=self.cancel_edit)
        self.cancel_button.grid(row=13, column=1, sticky=(tk.W, tk.E), pady=(0, 15))
        self.cancel_button.grid_remove()  # Hide initially
        
        # Back to login button
        self.back_button = ttk.Button(parent, text="ログインに戻る", command=self.back_to_login)
        self.back_button.grid(row=14, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Progress bar
        self.progress = ttk.Progressbar(parent, mode='indeterminate')
        self.progress.grid(row=15, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Status label
        self.status_label = ttk.Label(parent, text="", font=("Arial", 9))
        self.status_label.grid(row=16, column=0)
        
        # Bind Enter key to register
        self.root.bind('<Return>', lambda event: self.register())
        
        # Focus on name entry
        self.name_entry.focus()
    
    def toggle_password_visibility(self):
        """Toggle password field visibility"""
        if self.show_password_var.get():
            self.password_entry.config(show="")
            self.confirm_password_entry.config(show="")
        else:
            self.password_entry.config(show="*")
            self.confirm_password_entry.config(show="*")
    
    def register(self):
        """Handle registration process"""
        name = self.name_var.get().strip()
        email = self.email_var.get().strip()
        password = self.password_var.get()
        confirm_password = self.confirm_password_var.get()
        
        # Validation
        if not all([name, email, password, confirm_password]):
            messagebox.showerror("エラー", "すべての項目にご記入ください")
            return
        
        if not self.is_valid_email(email):
            messagebox.showerror("エラー", "有効なメールアドレスを入力してください")
            return
        
        if len(password) < 6:
            messagebox.showerror("エラー", "パスワードは6文字以上でなければなりません")
            return
        
        if password != confirm_password:
            messagebox.showerror("エラー", "パスワードが一致しません")
            return
        
        # Start registration process in separate thread
        self.set_loading_state(True)
        
        if self.edit_mode:
            # Update existing user
            self.update_user(name, email, password)
        else:
            # Create new user
            self.create_new_user(name, email, password)
            
    def create_new_user(self, name, email, password):
        """Create a new user in the database"""
        # Create user in database
        try:
            from datetime import datetime
            user_data = {
                'name': name,
                'email': email,
                'password': password,  # In production, this should be hashed
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'status': self.status_var.get() # Use selected status
            }
            
            # Add user to database
            users_ref = self.db.collection('users')
            users_ref.add(user_data)
            
            # Clear form
            self.clear_form()
            
            # Refresh user table
            self.load_users()
            
            # Show success message
            messagebox.showinfo("成功", f"{name}様のアカウントが正常に作成されました!")
            
        except Exception as e:
            messagebox.showerror("エラー", f"ユーザー作成に失敗しました: {str(e)}")
        finally:
            self.set_loading_state(False)
            
    def update_user(self, name, email, password):
        """Update existing user in the database"""
        try:
            from datetime import datetime
            user_data = {
                'name': name,
                'email': email,
                'password': password,  # In production, this should be hashed
                'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'status': self.status_var.get() # Update status
            }
            
            # Update user in database
            users_ref = self.db.collection('users')
            users_ref.document(self.current_edit_user_id).update(user_data)
            
            # Clear form and exit edit mode
            self.clear_form()
            self.exit_edit_mode()
            
            # Refresh user table
            self.load_users()
            
            # Show success message
            messagebox.showinfo("成功", f"{name}様のアカウントが正常に更新されました!")
            
        except Exception as e:
            messagebox.showerror("エラー", f"ユーザー更新に失敗しました: {str(e)}")
        finally:
            self.set_loading_state(False)
            
    def clear_form(self):
        """Clear all form fields"""
        self.name_var.set('')
        self.email_var.set('')
        self.password_var.set('')
        self.confirm_password_var.set('')
        self.show_password_var.set(False)
        self.toggle_password_visibility()
        self.status_var.set("active") # Reset status
        
    def get_status_display(self, status):
        """Convert status value to display text"""
        status_map = {
            'active': 'アクティブ',
            'inactive': '非アクティブ'
        }
        return status_map.get(status, status)
        
    def enter_edit_mode(self, user_id, user_data):
        """Enter edit mode and populate form with user data"""
        self.edit_mode = True
        self.current_edit_user_id = user_id
        
        # Populate form with user data
        self.name_var.set(user_data.get('name', ''))
        self.email_var.set(user_data.get('email', ''))
        self.password_var.set(user_data.get('password', ''))
        self.confirm_password_var.set(user_data.get('password', ''))
        self.status_var.set(user_data.get('status', 'active')) # Populate status
        
        # Change button text
        self.register_button.config(text="編集")
        self.cancel_button.grid() # Show cancel button
        
        # Show edit mode status
        self.edit_status_label.config(text=f"編集モード: {user_data.get('name', '')}")
        
        # Focus on name entry
        self.name_entry.focus()
        
    def exit_edit_mode(self):
        """Exit edit mode and reset form"""
        self.edit_mode = False
        self.current_edit_user_id = None
        
        # Change button text back
        self.register_button.config(text="登録")
        self.cancel_button.grid_remove() # Hide cancel button
        
        # Clear edit mode status
        self.edit_status_label.config(text="")
        
        # Clear form
        self.clear_form()
    
    def cancel_edit(self):
        """Cancel edit mode and reset form"""
        self.exit_edit_mode()
        messagebox.showinfo("キャンセル", "ユーザー編集をキャンセルしました。")
    
    def perform_register(self, name: str, email: str, password: str):
        """Perform actual registration with Firebase Auth"""
        try:
            # Note: Firebase Admin SDK doesn't support user creation directly
            # You would need to use Firebase Auth REST API or Firebase Auth client SDK
            # For now, we'll simulate the registration process
            
            # Simulate API call delay
            import time
            time.sleep(1)
            
            # For demonstration, we'll simulate successful registration
            self.root.after(0, self.register_success, {"name": name, "email": email})
                
        except Exception as e:
            self.root.after(0, self.register_failed, f"新規登録エラー: {str(e)}")
    
    def register_success(self, user_data: dict):
        """Handle successful registration"""
        self.set_loading_state(False)
        messagebox.showinfo("Success", f"{user_data['name']}様のアカウントが正常に作成されました!")
        
        # Return to login window
        self.back_to_login()
    
    def register_failed(self, error_message: str):
        """Handle failed registration"""
        self.set_loading_state(False)
        messagebox.showerror("登録に失敗しました", error_message)
    
    def set_loading_state(self, loading: bool):
        """Set loading state for UI elements"""
        if loading:
            self.register_button.config(state="disabled")
            self.back_button.config(state="disabled")
            self.progress.start()
            self.status_label.config(text="アカウントを作成しています...")
        else:
            self.register_button.config(state="normal")
            self.back_button.config(state="normal")
            self.progress.stop()
            self.status_label.config(text="")
    
    def is_valid_email(self, email: str) -> bool:
        """Validate email format"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def back_to_login(self):
        """Return to login window"""
        # Don't destroy the root window - let the parent handle the transition
        print("Returning to login window...")
        self.parent.show_login()

    def create_user_table(self, parent):
        """Create the user management table"""
        try:
            # Table controls
            controls_frame = ttk.Frame(parent)
            controls_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
            
            # Refresh button
            refresh_btn = ttk.Button(controls_frame, text="更新", command=self.load_users)
            refresh_btn.pack(side="left", padx=(0, 10))
            
            # Search entry (without placeholder for compatibility)
            self.search_var = tk.StringVar()
            search_entry = ttk.Entry(controls_frame, textvariable=self.search_var)
            search_entry.pack(side="left", padx=(0, 10))
            search_entry.bind('<KeyRelease>', self.filter_users)
            
            # Add placeholder text manually
            search_entry.insert(0, "検索...")
            search_entry.bind('<FocusIn>', lambda e: self.on_search_focus_in(search_entry))
            search_entry.bind('<FocusOut>', lambda e: self.on_search_focus_out(search_entry))
            
            # Create Treeview for user table
            columns = ('name', 'email', 'created_at', 'status')
            self.user_tree = ttk.Treeview(parent, columns=columns, show='headings', height=15)
            
            # Define headings
            self.user_tree.heading('name', text='名前')
            self.user_tree.heading('email', text='メール')
            self.user_tree.heading('created_at', text='作成日')
            self.user_tree.heading('status', text='ステータス')
            
            # Define column widths
            self.user_tree.column('name', width=150)
            self.user_tree.column('email', width=200)
            self.user_tree.column('created_at', width=120)
            self.user_tree.column('status', width=80)
            
            # Add scrollbar
            scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.user_tree.yview)
            self.user_tree.configure(yscrollcommand=scrollbar.set)
            
            # Grid the tree and scrollbar
            self.user_tree.grid(row=1, column=0, sticky="nsew")
            scrollbar.grid(row=1, column=1, sticky="ns")
            
            # Context menu for user actions
            self.create_context_menu()
            
            # Add alternative ways to access edit/delete functions for macOS compatibility
            self.user_tree.bind("<Double-1>", self.on_double_click)  # Double-click to edit
            self.user_tree.bind("<Delete>", self.on_delete_key)      # Delete key to delete
            self.user_tree.bind("<Return>", self.on_enter_key)       # Enter key to edit
            
            # Add selection change event
            self.user_tree.bind("<<TreeviewSelect>>", self.on_selection_change)
            
            # Create action buttons for macOS compatibility
            self.create_action_buttons(parent)
            
        except Exception as e:
            print(f"Error creating user table: {e}")
            import traceback
            traceback.print_exc()
            
            # Show error in table only if user_tree exists
            if hasattr(self, 'user_tree') and self.user_tree is not None:
                self.user_tree.insert('', 'end', values=('Error loading users', str(e), '', ''))
            
    def on_search_focus_in(self, entry):
        """Handle search entry focus in"""
        if entry.get() == "検索...":
            entry.delete(0, tk.END)
            entry.config(foreground='black')
            
    def on_search_focus_out(self, entry):
        """Handle search entry focus out"""
        if entry.get() == "":
            entry.insert(0, "検索...")
            entry.config(foreground='gray')
            
    def create_context_menu(self):
        """Create right-click context menu for user actions"""
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="編集", command=self.edit_user)
        self.context_menu.add_command(label="削除", command=self.delete_user)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="詳細表示", command=self.view_user_details)
        
        # Bind right-click to show context menu
        self.user_tree.bind("<Button-3>", self.show_context_menu)
        
        # Add macOS-specific right-click binding
        self.user_tree.bind("<Button-2>", self.show_context_menu)  # Alternative right-click
        
    def create_action_buttons(self, parent):
        """Create action buttons for macOS compatibility"""
        # Action buttons frame
        action_frame = ttk.Frame(parent)
        action_frame.grid(row=2, column=0, sticky="ew", pady=(10, 0))
        
        # Edit button
        self.edit_button = ttk.Button(action_frame, text="選択したユーザーを編集", command=self.edit_user)
        self.edit_button.pack(side="left", padx=(0, 10))
        
        # Delete button
        self.delete_button = ttk.Button(action_frame, text="選択したユーザーを削除", command=self.delete_user)
        self.delete_button.pack(side="left", padx=(0, 10))
        
        # View details button
        self.view_button = ttk.Button(action_frame, text="詳細表示", command=self.view_user_details)
        self.view_button.pack(side="left")
        
        # Help button
        self.help_button = ttk.Button(action_frame, text="ヘルプ", command=self.show_help)
        self.help_button.pack(side="right")
        
        # Initially disable buttons (no selection)
        self.edit_button.config(state="disabled")
        self.delete_button.config(state="disabled")
        self.view_button.config(state="disabled")
        
    def show_help(self):
        """Show help dialog with keyboard shortcuts"""
        help_text = """
ユーザー管理の操作方法:

【マウス操作】
• クリック: ユーザーを選択
• ダブルクリック: ユーザーを編集
• 右クリック: コンテキストメニュー（macOSでは利用できない場合があります）

【キーボード操作】
• Enter: 選択したユーザーを編集
• Delete: 選択したユーザーを削除

【ボタン操作】
• 「選択したユーザーを編集」: ユーザーを編集モードに切り替え
• 「選択したユーザーを削除」: ユーザーを削除
• 「詳細表示」: ユーザーの詳細情報を表示

【macOSでの注意点】
• 右クリックメニューが動作しない場合は、下のボタンを使用してください
• キーボードショートカットが利用できます
        """
        
        help_window = tk.Toplevel(self.root)
        help_window.title("ヘルプ")
        help_window.geometry("500x400")
        help_window.resizable(False, False)
        
        # Center the window
        help_window.transient(self.root)
        help_window.grab_set()
        
        # Create help frame
        help_frame = ttk.Frame(help_window, padding="20")
        help_frame.pack(fill="both", expand=True)
        
        # Display help text
        ttk.Label(help_frame, text="ユーザー管理ヘルプ", font=("Arial", 16, "bold")).pack(pady=(0, 20))
        
        text_widget = tk.Text(help_frame, height=15, width=60, wrap="word")
        text_widget.pack(fill="both", expand=True)
        text_widget.insert("1.0", help_text)
        text_widget.config(state="disabled")
        
        # Close button
        ttk.Button(help_frame, text="閉じる", command=help_window.destroy).pack(pady=(10, 0))
        
    def on_double_click(self, event):
        """Handle double-click on user row"""
        selection = self.user_tree.selection()
        if selection:
            self.edit_user()
            
    def on_delete_key(self, event):
        """Handle delete key press"""
        selection = self.user_tree.selection()
        if selection:
            self.delete_user()
            
    def on_enter_key(self, event):
        """Handle enter key press"""
        selection = self.user_tree.selection()
        if selection:
            self.edit_user()
            
    def on_selection_change(self, event):
        """Handle selection change in treeview"""
        selection = self.user_tree.selection()
        if selection:
            # Enable action buttons when user is selected
            self.edit_button.config(state="normal")
            self.delete_button.config(state="normal")
            self.view_button.config(state="normal")
        else:
            # Disable action buttons when no selection
            self.edit_button.config(state="disabled")
            self.delete_button.config(state="disabled")
            self.view_button.config(state="disabled")
            
    def show_context_menu(self, event):
        """Show context menu on right-click"""
        try:
            # Check if there's a selection
            selection = self.user_tree.selection()
            if not selection:
                return  # Don't show menu if no user is selected
                
            # Update menu items based on selection
            self.context_menu.entryconfig("編集", state="normal")
            self.context_menu.entryconfig("削除", state="normal")
            self.context_menu.entryconfig("詳細表示", state="normal")
            
            self.context_menu.tk_popup(event.x_root, event.y_root)
        except Exception as e:
            print(f"Context menu error: {e}")
            # Fallback: show a simple message
            selection = self.user_tree.selection()
            if selection:
                messagebox.showinfo("操作", "右クリックメニューが利用できません。\n代わりに下のボタンを使用してください。")
        finally:
            self.context_menu.grab_release()
            
    def load_users(self):
        """Load users from database and populate table"""
        try:
            # Check if user_tree exists
            if not hasattr(self, 'user_tree') or self.user_tree is None:
                print("User tree not created yet, skipping load_users")
                return
                
            # Clear existing items
            for item in self.user_tree.get_children():
                self.user_tree.delete(item)
            
            print("Loading users from Firestore...")
            
            # Get users from database
            users_ref = self.db.collection('users')
            users = users_ref.stream()
            
            user_count = 0
            for user in users:
                user_data = user.to_dict()
                user_id = user.id
                
                print(f"Processing user: {user_id} - {user_data}")
                
                # Format the data for display
                name = user_data.get('name', 'N/A')
                email = user_data.get('email', 'N/A')
                created_at = user_data.get('created_at', 'N/A')
                status = self.get_status_display(user_data.get('status', 'active'))
                
                # Insert into treeview with user_id as item identifier
                item = self.user_tree.insert('', 'end', iid=user_id, values=(
                    name,
                    email,
                    created_at,
                    status
                ))
                
                user_count += 1
            
            print(f"Loaded {user_count} users from Firestore")
            
            # Update status if no users found
            if user_count == 0:
                print("No users found in database")
                self.user_tree.insert('', 'end', values=('No users found', '', '', ''))
                
        except Exception as e:
            print(f"Error loading users: {e}")
            import traceback
            traceback.print_exc()
            
            # Show error in table only if user_tree exists
            if hasattr(self, 'user_tree') and self.user_tree is not None:
                self.user_tree.insert('', 'end', values=('Error loading users', str(e), '', ''))
            
    def filter_users(self, event=None):
        """Filter users based on search text"""
        # Check if user_tree exists
        if not hasattr(self, 'user_tree') or self.user_tree is None:
            print("User tree not created yet, skipping filter_users")
            return
            
        search_term = self.search_var.get().lower()
        
        # Ignore placeholder text
        if search_term == "検索...":
            return
            
        print(f"Filtering users with search term: '{search_term}'")
        
        # Clear current items
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)
            
        # Re-add filtered items
        try:
            users_ref = self.db.collection('users')
            users = users_ref.stream()
            
            filtered_count = 0
            for user in users:
                user_data = user.to_dict()
                user_id = user.id
                
                name = user_data.get('name', '').lower()
                email = user_data.get('email', '').lower()
                
                if search_term in name or search_term in email:
                    # Insert into treeview with user_id as item identifier
                    self.user_tree.insert('', 'end', iid=user_id, values=(
                        user_data.get('name', ''),
                        user_data.get('email', ''),
                        user_data.get('created_at', ''),
                        self.get_status_display(user_data.get('status', 'active'))
                    ))
                    filtered_count += 1
            
            print(f"Found {filtered_count} users matching search term")
            
            if filtered_count == 0 and search_term:
                self.user_tree.insert('', 'end', values=('No matching users', '', '', ''))
                
        except Exception as e:
            print(f"Error filtering users: {e}")
            import traceback
            traceback.print_exc()
            
    def get_selected_user_data(self):
        """Get the data of the currently selected user"""
        selection = self.user_tree.selection()
        if selection:
            user_id = selection[0]
            try:
                # Get user data from Firestore using the user_id
                user_doc = self.db.collection('users').document(user_id).get()
                if user_doc.exists:
                    return user_id, user_doc.to_dict()
                else:
                    print(f"User document {user_id} not found")
                    return None, None
            except Exception as e:
                print(f"Error getting user data: {e}")
                return None, None
        return None, None
            
    def edit_user(self):
        """Edit selected user"""
        user_id, user_data = self.get_selected_user_data()
        if user_id and user_data:
            print(f"Edit user: {user_id} - {user_data}")
            self.enter_edit_mode(user_id, user_data)
        else:
            messagebox.showwarning("警告", "ユーザーを選択してください。")
            
    def delete_user(self):
        """Delete selected user"""
        user_id, user_data = self.get_selected_user_data()
        if user_id and user_data:
            user_name = user_data.get('name', 'Unknown')
            if messagebox.askyesno("確認", f"ユーザー '{user_name}' を削除しますか？"):
                try:
                    # Delete user from Firestore
                    self.db.collection('users').document(user_id).delete()
                    print(f"Deleted user: {user_id}")
                    
                    # Refresh the table
                    self.load_users()
                    
                    messagebox.showinfo("削除完了", f"ユーザー '{user_name}' を削除しました。")
                except Exception as e:
                    print(f"Error deleting user: {e}")
                    messagebox.showerror("エラー", f"ユーザー削除に失敗しました: {str(e)}")
        else:
            messagebox.showwarning("警告", "ユーザーを選択してください。")
                
    def view_user_details(self):
        """View details of selected user"""
        user_id, user_data = self.get_selected_user_data()
        if user_id and user_data:
            print(f"View user details: {user_id} - {user_data}")
            
            # Create a detailed view dialog
            details_window = tk.Toplevel(self.root)
            details_window.title("ユーザー詳細")
            details_window.geometry("400x300")
            details_window.resizable(False, False)
            
            # Center the window
            details_window.transient(self.root)
            details_window.grab_set()
            
            # Create details frame
            details_frame = ttk.Frame(details_window, padding="20")
            details_frame.pack(fill="both", expand=True)
            
            # Display user details
            ttk.Label(details_frame, text="ユーザー詳細", font=("Arial", 16, "bold")).pack(pady=(0, 20))
            
            details_text = f"""
ユーザーID: {user_id}
名前: {user_data.get('name', 'N/A')}
メール: {user_data.get('email', 'N/A')}
作成日: {user_data.get('created_at', 'N/A')}
ステータス: {user_data.get('status', 'N/A')}
            """
            
            text_widget = tk.Text(details_frame, height=10, width=50, wrap="word")
            text_widget.pack(fill="both", expand=True)
            text_widget.insert("1.0", details_text)
            text_widget.config(state="disabled")
            
            # Close button
            ttk.Button(details_frame, text="閉じる", command=details_window.destroy).pack(pady=(10, 0))
        else:
            messagebox.showwarning("警告", "ユーザーを選択してください。")

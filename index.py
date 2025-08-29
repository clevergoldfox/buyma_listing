import firebase_admin
from firebase_admin import credentials, firestore
from typing import Dict, List, Any, Optional
import datetime

import os
import sys
import platform


import tkinter as tk
from views.login_window import LoginWindow
from views.register_window import RegisterWindow
from views.main_window import MainWindow
from views.initial_option_window import InitialOptionWindow
from controllers.scraping.index import scraping
from tkinter import messagebox

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BuymaLister")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        self.current_window = None
        self.window_instance = None
        
        # macOS-specific setup
        self.setup_macos()
        
        # Initialize Firebase
        self.init_firebase()

        # Center the window
        self.center_window()
        
        # Create GUI elements
        self.show_login()
        # self.show_register()
        # self.show_main_page()
        # self.show_initial_option_window()
        
        self.products = []
        self.user = {}
    
    def setup_macos(self):
        """Setup macOS-specific configurations"""
        if platform.system() == "Darwin":
            # Set macOS-specific window properties
            self.root.tk.call('tk', 'scaling', 2.0)  # Retina display support
            
            # Set app icon if available
            try:
                icon_path = resource_path('assets/icon.icns')
                if os.path.exists(icon_path):
                    self.root.iconbitmap(icon_path)
            except Exception as e:
                print(f"Could not set app icon: {e}")
            
            # Enable dark mode support
            try:
                # Check if dark mode is enabled
                if os.system('defaults read -g AppleInterfaceStyle 2>/dev/null') == 0:
                    # Dark mode is enabled, we can add dark theme support here
                    pass
            except:
                pass
            
            # Set macOS window style
            self.root.attributes('-alpha', 0.95)  # Slight transparency
            
            # Prevent window from being resized by user
            self.root.resizable(False, False)
            
            # Set minimum size
            self.root.minsize(400, 500)
            
            print("✅ macOS-specific configurations applied")
    
    def init_firebase(self):
        """Initialize Firebase Admin SDK"""
        try:
            # Initialize Firebase Admin SDK with service account credentials
            cred = credentials.Certificate(resource_path('./buyma-6adf5-firebase-adminsdk-fbsvc-5be0be7cdb.json'))
            firebase_admin.initialize_app(cred)
            self.db = firestore.client()
            print("Firebase initialized successfully")
        except Exception as e:
            messagebox.showerror("Firebase Error", f"Failed to initialize Firebase: {e}")

    def center_window(self):
        """Center the window on screen with improved error handling"""
        try:
            if not hasattr(self, 'root') or not self.root or not self.root.winfo_exists():
                print("Warning: Root window not available for centering")
                return
                
            self.root.update_idletasks()
            
            try:
                width = self.root.winfo_width()
                height = self.root.winfo_height()
            except tk.TclError as e:
                print(f"Error getting window dimensions: {e}")
                return
                
            try:
                screen_width = self.root.winfo_screenwidth()
                screen_height = self.root.winfo_screenheight()
            except tk.TclError as e:
                print(f"Error getting screen dimensions: {e}")
                return
                
            x = (screen_width // 2) - (width // 2)
            y = (screen_height // 2) - (height // 2)
            
            # Ensure window is not off-screen
            x = max(0, min(x, screen_width - width))
            y = max(0, min(y, screen_height - height))
            
            self.root.geometry(f'{width}x{height}+{x}+{y}')
            
        except Exception as e:
            print(f"Error in center_window: {e}")
            import traceback
            traceback.print_exc()

    def show_login(self):
        self.switch_to_window(LoginWindow, database=self.db, parent=self)
        
    def show_register(self):
        self.switch_to_window(RegisterWindow, database=self.db, parent=self)
    
    def show_main_page(self, auto_listing):
        self.auto_listing = auto_listing
        self.switch_to_window(MainWindow, database=self.db, parent=self)

    def show_initial_option_window(self, user_data):
        self.user = user_data
        self.switch_to_window(InitialOptionWindow, database=self.db, parent=self)

    def switch_to_window(self, window_class, **kwargs):
        """Safely switch to a new window with improved macOS support"""
        try:
            # Check if root window is still valid - use safer checks
            if not hasattr(self, 'root') or not self.root:
                print("ERROR: Root window reference is missing!")
                return
                
            # Use a safer approach to check if root exists
            try:
                root_exists = self.root.winfo_exists()
                if not root_exists:
                    print("ERROR: Root window has been destroyed!")
                    return
            except Exception as e:
                print(f"ERROR: Cannot check root window existence: {e}")
                return
            
            # Clean up current window instance if it exists (but don't destroy the root)
            if hasattr(self, 'window_instance') and self.window_instance:
                try:
                    # Only destroy if it's a separate window, not the root
                    if (hasattr(self.window_instance, 'winfo_exists') and 
                        self.window_instance.winfo_exists() and 
                        self.window_instance != self.root):
                        print("Destroying current window instance...")
                        self.window_instance.destroy()
                    else:
                        print("Current window instance already destroyed or is root")
                except Exception as e:
                    print(f"Error destroying current window instance: {e}")
                finally:
                    self.window_instance = None
            
            # Clear all widgets from the main root safely (but preserve the root window)
            try:
                children = self.root.winfo_children()
                for widget in children:
                    try:
                        if widget.winfo_exists() and widget != self.root:
                            widget.destroy()
                    except Exception as e:
                        print(f"Error destroying widget: {e}")
            except Exception as e:
                print(f"Error clearing widgets: {e}")
            
            # Clear references
            self.current_window = None
            
            # Wait a bit for cleanup to complete
            try:
                self.root.update_idletasks()
            except Exception as e:
                print(f"Error updating root tasks: {e}")
                return
            
            # Check root window again before proceeding - use safer check
            try:
                if not self.root.winfo_exists():
                    print("ERROR: Root window destroyed during cleanup!")
                    return
            except Exception as e:
                print(f"ERROR: Cannot verify root window after cleanup: {e}")
                return
            
            # Create new window using the main root
            try:
                self.root.title("BuymaLister")
                self.root.geometry("400x500")
                self.root.resizable(False, False)
                
                # Re-apply macOS-specific settings
                if platform.system() == "Darwin":
                    self.root.attributes('-alpha', 0.95)
                    self.root.minsize(400, 500)
                
                print("Root window configured successfully")
            except Exception as e:
                print(f"Error configuring root window: {e}")
                return
            
            # Center the window
            self.center_window()
            
            # Create the window instance
            self.window_instance = window_class(self.root, **kwargs)
            self.current_window = self.window_instance
            
            # Set up window close handler
            def on_window_close():
                try:
                    print("Window close requested")
                    # macOS-specific: bring app to front before quitting
                    if platform.system() == "Darwin":
                        os.system("osascript -e 'tell application \"System Events\" to set frontmost of every process whose name contains \"BuymaLister\" to true'")
                    self.root.quit()
                except Exception as e:
                    print(f"Error during application shutdown: {e}")
                    import sys
                    sys.exit(0)
            
            self.root.protocol("WM_DELETE_WINDOW", on_window_close)
            
        except Exception as e:
            print(f"Error creating new window: {e}")
            import traceback
            traceback.print_exc()
            try:
                messagebox.showerror("Error", f"Failed to create window: {e}")
            except:
                print("Could not show error message box")

    def scraping_init(self, set_value, logging=None):
        if logging:
            logging("Starting scraping process...")
            logging(f"Configuration loaded: {len(set_value)} settings")
        
        # scraping(set_value, self.user, logging)
        self.products = scraping(set_value, self.user, logging)
        
        if logging:
            logging(f"Scraping completed. Found {len(self.products)} products")
        
        
    
    def on_closing(self):
        try:
            if self.current_window and self.current_window.winfo_exists():
                self.current_window.destroy()
            self.root.quit()
        except Exception as e:
            print(f"Error during application shutdown: {e}")
            self.root.quit()



if __name__ == "__main__":
    try:
        # macOS-specific fixes
        if platform.system() == "Darwin":
            # Set environment variables to prevent Tkinter issues
            os.environ['TK_SILENCE_DEPRECATION'] = '1'
            # Additional macOS-specific settings
            os.environ['PYTHONUNBUFFERED'] = '1'
            # Disable GPU acceleration for Tkinter on macOS
            os.environ['TK_SILENCE_DEPRECATION'] = '1'
            
            # Set macOS-specific Python path
            if hasattr(sys, 'frozen'):
                # Running as compiled app
                os.environ['PYTHONPATH'] = sys._MEIPASS
            else:
                # Running as script
                os.environ['PYTHONPATH'] = os.path.dirname(os.path.abspath(__file__))
        
        # Create root window with error handling
        try:
            root = tk.Tk()
        except Exception as e:
            print(f"Failed to create root window: {e}")
            import sys
            sys.exit(1)
        
        # Create app with error handling
        try:
            app = MainApp(root)
        except Exception as e:
            print(f"Failed to create MainApp: {e}")
            root.destroy()
            import sys
            sys.exit(1)
        
        # Start mainloop with error handling
        try:
            root.mainloop()
        except Exception as e:
            print(f"Mainloop error: {e}")
            import sys
            sys.exit(1)
            
    except Exception as e:
        print(f"Application error: {e}")
        import traceback
        traceback.print_exc()
        import sys
        sys.exit(1)

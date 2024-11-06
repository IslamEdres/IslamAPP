import tkinter as tk
from tkinter import Menu, Toplevel, messagebox
import hashlib

class VoIPApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Screen")
        self.root.geometry("1024x800")
        self.root.configure(bg='#0a0a0a')
        
        self.create_menu()
        self.create_title_label()

    def create_menu(self):
        menu_bar = Menu(self.root)
        self.root.config(menu=menu_bar)
        # Menu Bar >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        file_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Add New Server", command=self.open_new_server_window)
        file_menu.add_separator()
        file_menu.add_command(label="Edit Server", command=self.open_edit_window)
        file_menu.add_separator()
        file_menu.add_command(label="Manage Data Base", command=self.open_manage_data_base_window)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.confirm_exit)
        # Menu Bar >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        
    def create_title_label(self):
        title_label = tk.Label(self.root, text="VoIP Team App", font=("Helvetica", 32, "bold"), fg="#ffffff", bg='#0a0a0a')
        title_label.pack(pady=100)

    # ------------------------------------------------------------------------
    # def New Window for Add New Server 
    def open_new_server_window(self):
        new_window = Toplevel(self.root)  # Create a new window
        new_window.title("Add New Server")  # Title of the new window
        new_window.geometry("600x400")  # Initial size of the new window
        new_window.minsize(600, 400)  # Minimum size of the new window
        new_window.configure(bg='#1a1a1a')  # Background color of the new window

        new_label = tk.Label(
            new_window, 
            text="Add New Server", 
            font=("Helvetica", 28, "bold"), 
            fg="#ffffff", 
            bg='#1a1a1a'
        )
        new_label.pack(pady=20)  # Add the title with vertical padding

        # Use a frame to hold the input fields and allow for better resizing
        input_frame = tk.Frame(new_window, bg='#1a1a1a')
        input_frame.pack(pady=10, fill='both', expand=True)  # Pack the frame with expansion

        # Create input fields
        self.create_input_field(input_frame, "Server Name:")
        self.create_input_field(input_frame, "Server IP Address:")
        self.create_input_field(input_frame, "Server Port:")
        self.create_input_field(input_frame, "Username:")
        self.create_input_field(input_frame, "Password:", show="*")

        # Back button
        back_button = tk.Button(
            new_window, 
            text="Back", 
            font=("Helvetica", 14), 
            bg="#ff4d4d", 
            fg="#ffffff", 
            command=new_window.destroy
        )
        back_button.pack(pady=20)

    def create_input_field(self, parent, label_text, show=None):
        label = tk.Label(parent, text=label_text, fg="#ffffff", bg='#1a1a1a')
        label.pack(pady=5)  # Add the label with vertical padding
        entry = tk.Entry(parent, show=show)  # Entry field, show='*' for password
        entry.pack(pady=5)  # Add the entry field with vertical padding

    # ----------------------------------------------------------------------------------
    # def New Window for Edit the Server 
    def open_edit_window(self):
        new_window = Toplevel(self.root)
        new_window.title("Edit the Server")
        new_window.geometry("600x400")
        new_window.configure(bg='#1a1a1a')

        new_label = tk.Label(
            new_window, 
            text="Edit the Servers", 
            font=("Helvetica", 28, "bold"), 
            fg="#ffffff", 
            bg='#1a1a1a'
        )
        new_label.pack(pady=50)

        # Back button
        back_button = tk.Button(
            new_window, 
            text="Back", 
            font=("Helvetica", 14), 
            bg="#ff4d4d", 
            fg="#ffffff", 
            command=new_window.destroy
        )
        back_button.pack(pady=20)

    # ----------------------------------------------------------------------------------
    # def New Window for Data Base 
    def open_manage_data_base_window(self):
        new_window = Toplevel(self.root)
        new_window.title("DataBase")
        new_window.geometry("600x400")
        new_window.configure(bg='#1a1a1a')

        new_label = tk.Label(
            new_window, 
            text="DataBase", 
            font=("Helvetica", 28, "bold"), 
            fg="#ffffff", 
            bg='#1a1a1a'
        )
        new_label.pack(pady=50)

        # Back button
        back_button = tk.Button(
            new_window, 
            text="Back", 
            font=("Helvetica", 14), 
            bg="#ff4d4d", 
            fg="#ffffff", 
            command=new_window.destroy
        )
        back_button.pack(pady=20)

    # ----------------------------------------------------------------------------------
    # def message for Exit
    def confirm_exit(self):
        if messagebox.askokcancel("Exit", "Do you really want to exit?"):
            self.root.quit()

# ------------------------------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = VoIPApp(root)
    root.mainloop()

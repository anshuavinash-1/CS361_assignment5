import tkinter as tk
from tkinter import font, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from tkmacosx import Button

# Global variable to keep track of borrowed books
borrowed_books = []
registered_users = [] 

# Function to create a new Toplevel window for forms
def create_form_window(title):
    form_window = tk.Toplevel(root)
    form_window.title(title)
    form_window.geometry("400x500")
    form_window.configure(bg="#f5f5f5")

    # Title Label
    title_label = tk.Label(form_window, text=title, font=("Arial", 24, "bold"), bg="#f5f5f5", fg="#333")
    title_label.pack(pady=20)

    return form_window

# Function to show the book details
def show_book_details(book):
    detail_window = tk.Toplevel(root)
    detail_window.title("Book Details")
    detail_window.geometry("400x400")
    detail_window.configure(bg="#f5f5f5")

    # Book Image
    try:
        image = Image.open(book['image'])
        image = image.resize((100, 150), Image.LANCZOS)
        book_image = ImageTk.PhotoImage(image)
    except Exception as e:
        book_image = None
        print(f"Error loading image: {e}")

    if book_image:
        img_label = tk.Label(detail_window, image=book_image, bg="#f5f5f5")
        img_label.image = book_image  # Keep a reference
        img_label.pack(pady=10)

    # Book Description
    description_label = tk.Label(detail_window, text=book['description'], font=("Arial", 12), bg="#f5f5f5", fg="#333")
    description_label.pack(pady=10)

    # Available Date
    available_label = tk.Label(detail_window, text=f"Available Date: {book['available_date']}", font=("Arial", 12), bg="#f5f5f5", fg="#333")
    available_label.pack(pady=10)

    # Borrow Book Button
    def borrow_book():
        if book['title'] not in borrowed_books:
            borrowed_books.append(book['title'])
            messagebox.showinfo("Success", f"You have borrowed '{book['title']}'!")
            detail_window.destroy()
        else:
            messagebox.showinfo("Notice", f"'{book['title']}' is already borrowed.")

    borrow_button = Button(
                        detail_window,
                        text="Borrow Book",
                        command=borrow_book,
                        font=("Arial", 14),
                        bg="#4CAF50",
                        fg="white",
                        borderless=1  
                    )
    borrow_button.pack(pady=20)

# Function to load books and create clickable book buttons
def load_books(frame, search_filter=""):
    books = [
        {"title": "The Hunger Games", "description": "In the ruins of a place once known as North America lies the nation of Panem, a shining Capitol surrounded by twelve outlying districts.", "available_date": "2024-11-03", "image": "images/book-1.jpg"},
        {"title": "Dune", "description": "Set on the desert planet Arrakis, Dune is the story of the boy Paul Atreides, heir to a noble family tasked with ruling an inhospitable world where the only thing of value is the “spice” melange", "available_date": "2024-11-03", "image": "images/book-2.jpg"},
        {"title": "The Fault in Our Stars", "description": "Despite the tumor-shrinking medical miracle that has bought her a few years, Hazel has never been anything but terminal.", "available_date": "2024-11-20", "image": "images/book-3.jpg"},
        {"title": "One Hundred Years of Solitude", "description": "The brilliant, bestselling, landmark novel that tells the story of the Buendia family, and chronicles the irreconcilable conflict between the desire for solitude", "available_date": "2024-11-10", "image": "images/book-4.jpg"},
        {"title": "To Kill a Mockingbird", "description": "The unforgettable novel of a childhood in a sleepy Southern town and the crisis of conscience that rocked it.", "available_date": "2024-11-15", "image": "images/book-5.jpg"},
        {"title": "The Lord of the Rings", "description": "In ancient times the Rings of Power were crafted by the Elven-smiths, and Sauron, the Dark Lord, forged the One Ring", "available_date": "2024-11-20", "image": "images/book-6.jpg"},
        {"title": "Anna Karenina", "description": "Acclaimed by many as the world's greatest novel, Anna Karenina provides a vast panorama of contemporary life in Russia and of humanity in general.", "available_date": "2024-11-10", "image": "images/book-7.jpg"},
        {"title": "Harry Potter and the Sorcerer’s Stone", "description": "Turning the envelope over, his hand trembling, Harry saw a purple wax seal bearing a coat of arms; a lion, an eagle, a badger and a snake surrounding a large letter 'H'.", "available_date": "2024-11-15", "image": "images/book-8.jpg"},
        {"title": "The Brothers Karamazov", "description": "The Brothers Karamazov is a murder mystery, a courtroom drama, and an exploration of erotic rivalry in a series of triangular love affairs", "available_date": "2024-11-20", "image": "images/book-8.jpg"},
        {"title": "The Brothers Karamazov", "description": "The Brothers Karamazov is a murder mystery, a courtroom drama, and an exploration of erotic rivalry in a series of triangular love affairs", "available_date": "2024-11-20", "image": "images/book-8.jpg"},
    ]

    for widget in frame.winfo_children():
        widget.destroy()

    for book in books:
        if search_filter.lower() in book['title'].lower():
            btn = Button(
                    frame,
                    text=book['title'],
                    font=("Arial", 12),
                    command=lambda b=book: show_book_details(b),
                    bg="#2196F3",   # Optional: Set background color
                    fg="white",     # Optional: Set text color
                    borderless=1    # Removes the default macOS border
                )
            btn.pack(pady=10)

# Placeholder management for Entry fields
def setup_entry_with_placeholder(entry, placeholder):
    entry.insert(0, placeholder)
    entry.bind("<FocusIn>", lambda e: e.widget.delete(0, tk.END) if e.widget.get() == placeholder else None)
    entry.bind("<FocusOut>", lambda e, ph=placeholder: e.widget.insert(0, ph) if not e.widget.get() else None)

# Create the main application window
root = tk.Tk()
root.title("Library System")
root.geometry("800x600")

# Load background image
background_image = Image.open("images/login-bg.png")
background_image = background_image.resize((800, 600), Image.LANCZOS)
background_photo = ImageTk.PhotoImage(background_image)

background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Welcome message
welcome_label = tk.Label(root, text="Welcome!!", font=("Arial", 36, "bold"), bg="#000000", fg="#FFFFFF")
welcome_label.place(relx=0.5, rely=0.2, anchor="center")

description_text = (
    "Greetings from the library! Our library offers something for everyone,\n"
    "whether you’re seeking books, electronic resources, study areas, or\n"
    "research help. Explore, ask questions, and take advantage of our services."
)
description_label = tk.Label(root, text=description_text, font=("Arial", 14), bg="#000000", fg="#FFFFFF", justify="center")
description_label.place(relx=0.5, rely=0.4, anchor="center")

# Functions for Sign Up and Login
def on_signup():
    signup_window = create_form_window("Registration")
    placeholders = ["First Name", "Last Name", "Email", "Password", "Confirm Password"]
    entries = [tk.Entry(signup_window, font=("Arial", 12), bd=2, relief="solid") for _ in placeholders]
    for i, entry in enumerate(entries):
        setup_entry_with_placeholder(entry, placeholders[i])
        entry.pack(pady=(10, 5), padx=20, fill="x")

    def register():

        for user in registered_users:
            if user['email'] == entries[2].get():
                messagebox.showerror("Error", "Email already registered!")
                return
            
        if entries[3].get() != entries[4].get():
            messagebox.showerror("Error", "Passwords do not match!")
        else:
            user_data = {
                "first_name": entries[0].get(),
                "last_name": entries[1].get(),
                "email": entries[2].get(),
                "password": entries[3].get()
            }
            registered_users.append(user_data)
            messagebox.showinfo("Success", "Registration successful!")
            signup_window.destroy()

    Button(
        signup_window,
        text="Register",
        command=register,
        font=("Arial", 14),
        bg="#4CAF50",      # Background color
        fg="white",        # Text color
        padx=10,           # Padding on the x-axis
        pady=5,            # Padding on the y-axis
        borderless=1       # Removes the default macOS border
    ).pack(pady=20)

def on_login():
    login_window = create_form_window("Login")
    login_fields = ["Email", "Password"]
    entries = [tk.Entry(login_window, font=("Arial", 12), bd=2, relief="solid") for _ in login_fields]
    for i, entry in enumerate(entries):
        setup_entry_with_placeholder(entry, login_fields[i])
        entry.pack(pady=(10, 5), padx=20, fill="x")

  

    def login():
        for user in registered_users:
            if user['email'] == entries[0].get() and user['password'] == entries[1].get():
                messagebox.showinfo("Login", f"Logged in as {user['first_name']}!")
                login_window.destroy()
                main_screen()
                return
        messagebox.showerror("Error", "Invalid email or password!")

    Button(
        login_window,
        text="Login",
        command=login,
        font=("Arial", 14),
        bg="#4CAF50",      # Background color
        fg="white",        # Text color
        padx=10,           # Padding on the x-axis
        pady=5,            # Padding on the y-axis
        borderless=1       # Removes the default macOS border
    ).pack(pady=20)


# Main screen after login
def main_screen():
    # Clear the welcome screen
    for widget in root.winfo_children():
        widget.destroy()

    # Main frame background
    main_frame = tk.Frame(root, bg="#f0f0f0")
    main_frame.pack(fill="both", expand=True)

    # Top bar frame for buttons and search box
    top_frame = tk.Frame(main_frame, bg="#3b5998", height=60)
    top_frame.pack(side="top", fill="x")

    # Help and My Account buttons
   
                    

    # Create the Help button
    help_button = Button(
        top_frame,
        text="Help",
        font=("Arial", 14),
        bg="#4CAF50",      # Background color
        fg="white",        # Text color
        padx=10,           # Padding on the x-axis
        pady=5,            # Padding on the y-axis
        borderless=1       # Removes the default macOS border
    )
    help_button.pack(side="left", padx=(10, 5), pady=10)

    style = ttk.Style()
    style.configure("MyAccount.TButton",
                    font=("Arial", 12),
                    padding=(5, 2),
                    background="#2196F3",  # Background color
                    foreground="white")     # Text color

    # Create the My Account button
   
    my_account_button = Button(
        top_frame,
        text="My Account",
        command=my_account_page,
        font=("Arial", 14),
        bg="#4CAF50",      # Background color
        fg="white",        # Text color
        padx=10,           # Padding on the x-axis
        pady=5,            # Padding on the y-axis
        borderless=1       # Removes the default macOS border
    )
    my_account_button.pack(side="left", padx=5, pady=10)

    

    # Title label in main screen
    title_label = tk.Label(main_frame, text="Library Collection", font=("Arial", 24, "bold"), bg="#f0f0f0", fg="#333")
    title_label.pack(pady=20)

    # Book display area with a grid layout
    book_frame = tk.Frame(main_frame, bg="#f0f0f0")
    book_frame.pack(pady=10)

    # Sample grid layout for displaying books
    books = [
        {"title": "The Hunger Games", "description": "In the ruins of a place once known as North America lies the nation of Panem, a shining Capitol surrounded by twelve outlying districts.", "available_date": "2024-11-03", "image": "images/book-1.jpg"},
        {"title": "Dune", "description": "Set on the desert planet Arrakis, Dune is the story of the boy Paul Atreides, heir to a noble family tasked with ruling an inhospitable world where the only thing of value is the “spice” melange", "available_date": "2024-11-03", "image": "images/book-2.jpg"},
        {"title": "The Fault in Our Stars", "description": "Despite the tumor-shrinking medical miracle that has bought her a few years, Hazel has never been anything but terminal.", "available_date": "2024-11-20", "image": "images/book-3.jpg"},
        {"title": "One Hundred Years of Solitude", "description": "The brilliant, bestselling, landmark novel that tells the story of the Buendia family, and chronicles the irreconcilable conflict between the desire for solitude", "available_date": "2024-11-10", "image": "images/book-4.jpg"},
        {"title": "To Kill a Mockingbird", "description": "The unforgettable novel of a childhood in a sleepy Southern town and the crisis of conscience that rocked it.", "available_date": "2024-11-15", "image": "images/book-5.jpg"},
        {"title": "The Lord of the Rings", "description": "In ancient times the Rings of Power were crafted by the Elven-smiths, and Sauron, the Dark Lord, forged the One Ring", "available_date": "2024-11-20", "image": "images/book-6.jpg"},
        {"title": "Anna Karenina", "description": "Acclaimed by many as the world's greatest novel, Anna Karenina provides a vast panorama of contemporary life in Russia and of humanity in general.", "available_date": "2024-11-10", "image": "images/book-7.jpg"},
        {"title": "Harry Potter and the Sorcerer’s Stone", "description": "Turning the envelope over, his hand trembling, Harry saw a purple wax seal bearing a coat of arms; a lion, an eagle, a badger and a snake surrounding a large letter 'H'.", "available_date": "2024-11-15", "image": "images/book-8.jpg"},
        {"title": "The Brothers Karamazov", "description": "The Brothers Karamazov is a murder mystery, a courtroom drama, and an exploration of erotic rivalry in a series of triangular love affairs", "available_date": "2024-11-20", "image": "images/book-8.jpg"},
        {"title": "The Brothers Karamazov", "description": "The Brothers Karamazov is a murder mystery, a courtroom drama, and an exploration of erotic rivalry in a series of triangular love affairs", "available_date": "2024-11-20", "image": "images/book-8.jpg"},
    ]

    rows, cols = 2,5   # Adjust based on the number of books and layout preference
    for i, book in enumerate(books):
        book_frame_inner = tk.Frame(book_frame, bg="#ffffff", bd=2, relief="solid", width=150, height=200)
        book_frame_inner.grid(row=i // cols, column=i % cols, padx=10, pady=10)

        # Book image
        image = Image.open(book['image'])
        image = image.resize((80, 120), Image.LANCZOS)
        book_image = ImageTk.PhotoImage(image)
        img_label = tk.Label(book_frame_inner, image=book_image, bg="#ffffff")
        img_label.image = book_image
        img_label.pack(pady=5)

        # Book title
        title_label = tk.Label(book_frame_inner, text=book['title'], font=("Arial", 12, "bold"), bg="#ffffff", fg="#333")
        title_label.pack(pady=5)

        # Book available date
        available_label = tk.Label(book_frame_inner, text=f"Available: {book['available_date']}", font=("Arial", 10), bg="#ffffff", fg="#777")
        available_label.pack(pady=2)

        # View details button
        view_button = Button(
                        book_frame_inner,
                        text="View Details",
                        command=lambda b=book: show_book_details(b),
                        font=("Arial", 10),
                        bg="#4CAF50",
                        fg="white",
                        borderless=1  
                    )
        view_button.pack(pady=5)


def my_account_page():
    account_window = create_form_window("My Account")
    if registered_users:
        user_info = registered_users[-1]  # Show info of the last registered user for demo
        info_text = f"Name: {user_info['first_name']} {user_info['last_name']}\nEmail: {user_info['email']}"
    else:
        info_text = "No registered users."

    # Borrowed Books Label
    borrowed_label = tk.Label(account_window, text="Borrowed Books:", font=("Arial", 18, "bold"), bg="#f5f5f5", fg="#333")
    borrowed_label.pack(pady=10)

    # List borrowed books or show a message if none
    if borrowed_books:
        for book_title in borrowed_books:
            book_label = tk.Label(account_window, text=book_title, font=("Arial", 14), bg="#f5f5f5", fg="#333")
            book_label.pack(pady=5)
    else:
        no_books_label = tk.Label(account_window, text="No books borrowed yet.", font=("Arial", 14), bg="#f5f5f5", fg="#777")
        no_books_label.pack(pady=10)


# Define buttons for Sign Up and Login
# Define the font
button_font = font.Font(family="Arial", size=14)

# Create the Sign Up button with tkmacosx.Button
signup_button = Button(root, text="Sign Up", command=on_signup, font=button_font, bg="#4CAF50", fg="white", borderless=1)
signup_button.place(relx=0.4, rely=0.8, anchor="center")

# Create the Login button with tkmacosx.Button
login_button = Button(root, text="Login", command=on_login, font=button_font, bg="#2196F3", fg="white", borderless=1)
login_button.place(relx=0.6, rely=0.8, anchor="center")

root.mainloop()

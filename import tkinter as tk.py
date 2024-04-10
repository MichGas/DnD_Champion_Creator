import tkinter as tk
from tkinter import messagebox
import json
import requests

class DnDClassMenu(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.label = tk.Label(self, text="Wybierz klasę postaci:")
        self.label.pack()

        # Pobierz dostępne klasy z API
        self.classes = self.fetch_classes()

        # Utwórz osobne przyciski dla każdej klasy postaci
        for dnd_class in self.classes:
            button = tk.Button(self, text=dnd_class, command=lambda c=dnd_class: self.show_class_info(c), bg='SystemButtonFace')
            button.pack()

        # Przycisk "Back"
        back_button = tk.Button(self, text="Back", command=self.show_menu, bg='SystemButtonFace')
        back_button.pack()

    def fetch_classes(self):
        try:
            # Wykonaj zapytanie do API, aby pobrać dostępne klasy
            response = requests.get("https://www.dnd5eapi.co/api/classes")
            response_data = response.json()
            # Wyodrębnij nazwy klas
            classes = [class_data["name"] for class_data in response_data["results"]]
            return classes
        except Exception as e:
            # Obsłuż błędy połączenia z API
            messagebox.showerror("Błąd", f"Wystąpił błąd podczas pobierania danych z API: {e}")
            return []

    def show_class_info(self, selected_class):
        messagebox.showinfo("Wybrana klasa", f"Wybrana klasa postaci to: {selected_class}")

    def show_menu(self):
        # Ukryj ramkę wyboru klasy postaci
        self.pack_forget()
        # Wyświetl ramkę menu głównego
        menu_frame.pack()

def create_character():
    # Ukryj ramkę menu
    menu_frame.pack_forget()
    # Wyświetl ramkę wyboru klasy postaci
    dnd_menu_frame.pack()

def edit_character():
    messagebox.showinfo("Info", "Edytowanie postaci...")  # Tutaj możesz dodać logikę edytowania postaci

root = tk.Tk()
root.title('gowno')
root.geometry("750x490")

# Set background
bg = tk.PhotoImage(file="background_image.png")

# Create canvas
my_canvas = tk.Canvas(root, width=790, height=490)
my_canvas.pack(fill="both", expand=True)

# Set an image
my_canvas.create_image(0, 0, anchor="nw", image=bg)

# Create menu frame
menu_frame = tk.Frame(my_canvas)
menu_frame.pack()

# Create "Create Character" button
create_button = tk.Button(menu_frame, text="Create Character", command=create_character, bg='SystemButtonFace')
create_button.pack()

# Create "Edit Character" button
edit_button = tk.Button(menu_frame, text="Edit Character", command=edit_character, bg='SystemButtonFace')
edit_button.pack()

# Create DnDClassMenu frame
dnd_menu_frame = DnDClassMenu(my_canvas)

root.mainloop()

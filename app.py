import tkinter as tk
from tkinter import ttk, messagebox
from scraper import CineScraper


url = "https://cinecentre.fr/FR/9/cinema-cinecentre-dreux.html"
scraper = CineScraper(url)
films = scraper.get_film()

root = tk.Tk()
root.title("🎬 Horaires Cinéma Dreux")
root.geometry("500x500")

label = tk.Label(root, text="Choisis un film :", font=("Arial", 12))
label.pack(pady=10)

combo = ttk.Combobox(root, values=[film["titre"] for film in films], font=("Arial", 11))
combo.pack(pady=5)
combo.current(0)

text = tk.Text(root, height=20, width=60, wrap=tk.WORD)
text.pack(pady=10)

def afficher_horaires():
    selected_index = combo.current()
    film = films[selected_index]
    url_film = scraper.get_CreateNewUrl(film["code"], film["titre"])
    
    try:
        import io
        import sys
        old_stdout = sys.stdout
        sys.stdout = mystdout = io.StringIO()
        
        scraper.get_GetHorraire(url_film)
        
        sys.stdout = old_stdout
        horaires = mystdout.getvalue()
        text.delete(1.0, tk.END)
        text.insert(tk.END, horaires)
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

btn = tk.Button(root, text="Afficher les horaires", command=afficher_horaires, font=("Arial", 11))
btn.pack(pady=10)

root.mainloop()

import tkinter
from tkinter import messagebox
import csv
from PIL import Image, ImageTk
from tkinter import ttk


# Fonction pour charger les étudiants depuis un fichier CSV
def charger_etudiants(fichier_csv):
    etudiants = [
("Section 1", "BELARBI", "ZAKARIAE", 18.25),
("Section 1", "BELLAMARI", "HAJAR", 12.75),
("Section 1", "BEN", "HASSANE EL BARAE", 15.5),
("Section 1", "BENDADDA", "SOUAD", 19.0),
("Section 1", "BENHADYR", "KHALIL", 14.75),
("Section 2", "ELMESSOUSI", "MOHAMED SAAD", 16.75),
("Section 1", "BENNIS", "MANAR", 17.0),
("Section 1", "BENNOUNA", "MOUAD", 13.5),
("Section 1", "BERNOUSSI", "RHITA", 12.25),
("Section 2", "ENNAKHLAOUI", "AYA", 18.5),
("Section 1", "BOUGALLA", "YASSIR", 14.0),
("Section 2", "BOULARJAB", "ANASS", 16.75),
("Section 2", "BOUMENZEL", "NOR", 11.5),
("Section 2", "BOUMESHOULI", "LAMYA", 19.5),
("Section 2", "BOUTAJRIT", "AMINE", 15.25),
("Section 2", "BOUZAMMIT", "ALI", 18.75),
("Section 2", "CHEHHAL", "AYA", 17.5),
("Section 2", "CHFII", "FATIMA ZAHRAE", 16.0),
("Section 2", "CHTIOUI", "WIJDANE", 14.25),
("Section 2", "DAFI", "IMANE", 18.5),
("Section 2", "DAOUDY", "FERDAOUS", 12.5),
("Section 2", "DEBBAGH", "OMAR", 19.25),
("Section 2", "DIAW", "ALIOUNE BADARA", 15.0),
("Section 2", "DRIAR", "ZIAD", 11.75),
("Section 2", "DRISSI", "ADAM", 16.5)
]
    try:
        with open(fichier_csv, mode="r", newline="", encoding="utf-8") as fichier:
            reader = csv.reader(fichier)
            etudiants = list(reader)
    except FileNotFoundError:
        pass  # Si le fichier n'existe pas encore, on retourne une liste vide
    return etudiants
def modifier_etudiant(table, etudiants, fichier_csv, entry_section, entry_nom, entry_prenom, entry_moyenne):
    try:
        selected_item = table.selection()[0]
        valeurs = table.item(selected_item, "values")
        section, nom, prenom, moyenne = valeurs

        # Remplir les champs pour modification
        entry_section.delete(0, tkinter.END)
        entry_section.insert(0, section)
        entry_nom.delete(0, tkinter.END)
        entry_nom.insert(0, nom)
        entry_prenom.delete(0, tkinter.END)
        entry_prenom.insert(0, prenom)
        entry_moyenne.delete(0, tkinter.END)
        entry_moyenne.insert(0, moyenne)
        def sauvegarder_modification():
            nouvelle_section = entry_section.get()
            nouveau_nom = entry_nom.get()
            nouveau_prenom = entry_prenom.get()
            try:
                nouvelle_moyenne = float(entry_moyenne.get())
                if nouvelle_moyenne < 0 or nouvelle_moyenne > 20:
                    raise ValueError  # Si la moyenne est hors des bornes, déclenche une exception
            except ValueError:
                messagebox.showerror("Erreur", "Veuillez entrer une moyenne valide entre 0 et 20.")
                return

            # Mettre à jour l'entrée sélectionnée dans la table
            table.item(selected_item, values=(nouvelle_section, nouveau_nom, nouveau_prenom, nouvelle_moyenne))

            # Mettre à jour dans la liste des étudiants
            index = table.index(selected_item)
            etudiants[index] = [nouvelle_section, nouveau_nom, nouveau_prenom, nouvelle_moyenne]

            # Sauvegarder dans le fichier CSV
            sauvegarder_etudiants(fichier_csv, etudiants)
    
            bouton_sauvegarder.destroy()
            messagebox.showinfo("Succès", "L'étudiant a été modifié avec succès.")
         # Effacer les champs
            entry_section.delete(0, tkinter.END)
            entry_nom.delete(0, tkinter.END)
            entry_prenom.delete(0, tkinter.END)
            entry_moyenne.delete(0, tkinter.END)

        # Bouton pour sauvegarder la modification
        bouton_sauvegarder = tkinter.Button(table, text="Sauvegarder Modifications", command=sauvegarder_modification)
        bouton_sauvegarder.grid(row=4, columnspan=2, pady=10)


    except IndexError:
        messagebox.showwarning("Attention", "Veuillez sélectionner un étudiant à modifier.")
        

# Fonction pour sauvegarder les étudiants dans un fichier CSV
def sauvegarder_etudiants(fichier_csv, etudiants):
    with open(fichier_csv, mode="w", newline="", encoding="utf-8") as fichier:
        writer = csv.writer(fichier)
        writer.writerows(etudiants)
    messagebox.showinfo("Sauvegarde", "Les données ont été sauvegardées avec succès.")


def supprimer_etudiant(table, etudiants,fichier_csv):
    try:
        # Vérifie si un étudiant est sélectionné
        selected_item = table.selection()[0]
        index = table.index(selected_item)
        valeurs = table.item(selected_item, "values")
        section, nom, prenom, moyenne = valeurs

        # Demande de confirmation avant suppression
        confirm = messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer cet étudiant ?")
        if not confirm:
            return

        # Supprime l'étudiant de la table
        table.delete(selected_item)

        # Supprime l'étudiant de la liste des étudiants
        del etudiants[index]  # On utilise l'index pour éviter toute ambiguïté

        messagebox.showinfo("Succès", "L'étudiant a été supprimé avec succès.")
    except IndexError:
        messagebox.showwarning("Attention", "Veuillez sélectionner un étudiant à supprimer.")

# Fonction pour ajouter un étudiant à la liste et au fichier CSV
def ajouter_etudiant(table, etudiants, fichier_csv, entry_section, entry_nom, entry_prenom, entry_moyenne):
    # Récupérer les valeurs du formulaire
    section = entry_section.get()
    nom = entry_nom.get()
    prenom = entry_prenom.get()
    try:
        moyenne = float(entry_moyenne.get())
        if moyenne < 0 or moyenne > 20:
            raise ValueError  # Si la moyenne est hors des bornes, déclenche une exception
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer une moyenne valide entre 0 et 20.")
        return

    # Ajouter l'étudiant à la liste des étudiants
    etudiants.append([section, nom, prenom, moyenne])

    # Ajouter l'étudiant dans la table
    table.insert("", tkinter.END, values=(section, nom, prenom, moyenne))

    # Sauvegarder les étudiants dans le fichier CSV
    sauvegarder_etudiants(fichier_csv, etudiants)

    # Vider les champs de saisie
    entry_section.delete(0, tkinter.END)
    entry_nom.delete(0, tkinter.END)
    entry_prenom.delete(0, tkinter.END)
    entry_moyenne.delete(0, tkinter.END)


# Fonction pour afficher la liste des étudiants
def afficher_liste_etudiants():
    
    fichier_csv = "etudiants.csv"
    etudiants = charger_etudiants(fichier_csv)

    # Interface
    root = tkinter.Tk()
    root.title("Gestion des Étudiants")
    root.geometry("800x600")
    root.configure(bg="#f7f7f7")

    # Configuration du style du tableau
    style = ttk.Style()
    style.theme_use("clam")

    style.configure("Treeview", 
                    background="#D8F0FA", 
                    foreground="black", 
                    rowheight=25, 
                    fieldbackground="white", 
                    font=("Times New Roman", 12))
    
    style.configure("Treeview.Heading", 
                    font=("Times New Roman", 14, "bold"), 
                    background="#4CAF50", 
                    foreground="White")
    # Titre
    header_label = tkinter.Label(root, text="Liste des Étudiants", bg="#AFEEEE", fg="Black", font=("Times New Roman", 16, "bold"))
    header_label.pack(fill=tkinter.X, pady=10)

    # Table des étudiants
    table = ttk.Treeview(root, columns=("Section", "Nom", "Prénom", "Moyenne"), show="headings")
    
    table.heading("Section", text="Section")
    table.heading("Nom", text="Nom")
    table.heading("Prénom", text="Prénom")
    table.heading("Moyenne", text="Moyenne")
    table.pack(fill=tkinter.BOTH, expand=True, padx=20, pady=20)
    

    # Ajouter les données à la table
    for etudiant in etudiants:
        table.insert("", tkinter.END, values=etudiant)

    # Zone de saisie pour ajouter un étudiant
    fields_frame = tkinter.Frame(root, bg="#F0F0F0")  # Couleur d'arrière-plan pour distinguer la zone
    fields_frame.pack(pady=20, padx=20)

    # Configuration des colonnes pour les champs (disposition horizontale)
    tkinter.Label(fields_frame, text="Section:", font=("Helvetica", 12), bg="#F0F0F0").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    entry_section = tkinter.Entry(fields_frame, font=("Helvetica", 12), width=20)
    entry_section.grid(row=0, column=1, padx=10, pady=10)

    tkinter.Label(fields_frame, text="Nom:", font=("Helvetica", 12), bg="#F0F0F0").grid(row=0, column=2, padx=10, pady=10, sticky="w")
    entry_nom = tkinter.Entry(fields_frame, font=("Helvetica", 12), width=20)
    entry_nom.grid(row=0, column=3, padx=10, pady=10)

    tkinter.Label(fields_frame, text="Prénom:", font=("Helvetica", 12), bg="#F0F0F0").grid(row=1, column=0, padx=10, pady=10, sticky="w")
    entry_prenom = tkinter.Entry(fields_frame, font=("Helvetica", 12), width=20)
    entry_prenom.grid(row=1, column=1, padx=10, pady=10)

    tkinter.Label(fields_frame, text="Moyenne:", font=("Helvetica", 12), bg="#F0F0F0").grid(row=1, column=2, padx=10, pady=10, sticky="w")
    entry_moyenne = tkinter.Entry(fields_frame, font=("Helvetica", 12), width=20)
    entry_moyenne.grid(row=1, column=3, padx=10, pady=10)
    form_frame = tkinter.Frame(root, bg="White")
    form_frame.pack(pady=10)

    # Bouton pour ajouter un étudiant
    ajouter_button = tkinter.Button(
    form_frame,
    text="Ajouter Étudiant",
    command=lambda: ajouter_etudiant(table, etudiants, fichier_csv, entry_section, entry_nom, entry_prenom, entry_moyenne),
    font=("Times New Roman", 12, "bold"),  # Police personnalisée
    bg="#4B0082",  # Couleur de fond indigo
    fg="white",  # Texte blanc
    activebackground="#43A047",  # Couleur de fond active (vert plus foncé)
    activeforeground="white",  # Texte blanc lorsqu'il est actif
    bd=2,  # Bordure
    relief="raised",  # Style de relief
    cursor="hand2",  # Curseur interactif
)
    ajouter_button.grid(row=4, column=0, pady=5,padx=5)


    # Bouton pour modifier un étudiant
    modifier_button = tkinter.Button(
    form_frame,
    text="Modifier Étudiant",
    command=lambda: modifier_etudiant(table, etudiants, fichier_csv, entry_section, entry_nom, entry_prenom, entry_moyenne),
    font=("Times New Roman", 12, "bold"),  # Police personnalisée
    bg="#2196F3",  # Couleur de fond bleue
    fg="white",  # Texte blanc
    activebackground="#1E88E5",  # Couleur de fond active
    activeforeground="white",  # Texte blanc lorsqu'il est actif
    bd=2,  # Bordure
    relief="raised",  # Style de relief
    cursor="hand2",  # Curseur interactif
)
    modifier_button.grid(row=4, column=1, pady=5,padx=5)

# Bouton pour supprimer un étudiant
    supprimer_button = tkinter.Button(
    form_frame,
    text="Supprimer Étudiant",
    command=lambda: supprimer_etudiant(table, etudiants, fichier_csv),
    font=("Times New Roman", 12, "bold"),  # Police personnalisée
    bg="#F44336",  # Couleur de fond rouge
    fg="white",  # Texte blanc
    activebackground="#E53935",  # Couleur de fond active
    activeforeground="white",  # Texte blanc lorsqu'il est actif
    bd=2,  # Bordure
    relief="raised",  # Style de relief
    cursor="hand2",  # Curseur interactif
)
    supprimer_button.grid(row=5, columnspan=2, pady=5,padx=5)

# Bouton pour sauvegarder les données
    sauvegarder_button = tkinter.Button(
    form_frame,
    text="Sauvegarder les données",
    command=lambda: sauvegarder_etudiants(fichier_csv, etudiants),
    font=("Times New Roman", 12, "bold"),  # Police personnalisée
    bg="#FF9800",  # Couleur de fond orange
    fg="white",  # Texte blanc
    activebackground="#FB8C00",  # Couleur de fond active
    activeforeground="white",  # Texte blanc lorsqu'il est actif
    bd=2,  # Bordure
    relief="raised",  # Style de relief
    cursor="hand2",  # Curseur interactif
    )
    sauvegarder_button.grid(row=6, columnspan=2, pady=5,padx=5)

    root.mainloop()



def effacer_root1(fenetre_principale):
    fenetre_principale.destroy()
    afficher_liste_etudiants()



def interface():
   
    root1 = tkinter.Tk()
    root1.title("Votre application CRUD")
    root1.attributes('-fullscreen', True)

    # Charger et redimensionner l'image de fond
    image = Image.open(r"C:\Users\lenovo\OneDrive\Images\logo_app.jpg")
    screen_width = root1.winfo_screenwidth()
    screen_height = root1.winfo_screenheight()
    image = image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
    bg_image = ImageTk.PhotoImage(image)

    # Créer un Canvas pour gérer le fond et les éléments
    canvas = tkinter.Canvas(root1, width=screen_width, height=screen_height)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=bg_image, anchor="nw")

    # Dessiner une forme non rectangulaire (un ovale avec dégradé possible)
    cadre = canvas.create_oval(
        screen_width//2 - 300, screen_height//3 - 100, 
        screen_width//2 + 300, screen_height//3 + 100,
        fill="#E3F2FD", outline="#1E88E5", width=5
    )

    # Ajouter un texte dans le cadre
    label1 = tkinter.Label(
        root1, 
        text="Bonjour dans votre application.\nCliquez sur commencer", 
        bg="#E3F2FD", 
        font=("Times New Roman", 24, "bold"),
        fg="#1E88E5",
    )
    canvas.create_window(screen_width//2, screen_height//3, window=label1)

    # Bouton "Commencer" avec style modernisé
    boutton1 = tkinter.Button(
        root1, 
        text="Commencer", 
        command=lambda: effacer_root1(root1), 
        font=("Times New Roman", 18, "bold"), 
        bg="#4682B4", 
        fg="white", 
        activebackground="#4682B4", 
        activeforeground="white", 
        cursor="hand2",
        bd=5,
        relief="raised"
    )
    canvas.create_window(screen_width//2, screen_height//2, window=boutton1)

    # Afficher les noms des participants en bas à gauche
    participants = ["BELARBI Zakariae", "Dafi Imane ", "ELMESSOUSSI Mohamed Saad", "ENNAKHLAOUI Aya"]
    participants_text = "\n".join(participants)

    cadre_participants = canvas.create_rectangle(
        80, screen_height - 120, 300, screen_height - 20,  # Décalage à droite
        fill="#FFFFFF", outline="#1E88E5", width=2
    )
    participants_label = tkinter.Label(
        root1,
        text=f"Participants :\n{participants_text}",
        bg="#FFFFFF",
        fg="#1E88E5",
        font=("Times New Roman", 14, "bold"),
        justify="left"
    )
    canvas.create_window(190, screen_height - 70, window=participants_label)

    root1.mainloop()

interface()
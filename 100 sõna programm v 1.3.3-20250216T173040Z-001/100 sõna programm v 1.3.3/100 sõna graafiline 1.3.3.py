import customtkinter as ctk
import math
import pygame
from tkinter import messagebox

class ModernWordGame:
    def __init__(self, root):
        self.root = root
        self.root.title("100 sõna kordamine")
        self.root.geometry("900x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.words = [
            "valijaskond", "läänemeresoome keeled", "Tartu raekoda", "Ahhaa teaduskeskus", "viieleheküljeline",
            "mööda auklikku teed", "toidu- ja tööstuskaubad", "kaitses oma peret", "tund-tunnilt", "Emajõe-äärne",
            "Koidula-aegne Pärnu", "jõudsin bussi peale", "ehteestilik", "ümmargune bassein", "Ida-Euroopa riigid",
            "Euroopa Liit", "lähestikused", "dramaatika", "materiaalne", "Jõgeva maakond",
            "kasutati pöidlaküüti", "A4 paber", "piklik pikkpoiss", "mänguasjamuuseum", "žanr",
            "annulleerima", "ETV saade 'Aktuaalne kaamera'", "esmakordselt", "kõrvaldatav kandidaat", "püüa mind kinni",
            "potentsiaalne", "määrati koordinaate", "lutsulik stiil", "keskkonnasõbralik", "gripiepideemia",
            "loiuvõitu portugalane", "konkurentsivõimeline aktsiaselts", "kuperjanovlased", "Balti riigid", "süüakse kotlette",
            "arhitektuur", "suvistel kontsertidel", "film 'Eia jõulud Tondikakul'", "Otepää kui talvepealinn", "sümfooniaorkestri dirigent",
            "pealinlasedki", "Tere, õpetaja Mets!", "suhtles kirja teel", "Aitäh, tädi Anu!", "kadri-ja mardipäev",
            "bioloogiaolümpiaad", "sünniaeg ja -koht", "detektiiv", "kasutati uut taktikat", "kogu aeg korraldatakse",
            "generatsioon e põlvkond", "Tallinna transport", "Võru folkloorifestival", "intervjuu juutuuberiga", "mõttetu toiming",
            "Suur Munamägi", "monoloog ja dialoog", "Piusa jõgi", "tallinlane", "Google'i tõlge",
            "kodakondsusseadus", "Uhtjärve nõiariik", "alkoholivaba üritus", "digitelevisioon", "Eesti president Alar Karis",
            "kagueestlane", "umbusaldusavaldus", "Vikipeedia artikkel", "suur reede", "katastroofipiirkond",
            "ortograafiaviga", "klienditeenindaja", "ballett 'Luikede järv'", "fotokonkurss", "batsill",
            "linlik elustiil", "Eesti-aegsed metallrahad", "intelligentne", "dušigeel", "orienteeruja",
            "ingliskeelne lemmiklaul", "humaanne otsus", "Vabaduse väljak", "kondenspiim", "Skorpioni tähtkuju",
            "ajaleht Eesti Kirik", "eestimaine toodang", "läti rahvas", "Eesti kuulub NATO-sse", "emakeelepäeval, 14. märtsil",
            "mobiiltelefoni akulaadija", "dieettoit", "aksessuaarid", "ootamatud leiud", "infektsioon"
        ]
        self.correct_words = 0
        self.mistakes = 0
        self.difficulty = 1
        self.current_phrase_index = 0

     
        self.bg_frame = ctk.CTkFrame(root, corner_radius=0)
        self.bg_frame.pack(fill="both", expand=True)


        self.title_label = ctk.CTkLabel(self.bg_frame, text="100 Sõna Töö Kordamine", font=("Arial Rounded MT Bold", 26))
        self.title_label.pack(pady=15)

        
        self.difficulty_label = ctk.CTkLabel(self.bg_frame, text="Vali raskusaste (1-4):", font=("Arial", 16))
        self.difficulty_label.pack()

        self.difficulty_entry = ctk.CTkEntry(self.bg_frame, font=("Arial", 16), width=50)
        self.difficulty_entry.pack(pady=5)

        self.start_button = ctk.CTkButton(self.bg_frame, text="Alusta", command=self.start_game)
        self.start_button.pack(pady=10)

    
        self.word_frame = ctk.CTkFrame(self.bg_frame, corner_radius=15)
        self.word_frame.pack(pady=20, fill="both", expand=True)

        self.word_label = ctk.CTkLabel(self.word_frame, text=".....", wraplength=600, font=("Arial", 18))
        self.word_label.pack(pady=10)

   
        self.input_entry = ctk.CTkEntry(self.bg_frame, font=("Arial", 16))
        self.input_entry.pack(pady=10)
        self.input_entry.bind("<Return>", self.check_answer)

        self.check_button = ctk.CTkButton(self.bg_frame, text="Kontrolli vastus", command=self.check_answer, state="disabled")
        self.check_button.pack(pady=10)

        
        self.progress_label = ctk.CTkLabel(self.bg_frame, text="Progress: 0%", font=("Arial", 14))
        self.progress_label.pack(pady=5)

        self.progress_bar = ctk.CTkProgressBar(self.bg_frame, width=300)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=5)

       
        self.score_label = ctk.CTkLabel(self.bg_frame, text="Õigesti: 0  |  Valesti: 0", font=("Arial", 14))
        self.score_label.pack(pady=10)

        self.motivation_label = ctk.CTkLabel(self.bg_frame, text="", font=("Arial", 14), text_color="yellow")
        self.motivation_label.pack(pady=10)

    def start_game(self):
        try:
            self.difficulty = int(self.difficulty_entry.get())
            if self.difficulty not in [1, 2, 3, 4]:
                raise ValueError
        except ValueError:
            messagebox.showerror("Viga", "Palun sisesta number 1-4.")
            return

        self.correct_words = 0
        self.mistakes = 0
        self.current_phrase_index = 0
        self.show_word()
        self.check_button.configure(state="normal")
        self.update_progress()

    def show_word(self):
        phrase = self.words[self.current_phrase_index]
        reveal_percentage = {1: 0.75, 2: 0.50, 3: 0.25, 4: 0.10}[self.difficulty]
        self.revealed_words = [word[:math.ceil(len(word) * reveal_percentage)] + "..." for word in phrase.split()]
        self.word_label.configure(text=f"Arvatav sõna: {' '.join(self.revealed_words)}")

    def check_answer(self, event=None):
        user_input = self.input_entry.get().strip()
        correct_phrase = self.words[self.current_phrase_index]

        if user_input.lower() == correct_phrase.lower():
            self.correct_words += 1
            self.current_phrase_index += 1
            self.motivation_label.configure(text="Õige!", text_color="green")
        else:
            self.mistakes += 1
            self.motivation_label.configure(text="Vale! Proovi uuesti.", text_color="red")

        if self.current_phrase_index < len(self.words):
            self.show_word()
            self.input_entry.delete(0, "end")
        else:
            messagebox.showinfo("Mäng Läbi", f"Oled õigesti vastanud {self.correct_words} korda!")
            self.root.quit()

        self.update_progress()

    def update_progress(self):
        progress = self.current_phrase_index / len(self.words)
        self.progress_bar.set(progress)
        self.progress_label.configure(text=f"Progress: {int(progress * 100)}%")
        self.score_label.configure(text=f"Õigesti: {self.correct_words}  |  Valesti: {self.mistakes}")

if __name__ == "__main__":
    root = ctk.CTk()
    app = ModernWordGame(root)
    root.mainloop()

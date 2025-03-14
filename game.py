import tkinter as tk
from tkinter import ttk, messagebox
from character import Warrior, Mage
from enemy import Goblin, Orc
import random
from PIL import Image, ImageTk  # Add PIL import for image handling

class RPGGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Residência TI Adventure")
        self.window.geometry("800x600")
        self.window.configure(bg='#2C3E50')
        
        self.player = None
        self.current_enemy = None
        self.stage = 0
        self.setup_gui()

    def setup_gui(self):
        # Logo
        try:
            logo_image = Image.open("assets/logo_residencia_ti_adventure.png")
            # Resize the image to fit nicely in the window (adjust size as needed)
            logo_image = logo_image.resize((300, 300), Image.Resampling.LANCZOS)
            logo_photo = ImageTk.PhotoImage(logo_image)
            logo_label = tk.Label(
                self.window,
                image=logo_photo,
                bg='#2C3E50'
            )
            logo_label.image = logo_photo  # Keep a reference to prevent garbage collection
            logo_label.pack(pady=10)
        except Exception as e:
            print(f"Error loading logo: {e}")


        # Character Selection
        self.char_var = tk.StringVar(value="Warrior")
        char_frame = tk.Frame(self.window, bg='#2C3E50')
        char_frame.pack(pady=10)

        char_label = tk.Label(
            char_frame,
            text="Selecione seu personagem",
            font=("Arial", 12),
            bg='#2C3E50',
            fg='white'
        )
        char_label.pack()

        # Warrior selection with icon
        warrior_frame = tk.Frame(char_frame, bg='#2C3E50')
        warrior_frame.pack(pady=5)
        
        try:
            warrior_image = Image.open("assets/warrior_icon.png")
            warrior_image = warrior_image.resize((50, 50), Image.Resampling.LANCZOS)
            warrior_photo = ImageTk.PhotoImage(warrior_image)
            warrior_icon = tk.Label(
                warrior_frame,
                image=warrior_photo,
                bg='#2C3E50'
            )
            warrior_icon.image = warrior_photo
            warrior_icon.pack(side='left', padx=5)
        except Exception as e:
            print(f"Error loading warrior icon: {e}")

        warrior_rb = ttk.Radiobutton(
            warrior_frame,
            text="Warrior",
            value="Warrior",
            variable=self.char_var
        )
        warrior_rb.pack(side='left')

        # Mage selection with icon
        mage_frame = tk.Frame(char_frame, bg='#2C3E50')
        mage_frame.pack(pady=5)
        
        try:
            mage_image = Image.open("assets/mage_icon.png")
            mage_image = mage_image.resize((50, 50), Image.Resampling.LANCZOS)
            mage_photo = ImageTk.PhotoImage(mage_image)
            mage_icon = tk.Label(
                mage_frame,
                image=mage_photo,
                bg='#2C3E50'
            )
            mage_icon.image = mage_photo
            mage_icon.pack(side='left', padx=5)
        except Exception as e:
            print(f"Error loading mage icon: {e}")

        mage_rb = ttk.Radiobutton(
            mage_frame,
            text="Mage",
            value="Mage",
            variable=self.char_var
        )
        mage_rb.pack(side='left')

        # Name Entry
        name_frame = tk.Frame(self.window, bg='#2C3E50')
        name_frame.pack(pady=10)

        name_label = tk.Label(
            name_frame,
            text="Enter your name:",
            font=("Arial", 12),
            bg='#2C3E50',
            fg='white'
        )
        name_label.pack()

        self.name_entry = tk.Entry(name_frame)
        self.name_entry.pack()

        # Start Button
        start_button = tk.Button(
            self.window,
            text="Começar Jogo",
            command=self.start_game,
            font=("Arial", 14),
            bg='#27AE60',
            fg='white',
            padx=20,
            pady=10
        )
        start_button.pack(pady=20)

    def create_combat_gui(self):
        self.window.geometry("800x600")
        for widget in self.window.winfo_children():
            widget.destroy()

        # Status Frame
        status_frame = tk.Frame(self.window, bg='#2C3E50')
        status_frame.pack(fill='x', padx=20, pady=10)

        # Player Status Frame with icons
        player_status_frame = tk.Frame(status_frame, bg='#2C3E50')
        player_status_frame.pack(side='left', padx=10)

        # Player Name with character icon
        name_frame = tk.Frame(player_status_frame, bg='#2C3E50')
        name_frame.pack(fill='x', pady=2)
        try:
            char_icon = "assets/warrior_icon.png" if isinstance(self.player, Warrior) else "assets/mage_icon.png"
            char_image = Image.open(char_icon)
            char_image = char_image.resize((30, 30), Image.Resampling.LANCZOS)
            char_photo = ImageTk.PhotoImage(char_image)
            char_label = tk.Label(name_frame, image=char_photo, bg='#2C3E50')
            char_label.image = char_photo
            char_label.pack(side='left', padx=5)
        except Exception as e:
            print(f"Error loading character icon: {e}")
        
        tk.Label(
            name_frame,
            text=f"Player: {self.player.name}",
            font=("Arial", 12, "bold"),
            bg='#2C3E50',
            fg='white'
        ).pack(side='left')

        # HP with icon
        hp_frame = tk.Frame(player_status_frame, bg='#2C3E50')
        hp_frame.pack(fill='x', pady=2)
        try:
            hp_image = Image.open("assets/health_icon.png")
            hp_image = hp_image.resize((20, 20), Image.Resampling.LANCZOS)
            hp_photo = ImageTk.PhotoImage(hp_image)
            hp_icon = tk.Label(hp_frame, image=hp_photo, bg='#2C3E50')
            hp_icon.image = hp_photo
            hp_icon.pack(side='left', padx=5)
        except Exception as e:
            print(f"Error loading HP icon: {e}")
        
        tk.Label(
            hp_frame,
            text=f"HP: {self.player.health}/{self.player.max_health}",
            font=("Arial", 12),
            bg='#2C3E50',
            fg='white'
        ).pack(side='left')

        # Resource (Rage/Mana) with icon
        resource_frame = tk.Frame(player_status_frame, bg='#2C3E50')
        resource_frame.pack(fill='x', pady=2)
        try:
            resource_icon = "assets/rage_icon.png" if isinstance(self.player, Warrior) else "assets/mana_icon.png"
            resource_image = Image.open(resource_icon)
            resource_image = resource_image.resize((20, 20), Image.Resampling.LANCZOS)
            resource_photo = ImageTk.PhotoImage(resource_image)
            resource_label = tk.Label(resource_frame, image=resource_photo, bg='#2C3E50')
            resource_label.image = resource_photo
            resource_label.pack(side='left', padx=5)
        except Exception as e:
            print(f"Error loading resource icon: {e}")
        
        resource_text = f"Rage: {self.player.rage}" if isinstance(self.player, Warrior) else f"Mana: {self.player.mana}"
        tk.Label(
            resource_frame,
            text=resource_text,
            font=("Arial", 12),
            bg='#2C3E50',
            fg='white'
        ).pack(side='left')

        # Level with icon
        level_frame = tk.Frame(player_status_frame, bg='#2C3E50')
        level_frame.pack(fill='x', pady=2)
        try:
            level_image = Image.open("assets/level_icon.png")
            level_image = level_image.resize((20, 20), Image.Resampling.LANCZOS)
            level_photo = ImageTk.PhotoImage(level_image)
            level_icon = tk.Label(level_frame, image=level_photo, bg='#2C3E50')
            level_icon.image = level_photo
            level_icon.pack(side='left', padx=5)
        except Exception as e:
            print(f"Error loading level icon: {e}")
        
        tk.Label(
            level_frame,
            text=f"Level: {self.player.level}",
            font=("Arial", 12),
            bg='#2C3E50',
            fg='white'
        ).pack(side='left')

        # Gold with icon
        gold_frame = tk.Frame(player_status_frame, bg='#2C3E50')
        gold_frame.pack(fill='x', pady=2)
        try:
            gold_image = Image.open("assets/gold_icon.png")
            gold_image = gold_image.resize((20, 20), Image.Resampling.LANCZOS)
            gold_photo = ImageTk.PhotoImage(gold_image)
            gold_icon = tk.Label(gold_frame, image=gold_photo, bg='#2C3E50')
            gold_icon.image = gold_photo
            gold_icon.pack(side='left', padx=5)
        except Exception as e:
            print(f"Error loading gold icon: {e}")
        
        tk.Label(
            gold_frame,
            text=f"Gold: {self.player.gold}",
            font=("Arial", 12),
            bg='#2C3E50',
            fg='white'
        ).pack(side='left')

        # Stage Info
        stage_info = tk.Label(
            self.window,
            text=f"Stage {self.stage}/5",
            font=("Arial", 16, "bold"),
            bg='#2C3E50',
            fg='white'
        )
        stage_info.pack(pady=10)

        # Enemy Info
        if self.current_enemy:
            enemy_image = Image.open(self.current_enemy.image)
            enemy_image = enemy_image.resize((100, 100), Image.Resampling.LANCZOS)
            enemy_photo = ImageTk.PhotoImage(enemy_image)
            enemy_icon = tk.Label(
                self.window,
                image=enemy_photo,
                bg='#2C3E50'
            )
            enemy_icon.image = enemy_photo
            enemy_icon.pack(pady=10)

            enemy_info = tk.Label(
                self.window,
                text=f"Enemy: {self.current_enemy.name} | HP: {self.current_enemy.health}",
                font=("Arial", 14),
                bg='#2C3E50',
                fg='white'
            )
            enemy_info.pack(pady=10)

        # Combat Buttons
        button_frame = tk.Frame(self.window, bg='#2C3E50')
        button_frame.pack(pady=20)

        # Attack button with icon
        try:
            attack_image = Image.open("assets/attack_icon.png")
            attack_image = attack_image.resize((20, 20), Image.Resampling.LANCZOS)
            attack_photo = ImageTk.PhotoImage(attack_image)
            attack_btn = tk.Button(
                button_frame,
                text="Atacar",
                image=attack_photo,
                compound=tk.LEFT,
                command=self.handle_attack,
                font=("Arial", 12),
                bg='#E74C3C',
                fg='white',
                padx=15,
                pady=5
            )
            attack_btn.image = attack_photo
            attack_btn.pack(side='left', padx=5)
        except Exception as e:
            print(f"Error loading attack icon: {e}")
            # Fallback without icon
            attack_btn = tk.Button(
                button_frame,
                text="Atacar",
                command=self.handle_attack,
                font=("Arial", 12),
                bg='#E74C3C',
                fg='white',
                padx=15,
                pady=5
            )
            attack_btn.pack(side='left', padx=5)

        # Special Attack button with icon
        try:
            special_image = Image.open("assets/especial_attack_icon.png")
            special_image = special_image.resize((20, 20), Image.Resampling.LANCZOS)
            special_photo = ImageTk.PhotoImage(special_image)
            special_btn = tk.Button(
                button_frame,
                text="Ataque Especial",
                image=special_photo,
                compound=tk.LEFT,
                command=self.handle_special_attack,
                font=("Arial", 12),
                bg='#8E44AD',
                fg='white',
                padx=15,
                pady=5
            )
            special_btn.image = special_photo
            special_btn.pack(side='left', padx=5)
        except Exception as e:
            print(f"Error loading special attack icon: {e}")
            # Fallback without icon
            special_btn = tk.Button(
                button_frame,
                text="Ataque Especial",
                command=self.handle_special_attack,
                font=("Arial", 12),
                bg='#8E44AD',
                fg='white',
                padx=15,
                pady=5
            )
            special_btn.pack(side='left', padx=5)

        # Potion button with icon
        try:
            potion_image = Image.open("assets/potion_icon.png")
            potion_image = potion_image.resize((20, 20), Image.Resampling.LANCZOS)
            potion_photo = ImageTk.PhotoImage(potion_image)
            potion_btn = tk.Button(
                button_frame,
                text=f"Usar Poção ({self.player.health_potions})",
                image=potion_photo,
                compound=tk.LEFT,
                command=self.handle_potion,
                font=("Arial", 12),
                bg='#27AE60',
                fg='white',
                padx=15,
                pady=5
            )
            potion_btn.image = potion_photo
            potion_btn.pack(side='left', padx=5)
        except Exception as e:
            print(f"Error loading potion icon: {e}")
            # Fallback without icon
            potion_btn = tk.Button(
                button_frame,
                text=f"Usar Poção ({self.player.health_potions})",
                command=self.handle_potion,
                font=("Arial", 12),
                bg='#27AE60',
                fg='white',
                padx=15,
                pady=5
            )
            potion_btn.pack(side='left', padx=5)

    def start_game(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Escreva seu nome!")
            return

        character_class = self.char_var.get()
        if character_class == "Warrior":
            self.player = Warrior(name)
        else:
            self.player = Mage(name)

        self.stage = 1
        self.start_stage()

    def start_stage(self):
        if self.stage > 5:
            messagebox.showinfo("Parabéns!", 
                f"Você venceu todos os inimigos!")
            # self.window.quit()
            return

        # Create enemies based on stage
        if self.stage < 3:
            self.current_enemy = Goblin()
        else:
            self.current_enemy = Orc()

        self.create_combat_gui()

    def handle_attack(self):
        if not self.current_enemy or not self.current_enemy.is_alive():
            return

        # Player attacks and generates resource
        damage = self.player.attack()
        self.current_enemy.take_damage(damage)
        
        # Generate rage/mana on attack
        resource_message = ""
        if isinstance(self.player, Warrior):
            rage_gain = 10
            self.player.rage = min(100, self.player.rage + rage_gain)
            resource_message = f"\nRaiva gerada: +{rage_gain}"
        elif isinstance(self.player, Mage):
            mana_gain = 15
            self.player.mana = min(100, self.player.mana + mana_gain)
            resource_message = f"\nMana regenerada: +{mana_gain}"
        
        # Enemy attacks if alive
        if self.current_enemy.is_alive():
            enemy_damage = self.current_enemy.attack()
            self.player.take_damage(enemy_damage)
            message = f"Você causou {damage} de dano!{resource_message}\nInimigo causou {enemy_damage} de dano!"
        else:
            message = self.handle_enemy_defeat()

        self.create_combat_gui()
        messagebox.showinfo("Combate", message)

        if not self.player.is_alive():
            messagebox.showinfo("Game Over", "Você foi derrotado!")
            self.window.quit()

    def handle_special_attack(self):
        if not self.current_enemy or not self.current_enemy.is_alive():
            return

        # Player special attack
        message, damage = self.player.special_ability()
        self.current_enemy.take_damage(damage)
        
        # Enemy attacks if alive
        if self.current_enemy.is_alive():
            enemy_damage = self.current_enemy.attack()
            self.player.take_damage(enemy_damage)
            message += f"\nEnemy deals {enemy_damage} damage!"
        else:
            message += "\n" + self.handle_enemy_defeat()

        self.create_combat_gui()
        messagebox.showinfo("Combat Round", message)

        if not self.player.is_alive():
            messagebox.showinfo("Game Over", "You have been defeated!")
            self.window.quit()

    def handle_potion(self):
        message = self.player.use_health_potion()
        self.create_combat_gui()
        messagebox.showinfo("Use Potion", message)

    def handle_enemy_defeat(self):
        loot_message = self.player.collect_loot(self.current_enemy.drop_loot())
        self.player.gain_experience(25)
        level_message = ""
        if self.player.experience >= 100:
            level_message = "\n" + self.player.level_up()
        
        self.stage += 1
        self.start_stage()
        
        return f"Enemy defeated!\n{loot_message}{level_message}"

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = RPGGame()
    game.run() 
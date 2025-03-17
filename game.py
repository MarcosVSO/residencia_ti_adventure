import tkinter as tk
from tkinter import ttk, messagebox
from character import Warrior, Mage
from enemy import Goblin, Orc
import random
from PIL import Image, ImageTk
import pygame

class RPGGame:
    def __init__(self):
        # Inicializa a janela principal do jogo
        self.window = tk.Tk()
        self.window.title("Residência TI Adventure")
        self.window.geometry("800x600")
        self.window.configure(bg='#2C3E50')
        
        # Inicializa o sistema de áudio
        pygame.mixer.init()
        
        # Carrega os efeitos sonoros do jogo
        try:
            self.title_sound = pygame.mixer.Sound("assets/title_screen_sound.mp3")
            self.fight_sound = pygame.mixer.Sound("assets/fight_screen_sound.mp3")
            self.victory_sound = pygame.mixer.Sound("assets/victory_sound.mp3")
        except Exception as e:
            print(f"Erro ao carregar sons: {e}")
            self.title_sound = None
            self.fight_sound = None
            self.victory_sound = None
        
        # Inicializa variáveis do jogo
        self.player = None
        self.current_enemy = None
        self.stage = 0
        self.setup_gui()
        
        # Inicia a música da tela inicial
        if self.title_sound:
            self.title_sound.play(-1)

    def setup_gui(self):
        # Carrega e exibe o logo do jogo
        try:
            logo_image = Image.open("assets/logo_residencia_ti_adventure.png")
            logo_image = logo_image.resize((300, 300), Image.Resampling.LANCZOS)
            logo_photo = ImageTk.PhotoImage(logo_image)
            logo_label = tk.Label(
                self.window,
                image=logo_photo,
                bg='#2C3E50'
            )
            logo_label.image = logo_photo
            logo_label.pack(pady=10)
        except Exception as e:
            print(f"Erro ao carregar logo: {e}")

        # Configuração da seleção de personagem
        self.char_var = tk.StringVar(value="Warrior")
        char_frame = tk.Frame(self.window, bg='#2C3E50')
        char_frame.pack(pady=10)

        # Rótulo para seleção de personagem
        char_label = tk.Label(
            char_frame,
            text="Selecione seu personagem",
            font=("Arial", 12),
            bg='#2C3E50',
            fg='white'
        )
        char_label.pack()

        # Frame para os personagens lado a lado
        char_select_frame = tk.Frame(char_frame, bg='#2C3E50')
        char_select_frame.pack(pady=10)

        # Frame do Guerreiro
        warrior_frame = tk.Frame(char_select_frame, bg='#2C3E50')
        warrior_frame.pack(side='left', padx=20)
        
        # Carrega e exibe o ícone do Guerreiro
        try:
            warrior_image = Image.open("assets/warrior_icon.png")
            warrior_image = warrior_image.resize((80, 80), Image.Resampling.LANCZOS)
            warrior_photo = ImageTk.PhotoImage(warrior_image)
            warrior_icon = tk.Label(
                warrior_frame,
                image=warrior_photo,
                bg='#2C3E50'
            )
            warrior_icon.image = warrior_photo
            warrior_icon.pack(pady=5)
        except Exception as e:
            print(f"Erro ao carregar ícone do guerreiro: {e}")

        # Botão de rádio para selecionar Guerreiro
        warrior_rb = ttk.Radiobutton(
            warrior_frame,
            text="Guerreiro",
            value="Warrior",
            variable=self.char_var
        )
        warrior_rb.pack()

        # Frame do Mago
        mage_frame = tk.Frame(char_select_frame, bg='#2C3E50')
        mage_frame.pack(side='left', padx=20)
        
        # Carrega e exibe o ícone do Mago
        try:
            mage_image = Image.open("assets/mage_icon.png")
            mage_image = mage_image.resize((80, 80), Image.Resampling.LANCZOS)
            mage_photo = ImageTk.PhotoImage(mage_image)
            mage_icon = tk.Label(
                mage_frame,
                image=mage_photo,
                bg='#2C3E50'
            )
            mage_icon.image = mage_photo
            mage_icon.pack(pady=5)
        except Exception as e:
            print(f"Erro ao carregar ícone do mago: {e}")

        # Botão de rádio para selecionar Mago
        mage_rb = ttk.Radiobutton(
            mage_frame,
            text="Mago",
            value="Mage",
            variable=self.char_var
        )
        mage_rb.pack()

        # Frame para entrada do nome
        name_frame = tk.Frame(self.window, bg='#2C3E50')
        name_frame.pack(pady=10)

        # Rótulo para entrada do nome
        name_label = tk.Label(
            name_frame,
            text="Digite seu nome:",
            font=("Arial", 12),
            bg='#2C3E50',
            fg='white'
        )
        name_label.pack()

        # Campo de entrada do nome
        self.name_entry = tk.Entry(name_frame)
        self.name_entry.pack()

        # Botão para iniciar o jogo
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
        # Limpa a janela e configura o tamanho
        self.window.geometry("800x600")
        for widget in self.window.winfo_children():
            widget.destroy()

        # Frame para status do jogador
        status_frame = tk.Frame(self.window, bg='#2C3E50')
        status_frame.pack(fill='x', padx=20, pady=10)

        # Frame para informações do jogador
        player_status_frame = tk.Frame(status_frame, bg='#2C3E50')
        player_status_frame.pack(side='left', padx=10)

        # Frame para nome do jogador com ícone
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
            print(f"Erro ao carregar ícone do personagem: {e}")
        
        # Exibe nome do jogador
        tk.Label(
            name_frame,
            text=f"Jogador: {self.player.name}",
            font=("Arial", 12, "bold"),
            bg='#2C3E50',
            fg='white'
        ).pack(side='left')

        # Frame para HP com ícone
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
            print(f"Erro ao carregar ícone de HP: {e}")
        
        # Exibe HP do jogador
        tk.Label(
            hp_frame,
            text=f"HP: {self.player.health}/{self.player.max_health}",
            font=("Arial", 12),
            bg='#2C3E50',
            fg='white'
        ).pack(side='left')

        # Frame para recurso (Raiva/Mana) com ícone
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
            print(f"Erro ao carregar ícone de recurso: {e}")
        
        # Exibe recurso do jogador (Raiva ou Mana)
        resource_text = f"Raiva: {self.player.rage}" if isinstance(self.player, Warrior) else f"Mana: {self.player.mana}"
        tk.Label(
            resource_frame,
            text=resource_text,
            font=("Arial", 12),
            bg='#2C3E50',
            fg='white'
        ).pack(side='left')

        # Frame para nível com ícone
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
            print(f"Erro ao carregar ícone de nível: {e}")
        
        # Exibe nível do jogador
        tk.Label(
            level_frame,
            text=f"Nível: {self.player.level}",
            font=("Arial", 12),
            bg='#2C3E50',
            fg='white'
        ).pack(side='left')

        # Frame para ouro com ícone
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
            print(f"Erro ao carregar ícone de ouro: {e}")
        
        # Exibe ouro do jogador
        tk.Label(
            gold_frame,
            text=f"Ouro: {self.player.gold}",
            font=("Arial", 12),
            bg='#2C3E50',
            fg='white'
        ).pack(side='left')

        # Exibe informação da fase atual
        stage_info = tk.Label(
            self.window,
            text=f"Fase {self.stage}/5",
            font=("Arial", 16, "bold"),
            bg='#2C3E50',
            fg='white'
        )
        stage_info.pack(pady=10)

        # Exibe inimigo atual com ícone
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

            # Exibe informações do inimigo
            enemy_info = tk.Label(
                self.window,
                text=f"{self.current_enemy.name} | HP: {self.current_enemy.health}",
                font=("Arial", 14),
                bg='#2C3E50',
                fg='white'
            )
            enemy_info.pack(pady=10)

        # Frame para botões de combate
        button_frame = tk.Frame(self.window, bg='#2C3E50')
        button_frame.pack(pady=20)

        # Botão de ataque com ícone
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
            print(f"Erro ao carregar ícone de ataque: {e}")
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

        # Botão de ataque especial com ícone
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
            print(f"Erro ao carregar ícone de ataque especial: {e}")
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

        # Botão de poção com ícone
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
            print(f"Erro ao carregar ícone de poção: {e}")
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
        # Verifica se o nome foi digitado
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Escreva seu nome!")
            return

        # Troca a música da tela inicial pela música de combate
        if self.title_sound:
            self.title_sound.stop()
        if self.fight_sound:
            self.fight_sound.play(-1)

        # Cria o personagem baseado na seleção
        character_class = self.char_var.get()
        if character_class == "Warrior":
            self.player = Warrior(name)
        else:
            self.player = Mage(name)

        # Inicia o jogo
        self.stage = 1
        self.start_stage()

    def start_stage(self):
        # Verifica se o jogo foi completado
        if self.stage > 5:
            # Toca o som de vitória
            if self.fight_sound:
                self.fight_sound.stop()
            if self.victory_sound:
                self.victory_sound.play()
            
            messagebox.showinfo("Parabéns!", 
                f"Você venceu todos os inimigos!")
            self.window.quit()
            return

        # Cria o inimigo baseado na fase
        if self.stage < 3:
            self.current_enemy = Goblin()
        else:
            self.current_enemy = Orc()

        self.create_combat_gui()

    def handle_attack(self):
        # Verifica se há um inimigo vivo
        if not self.current_enemy or not self.current_enemy.is_alive():
            return

        # Jogador ataca
        damage = self.player.attack()
        self.current_enemy.take_damage(damage)
        
        # Gera recurso (Raiva/Mana) baseado no tipo de personagem
        resource_message = ""
        if isinstance(self.player, Warrior):
            rage_gain = 10
            self.player.rage = min(100, self.player.rage + rage_gain)
            resource_message = f"\nRaiva gerada: +{rage_gain}"
        elif isinstance(self.player, Mage):
            mana_gain = 15
            self.player.mana = min(100, self.player.mana + mana_gain)
            resource_message = f"\nMana regenerada: +{mana_gain}"
        
        # Inimigo contra-ataca se estiver vivo
        if self.current_enemy.is_alive():
            enemy_damage = self.current_enemy.attack()
            self.player.take_damage(enemy_damage)
            message = f"Você causou {damage} de dano!{resource_message}\nInimigo causou {enemy_damage} de dano!"
        else:
            message = self.handle_enemy_defeat()

        self.create_combat_gui()
        messagebox.showinfo("Combate", message)

        # Verifica se o jogador morreu
        if not self.player.is_alive():
            messagebox.showinfo("Game Over", "Você foi derrotado!")
            self.window.quit()

    def handle_special_attack(self):
        # Verifica se há um inimigo vivo
        if not self.current_enemy or not self.current_enemy.is_alive():
            return

        # Jogador usa ataque especial
        message, damage = self.player.special_ability()
        self.current_enemy.take_damage(damage)
        
        # Inimigo contra-ataca se estiver vivo
        if self.current_enemy.is_alive():
            enemy_damage = self.current_enemy.attack()
            self.player.take_damage(enemy_damage)
            message += f"\nInimigo causa {enemy_damage} de dano!"
        else:
            message += "\n" + self.handle_enemy_defeat()

        self.create_combat_gui()
        messagebox.showinfo("Combate", message)

        # Verifica se o jogador morreu
        if not self.player.is_alive():
            messagebox.showinfo("Game Over", "Você foi derrotado!")
            self.window.quit()

    def handle_potion(self):
        # Usa poção de vida
        message = self.player.use_health_potion()
        self.create_combat_gui()
        messagebox.showinfo("Usou poção!", message)

    def handle_enemy_defeat(self):
        # Coleta loot do inimigo
        loot_message = self.player.collect_loot(self.current_enemy.drop_loot())
        self.player.gain_experience(25)
        level_message = ""
        if self.player.experience >= 100:
            level_message = "\n" + self.player.level_up()
        
        # Avança para a próxima fase
        self.stage += 1
        self.start_stage()
        
        return f"Inimigo Derrotado!\n{loot_message}{level_message}"

    def __del__(self):
        # Limpa o sistema de áudio ao fechar o jogo
        try:
            pygame.mixer.quit()
        except:
            pass

    def run(self):
        # Inicia o loop principal do jogo
        self.window.mainloop()

if __name__ == "__main__":
    game = RPGGame()
    game.run() 
import pygame
import math
import random
import sys
import main as accueil
from setting import *
import cv2

# Initialisation de Pygame
pygame.init()
running = True
paused = False

info = pygame.display.Info()
LARGEUR_ECRAN, HAUTEUR_ECRAN = info.current_w, info.current_h

# Taille de la carte (map)
largeur_map = LARGEUR_ECRAN * 2
hauteur_map = HAUTEUR_ECRAN * 2

x = largeur_map // 2 - square_size // 2  # Position initiale du carré (au centre de la carte)
y = hauteur_map // 2 - square_size // 2

# Fenêtre en plein écran
FENETRE = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN), pygame.FULLSCREEN)

logo = pygame.image.load("images/logo.png").convert_alpha()

# Charge les images du personnages pour son animation
marche_droit = [pygame.image.load(f'images/homme_droit_{i}.png') for i in range(1, 3)]
marche_gauche = [pygame.image.load(f'images/homme_gauche_{i}.png') for i in range(1, 3)]
marche_haut = [pygame.image.load(f'images/homme_haut_{i}.png') for i in range(1, 3)]
marche_bas = [pygame.image.load(f'images/homme_bas_{i}.png') for i in range(1, 3)]

# Recadre les images du personnages à la bonne taille si besoin
marche_droit = [pygame.transform.scale(img, (square_size, square_size)) for img in marche_droit]
marche_gauche = [pygame.transform.scale(img, (square_size, square_size)) for img in marche_gauche]
marche_haut = [pygame.transform.scale(img, (square_size, square_size)) for img in marche_haut]
marche_bas = [pygame.transform.scale(img, (square_size, square_size)) for img in marche_bas]

# Charger l'image de fond
fond = pygame.image.load('images/test_map.jpg')

# Redimensionner l'image si nécessaire
fond = pygame.transform.scale(fond, (largeur_map, hauteur_map))

# Gestion du temps pour l'animation du personnage
current_frame = 0
frame_delay = 5  # Nombre de frames avant de changer d'image
frame_count = 0
current_direction = "bas"

# Classe Bouton
class Bouton:
    def __init__(self, texte, position, action, image=None):
        self.texte = texte
        self.position = position
        self.action = action
        self.image = image
        if self.image:
            self.rect = self.image.get_rect(topleft=position)
        else:
            self.rect = pygame.Rect(position[0], position[1], 180, 50)
        self.couleur = (30, 30, 30)
        self.couleur_hover = (60, 60, 60)

    def dessiner(self, surface):
        couleur = self.couleur_hover if self.rect.collidepoint(pygame.mouse.get_pos()) else self.couleur
        if self.image:
            surface.blit(self.image, self.rect.topleft)
        else:
            pygame.draw.rect(surface, couleur, self.rect, border_radius=5)
            font = pygame.font.Font(None, 36)
            texte_surface = font.render(self.texte, True, (255, 255, 255))
            texte_rect = texte_surface.get_rect(center=self.rect.center)
            surface.blit(texte_surface, texte_rect)

    def clic(self, pos):
        return self.rect.collidepoint(pos)

# Fonction pour afficher le menu de pause
def afficher_menu_pause():
    """Affiche le menu de pause."""
    clock = pygame.time.Clock()
    
    # Charger les images des boutons
    image_controles = pygame.image.load('images/bouton_controles.png').convert_alpha()
    image_quitter = pygame.image.load('images/bouton_quitter.png').convert_alpha()
    
    # Redimensionner les images des boutons pour qu'elles aient la taille souhaitée
    largeur_bouton = 200  # Largeur souhaitée pour les boutons
    hauteur_bouton = 110   # Hauteur souhaitée pour les boutons
    image_controles = pygame.transform.scale(image_controles, (largeur_bouton, hauteur_bouton))
    image_quitter = pygame.transform.scale(image_quitter, (largeur_bouton, hauteur_bouton))
    
    boutons = [
        Bouton("Contrôles", (LARGEUR_ECRAN // 2 - largeur_bouton // 2, HAUTEUR_ECRAN // 2 - 60), afficher_controles(), image=image_controles),
        Bouton("Quitter", (LARGEUR_ECRAN // 2 - largeur_bouton // 2, HAUTEUR_ECRAN // 2 + 60), lambda: pygame.quit() or sys.exit(), image=image_quitter)
    ]
    
    while True:
        FENETRE.blit(fond, (0, 0))
        for bouton in boutons:
            bouton.dessiner(FENETRE)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for bouton in boutons:
                    if bouton.clic(event.pos):
                        bouton.action()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return  # Retourner au jeu
        
        clock.tick(30)
# Fonction pour avoir la bonne image de l'animation
def get_current_image():
    if current_direction == "droit":
        return marche_droit[current_frame]
    elif current_direction == "gauche":
        return marche_gauche[current_frame]
    elif current_direction == "haut":
        return marche_haut[current_frame]
    elif current_direction == "bas":
        return marche_bas[current_frame]
    return marche_bas[0]

# Fonction pour afficher le menu de pause
def pause_menu():
    global paused
    paused = True
    afficher_menu_pause()
    paused = False

# Fonction pour afficher la carte de la map
def pause_map():
    global paused
    paused = True  # Bloque le jeu pendant l'affichage de la carte
    font = pygame.font.Font(None, 50)

    while paused:
        # Afficher la carte complète redimensionnée pour tenir dans l'écran
        mini_map = pygame.transform.scale(fond, (LARGEUR_ECRAN, HAUTEUR_ECRAN))
        FENETRE.blit(mini_map, (0, 0))

        # Calculer la position du joueur sur la mini-map
        player_map_x = int(x / largeur_map * LARGEUR_ECRAN)
        player_map_y = int(y / hauteur_map * HAUTEUR_ECRAN)

        # Dessiner un rond de couleur derrière l'image du personnage
        pygame.draw.circle(FENETRE, (0, 255, 0), (player_map_x, player_map_y), square_size // 4 + 3)
        # Dessiner l'image du personnage
        player_image = pygame.transform.scale(marche_bas[0], (square_size//2, square_size//2))
        FENETRE.blit(player_image, (player_map_x - player_image.get_width() // 2, player_map_y - player_image.get_height() // 2))

        # Dessiner les ennemis sur la mini-carte
        for ennemi in ennemis:
            ennemi_map_x = int(ennemi.x / largeur_map * LARGEUR_ECRAN)
            ennemi_map_y = int(ennemi.y / hauteur_map * HAUTEUR_ECRAN)
            # Dessiner un rond de couleur derrière l'image de l'ennemi
            pygame.draw.circle(FENETRE, (255, 0, 0), (ennemi_map_x, ennemi_map_y), ennemi.size // 4 + 3)
            ennemi_image = pygame.transform.scale(ennemi.image, (ennemi.size//2, ennemi.size//2))
            FENETRE.blit(ennemi_image, (ennemi_map_x - ennemi_image.get_width() // 2, ennemi_map_y - ennemi_image.get_height() // 2))

        # Ajouter du texte pour quitter la carte
        text = font.render("Appuyez sur 'E' pour revenir au jeu", True, (255, 255, 255))
        text_rect = text.get_rect(center=(LARGEUR_ECRAN // 2, HAUTEUR_ECRAN - 50))
        FENETRE.blit(text, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                paused = False  # Retour au jeu

# Gestion de la batterie
battery = 100.0  # Batterie en pourcentage
battery_drain_rate = 5.0  # Pourcentage par seconde
clock = pygame.time.Clock()

# Fonction pour dessiner la batterie
def draw_battery():
    """Affiche la barre de batterie en bas et au centre de l'écran."""
    bar_width = 300
    bar_height = 20
    bar_x = (LARGEUR_ECRAN - bar_width) // 2
    bar_y = HAUTEUR_ECRAN - 40  # Position en bas de l'écran
    fill_width = int((battery / 100) * bar_width)
    pygame.draw.rect(FENETRE, noir, (bar_x, bar_y, bar_width, bar_height))
    pygame.draw.rect(FENETRE, vert if battery > 30 else rouge, (bar_x, bar_y, fill_width, bar_height))

def draw_health_bar():
    """Affiche la barre de vie en haut et au centre de l'écran."""
    bar_width = 300
    bar_height = 20
    bar_x = (LARGEUR_ECRAN - bar_width) // 2
    bar_y = 20  # Position en haut de l'écran
    fill_width = int((player_health / 100) * bar_width)
    pygame.draw.rect(FENETRE, noir, (bar_x, bar_y, bar_width, bar_height))
    pygame.draw.rect(FENETRE, vert if player_health > 30 else rouge, (bar_x, bar_y, fill_width, bar_height))

# Fonction pour créer et afficher le cône de lumière de la lampe-torche   
def cone_lumiere():
    """Affiche un cône de lumière avec un dégradé basé uniquement sur la distance et retourne les coordonnées du cône."""
    # Position du joueur sur l'écran
    player_screen_x = x - camera_x + square_size // 2
    player_screen_y = y - camera_y + square_size // 2

    # Direction vers la souris
    mouse_x, mouse_y = pygame.mouse.get_pos()
    dx = mouse_x - player_screen_x
    dy = mouse_y - player_screen_y
    angle = math.atan2(dy, dx)

    # Créer un masque semi-transparent
    mask = pygame.Surface((LARGEUR_ECRAN, HAUTEUR_ECRAN), pygame.SRCALPHA)
    mask.fill((0, 0, 0, 245))  # Ombre globale sur toute la scène

    cone_points = []

    if battery > 0:
        # Générer le cône de lumière avec un dégradé en fonction de la distance
        for i in range(cone_length, 0, -5):  # De l'intérieur vers l'extérieur
            # Calcul de l'opacité qui diminue avec la distance
            distance_factor = i / cone_length
            alpha = int(245 * (1 - distance_factor))  # Plus loin, moins intense

            color = (0, 0, 0, 245 - alpha)  # Noir avec un dégradé d'opacité, minimum à 0

            # Calcul du cône de lumière
            points = [(player_screen_x, player_screen_y)]  # Point de départ du cône (joueur)

            for j in range(-cone_angle // 2, cone_angle // 2 + 1, 5):
                ray_angle = angle + math.radians(j)
                end_x = player_screen_x + math.cos(ray_angle) * i
                end_y = player_screen_y + math.sin(ray_angle) * i
                points.append((end_x, end_y))

            # Vérifier si le polygone est valide avant de le dessiner
            if len(points) > 2:
                pygame.draw.polygon(mask, color, points)
                if i == cone_length:
                    cone_points = points

    # Assurer que le personnage soit toujours éclairé (cercle lumineux autour du personnage)
    player_light_radius = 65  # Rayon de la lumière autour du personnage
    pygame.draw.circle(mask, (0, 0, 0, 0), (player_screen_x, player_screen_y), player_light_radius)

    # Appliquer le masque à l'écran
    FENETRE.blit(mask, (0, 0))

    return cone_points

# Fonction pour vérifier si l'ennemi est dans le cône de lumière
def is_point_in_cone(px, py, cone_points):
    """Vérifie si un point (px, py) est dans le cône défini par cone_points."""
    if len(cone_points) < 3:
        return False

    # Utiliser la méthode de l'algorithme de l'angle pour vérifier si le point est dans le polygone
    angle_sum = 0
    for i in range(len(cone_points)):
        x1, y1 = cone_points[i]
        x2, y2 = cone_points[(i + 1) % len(cone_points)]
        angle = math.atan2(y2 - py, x2 - px) - math.atan2(y1 - py, x1 - px)
        if angle >= math.pi:
            angle -= 2 * math.pi
        elif angle <= -math.pi:
            angle += 2 * math.pi
        angle_sum += angle

    return abs(angle_sum) > 1e-6

# Initialisation de la class Ennemi
class Ennemi:
    def __init__(self, x, y, size=64):
        self.x = x
        self.y = y
        self.size = size
        self.speed = 5
        self.direction = random.choice(['haut', 'bas', 'gauche', 'droite'])
        self.timer = 0
        self.time_in_light = 0  # Temps passé dans le cône de lumière
        self.image = pygame.image.load('images/ennemi.png')
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.attack_cooldown = 0

    def ennemiIA(self, player_x, player_y, dt):
        """Gère le mouvement des ennemis en fonction du joueur."""
        global player_health

        distance_to_player = ((self.x - player_x) ** 2 + (self.y - player_y) ** 2) ** 0.5

        if distance_to_player < 300:
            # L'ennemi suit le joueur
            dx = player_x - self.x
            dy = player_y - self.y
            angle = math.atan2(dy, dx)
            self.x += self.speed * math.cos(angle)
            self.y += self.speed * math.sin(angle)

            # Infliger des dégâts au joueur
            if distance_to_player < self.size and self.attack_cooldown <= 0:
                player_health -= 10
                player_health = max(player_health, 0)
                self.attack_cooldown = 1  # 1 seconde de cooldown avant la prochaine attaque
        else:
            # L'ennemi se déplace aléatoirement
            self.time_in_light = 0
            self.timer += 1
            if self.timer > 30:  # Change de direction toutes les 30 frames
                self.direction = random.choice(['haut', 'bas', 'gauche', 'droite'])
                self.timer = 0
            if self.direction == 'haut':
                self.y -= self.speed
            elif self.direction == 'bas':
                self.y += self.speed
            elif self.direction == 'gauche':
                self.x -= self.speed
            elif self.direction == 'droite':
                self.x += self.speed

        # Empêcher l'ennemi de sortir de la carte
        self.x = max(0, min(largeur_map - self.size, self.x))
        self.y = max(0, min(hauteur_map - self.size, self.y))

        # Réduire le cooldown de l'attaque
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt

    def deposer_moisissure(self):
        """Dépose de la moisissure à la position actuelle de l'ennemi."""
        moisissures.append((self.x, self.y))

# Fonction pour faire apparaître les ennemis aléatoirement sur la map à intervalle régulier
def spawn_ennemi():
    """Génère un ennemi à une position aléatoire sur la carte."""
    ennemi_x = random.randint(0, largeur_map - 64)
    ennemi_y = random.randint(0, hauteur_map - 64)
    ennemi = Ennemi(ennemi_x, ennemi_y)
    ennemis.append(ennemi)

# Fonction pour afficher le compteur d'ennemis tués par le joueur
def draw_enemy_counter():
    font = pygame.font.Font(None, 40)
    text = font.render(f"Ennemis tués: {ennemis_tues}", True, (255, 255, 255))
    text_rect = text.get_rect(center=(LARGEUR_ECRAN // 2, 50))
    FENETRE.blit(text, text_rect)

# Dictionnaire pour stocker le temps de début de nettoyage pour chaque moisissure
nettoyage_temps_debut = {}

# Fonction pour afficher la moisissure laissée par les ennemis à leur mort
def nettoyer_moisissure():
    cone_points = []
    mouse_x, mouse_y = pygame.mouse.get_pos()
    temps_actuel = pygame.time.get_ticks()
    for moisissure in moisissures[:]:
        moisissure_screen_x = moisissure[0] - camera_x
        moisissure_screen_y = moisissure[1] - camera_y
        if is_point_in_cone(moisissure_screen_x, moisissure_screen_y, cone_points):
            distance = math.sqrt((mouse_x - moisissure_screen_x) ** 2 + (mouse_y - moisissure_screen_y) ** 2)
            if distance < 75:  # Si la souris est suffisamment proche de la moisissure
                if pygame.mouse.get_pressed()[0]:  # Si le bouton gauche de la souris est enfoncé
                    if moisissure not in nettoyage_temps_debut:
                        nettoyage_temps_debut[moisissure] = temps_actuel
                    elif temps_actuel - nettoyage_temps_debut[moisissure] >= 1500:  # 1500 ms = 1,5 secondes
                        moisissures.remove(moisissure)
                        del nettoyage_temps_debut[moisissure]
                else:
                    if moisissure in nettoyage_temps_debut:
                        del nettoyage_temps_debut[moisissure]
            else:
                if moisissure in nettoyage_temps_debut:
                    del nettoyage_temps_debut[moisissure]

spawn_timer = 0
spawn_interval = 5  # Intervalle de génération des ennemis en secondes

dialogues = [
    "Qu'est ce qu'il s'est passé ? Où suis-je ?",
    "Je me suis fait absorbé par le tableau ?",
    "Il faut que je trouve un moyen de sortir d'ici !"
]
current_dialogue_index = 0
show_dialogue = True
dialogue_speed = 50  # Vitesse d'affichage des lettres (en millisecondes)
last_update_time = 0
current_letter_index = 0
show_ellipsis = False
ellipsis_timer = 0
ellipsis_interval = 500  # Intervalle de clignotement des "..." (en millisecondes)
dialogues_termines = False

def draw_rounded_rect(surface, rect, color, corner_radius, border_width=0, border_color=(0, 0, 0)):
    """Draw a rectangle with rounded corners and an optional border."""
    if border_width:
        outer_rect = rect.inflate(border_width * 2, border_width * 2)
        pygame.draw.rect(surface, border_color, outer_rect, border_radius=corner_radius + border_width)
    pygame.draw.rect(surface, color, rect, border_radius=corner_radius)

def draw_dialogue():
    """Affiche le dialogue actuel en bas à gauche de l'écran."""
    global last_update_time, current_letter_index, show_ellipsis, ellipsis_timer

    if show_dialogue and current_dialogue_index < len(dialogues):
        current_time = pygame.time.get_ticks()
        font = pygame.font.Font(None, 36)
        instruction_font = pygame.font.Font(None, 24)
        
        dialogue_text = dialogues[current_dialogue_index]
        instruction_text = "Appuyez sur 'Espace' pour continuer"
        
        # Afficher les lettres une par une
        if current_time - last_update_time > dialogue_speed:
            current_letter_index += 1
            last_update_time = current_time

        # Limiter l'index des lettres à la longueur du texte
        current_letter_index = min(current_letter_index, len(dialogue_text))
        displayed_text = dialogue_text[:current_letter_index]

        # Gérer les "..." clignotants
        if current_letter_index == len(dialogue_text) and current_dialogue_index < len(dialogues) - 1:
            if current_time - ellipsis_timer > ellipsis_interval:
                show_ellipsis = not show_ellipsis
                ellipsis_timer = current_time
            if show_ellipsis:
                displayed_text += "..."

        dialogue_surface = font.render(displayed_text, True, (0, 0, 0))
        instruction_surface = instruction_font.render(instruction_text, True, (0, 0, 0))
        
        dialogue_rect = dialogue_surface.get_rect(topleft=(20, HAUTEUR_ECRAN - 100))
        instruction_rect = instruction_surface.get_rect(topleft=(20, dialogue_rect.bottom + 5))
        
        # Calculer la taille totale du cadre
        total_width = max(dialogue_rect.width, instruction_rect.width) + 20
        total_height = dialogue_rect.height + instruction_rect.height + 30
        
        # Positionner le cadre avec un espace par rapport au bord de l'écran
        frame_rect = pygame.Rect(20, HAUTEUR_ECRAN - total_height - 20, total_width, total_height)
        
        # Dessiner le cadre blanc avec un contour noir et des bords arrondis
        corner_radius = 20
        border_width = 4
        draw_rounded_rect(FENETRE, frame_rect, (255, 255, 255), corner_radius, border_width, (0, 0, 0))
        
        # Dessiner le texte dans le cadre
        FENETRE.blit(dialogue_surface, (frame_rect.x + 10, frame_rect.y + 10))
        FENETRE.blit(instruction_surface, (frame_rect.x + 10, frame_rect.y + dialogue_rect.height + 15))

VISIBILITY_DISTANCE = 100  # Distance à laquelle les ennemis deviennent visibles

def afficher_menu_pause():
    """Affiche le menu de pause."""
    clock = pygame.time.Clock()
    
    # Charger les images des boutons
    image_controles = pygame.image.load('images/bouton_controles.png').convert_alpha()
    image_quitter = pygame.image.load('images/bouton_quitter.png').convert_alpha()
    
    # Redimensionner les images des boutons pour qu'elles aient la taille souhaitée
    largeur_bouton = 200  # Largeur souhaitée pour les boutons
    hauteur_bouton = 110   # Hauteur souhaitée pour les boutons
    image_controles = pygame.transform.scale(image_controles, (largeur_bouton, hauteur_bouton))
    image_quitter = pygame.transform.scale(image_quitter, (largeur_bouton, hauteur_bouton))
    
    boutons = [
        Bouton("Contrôles", (LARGEUR_ECRAN // 2 - largeur_bouton // 2, HAUTEUR_ECRAN // 2 - 60), afficher_controles, image=image_controles),
        Bouton("Quitter", (LARGEUR_ECRAN // 2 - largeur_bouton // 2, HAUTEUR_ECRAN // 2 + 60), accueil.afficher_menu_principal, image=image_quitter)
    ]
    
    while True:
        FENETRE.blit(fond, (0, 0))
        FENETRE.blit(logo, (LARGEUR_ECRAN // 2 - logo.get_width() // 2, 50))
        for bouton in boutons:
            bouton.dessiner(FENETRE)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for bouton in boutons:
                    if bouton.clic(event.pos):
                        bouton.action()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return  # Retourner au jeu
        
        clock.tick(30)

# Charger et redimensionner les images des touches
touche_Z = pygame.transform.scale(pygame.image.load('images/touche_Z.png').convert_alpha(), (64, 64))
touche_S = pygame.transform.scale(pygame.image.load('images/touche_S.png').convert_alpha(), (64, 64))
touche_D = pygame.transform.scale(pygame.image.load('images/touche_D.png').convert_alpha(), (64, 64))
touche_Q = pygame.transform.scale(pygame.image.load('images/touche_Q.png').convert_alpha(), (64, 64))
touche_Echap = pygame.transform.scale(pygame.image.load('images/touche_Echap.png').convert_alpha(), (64, 64))
touche_E = pygame.transform.scale(pygame.image.load('images/touche_E.png').convert_alpha(), (64, 64))
touche_CliqueDroit = pygame.transform.scale(pygame.image.load('images/touche_CliqueDroit.png').convert_alpha(), (64, 64))
touche_CliqueGauche = pygame.transform.scale(pygame.image.load('images/touche_CliqueGauche.png').convert_alpha(), (64, 64))

def draw_text_with_outline(surface, text, font, color, outline_color, pos, outline_width=2):
    text_surface = font.render(text, True, color)
    outline_surface = font.render(text, True, outline_color)
    x, y = pos
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx != 0 or dy != 0:
                surface.blit(outline_surface, (x + dx, y + dy))
    surface.blit(text_surface, pos)

def afficher_controles():
    """Affiche une fenêtre avec les contrôles du jeu."""
    controles_actif = True
    font = pygame.font.Font(None, 36)
    controles = [
        ("Aller en haut", touche_Z),
        ("Aller en bas", touche_S),
        ("Aller à droite", touche_D),
        ("Aller à gauche", touche_Q),
        ("Accéder au menu", touche_Echap),
        ("Accéder à la carte", touche_E),
        ("Allumer la lampe torche", touche_CliqueDroit),
        ("Nettoyer la moisissure", touche_CliqueGauche)
    ]
    
    bouton_retour = Bouton("Retour", (LARGEUR_ECRAN // 2 - 90, HAUTEUR_ECRAN - 100), afficher_menu_pause)
    
    while controles_actif:
        fond_controles = pygame.image.load("images/fond.jpg").convert()
        fond_controles = pygame.transform.scale(fond_controles, (LARGEUR_ECRAN, HAUTEUR_ECRAN))
        
        # Convertir l'image en format compatible avec OpenCV
        fond_controles_array = pygame.surfarray.array3d(fond_controles)
        fond_controles_array = cv2.cvtColor(fond_controles_array, cv2.COLOR_RGB2BGR)
        
        # Appliquer un flou léger
        fond_controles_array = cv2.GaussianBlur(fond_controles_array, (15, 15), 0)
        
        # Convertir l'image floue en format compatible avec Pygame
        fond_controles_array = cv2.cvtColor(fond_controles_array, cv2.COLOR_BGR2RGB)
        fond_controles = pygame.surfarray.make_surface(fond_controles_array)
        
        FENETRE.blit(fond_controles, (0, 0))      

        y_offset_left = int(HAUTEUR_ECRAN * 0.3)
        y_offset_right = int(HAUTEUR_ECRAN * 0.3)
        x_offset_left = int(LARGEUR_ECRAN * 0.25)
        x_offset_right = int(LARGEUR_ECRAN * 0.75)
        
        for i, (texte, image) in enumerate(controles):
            if i < 4:
                FENETRE.blit(image, (x_offset_left - 70, y_offset_left - 32))  # Ajustement pour centrer l'image
                draw_text_with_outline(FENETRE, texte, font, (255, 255, 255), (0, 0, 0), (x_offset_left, y_offset_left))
                y_offset_left += int(HAUTEUR_ECRAN * 0.15)
            else:
                FENETRE.blit(image, (x_offset_right - 70, y_offset_right - 32))  # Ajustement pour centrer l'image
                draw_text_with_outline(FENETRE, texte, font, (255, 255, 255), (0, 0, 0), (x_offset_right, y_offset_right))
                y_offset_right += int(HAUTEUR_ECRAN * 0.15)
        
        bouton_retour.dessiner(FENETRE)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                controles_actif = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_retour.clic(event.pos):
                    controles_actif = False
                    afficher_menu_pause

def main():
    global fond, x, y, running, camera_x, camera_y, frame_count, current_frame, current_direction, battery, cone_active, ennemis_tues, spawn_timer, spawn_interval, current_dialogue_index, show_dialogue, dialogue_speed, last_update_time, current_letter_index, show_ellipsis, ellipsis_timer, ellipsis_interval, dialogues_termines
    while running:
        pygame.time.delay(30)  # Contrôle la vitesse de la boucle

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause_menu()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                pause_map()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if show_dialogue:
                    current_dialogue_index += 1
                    current_letter_index = 0
                    last_update_time = pygame.time.get_ticks()
                    show_ellipsis = False
                    ellipsis_timer = 0
                    if current_dialogue_index >= len(dialogues):
                        show_dialogue = False
                        dialogues_termines = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                if battery > 0:
                    cone_active = not cone_active
        dt = clock.tick(30) / 1000.0  # Temps écoulé en secondes

        if cone_active:
            battery -= battery_drain_rate * dt
            battery = max(battery, 0)
            if battery == 0:
                cone_active = False
        else:
            battery += battery_drain_rate * dt
            battery = min(battery, 100)

        # Gestion des déplacements du personnage
        keys = pygame.key.get_pressed()
        moving = False
        if keys[pygame.K_q]:
            x -= velocity
            current_direction = "gauche"
            moving = True
        if keys[pygame.K_d]: 
            x += velocity
            current_direction = "droit"
            moving = True
        if keys[pygame.K_z]: 
            y -= velocity
            current_direction = "haut"
            moving = True
        if keys[pygame.K_s]:  
            y += velocity
            current_direction = "bas"
            moving = True

        if moving:
            frame_count += 1
            if frame_count >= frame_delay:
                current_frame = (current_frame + 1) % len(marche_droit) 
                frame_count = 0
        else:
            current_frame = 0

        # Empêcher le personnage de sortir de la carte
        x = max(0, min(largeur_map - square_size, x))
        y = max(0, min(hauteur_map - square_size, y))

        # Mettre à jour la caméra pour suivre le personnage (le centrer dans la fenêtre)
        camera_x = x - LARGEUR_ECRAN // 2 + square_size // 2
        camera_y = y - HAUTEUR_ECRAN // 2 + square_size // 2

        # Empêcher la caméra de sortir de la carte
        camera_x = max(0, min(largeur_map - LARGEUR_ECRAN, camera_x))
        camera_y = max(0, min(hauteur_map - HAUTEUR_ECRAN, camera_y))

        # Effacer l'écran (fenêtre) à chaque frame
        FENETRE.fill(blanc)
        # Afficher l'image de fond décalée par rapport à la caméra
        FENETRE.blit(fond, (-camera_x, -camera_y))

        # Dessiner la moisissure sur la fenêtre
        for moisissure in moisissures:
            FENETRE.blit(moisissure_image, (moisissure[0] - camera_x, moisissure[1] - camera_y))

        # Dessiner le carré sur la fenêtre avec son décalage dû à la caméra
        FENETRE.blit(get_current_image(), (x - camera_x, y - camera_y))

        if cone_active or battery == 0:
            cone_points = cone_lumiere()
        else:
            # Assombrir les ennemis lorsque la batterie est épuisée
            mask = pygame.Surface((LARGEUR_ECRAN, HAUTEUR_ECRAN), pygame.SRCALPHA)
            mask.fill((0, 0, 0, 245))
            player_screen_x = x - camera_x + square_size // 2
            player_screen_y = y - camera_y + square_size // 2
            player_light_radius = 35  # Rayon de la lumière autour du personnage
            pygame.draw.circle(mask, (0, 0, 0, 150), (player_screen_x, player_screen_y), player_light_radius)
            FENETRE.blit(mask, (0, 0))
            cone_points = []

        draw_battery()

        draw_health_bar()  # Afficher la barre de vie

        if player_health == 0:
            pygame.quit()

        draw_enemy_counter()

        # Mettre à jour les ennemis et vérifier s'ils sont dans le cône de lumière
        for ennemi in ennemis[:]:
            ennemi.ennemiIA(x, y, dt)
            ennemi_screen_x = ennemi.x - camera_x + ennemi.size // 2
            ennemi_screen_y = ennemi.y - camera_y + ennemi.size // 2
            distance_to_player = math.sqrt((ennemi_screen_x - player_screen_x) ** 2 + (ennemi_screen_y - player_screen_y) ** 2)
            if is_point_in_cone(ennemi_screen_x, ennemi_screen_y, cone_points) or distance_to_player < VISIBILITY_DISTANCE:
                ennemi.time_in_light += dt
                FENETRE.blit(ennemi.image, (ennemi.x - camera_x, ennemi.y - camera_y))  # Dessiner l'ennemi s'il est dans le cône de lumière ou proche du joueur
            else:
                ennemi.time_in_light = 0

            if ennemi.time_in_light > 3:
                ennemi.deposer_moisissure()
                ennemis.remove(ennemi)
                ennemis_tues += 1  # Incrémenter le compteur d'ennemis tués
                if ennemis_tues >= 5:  # Vérifier si le joueur a atteint le nombre requis
                    # Charger la nouvelle carte ici
                    fond = pygame.image.load('images/map2.png')
                    fond = pygame.transform.scale(fond, (largeur_map, hauteur_map))

        # Nettoyer la moisissure
        nettoyer_moisissure()

        # Générer des ennemis à intervalles réguliers
        if dialogues_termines:
            spawn_timer += dt
            if spawn_timer >= spawn_interval:
                spawn_ennemi()
                spawn_timer = 0

        # Afficher le dialogue si nécessaire
        draw_dialogue()

        # Mettre à jour l'affichage de la fenêtre
        pygame.display.update()

    # Quitter Pygame proprement
    pygame.quit()

if __name__ == "__main__":
    main()
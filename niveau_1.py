import pygame
import math
import random

# Initialisation de Pygame
pygame.init()
running = True
paused = False
# Paramètres du carré (personnage)
square_size = 64

# Paramètres de la fenêtre
info = pygame.display.Info()
largeur = info.current_w # Largeur de la fenêtre adaptée à l'écran de l'utilisateur
hauteur = info.current_h # Hauteur de la fenêtre adaptée à l'écran de l'utilisateur

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

# Fenêtre en plein écran
WIN = pygame.display.set_mode((largeur, hauteur), pygame.FULLSCREEN)

# Couleurs
blanc = (255, 255, 255)
rouge = (255, 0, 0)
vert = (0, 255, 0)
noir = (0, 0, 0)

# Taille de la carte (map)
largeur_map = largeur * 2
hauteur_map = hauteur * 2

# Charger l'image de fond
fond = pygame.image.load('images/test_map.jpg')

# Redimensionner l'image si nécessaire
fond = pygame.transform.scale(fond, (largeur_map, hauteur_map))

# Gestion du temps pour l'animation du personnage
current_frame = 0
frame_delay = 5  # Nombre de frames avant de changer d'image
frame_count = 0
current_direction = "bas"

# Image du personnage au lancement du jeu
personnage = pygame.image.load('images/homme_droit_1.png')
personnage = pygame.transform.scale(personnage, (square_size, square_size))

x = largeur_map // 2 - square_size // 2  # Position initiale du carré (au centre de la carte)
y = hauteur_map // 2 - square_size // 2
velocity = 10  # Vitesse de déplacement

# Position de la caméra
camera_x, camera_y = 0, 0

# Angle et longueur du cône de lumière
cone_angle = 70  # Angle du cône
cone_length = 400  # Portée de la lumière
cone_active = True  # Le cône est allumé au début

# Ajouter une texture de moisissure
moisissure_image = pygame.image.load('images/boue.png')
moisissure_image = pygame.transform.scale(moisissure_image, (64, 64))

# Liste pour stocker les positions de la moisissure
moisissures = []
ennemis = []
ennemis_tues = 0

# Initialisation de la santé du joueur
player_health = 100


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
    font = pygame.font.Font(None, 74)
    button_rect = pygame.Rect(WIN.get_width() // 2 - 150, WIN.get_height() // 2, 300, 80)

    while paused:
        WIN.fill((0, 0, 0))  # Remplir la fenêtre en noir pour afficher le menu
        text = font.render("Pause", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIN.get_width() // 2, WIN.get_height() // 2 - 100))
        WIN.blit(text, text_rect)

        pygame.draw.rect(WIN, (200, 0, 0), button_rect)
        quit_text = font.render("Quitter", True, (255, 255, 255))
        quit_text_rect = quit_text.get_rect(center=button_rect.center)
        WIN.blit(quit_text, quit_text_rect)

        text = font.render("Appuyez sur 'Echap' pour revenir au jeu", True, (255, 255, 255))
        text_rect = text.get_rect(center=(largeur // 2, hauteur - 50))
        WIN.blit(text, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                paused = False
            if event.type == pygame.MOUSEBUTTONDOWN and button_rect.collidepoint(event.pos):
                pygame.quit()
                exit()

# Fonction pour afficher la carte de la map
def pause_map():
    global paused
    paused = True  # Bloque le jeu pendant l'affichage de la carte
    font = pygame.font.Font(None, 50)

    while paused:
        # Afficher la carte complète redimensionnée pour tenir dans l'écran
        mini_map = pygame.transform.scale(fond, (largeur, hauteur))
        WIN.blit(mini_map, (0, 0))

        # Calculer la position du joueur sur la mini-map
        player_map_x = int(x / largeur_map * largeur)
        player_map_y = int(y / hauteur_map * hauteur)

        # Dessiner un point représentant le joueur
        pygame.draw.circle(WIN, (255, 0, 0), (player_map_x, player_map_y), 10)  # Point rouge

        # Dessiner les ennemis sur la mini-carte
        for ennemi in ennemis:
            ennemi_map_x = int(ennemi.x / largeur_map * largeur)
            ennemi_map_y = int(ennemi.y / hauteur_map * hauteur)
            pygame.draw.circle(WIN, (0, 0, 255), (ennemi_map_x, ennemi_map_y), 10)  # Point bleu pour les ennemis

        # Ajouter du texte pour quitter la carte
        text = font.render("Appuyez sur 'E' pour revenir au jeu", True, (255, 255, 255))
        text_rect = text.get_rect(center=(largeur // 2, hauteur - 50))
        WIN.blit(text, text_rect)

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
    bar_x = (largeur - bar_width) // 2
    bar_y = hauteur - 40  # Position en bas de l'écran
    fill_width = int((battery / 100) * bar_width)
    pygame.draw.rect(WIN, noir, (bar_x, bar_y, bar_width, bar_height))
    pygame.draw.rect(WIN, vert if battery > 30 else rouge, (bar_x, bar_y, fill_width, bar_height))

def draw_health_bar():
    """Affiche la barre de vie en haut et au centre de l'écran."""
    bar_width = 300
    bar_height = 20
    bar_x = (largeur - bar_width) // 2
    bar_y = 20  # Position en haut de l'écran
    fill_width = int((player_health / 100) * bar_width)
    pygame.draw.rect(WIN, noir, (bar_x, bar_y, bar_width, bar_height))
    pygame.draw.rect(WIN, vert if player_health > 30 else rouge, (bar_x, bar_y, fill_width, bar_height))

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
    mask = pygame.Surface((largeur, hauteur), pygame.SRCALPHA)
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
    player_light_radius = 35  # Rayon de la lumière autour du personnage
    pygame.draw.circle(mask, (0, 0, 0, 0), (player_screen_x, player_screen_y), player_light_radius)

    # Appliquer le masque à l'écran
    WIN.blit(mask, (0, 0))

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
    text_rect = text.get_rect(center=(largeur // 2, 50))
    WIN.blit(text, text_rect)

# Dictionnaire pour stocker le temps de début de nettoyage pour chaque moisissure
nettoyage_temps_debut = {}

# Fonction pour afficher la moisissure laissée par les ennemis à leur mort
def nettoyer_moisissure():
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
                    elif temps_actuel - nettoyage_temps_debut[moisissure] >= 2000:  # 2000 ms = 2 secondes
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

# Boucle principale du jeu
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
    camera_x = x - largeur // 2 + square_size // 2
    camera_y = y - hauteur // 2 + square_size // 2

    # Empêcher la caméra de sortir de la carte
    camera_x = max(0, min(largeur_map - largeur, camera_x))
    camera_y = max(0, min(hauteur_map - hauteur, camera_y))

    # Effacer l'écran (fenêtre) à chaque frame
    WIN.fill(blanc)
    # Afficher l'image de fond décalée par rapport à la caméra
    WIN.blit(fond, (-camera_x, -camera_y))

    # Dessiner la moisissure sur la fenêtre
    for moisissure in moisissures:
        WIN.blit(moisissure_image, (moisissure[0] - camera_x, moisissure[1] - camera_y))

    # Dessiner le carré sur la fenêtre avec son décalage dû à la caméra
    WIN.blit(get_current_image(), (x - camera_x, y - camera_y))

    if cone_active or battery == 0:
        cone_points = cone_lumiere()
    else:
        # Assombrir les ennemis lorsque la batterie est épuisée
        mask = pygame.Surface((largeur, hauteur), pygame.SRCALPHA)
        mask.fill((0, 0, 0, 245))
        player_screen_x = x - camera_x + square_size // 2
        player_screen_y = y - camera_y + square_size // 2
        player_light_radius = 35  # Rayon de la lumière autour du personnage
        pygame.draw.circle(mask, (0, 0, 0, 150), (player_screen_x, player_screen_y), player_light_radius)
        WIN.blit(mask, (0, 0))
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
        if is_point_in_cone(ennemi_screen_x, ennemi_screen_y, cone_points):
            ennemi.time_in_light += dt
            print(f"Ennemi {ennemi} dans le cône de lumière pendant {ennemi.time_in_light} secondes")
            WIN.blit(ennemi.image, (ennemi.x - camera_x, ennemi.y - camera_y))  # Dessiner l'ennemi seulement s'il est dans le cône de lumière
        else:
            ennemi.time_in_light = 0

        if ennemi.time_in_light > 3:
            print(f"Ennemi {ennemi} tué")
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
    spawn_timer += dt
    if spawn_timer >= spawn_interval:
        spawn_ennemi()
        spawn_timer = 0

    # Mettre à jour l'affichage de la fenêtre
    pygame.display.update()

# Quitter Pygame proprement
pygame.quit()

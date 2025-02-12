import pygame
import math

# Initialisation de Pygame
pygame.init()
running = True
paused = False

# Paramètres de la fenêtre
info = pygame.display.Info()
largeur = info.current_w
hauteur = info.current_h

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
fond = pygame.image.load('test_map.jpg')  # Remplace 'ton_image_de_fond.png' par le chemin de ton image

# Redimensionner l'image si nécessaire
fond = pygame.transform.scale(fond, (largeur_map, hauteur_map))

# Paramètres du carré
square_size = 64

personnage = pygame.image.load('homme_droit.png')  # Remplace par le chemin de ton image
personnage = pygame.transform.scale(personnage, (square_size, square_size))  # Redimensionner l'image pour correspondre à la taille du carré

x = largeur_map // 2 - square_size // 2  # Position initiale du carré (au centre de la carte)
y = hauteur_map // 2 - square_size // 2
velocity = 10  # Vitesse de déplacement

# Position de la caméra
camera_x, camera_y = 0, 0

# Angle et longueur du cône de lumière
cone_angle = 70  # Angle du cône
cone_length = 400  # Portée de la lumière
cone_active = True  # Le cône est allumé au début

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

def draw_battery():
    """Affiche la barre de batterie en bas et au centre de l'écran."""
    bar_width = 300
    bar_height = 20
    bar_x = (largeur - bar_width) // 2
    bar_y = hauteur - 40  # Position en bas de l'écran
    fill_width = int((battery / 100) * bar_width)
    pygame.draw.rect(WIN, noir, (bar_x, bar_y, bar_width, bar_height))
    pygame.draw.rect(WIN, vert if battery > 30 else rouge, (bar_x, bar_y, fill_width, bar_height))
    
def cone_lumiere():
    """Affiche un cône de lumière avec un dégradé basé uniquement sur la distance."""
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
    mask.fill((0, 0, 0, 230))  # Ombre globale sur toute la scène

    # Générer le cône de lumière avec un dégradé en fonction de la distance
    for i in range(cone_length, 0, -5):  # De l'intérieur vers l'extérieur
        # Calcul de l'opacité qui diminue avec la distance
        distance_factor = i / cone_length
        alpha = int(255 * (1 - distance_factor))  # Plus loin, moins intense

        color = (0, 0, 0, 255 - alpha)  # Noir avec un dégradé d'opacité, minimum à 240

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

    # Assurer que le personnage soit toujours éclairé (cercle lumineux autour du personnage)
    player_light_radius = 35  # Rayon de la lumière autour du personnage
    pygame.draw.circle(mask, (0, 0, 0, 255 - alpha), (player_screen_x, player_screen_y), player_light_radius)

    # Appliquer le masque à l'écran
    WIN.blit(mask, (0, 0))

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

    # Gestion des déplacements du carré
    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:  # Déplacement vers la gauche
        x -= velocity
    if keys[pygame.K_d]:  # Déplacement vers la droite
        x += velocity
    if keys[pygame.K_z]:  # Déplacement vers le haut
        y -= velocity
    if keys[pygame.K_s]:  # Déplacement vers le bas
        y += velocity

    # Empêcher le carré de sortir de la carte
    x = max(0, min(largeur_map - square_size, x))
    y = max(0, min(hauteur_map - square_size, y))

    # Mettre à jour la caméra pour suivre le carré (le centrer dans la fenêtre)
    camera_x = x - largeur // 2 + square_size // 2
    camera_y = y - hauteur // 2 + square_size // 2

    # Empêcher la caméra de sortir de la carte
    camera_x = max(0, min(largeur_map - largeur, camera_x))
    camera_y = max(0, min(hauteur_map - hauteur, camera_y))

    # Effacer l'écran (fenêtre) à chaque frame
    WIN.fill(blanc)
    # Afficher l'image de fond décalée par rapport à la caméra
    WIN.blit(fond, (-camera_x, -camera_y))

    # Dessiner le carré sur la fenêtre avec son décalage dû à la caméra
    WIN.blit(personnage, (x - camera_x, y - camera_y))

    if cone_active:
        cone_lumiere()

    else:
        WIN.fill((0,0,0))

    draw_battery()
    
    # Mettre à jour l'affichage de la fenêtre
    pygame.display.update()

# Quitter Pygame proprement
pygame.quit()

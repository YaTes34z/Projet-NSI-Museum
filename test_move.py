import pygame 
import math

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
info = pygame.display.Info()
largeur = info.current_w
hauteur = info.current_h
WIN = pygame.display.set_mode((largeur, hauteur), pygame.FULLSCREEN)

# Couleurs
blanc = (255, 255, 255)
rouge = (255, 0, 0)
vert = (0, 255, 0)
noir = (0, 0, 0)

# Charger l'image de fond
fond = pygame.image.load('test_map.jpg')
fond = pygame.transform.scale(fond, (largeur * 2, hauteur * 2))

# Paramètres du joueur
square_size = 64
x, y = (largeur, hauteur)
velocity = 10

# Position de la caméra
camera_x, camera_y = 0, 0

# Cône de lumière
cone_angle = 70
cone_length = 350
cone_active = False

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
    """Affiche un cône de lumière simulant une lampe torche."""
    player_screen_x = x - camera_x + square_size // 2
    player_screen_y = y - camera_y + square_size // 2
    mouse_x, mouse_y = pygame.mouse.get_pos()
    angle = math.atan2(mouse_y - player_screen_y, mouse_x - player_screen_x)
    mask = pygame.Surface((largeur, hauteur), pygame.SRCALPHA)
    mask.fill((0, 0, 0, 200))
    for i in range(cone_length, 0, -5):
        alpha = int(255 * (1 - i / cone_length))
        color = (0, 0, 0, 255 - alpha)
        points = [(player_screen_x, player_screen_y)]
        for j in range(-cone_angle // 2, cone_angle // 2 + 1, 5):
            ray_angle = angle + math.radians(j)
            points.append((player_screen_x + math.cos(ray_angle) * i, player_screen_y + math.sin(ray_angle) * i))
        if len(points) > 2:
            pygame.draw.polygon(mask, color, points)
    WIN.blit(mask, (0, 0))

def handle_events():
    """Gère les événements utilisateur comme la fermeture du jeu et l'activation du cône de lumière."""
    global running, cone_active, battery
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            if battery > 0:
                cone_active = not cone_active

def update_battery(dt):
    """Met à jour l'état de la batterie en fonction de l'utilisation du cône de lumière."""
    global battery, cone_active
    if cone_active:
        battery -= battery_drain_rate * dt
        battery = max(battery, 0)
        if battery == 0:
            cone_active = False
    else:
        battery += battery_drain_rate * dt
        battery = min(battery, 100)

def update_player_position():
    """Met à jour la position du joueur en fonction des entrées clavier."""
    global x, y, camera_x, camera_y
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= velocity
    if keys[pygame.K_RIGHT]:
        x += velocity
    if keys[pygame.K_UP]:
        y -= velocity
    if keys[pygame.K_DOWN]:
        y += velocity
    camera_x = max(0, min(largeur * 2 - largeur, x - largeur // 2 + square_size // 2))
    camera_y = max(0, min(hauteur * 2 - hauteur, y - hauteur // 2 + square_size // 2))

def draw_scene():
    """Dessine la scène avec le joueur et les éléments de l'environnement."""
    WIN.fill(blanc)
    WIN.blit(fond, (-camera_x, -camera_y))
    pygame.draw.rect(WIN, rouge, (x - camera_x, y - camera_y, square_size, square_size))
    if cone_active:
        cone_lumiere()
    draw_battery()
    pygame.display.update()

# Boucle principale
running = True
while running:
    dt = clock.tick(30) / 1000.0  # Temps écoulé en secondes
    handle_events()
    update_battery(dt)
    update_player_position()
    draw_scene()

pygame.quit()

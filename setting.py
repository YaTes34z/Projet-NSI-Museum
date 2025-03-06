import pygame

# Paramètres du carré (personnage)
square_size = 128

# Couleurs
blanc = (255, 255, 255)
rouge = (255, 0, 0)
vert = (0, 255, 0)
noir = (0, 0, 0)

# Angle et longueur du cône de lumière
cone_angle = 70  # Angle du cône
cone_length = 400  # Portée de la lumière
cone_active = True  # Le cône est allumé au début

# Liste pour stocker les positions de la moisissure et des ennemis 
moisissures = []
ennemis = []
ennemis_tues = 0

# Initialisation de la santé du joueur
player_health = 100

# Image du personnage au lancement du jeu
personnage = pygame.image.load('images/homme_droit_1.png')
personnage = pygame.transform.scale(personnage, (square_size, square_size))

velocity = 10  # Vitesse de déplacement

# Position de la caméra
camera_x, camera_y = 0, 0

# Ajouter une texture de moisissure
moisissure_image = pygame.image.load('images/boue.png')
moisissure_image = pygame.transform.scale(moisissure_image, (100, 100))
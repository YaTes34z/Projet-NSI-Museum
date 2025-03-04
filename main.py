import sys
import pygame
import cv2
import niveau_1
import pygame.mixer

pygame.init()

# Constantes de la fenêtre
info = pygame.display.Info()
LARGEUR_ECRAN, HAUTEUR_ECRAN = info.current_w, info.current_h

try:
    FENETRE = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN), pygame.FULLSCREEN)
    pygame.display.set_caption("Mon Jeu")
except pygame.error as e:
    print(f"Erreur lors de la création de la fenêtre : {e}")
    sys.exit()

# Chargement des images
try:
    fond = pygame.image.load("images/fond.png").convert()
    logo = pygame.image.load("images/logo.png").convert_alpha()
except pygame.error as e:
    print(f"Erreur lors du chargement des images : {e}")
    sys.exit()

# Redimensionnement des images pour s'adapter à la résolution de l'écran
fond = pygame.transform.scale(fond, (LARGEUR_ECRAN, HAUTEUR_ECRAN))
logo = pygame.transform.scale(logo, (int(LARGEUR_ECRAN * 0.175), int(LARGEUR_ECRAN * 0.175)))  # 300/800 = 0.375, 150/600 = 0.25

# Boutons
class Bouton:
    def __init__(self, texte, position, action, largeur=180, hauteur=50):
        self.texte = texte
        self.position = position
        self.action = action
        self.rect = pygame.Rect(position[0], position[1], largeur, hauteur)
        self.couleur = (30, 30, 30)
        self.couleur_hover = (60, 60, 60)

    def dessiner(self, surface):
        couleur = self.couleur_hover if self.rect.collidepoint(pygame.mouse.get_pos()) else self.couleur
        pygame.draw.rect(surface, couleur, self.rect, border_radius=5)
        font = pygame.font.Font(None, 36)
        texte_surface = font.render(self.texte, True, (255, 255, 255))
        texte_rect = texte_surface.get_rect(center=self.rect.center)
        surface.blit(texte_surface, texte_rect)

    def clic(self, pos):
        return self.rect.collidepoint(pos)

def jouer_cinematique(niveau):
    cap = cv2.VideoCapture(f'images/cinematique_{niveau}.mp4')
    if not cap.isOpened():
        print(f"Erreur : Impossible de lire la cinématique {niveau}")
        return
    
    # Charger et jouer l'audio
    pygame.mixer.init()
    pygame.mixer.music.load(f'images/cinematique_{niveau}.mp3')
    pygame.mixer.music.play()
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    clock = pygame.time.Clock()
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (LARGEUR_ECRAN, HAUTEUR_ECRAN))  # Redimensionner la frame
        frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        FENETRE.blit(frame, (0, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                pygame.quit()
                sys.exit()
        clock.tick(fps)
    
    cap.release()
    pygame.mixer.music.stop()

def lancer_niveau_1():
    jouer_cinematique(1)
    niveau_1.main()

def lancer_niveau_2():
    print("Le niveau 2 n'est pas encore disponible.")
    # jouer_cinematique(2)

def afficher_menu_principal():
    """Affiche le menu principal."""
    clock = pygame.time.Clock()
    boutons = [
        Bouton("Niveau 1", (LARGEUR_ECRAN // 2 - 90, HAUTEUR_ECRAN // 2 - 70), lancer_niveau_1),
        Bouton("Niveau 2", (LARGEUR_ECRAN // 2 - 90, HAUTEUR_ECRAN // 2 + 20), lancer_niveau_2),
        Bouton("Contrôles", (LARGEUR_ECRAN // 2 - 90, HAUTEUR_ECRAN // 2 + 110), afficher_controles),
        Bouton("Quitter", (LARGEUR_ECRAN // 2 - 90, HAUTEUR_ECRAN // 2 + 210), lambda: pygame.quit() or sys.exit())
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
        
        clock.tick(30)

def afficher_controles():
    """Affiche une fenêtre avec les contrôles du jeu."""
    controles_actif = True
    font = pygame.font.Font(None, 36)
    controles = [
        "Z : Aller haut",
        "S : Aller en bas",
        "D : Aller à droite",
        "Q : Aller à gauche",
        "Clic gauche : Enlever la moisissure",
        "Clic droit : Activer la lampe-torche",
        "Echap : Accéder au menu",
        "E : Accéder à la carte"
    ]
    
    bouton_retour = Bouton("Retour", (LARGEUR_ECRAN // 2 - 90, HAUTEUR_ECRAN - 100), afficher_menu_principal)
    
    while controles_actif:
        FENETRE.fill((50, 50, 50))
        y_offset_left = 420
        y_offset_right = 420
        x_offset_left = LARGEUR_ECRAN // 2 - 200
        x_offset_right = LARGEUR_ECRAN // 2 + 200
        
        for i, ligne in enumerate(controles):
            texte_surface = font.render(ligne, True, (255, 255, 255))
            if i < 4:
                texte_rect = texte_surface.get_rect(center=(x_offset_left, y_offset_left))
                y_offset_left += 50  # 40 pixels pour la hauteur du texte + 10 pixels pour le gap
            else:
                texte_rect = texte_surface.get_rect(center=(x_offset_right, y_offset_right))
                y_offset_right += 50  # 40 pixels pour la hauteur du texte + 10 pixels pour le gap
            FENETRE.blit(texte_surface, texte_rect)
        
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
                    afficher_menu_principal()

def main():
    afficher_menu_principal()

if __name__ == "__main__":
    main()
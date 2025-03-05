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
    
    # Charger les images des boutons
    image_niveau_1 = pygame.image.load('images/bouton_niveau1.png').convert_alpha()
    image_niveau_2 = pygame.image.load('images/bouton_niveau2.png').convert_alpha()
    image_controles = pygame.image.load('images/bouton_controles.png').convert_alpha()
    image_quitter = pygame.image.load('images/bouton_quitter.png').convert_alpha()
    
    # Redimensionner les images des boutons pour qu'elles aient la taille souhaitée
    largeur_bouton = 200  # Largeur souhaitée pour les boutons
    hauteur_bouton = 110   # Hauteur souhaitée pour les boutons
    image_niveau_1 = pygame.transform.scale(image_niveau_1, (largeur_bouton, hauteur_bouton))
    image_niveau_2 = pygame.transform.scale(image_niveau_2, (largeur_bouton, hauteur_bouton))
    image_controles = pygame.transform.scale(image_controles, (largeur_bouton, hauteur_bouton))
    image_quitter = pygame.transform.scale(image_quitter, (largeur_bouton, hauteur_bouton))
    
    boutons = [
        Bouton("Niveau 1", (LARGEUR_ECRAN // 2 - largeur_bouton // 2, HAUTEUR_ECRAN // 2 - 140), lancer_niveau_1, image=image_niveau_1),
        Bouton("Niveau 2", (LARGEUR_ECRAN // 2 - largeur_bouton // 2, HAUTEUR_ECRAN // 2 - 20), lancer_niveau_2, image=image_niveau_2),
        Bouton("Contrôles", (LARGEUR_ECRAN // 2 - largeur_bouton // 2, HAUTEUR_ECRAN // 2 + 100), afficher_controles, image=image_controles),
        Bouton("Quitter", (LARGEUR_ECRAN // 2 - largeur_bouton // 2, HAUTEUR_ECRAN // 2 + 220), lambda: pygame.quit() or sys.exit(), image=image_quitter)
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

# Charger et redimensionner les images des touches
touche_Z = pygame.transform.scale(pygame.image.load('images/touche_Z.png').convert_alpha(), (64, 64))
touche_S = pygame.transform.scale(pygame.image.load('images/touche_S.png').convert_alpha(), (64, 64))
touche_D = pygame.transform.scale(pygame.image.load('images/touche_D.png').convert_alpha(), (64, 64))
touche_Q = pygame.transform.scale(pygame.image.load('images/touche_Q.png').convert_alpha(), (64, 64))
touche_Echap = pygame.transform.scale(pygame.image.load('images/touche_Echap.png').convert_alpha(), (64, 64))
touche_E = pygame.transform.scale(pygame.image.load('images/touche_E.png').convert_alpha(), (64, 64))
touche_CliqueDroit = pygame.transform.scale(pygame.image.load('images/touche_CliqueDroit.png').convert_alpha(), (64, 64))
touche_CliqueGauche = pygame.transform.scale(pygame.image.load('images/touche_CliqueGauche.png').convert_alpha(), (64, 64))

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
    
    bouton_retour = Bouton("Retour", (LARGEUR_ECRAN // 2 - 90, HAUTEUR_ECRAN - 100), afficher_menu_principal)
    
    while controles_actif:
        fond_controles = pygame.image.load("images/fond.jpg").convert()
        fond_controles = pygame.transform.scale(fond_controles, (LARGEUR_ECRAN, HAUTEUR_ECRAN))
        FENETRE.blit(fond_controles, (0, 0))      

        y_offset_left = 320
        y_offset_right = 320
        x_offset_left = LARGEUR_ECRAN // 2 - 300  # Ajustement pour centrer davantage
        x_offset_right = LARGEUR_ECRAN // 2 + 250  # Ajustement pour centrer davantage
        
        for i, (texte, image) in enumerate(controles):
            if i < 4:
                FENETRE.blit(image, (x_offset_left - 70, y_offset_left - 32))  # Ajustement pour centrer l'image
                texte_surface = font.render(texte, True, (255, 255, 255))
                FENETRE.blit(texte_surface, (x_offset_left, y_offset_left))
                y_offset_left += 150  # 50 pixels pour la hauteur du texte + 40 pixels pour le gap
            else:
                FENETRE.blit(image, (x_offset_right - 70, y_offset_right - 32))  # Ajustement pour centrer l'image
                texte_surface = font.render(texte, True, (255, 255, 255))
                FENETRE.blit(texte_surface, (x_offset_right, y_offset_right))
                y_offset_right += 150  # 50 pixels pour la hauteur du texte + 40 pixels pour le gap
        
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
import sys
import pygame
import niveau_1
# import niveau_2
import cv2

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
    def __init__(self, texte, position, action, largeur=200, hauteur=50):
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
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        FENETRE.blit(frame, (0, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                pygame.quit()
                sys.exit()
    cap.release()

def lancer_niveau_1():
    jouer_cinematique(1)
    niveau_1.main()

def lancer_niveau_2():
    jouer_cinematique(2)
    # niveau_2.main(FENETRE, LARGEUR_ECRAN, HAUTEUR_ECRAN)

def afficher_menu():
    menu_actif = True
    boutons_menu = [
        Bouton("Reprendre", (LARGEUR_ECRAN // 2 - 100, HAUTEUR_ECRAN // 2 - 25), lambda: None),
        Bouton("Quitter", (LARGEUR_ECRAN // 2 - 100, HAUTEUR_ECRAN // 2 + 45), lambda: pygame.quit() or sys.exit())
    ]
    
    while menu_actif:
        FENETRE.fill((50, 50, 50))
        for bouton in boutons_menu:
            bouton.dessiner(FENETRE)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                menu_actif = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for bouton in boutons_menu:
                    if bouton.clic(event.pos):
                        bouton.action()
                        if bouton.texte == "Reprendre":
                            menu_actif = False

def main():
    clock = pygame.time.Clock()
    boutons = [
        Bouton("Niveau 1", (LARGEUR_ECRAN // 2 - 150, HAUTEUR_ECRAN // 2 - 75), lancer_niveau_1),
        Bouton("Niveau 2", (LARGEUR_ECRAN // 2 - 150, HAUTEUR_ECRAN // 2 + 25), lancer_niveau_2)
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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                afficher_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for bouton in boutons:
                    if bouton.clic(event.pos):
                        bouton.action()
        
        clock.tick(30)

if __name__ == "__main__":
    main()
import pygame
import random
import math

class Game:
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))    # Breite , Höhe des Fensters
        pygame.display.set_caption("Space Invaders")          # das ist die Überschrift des Fensters
        self.clock = pygame.time.Clock()    # hier wird ein Objekt vom Typ Clock erzeugt für die Frame-rate (Bildanzeige-Frequenz)
        self.running = True
        self.spaceship = Spaceship(self, 370, 515)  # Position des Spaceship zu Beginn (positioniert linke obere Ecke des Spaceship-png)
        self.score = 0

        self.enemies = []
        for i in range(12):
            self.enemies.append(Enemy(self, random.randint(0,736), random.randint(30, 130)))

        self.background_img = pygame.image.load("spr_space_himmel.png")     # ein Bild als Hintergrundbild laden
                                                                  # (muss immer zuerst aufgerufen werden, vor darauf platzierten Objekten)

        while self.running:        # das ist die GAME-LOOP  !!!!!!!!!!!!!
            self.clock.tick(60)           # Frame-rate: wie schnell "bewegt" sich etwas in unserem Spiel (z.B. das Raumschiff = png.Bild)
                     # das bedeutet: wie viele "Bilder" werden pro Minute erzeugt (und dadurch Bild-Objekte an neuen Stellen neu gezeichnet)!

            self.screen.fill((0, 255, 100)) # kann man hier weglassen, aber ggf ist die Reihenfolge wichtig!
                       # auch wichtig, wenn z.B. das Raumschiff auf einem Sternenhimmel platziert werden soll:
                       # d.h. erst den Sternenhimmel (background_img) anzeigen lassen, dann danach (= darauf) das Raumschiff!
            self.screen.blit(self.background_img, (0, 0))  # (0,0) bezeichnet die Start-Position ganz links oben im Anzeige- Fenster

            for event in pygame.event.get():
                if event.type == pygame.QUIT:           # wenn man auf das Kreuz zum Schliessen des Fensters drückt
                    self.running = False                # dadurch wird die Game-Loop beendet

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.spaceship.move(-10)
                    if event.key == pygame.K_RIGHT:
                        self.spaceship.move(10)
                    if event.key == pygame.K_SPACE:
                        self.spaceship.fire_bullet()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.spaceship.move(10)
                    if event.key == pygame.K_RIGHT:
                        self.spaceship.move(-10)

            self.spaceship.update()
            if len(self.spaceship.bullets) > 0:
                for bullet in self.spaceship.bullets:   # spaceship.bullets weist auf die Bullet-Liste
                    if bullet.is_fired == True:      # wird durch > Spaceship.fire_bullet () > bullet.fire() auf "True" gesetzt
                        bullet.update()              # der Schuss geht nach oben bis zum Rand, danach wird "is_fired" auf "False" gesetzt
                    else:
                        self.spaceship.bullets.remove(bullet)    # das Bullet wir aus der Liste entfernt

            for enemy in self.enemies:
                enemy.update()
                enemy.check_collision()
                if enemy.y > 460: # diese Höhe + die Grösse des Aliens entspricht der Höhe, auf der das Spaceship fliegt
                    for i in self.enemies:
                        i.y = 1000
                    self.print_game_over()
                    break
            self.print_score()
            pygame.display.update()   # SEHR wichtig für die korrekte Darstellung!! Dadurch wird das Fenster in jedem
                                        # Durchlauf d. Game-Loop neu aufgebaut (Farbe ect)..
    def print_game_over(self):
        go_font = pygame.font.Font("freesansbold.ttf", 64)              # hier wird der Font gewählt..
        go_text = go_font.render("GAME OVER", True, (255, 255, 255))    # Boolean steht für Anti-Alias (glatte Kanten ja/nein), RGB -Tupel für Farbe weiss
        self.screen.blit(go_text, (200, 250))


    def print_score(self):
        score_font = pygame.font.Font("freesansbold.ttf", 24)
        score_text = score_font.render("Punkte: " + str(self.score), True, (255, 255, 255))
        self.screen.blit(score_text, (8, 8))

class Spaceship:
    def __init__(self, game, x, y):
        self.x = x
        self.y = y
        self.change_x = 0
        self.game = game
        self.spaceship_img = pygame.image.load("spr_spaceship.png")
        self.bullets = []

    def fire_bullet(self):
        self.bullets.append(Bullet(self.game, self.x, self.y))    # jedes mal, wenn Space gedrückt wird um zu schiessen wird eine Bullet in die Liste eingefügt
        self.bullets[len(self.bullets)-1].fire()

    def move(self, speed):
        self.change_x += speed

    def update(self):                # hier geht es um die Bewegung des Raumschiffs
        self.x += self.change_x
        if self.x < 0:      # das ist der linke Rand, somit kann das Spaceship nicht links rausfliegen
            self.x = 0
        elif self.x > 736:  # das ist der rechte Rand minus die Grösse des Spaceship-png (800-64 pixel), damit kann das Spaceship nicht rechts rausfliegen
            self.x = 736
        self.game.screen.blit(self.spaceship_img, (self.x, self.y))      # das Spaceship-Bild wird abgebildet (blit-Methode)

class Bullet:
    def __init__(self, game, x, y):
        self.x = x
        self.y = y
        self.game = game
        self.is_fired = False
        self.bullet_speed = 10
        self.bullet_img = pygame.image.load("spr_patrone.png")

    def fire(self):
        self.is_fired = True

    def update(self):
        self.y -= self.bullet_speed    # der Schuss geht nach oben, d.h. die y-Werte werden immer kleiner
        if self.y <= 0:
            self.is_fired = False      # der Schuss kann so nicht aus dem Bild "rausfliegen" und belastet somit die Rechnerleistung nicht mehr..
        self.game.screen.blit(self.bullet_img, (self.x, self.y))     # das Bullet wird abgebildet


class Enemy:
    def __init__(self, game, x,y):
        self.x = x
        self.y = y
        self.change_x = 5
        self.change_y = 60
        self.game = game
        self.enemy_img = pygame.image.load("spr_space_enemy.png")

    def check_collision(self):
        for bullet in self.game.spaceship.bullets:
            distance = math.sqrt(math.pow(self.x - bullet.x, 2) + math.pow(self.y - bullet.y, 2))
            if distance < 35:
                bullet.is_fired = False
                self.game.score += 1
                self.x = random.randint(0, 736)
                self.y = random.randint(50, 150)


    def update(self):
        self.x += self.change_x
        if self.x >= 736:
            self.y += self.change_y
            self.change_x = -5
        elif self.x <= 0:
            self.y += self.change_y
            self.change_x = 5
        self.game.screen.blit(self.enemy_img, (self.x, self.y))


if __name__ == "__main__":
    game = Game(800, 600)
  # print(len(game.spaceship.bullets))


  #  print(__file__)       # wenn man nicht weiss wo das file auf dem Rechner liegt :) ..

import pygame
import random


class platek:
    def __init__(self,szer,wys):
        self.x=random.randint(0,szer)
        self.y=random.randint(0,wys)
        self.szer_okna = szer
        self.kolor = (255,255,255)
        self.rozmiar = random.randint(2,8)
        self.ksztalt = pygame.Rect(self.x,self.y,self.rozmiar,self.rozmiar)

    def rysuj(self,screen):
        pygame.draw.rect(screen,self.kolor,self.ksztalt)

    def ruch(self,v,v2=0):
        self.y += v
        self.x += v2
        self.x = self.x % self.szer_okna
        self.ksztalt = pygame.Rect(self.x,self.y,self.rozmiar,self.rozmiar)

    def kolizja(self,inny):
        if self.ksztalt.colliderect(inny):
            return True
        else:
            return False

class snieg:
    def __init__(self,pocz,szer,wys):
        self.szer_okna = szer
        self.wys_okna = wys
        self.all = [platek(szer,wys) for i in range(pocz)]
        self.akt = self.all[:]
        self.nie_akt = []

    def rysuj(self,screen):
        for p in self.all:
            p.rysuj(screen)

    def opad(self,ziemia,wiatr):
        for p in self.akt:
            p.ruch(2,wiatr)
            if p.kolizja(ziemia):
                self.akt.remove(p)
                self.nie_akt.append(p.ksztalt)
            elif self.nie_akt:
                if not (c:=p.ksztalt.collidelist(self.nie_akt)) == -1:
                    self.akt.remove(p)
                    self.nie_akt.remove(self.nie_akt[c])
                    self.nie_akt.append(p.ksztalt)

    def dodaj(self,n=1):
        temp = [platek(self.szer_okna,0) for i in range(n)]
        self.akt.extend(temp)
        self.all.extend(temp)


class tlo:
    def __init__(self,sz,wys):
        self.sz = sz
        self.wys = wys
        self.screen = pygame.display.set_mode((sz,wys))
        pygame.display.set_caption("Pada śnieg, pada śnieg ^^")
        b=random.randint(0,255)
        c=random.randint(150,255)
        if c<b:
            b,c=c,b
        self.kolor = (0,b,c)
        self.ziemia = pygame.Rect(0,wys-10,sz,10)

    def rysuj(self):
        self.screen.fill(self.kolor)
        pygame.draw.rect(self.screen,(255,255,255),self.ziemia)

class obrazek:
    def __init__(self):
        pygame.init()
        self.T=tlo(1000,700)
        self.S = snieg(400,1000,700)
        self.fps = pygame.time.Clock()
        self.tyk = 15
        self.wiatr = 0

    def ruszaj(self):
        while True:
            self.T.rysuj()
            self.S.rysuj(self.T.screen)
            pygame.display.update()
            self.S.opad(self.T.ziemia, self.wiatr)
            self.fps.tick(self.tyk)
            self.S.dodaj(2)
            self.handle_events()
    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                quit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    self.tyk+=5
                if e.key == pygame.K_DOWN:
                    self.tyk-=5
                if e.key == pygame.K_RIGHT:
                    self.wiatr += 0.2
                if e.key == pygame.K_LEFT:
                    self.wiatr -= 0.2
                if e.key == pygame.K_q:
                    b = random.randint(0, 255)
                    c = random.randint(150, 255)
                    if c < b:
                        b, c = c, b
                    self.T.kolor = (0, b, c)
if __name__ == "__main__":
    O = obrazek()
    O.ruszaj()
# Importar o módulo pygame
# se a execução deste import em Python3 ou Python2 der algum erro
# é porque o pygame não está bem instalado
import pygame, sys
from pygame.locals import *
from math import cos, sin, atan, sqrt
from PIL import Image

# inicialização do módulo pygame
pygame.init()

# criação de uma janela
largura = 937
altura = 696
tamanho = (largura, altura)
janela = pygame.display.set_mode(tamanho)
pygame.display.set_caption('CarRace da Leonor')  # nome da janela
# Nesta janela o ponto (0,0) é o canto superior esquerdo
# e (532-1,410-1) = (531,409) o canto inferior direito.


# número de imagens por segundo
frame_rate = 24

# relógio para controlo do frame rate
clock = pygame.time.Clock()

########################
#Musica
pygame.mixer.init()
motor = pygame.mixer.Sound("motor.mp3")
sirene = pygame.mixer.Sound("sirene.wav")

# ler uma imagem em formato bmp
pista = pygame.image.load("circuitoA50758.jpg")
carro = pygame.image.load("carroA50758.jpg")
#------------
policia = pygame.image.load("policiaA50758.jpg")
policia = pygame.transform.scale(policia, (30,30))
#-----------

# Inicializa o tempo
t = 0.0
motor.play()

#########################
# Para escrever o tempo:
font_size = 35
font = pygame.font.Font(None, font_size)  # fonte pré-definida
antialias = True  # suavização
WHITE = (255, 255, 255)  # cor (terno com os valores Red, Green, Blue entre 0 e 255)
BLACK = (5, 30, 5)

##################################
##Exemplo ajustado à pista

def parametrizacao(t):  # as curvas tem metade da velocidade das retas
    vreta = 250 # velocidade retas
    vcurva = vreta/2 # velocidade curvas
    if t >= 0:
        resultado = (0, 375) # (0,375)
    if 0 < t <= 2.20:
        resultado = (0 + 249 * t, 375 + -22 * t) # pf = (523,329)
    if 2.20 < t <= 4.9:
        raio = 70
        resultado = (533 + 70 * cos(1+t*vcurva/raio), 249 - 70 * sin(1+t*vcurva/raio)) # pf = (479,271)
    if 4.9 < t <= 5.1:
        ti = 4.9
        pix = 479 - 15
        piy = 271
        resultado = (pix - (t-ti), piy + vreta * (t-ti)) # pf = (474,425)
    if 5.1 < t <= 5.2:
        resultado = (0, 0)
        print("A passar por debaixo da estrada")
        #carro a passar por debaixo (477,332) a (481,377)
    if 5.2 < t <= 5.5:
        ti = 4.9
        pix = 479 - 15
        piy = 271
        resultado = (pix - (t - ti), piy + vreta * (t - ti))  # pf = (474,425)
    if 5.5 < t <= 8.3:
        raio = 70
        pix = 474 + 60
        piy = 425
        fi = -0.5
        resultado = (pix + 70 * cos(fi+t*vcurva/raio), piy - 70 * sin(fi+t*vcurva/raio)) # pf = (525,360)
    if 8.3 < t <= 10.5:
        ti = 8.3
        (pix,piy) = (525,360-5)
        resultado = (pix - 249 * (t-ti), piy + 22 * (t-ti)) # pf = (523,329)
        #print(resultado)
    if 10.5 < t:
        resultado = (0, 0)
    return resultado

def parametrizacao_policia(t):
    if t < 9:
        resultado2 = (0, 0) # (932,275)
    if t == 9:
        resultado2 = (0, 0)
    if 9 < t <= 15:
        sirene.play()
        ti = 9
        (pix, piy) = (940, 270)
        resultado2 = (pix - 220 * (t - ti), piy + 25 * (t - ti))  # pf = (523,329)
    if t > 15:
        pygame.mixer.pause()
        resultado2 = (0, 0)
    return resultado2

def carro_rotacao(t):
    vreta = 250  # velocidade retas
    vcurva = vreta / 2  # velocidade curvas
    if t >= 0:
        (velx, vely) = (0, 0)
    if 0 < t <= 2.20:
        (velx, vely) = (249, -22)
    if 2.20 < t <= 4.9:
        raio = 70
        ##             533 + raio * cos(1 + t * vcurva / raio), 249 - raio * sin(1 + t * vcurva / raio))
        (velx, vely) = ( -sin(1 + t * vcurva / raio) * vcurva, - cos(1 + t * vcurva / raio) * vcurva)
    if 4.9 < t <= 5.5:
        (velx, vely) = (-1, vreta)
    if 5.5 < t <= 8.3:
        raio = 70
        fi = -0.5
        (velx, vely) = (-sin(fi + t * vcurva / raio) * vcurva, - cos(fi + t * vcurva / raio) * vcurva)
    if 8.3 < t <= 10.5:
        (velx, vely) = (-249, 22)
    if 10.5 < t:
        (velx, vely) = (0, 0)

    if velx > 0:
        angulo = -atan(vely / velx)
    elif velx < 0:
        angulo = -atan(vely / velx) + 3.14159
    else:
        angulo = 0
    return pygame.transform.rotate(carro, angulo * 180/3.14159)

def modulo(x,y):
    return sqrt(x*x + y*y)

def veloc(t):
    vreta = 250  # velocidade retas
    vcurva = vreta / 2  # velocidade curvas
    if t >= 0:
        mod_vel = 0
    if 0 < t <= 2.20:
        mod_vel = modulo(249, -22)
    if 2.20 < t <= 4.9:
        raio = 70
        mod_vel = modulo(-sin(1 + t * vcurva / raio) * vcurva, - cos(1 + t * vcurva / raio) * vcurva)
    if 4.9 < t <= 5.5:
        mod_vel = modulo(-1, vreta)
    if 5.5 < t <= 8.3:
        raio = 70
        mod_vel = modulo(- sin(-0.5 + t * vcurva / raio) * vcurva, - cos(-0.5 + t * vcurva / raio) * vcurva)
    if 8.3 < t <= 10.5:
        mod_vel = modulo(-249, 22)
    if 10.5 < t:
        mod_vel = 0

    return round(mod_vel,3)

#######################

# (A) Se descomentar aqui (e comentar B) vejo onde passou/ rasto da trajetória
# Pois neste caso só junta a pista uma vez,
# no outro caso está sempre a juntar/desenhar a pista
janela.blit(pista, (0, 0))

#################################
# Ciclo principal do jogo
while True:
    tempo = font.render("t=" + str(int(t)), antialias, BLACK)
    velocidade = font.render("v=" + str(veloc(t)), antialias, BLACK) # ERRADO
    #janela.blit(pista, (0, 0))  # (B) se descomentar aqui (e comentar (A)) vejo movimento
    janela.blit(carro_rotacao(t), parametrizacao(t)) # pygame.transform.rotate(carro, 20 * t)
    janela.blit(policia, parametrizacao_policia(t))
    janela.blit(tempo, (20, 30))
    janela.blit(velocidade, (20, 50))  # Mostrar o valor da velocidade no ecra
    pygame.display.update()
    clock.tick(frame_rate)
    t = t + 0.1

    for event in pygame.event.get():
        # Para sair...
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # Ao clicar em qualquer local, o tempo recomeça com t=0
        # evento mouse click botão esquerdo (código = 1)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            t = 0
            pygame.mixer.unpause()
            motor.play()

##        #Quando queremos saber as coordenadas de um ponto:
##        # descomentar isto e comentar o "evento mouse click"...
##        #"clicar" nesse ponto... o python print as coordenadas.
##        # evento mouse click botão esquerdo (código = 1)
##        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
##            (x, y) = event.pos
##            localizacao = "posicao=(" + str(x) + "," + str(y) + ")"
##            print(localizacao)


##FAQs:
##            (1)
##            Quando parametrização (ou velocidade) não está definida
##            para algum valor de t, dá o erro:
##                "local variable "result/resultado" referenced before assignment"
##


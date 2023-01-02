# Importar o módulo pygame
# se a execução deste import em Python3 ou Python2 der algum erro
# é porque o pygame não está bem instalado
import pygame, sys
from pygame.locals import *
from math import cos, sin, sqrt


# inicialização do módulo pygame
pygame.init()

# criação de uma janela
largura = 937
altura  = 696
tamanho = (largura, altura)
janela  = pygame.display.set_mode(tamanho)
pygame.display.set_caption('CarRace da Leonor') #nome da janela
#Nesta janela o ponto (0,0) é o canto superior esquerdo
#e (532-1,410-1) = (531,409) o canto inferior direito.


# número de imagens por segundo
frame_rate = 24

# relógio para controlo do frame rate
clock = pygame.time.Clock()

# ler uma imagem em formato bmp
pista = pygame.image.load("circuitoA50758.jpg")
carro = pygame.image.load("carroA50758.jpg")

    
#Inicializa o tempo
t=0.0


#########################
#Para escrever o tempo:
font_size = 25
font = pygame.font.Font(None, font_size) # fonte pré-definida
antialias = True # suavização
WHITE = (255, 255, 255)# cor (terno com os valores Red, Green, Blue entre 0 e 255)
BLACK = (5, 60, 5)

##################################
##Exemplo ajustado à pista

def parametrizacao (t): # as curvas tem metade da velocidade das retas
    if t>=0:
        resultado = (0,370) # Posição incial
    if 0<t<=1:
        resultado = (0+500*t, 370 - 45*t) # primeira reta (em contra-mão)
    if 1 < t <= 5.14: # primeira volta para sair (em contra-mão)
        resultado = (500 - 100 * cos(0.57 + t), 325 + 100 * sin(-1 + t))
    #if 2 < t <= 2.5: # segunda reta para mudar de sentido
     #   resultado = (347.4 - 250 * (t - 3.64), 339.6)
    return resultado

'''
    if 0.5<t<=3.64:
        resultado=(355+110*cos(-2+t),190+150*sin(-2+t))
    if 3.64<t<=4:
        resultado=(347.4-250*(t-3.64), 339.6)
    if 4<t<=4.4:
        resultado=(250, 340-250*(t-4))
    if 4.4<t<=4.8:
        resultado=(250+250*(t-4.4), 230)
    if 4.8<t<=5.2:
        resultado=(355, 230-250*(t-4.8))
    if 5.2<t<=5.6:
        resultado=(355-500*(t-5.2), 120)#cerca do dobro da velocidade
    if 5.6<t<=5.9:
        resultado=(160, 140+500*(t-5.6))#cerca do dobro da velocidade
    if 5.9<t<=6.4:
        resultado=(120+450*(t-5.9), 340-(450*(t-5.9)**2))#cerca do dobro da velocidade
    if t>6.4:
        resultado=(0,0)
'''

#######################

#(A) Se descomentar aqui (e comentar B) vejo onde passou/ rasto da trajetória
# Pois neste caso só junta a pista uma vez,
#no outro caso está sempre a juntar/desenhar a pista
#janela.blit(pista, (0, 0)) 

#################################
#Ciclo principal do jogo
while True:
    tempo = font.render("t="+str(int(t)), antialias, BLACK)
    velocidade = font.render("v="+str(int(t)), antialias, BLACK)
    janela.blit(pista, (0, 0))  #(B) se descomentar aqui (e comentar (A)) vejo movimento
    janela.blit(carro, parametrizacao(t))
    janela.blit(tempo, (10, 10))
    janela.blit(velocidade, (10, 30)) #Mostrar o valor da velocidade no ecra
    pygame.display.update()
    clock.tick(frame_rate)
    t=t+0.1
    

    
    for event in pygame.event.get():
        #Para sair...
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        #Ao clicar em qualquer local, o tempo recomeça com t=0
        # evento mouse click botão esquerdo (código = 1)
        elif event.type== pygame.MOUSEBUTTONUP and event.button == 1:
            t = 0
                       

##        #Quando queremos saber as coordenadas de um ponto: 
##        # descomentar isto e comentar o "evento mouse click"...
##        #"clicar" nesse ponto... o python print as coordenadas.
##        # evento mouse click botão esquerdo (código = 1)
##        elif event.type== pygame.MOUSEBUTTONUP and event.button == 1:
##            (x, y) = event.pos
##            localizacao="posicao=(" + str(x) + "," + str(y) + ")"
##            print(localizacao)


##FAQs:
##            (1)
##            Quando parametrização (ou velocidade) não está definida
##            para algum valor de t, dá o erro:
##                "local variable "result/resultado" referenced before assignment"
##            
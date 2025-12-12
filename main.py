# configurações iniciais
import pygame
import random
import sys
# iniciando o pygame, sempre que for usar o pygame precisa de pygame.init
pygame.init()

# criando a tela do jogo
pygame.display.set_caption("Jogo da Cobrinha")
largura, altura = 1200, 800
tela = pygame.display.set_mode((largura, altura))
relogio = pygame.time.Clock()

# cores RGB
verde = (0, 255, 0)
branca = (255, 255, 255)
preta = (0, 0, 0)
vermelha = (255, 0, 0)

# parametros da cobrinha
tamanho_quadrado = 20
velocidade_jogo = 8

#carregando efeitos sonoros
musica_fundo = "asset/musica.mp3"
som_comer = "asset/comer.wav"

pygame.mixer.music.load(musica_fundo)
pygame.mixer.music.set_volume(0.3)

efeito_comer = pygame.mixer.Sound(som_comer)

def gerar_comida():
    comida_x = round(random.randrange(0, largura - tamanho_quadrado) /  tamanho_quadrado) * 20.0
    comida_y = round(random.randrange(0, altura - tamanho_quadrado) / tamanho_quadrado) * 20.0
    return comida_x, comida_y


def desenhar_comida(tamanho, comida_x, comida_y):
    raio = tamanho // 2
    centro_x = comida_x + raio
    centro_y = comida_y + raio
    pygame.draw.circle(tela, vermelha, (centro_x, centro_y), raio)


def desenhar_cobrinha(tamanho, pixels):
    for pixel in pixels:
        pygame.draw.rect(tela, branca, [pixel[0], pixel[1], tamanho, tamanho])


def desenhar_pontuacao(pontuacao):
    fonte = pygame.font.SysFont("helvetica", 29)
    texto = fonte.render(f"Pontos: {pontuacao}", True, verde)
    tela.blit(texto, [1, 1])


def selecionar_velocidade(tecla):
    if tecla == pygame.K_DOWN:
        return 0, tamanho_quadrado
    elif tecla == pygame.K_UP:
        return 0, -tamanho_quadrado
    elif tecla == pygame.K_RIGHT:
        return tamanho_quadrado, 0
    elif tecla == pygame.K_LEFT:
        return -tamanho_quadrado, 0

#Tela Inicial
def tela_inicial():
    rodando = True
    fonte_titulo = pygame.font.SysFont("helvetica", 60)
    fonte_texto = pygame.font.SysFont("helvetica", 30)
    fonte_comando = pygame.font.SysFont("helvetica", 25)

    while rodando:
        tela.fill(preta)

        titulo = fonte_titulo.render("Jogo da Cobrinha", True, verde)
        tela.blit(titulo, (largura/2 - titulo.get_width()/2, altura/6))

        iniciar = fonte_texto.render("Pressione ENTER para começa", True, branca)
        tela.blit(iniciar, (largura/2 - iniciar.get_width()/2, altura/3))

        comando1 = fonte_comando.render("↑ ↓ ← → : Movimentar a cobrinha", True, verde)
        comando2 = fonte_comando.render("ENTER : Iniciar o jogo", True, verde)
        comando3 = fonte_comando.render("ESC : Sair do jogo", True, verde)

        tela.blit(comando1, (largura/2 - comando1.get_width()/2, altura/1.8))
        tela.blit(comando2, (largura/2 - comando2.get_width()/2, altura/1.6))
        tela.blit(comando3, (largura/2 - comando3.get_width()/2, altura/1.45))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    rodando = False

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# Tela Game Over
def tela_game_over(pontos):
    rodando = True
    fonte = pygame.font.SysFont("helvetica", 50)
    fonte2 = pygame.font.SysFont("helvetica", 30)

    while rodando:
        tela.fill(preta)

        texto = fonte.render("GAME OVER", True, vermelha)
        pontos_txt = fonte2.render(f"Pontuação: {pontos}", True, branca)
        reiniciar = fonte2.render("Pressione ENTER para jogar novamente", True, verde)

        tela.blit(texto, (largura/2 - texto.get_width()/2, altura/3))
        tela.blit(pontos_txt, (largura/2 - pontos_txt.get_width()/2, altura/2))
        tela.blit(reiniciar, (largura/2 - reiniciar.get_width()/2, altura/1.5))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return

#Loop principal

def rodar_jogo():

    pygame.mixer.music.play(-1)    #inicia musica infinita

    fim_jogo = False

    x = largura / 2
    y = altura / 2

    velocidade_x = 0
    velocidade_y = 0

    tamanho_cobrinha = 1
    pixels = []

    comida_x, comida_y = gerar_comida()

    while not fim_jogo:
        tela.fill(preta)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                nova_vel = selecionar_velocidade(event.key)
                if nova_vel:
                    velocidade_x, velocidade_y = nova_vel


        desenhar_comida(tamanho_quadrado, comida_x, comida_y)

#atualizar a posiçao da cobrinha
        if x < 0 or x >= largura or y < 0 or y >= altura:
            tela_game_over(tamanho_cobrinha -1)
            fim_jogo = True

        x += velocidade_x
        y += velocidade_y

# atualiza corpo cobrinha
        pixels.append([x, y])
        if len(pixels) > tamanho_cobrinha:
            del pixels[0]

# verifica se a cobrinha bate no proprio corpo
        for pixel in pixels[: -1]:
            if pixel == [x, y]:
                tela_game_over(tamanho_cobrinha - 1)
                fim_jogo = True

        desenhar_cobrinha(tamanho_quadrado, pixels)
        desenhar_pontuacao(tamanho_cobrinha - 1)

# atualização da tela
        pygame.display.update()

# criar uma nova comida
        if x == comida_x and y == comida_y:
            tamanho_cobrinha += 1
            comida_x, comida_y = gerar_comida()
            efeito_comer.play()

        relogio.tick(velocidade_jogo)

tela_inicial()
rodar_jogo()





import random
import pygame
import sys
from pygame.locals import *


windows_width=800 # El tamaño de la ventana del juego, el origen está en la esquina superior izquierda
windows_height=600

cell_size=20   #El tamaño de serpiente debe ser divisible por el largo y ancho de la ventana.

# Algunas definiciones de color
white = (255, 255, 255)
black = (0, 0, 0)
gray = (230, 230, 230)
dark_gray = (40, 40, 40)
DARKGreen = (0, 155, 0)
Green = (0, 255, 0)
Red = (255, 0, 0)
blue = (0, 0, 255)
dark_blue =(0,0, 139)

BG_COLOR = (184,224,217)

#Tamaño del mapa de #  
map_width = int(windows_width / cell_size)
map_height = int(windows_height / cell_size)

# Velocidad de movimiento de la serpiente
snake_speed=10

# Definición de dirección
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

#Función principal
def main_game():
    pygame.init() #Inicializar gygame
    screen=pygame.display.set_mode((windows_width,windows_height))
    pygame.display.set_caption("El juego de la serpiente")
    snake_speed_clock = pygame.time.Clock()  # Crear objeto de reloj Pygame
    screen.fill(white)

    while True:
        run_game(screen,snake_speed_clock) # Asunto del juego
        gameover(screen)                #juego terminado


def run_game(screen,snake_speed_clock):
    #Inicializar la posición, dirección y posición de la comida de la serpiente
    start_x=random.randint(3,map_width-8)
    start_y=random.randint(3,map_width-8)
    snake_coords=[{'x':start_x,'y':start_y},{'x':start_x-1,'y':start_y},{'x':start_x-2,'y':start_y}]#Inicializar serpiente, también puede usar una lista de listas
    direction = RIGHT
    food=get_random_location()

    #ciclo
    while True:
        for event in pygame.event.get():  # Supervisión de eventos de teclado
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN: #Evento clave
                if (event.key==K_LEFT or event.key==K_a) and direction!=RIGHT:
                    direction=LEFT
                elif (event.key==K_RIGHT or event.key==K_d) and direction!=LEFT:
                    direction=RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        snake_move(direction,snake_coords)  #Según la dirección, mueve la serpiente

        alive=snake_is_alive(snake_coords)   # Juzgando la vida y la muerte de las serpientes
        if not alive:                        #Si cuelga, finalice el ciclo, salte de la función run_game y ejecute gameover
            break
        snake_eat_foods(snake_coords,food)   #No colgado, luego mira la comida tardía
        screen.fill(BG_COLOR)                #Actualización de fondo del juego

        # Dibujar a continuación, es dibujar la comida de la serpiente, etc.
        draw_snake(screen, snake_coords)
        draw_food(screen,food)
        draw_score(screen, len(snake_coords) - 3)
        # draw_grid(screen)
        pygame.display.flip()

        #Controla el número de ejecuciones
        snake_speed_clock.tick(snake_speed)  # Control de fps


# De acuerdo con la dirección de movimiento, actualice las coordenadas de la cabeza de la serpiente
def snake_move(directtion,snake_coords):
    if directtion==UP:
        newHead={'x':snake_coords[0]['x'],'y':snake_coords[0]['y']-1}
    elif directtion==DOWN:
        newHead = {'x': snake_coords[0]['x'], 'y': snake_coords[0]['y'] + 1}
    elif directtion==LEFT:
        newHead = {'x': snake_coords[0]['x']-1, 'y': snake_coords[0]['y'] }
    elif directtion == RIGHT:
        newHead = {'x': snake_coords[0]['x']+1, 'y': snake_coords[0]['y']}
    snake_coords.insert(0,newHead)

def snake_is_alive(snake_coords): # Si chocas contra una pared o estás muerto
    alive=True
    if snake_coords[0]['x'] == -1 or snake_coords[0]['x'] == map_width or snake_coords[0]['y'] == -1 or \
			snake_coords[0]['y'] == map_height:
        alive=False
    for snake_body in snake_coords[1:]:
        if snake_coords[0]['x']==snake_body['x'] and snake_coords[0]['y']==snake_body['y']:
            alive=False
    return alive

#Coordenadas coinciden, lo que significa que has comido comida, de lo contrario no hay, luego muévete, pon
def snake_eat_foods(snake_coords,food):
    if snake_coords[0]['x']==food['x'] and snake_coords[0]['y']==food['y']:
        food['x']=random.randint(0, map_width-1)
        food['y']=random.randint(0, map_height-1)
    else:
        del snake_coords[-1]

def get_random_location(): #Las coordenadas de los alimentos se generan aleatoriamente
    return {'x':random.randint(0,map_width-1),'y':random.randint(0,map_height-1)}

def draw_snake(screen, snake_coords):
    for coord in snake_coords:
        x=coord['x']*cell_size
        y=coord['y']*cell_size
        segmentRect=pygame.Rect(x,y,cell_size,cell_size)
        pygame.draw.rect(screen,dark_blue,segmentRect)

def draw_food(screen,food):
    x=food['x']*cell_size
    y=food['y']*cell_size

    foodRect=pygame.Rect(x,y,cell_size,cell_size)
    pygame.draw.rect(screen,Red,foodRect)

def draw_grid(screen):
    for x in range(0,windows_width,cell_size):
        pygame.draw.line(screen,gray,(x,0),(x,windows_height))
    for y in range(0,windows_height,cell_size):
        pygame.draw.line(screen,gray,(0,y),(windows_width,y))
def draw_score(screen, score):
    font = pygame.font.SysFont(None, 40)
    score_str = "{:,}".format(score)
    score_image=font.render('Score: '+score_str,True,Green,gray)
    score_rect=score_image.get_rect()

    score_rect.topleft=(windows_width-200,10)
    screen.blit(score_image, score_rect)

def gameover(screen):
    font=pygame.font.SysFont(None, 40)
    tips=font.render('Press Q or ESC to quit; Press anykey to continue',True, (65, 105, 225))
    screen.blit(tips,(80, 300))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_q:  # Terminar el programa
                    pygame.quit()
                    sys.exit() # Terminar el programa
                else:
                    return  # Finaliza esta función y reinicia el juego

if __name__=='__main__':
    main_game()



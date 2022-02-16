import pygame
import sys
pygame.init()
fps=30
fpsclock=pygame.time.Clock()
sur_obj=pygame.display.set_mode((400,300))
pygame.display.set_caption("Keyboard_Input")
White = (255,255,255)
Celeste = (62, 231, 237)
rojo = (255,0,0)
x=50
y=10
step=5
while True:
    sur_obj.fill(Celeste)
    pygame.draw.rect(sur_obj, (rojo), (x, y, 70, 65))
    for eve in pygame.event.get():
        if eve.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
    key_input = pygame.key.get_pressed()
    if key_input[pygame.K_LEFT]:
        x = x - step
    if key_input[pygame.K_UP]:
        y -= step
    if key_input[pygame.K_RIGHT]:
        x += step
    if key_input[pygame.K_DOWN]:
        y += step
    pygame.display.update()
    fpsclock.tick(fps)

    def draw_score(screen, score):
        font = pygame.font.SysFont(None, 40)
        score_str = "{:,}".format(score)
        score_image=font.render('Score: '+score_str,True,Green,gray)
        score_rect=score_image.get_rect()

        score_rect.topleft=(windows_width-200,10)
        screen.blit(score_image, score_rect)
from random import randrange as rnd, choice
import pygame
import math
import time
pygame.init()
pygame.font.init()

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BROWN = (150, 75, 0)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

FPS = 60
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

class ball():
    def __init__(self, x=40, y=HEIGHT - 50):
        """ Конструктор класса ball
        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.x, self.y = x, y
        self.r = 15
        self.vx = self.vy = 0
        self.color = choice([BLUE, GREEN, RED, BROWN])
        self.live = 10 * FPS

    def move(self):
        """Переместить мяч по прошествии единицы времени.
        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx / FPS
        self.y += self.vy / FPS
        self.vy = self.vy * 0.995 + 1
        self.vx *= 0.995
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.r, 0)
        if abs(self.x - WIDTH/2) > WIDTH/2 - self.r:
            self.vx *= -1
        if abs(self.y - HEIGHT/2) > HEIGHT/2 - self.r:
            self.vy *= -1
        self.live -= 1

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.
        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        return (math.dist([self.x, self.y], [obj.x, obj.y]) <= self.r + obj.r)


class gun():
    def __init__(self):
        self.f2_power = 10
        self.f2_on = 0
        self.color = BLACK
        self.an = 1
        #pygame.draw.line(screen, self.color, (20, HEIGHT - 50), (50, 420), 7)

    def fire2_start(self):
        self.f2_on = 1

    def fire2_end(self):
        """Выстрел мячом.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = ball()
        new_ball.vx = 10 * self.f2_power * math.cos(self.an)
        new_ball.vy = 10 * self.f2_power * math.sin(self.an)
        balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self):
        """Прицеливание. Зависит от положения мыши."""
        self.an = math.atan2((pygame.mouse.get_pos()[1]-(HEIGHT - 50)), (pygame.mouse.get_pos()[0]-20))
        if self.f2_on:
            self.color = ORANGE
            if self.f2_power < 100:
                self.f2_power += 1
        else:
            self.color = BLACK
        pygame.draw.line(screen, self.color, (20, HEIGHT - 50),
                        (20 + max(self.f2_power, 20) * math.cos(self.an),
                        (HEIGHT - 50) + max(self.f2_power, 20) * math.sin(self.an)), 7)


class Target():
    def __init__(self):
        self.live = 1
        self.x = rnd(WIDTH / 2, WIDTH - 20)
        self.y = rnd(50, HEIGHT)
        self.r = rnd(10, 50)
        self.vx = self.vy = 100
        color = self.color = RED
        #surface_points = labelFont.render(str(self.points), False, BLACK)

    def move_target(self):
        if self.x > WIDTH - self.r or self.x < WIDTH / 2 + self.r:
            self.vx *= -1
        if self.y > HEIGHT - self.r or self.y < 50 - self.r:
            self.vy *= -1
        self.x += self.vx / FPS
        self.y += self.vy / FPS
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.r, 0)

class Counter:
    def __init__(self):
        self.count = 0

    def increase(self, points=1):
        self.count += points

    def draw(self):
        surface_counter = labelFont.render(str(self.count), False, WHITE)
        screen.blit(surface_counter, (0, 0))
        
targets = [Target() for i in range (2)]
g1 = gun()
bullet = 0
balls = []
score = Counter()
labelFont = pygame.font.SysFont('Monaco', 50)
surface1 = labelFont.render('', False, WHITE)
pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            g1.fire2_start()
        elif event.type == pygame.MOUSEBUTTONUP:
            g1.fire2_end()
    for b in balls:
        if b.live <= 0:
            balls.pop(0)
        for t in targets:
            if b.hittest(t) and t.live:
                surface1 = labelFont.render('Вы уничтожили цель за ' + str(bullet) + ' выстрелов', False, BLACK)
                b.live = bullet = 0
                balls =[]
                score.increase()
                screen.blit(surface1, (100, HEIGHT / 2))
                pygame.display.update()
                pygame.time.wait(2000)
                targets.remove(t)
                targets += [Target()]
        b.move()
    for t in targets:
        t.move_target()
    #screen.blit(surface1, (0, 0))
    g1.targetting()
    pygame.display.update()
    screen.fill(WHITE)


pygame.quit()

import turtle
import math

wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Collision Detection by @TokyoEdtech (2020820054이승훈)")
wn.tracer(0)

pen = turtle.Turtle()
pen.speed(0)
pen.hideturtle()

shapes = ["wizard.gif", "goblin.gif", "pacman.gif", "cherry.gif", "bar.gif", "ball.gif", "x.gif"]

for shape in shapes:
    wn.register_shape(shape)
    
class Sprite():
    
    ## 생성자: 스프라이트의 위치, 가로/세로 크기, 이미지 지정

    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image

    ## 스프라이트 메서드

    # 지정된 위치로 스프라이트 이동 후 도장 찍기
    def render(self, pen):
        pen.goto(self.x, self.y)
        pen.shape(self.image)
        pen.stamp()

    # 충돌 감지 방법 1: 두 스프라이트의 중심이 일치할 때 충돌 발생
    def is_overlapping_collision(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    # 충돌 감지 방법 2: 두 스프라이트 사이의 거리가 두 객체의 너비의 평균값 보다 작을 때 충돌 발생
    def is_distance_collision(self, other):
        distance = (((self.x-other.x) ** 2) + ((self.y-other.y) ** 2)) ** 0.5
        if distance < (self.width + other.width)/2.0:
            return True
        else:
            return False

    # 충돌 감지 방법 3: 각각의 스프라이트를 둘러썬 경계상자가 겹칠 때 충돌 발생
    # aabb: Axis Aligned Bounding Box
    def is_aabb_collision(self, other):
        x_collision = (math.fabs(self.x - other.x) * 2) < (self.width + other.width)
        y_collision = (math.fabs(self.y - other.y) * 2) < (self.height + other.height)
        return (x_collision and y_collision)

class Character(Sprite):
	def __init__(self, x, y, width, height, image, jump=False):
		super().__init__(x, y, width, height, image)
		self.jump = jump

	def hop(self, distance=300):
		if self.jump == True:
			total_move_x = self.x + distance
			x_move = distance / (distance * 2)
			y_move = x_move * 0.75
			gravity = -(y_move / (distance / x_move / 2))

			while not self.x == total_move_x:
				self.x += x_move
				self.y += y_move
				
				y_move += gravity
				self.render(pen)
				wn.update()
				pen.clear()
	
wizard = Character(-128, 200, 128, 128, "wizard.gif")
goblin = Sprite(128, 200, 108, 128, "goblin.gif")

pacman = Character(-128, 0, 128, 128, "pacman.gif", jump=True)
cherry = Sprite(128, 0, 128, 128, "cherry.gif")

bar = Sprite(0, -400, 128, 24, "bar.gif")
ball = Sprite(0,-200, 32, 32, "ball.gif")

# 스프라이트 모음 리스트
sprites = [wizard, goblin, pacman, cherry, bar, ball]

# 고블린 이동
def move_goblin_left():
    goblin.x -= 64

def move_goblin_right():
    goblin.x += 64

def move_goblin_up():
    goblin.y += 64

def move_goblin_down():
    goblin.y -= 64

# 팩맨 이동, 팩맨 점프
def move_pacman_left():
    pacman.x -= 30

def move_pacman_right():
    pacman.x += 30

def move_pacman_up():
    pacman.y += 30

def move_pacman_down():
    pacman.y -= 30

def jump_pacman(distance=300):
    pacman.hop(distance)

# 야구공 이동
def move_ball_left():
    ball.x -= 24

def move_ball_right():
    ball.x += 24

def move_ball_up():
    ball.y += 24

def move_ball_down():
    ball.y -= 24

select_list = ["goblin", "pacman", "ball"]
select_index = 1

def draw_text():
    pen.up()
    pen.goto(-460, 370)
    pen.color("white")
    pen.write(f"Current Select : {select_list[select_index - 1]} \
(1: goblin, 2: pacman, 3: ball)"
        , False, "left", ("", 18))

def change_index_one():
    global select_index
    select_index = 1

def change_index_two():
    global select_index
    select_index = 2

def change_index_three():
    global select_index
    select_index = 3

# 이벤트 처리
wn.listen()
wn.onkeypress(change_index_one, "1")
wn.onkeypress(change_index_two, "2")
wn.onkeypress(change_index_three, "3")

while True:
    draw_text()
    
    # 각 스프라이트 위치 이동 및 도장 찍기
    for sprite in sprites:
        sprite.render(pen)

    # 고블린 이동 이벤트
    if select_index == 1:
        if goblin.image == "x.gif":
            wn.onkeypress(None, "Left")
            wn.onkeypress(None, "Right")
            wn.onkeypress(None, "Up")
            wn.onkeypress(None, "Down")
        else:
            wn.onkeypress(move_goblin_left, "Left")
            wn.onkeypress(move_goblin_right, "Right")
            wn.onkeypress(move_goblin_up, "Up")
            wn.onkeypress(move_goblin_down, "Down")
            wn.onkeypress(None, "space")
        
            # 고블린 충돌 여부 확인
            if wizard.is_overlapping_collision(goblin):
                wizard.image = "x.gif"
    
            if pacman.is_overlapping_collision(goblin):
                pacman.image = "x.gif"

            if cherry.is_overlapping_collision(goblin):
                cherry.image = "x.gif"

            if bar.is_overlapping_collision(goblin):
                bar.image = "x.gif"

            if ball.is_overlapping_collision(goblin):
                ball.image = "x.gif"
        
            if wizard.is_distance_collision(goblin):
                wizard.image = "x.gif"
    
            if pacman.is_distance_collision(goblin):
                pacman.image = "x.gif"

            if cherry.is_distance_collision(goblin):
                cherry.image = "x.gif"

            if bar.is_distance_collision(goblin):
                bar.image = "x.gif"

            if ball.is_distance_collision(goblin):
                ball.image = "x.gif"

            if wizard.is_aabb_collision(goblin):
                wizard.image = "x.gif"
    
            if pacman.is_aabb_collision(goblin):
                pacman.image = "x.gif"

            if cherry.is_aabb_collision(goblin):
                cherry.image = "x.gif"

            if bar.is_aabb_collision(goblin):
                bar.image = "x.gif"

            if ball.is_aabb_collision(goblin):
                ball.image = "x.gif"
        

    # 팩맨 이동 이벤트
    elif select_index == 2:
        if pacman.image == "x.gif":
            wn.onkeypress(None, "Left")
            wn.onkeypress(None, "Right")
            wn.onkeypress(None, "Up")
            wn.onkeypress(None, "Down")
            wn.onkeypress(None, "space")
        else:
            wn.onkeypress(move_pacman_left, "Left")
            wn.onkeypress(move_pacman_right, "Right")
            wn.onkeypress(move_pacman_up, "Up")
            wn.onkeypress(move_pacman_down, "Down")
            wn.onkeypress(jump_pacman, "space")
        
            # 팩맨 충돌 여부 확인
            if wizard.is_overlapping_collision(pacman):
                wizard.image = "x.gif"

            if goblin.is_overlapping_collision(pacman):
                goblin.image = "x.gif"
    
            if cherry.is_overlapping_collision(pacman):
                cherry.image = "x.gif"
    
            if bar.is_overlapping_collision(pacman):
                bar.image = "x.gif"
    
            if ball.is_overlapping_collision(pacman):
                ball.image = "x.gif"

            if wizard.is_distance_collision(pacman):
                wizard.image = "x.gif"

            if goblin.is_distance_collision(pacman):
                goblin.image = "x.gif"
    
            if cherry.is_distance_collision(pacman):
                cherry.image = "x.gif"
    
            if bar.is_distance_collision(pacman):
                bar.image = "x.gif"
    
            if ball.is_distance_collision(pacman):
                ball.image = "x.gif"
            
            if wizard.is_aabb_collision(pacman):
                wizard.image = "x.gif"

            if goblin.is_aabb_collision(pacman):
                goblin.image = "x.gif"
    
            if cherry.is_aabb_collision(pacman):
                cherry.image = "x.gif"
    
            if bar.is_aabb_collision(pacman):
                bar.image = "x.gif"
    
            if ball.is_aabb_collision(pacman):
                ball.image = "x.gif"

    # 야구공 이동 이벤트
    elif select_index == 3:
        if ball.image == "x.gif":
            wn.onkeypress(None, "Left")
            wn.onkeypress(None, "Right")
            wn.onkeypress(None, "Up")
            wn.onkeypress(None, "Down")
        else:
            wn.onkeypress(move_ball_left, "Left")
            wn.onkeypress(move_ball_right, "Right")
            wn.onkeypress(move_ball_up, "Up")
            wn.onkeypress(move_ball_down, "Down")
            wn.onkeypress(None, "space")
            
            # 야구공 충돌 여부 확인
            if wizard.is_overlapping_collision(ball):
                wizard.image = "x.gif"

            if goblin.is_overlapping_collision(ball):
                goblin.image = "x.gif"
    
            if pacman.is_overlapping_collision(ball):
                pacman.image = "x.gif"
    
            if cherry.is_overlapping_collision(ball):
                cherry.image = "x.gif"
    
            if bar.is_overlapping_collision(ball):
                bar.image = "x.gif"

            if wizard.is_distance_collision(ball):
                wizard.image = "x.gif"

            if goblin.is_distance_collision(ball):
                goblin.image = "x.gif"
    
            if pacman.is_distance_collision(ball):
                pacman.image = "x.gif"
    
            if cherry.is_distance_collision(ball):
                cherry.image = "x.gif"
    
            if bar.is_distance_collision(ball):
                bar.image = "x.gif"

            if wizard.is_aabb_collision(ball):
                wizard.image = "x.gif"

            if goblin.is_aabb_collision(ball):
                goblin.image = "x.gif"
    
            if pacman.is_aabb_collision(ball):
                pacman.image = "x.gif"
    
            if cherry.is_aabb_collision(ball):
                cherry.image = "x.gif"
    
            if bar.is_aabb_collision(ball):
                bar.image = "x.gif"
        
    wn.update() # 화면 업데이트
    pen.clear() # 스프라이트 이동흔적 삭제
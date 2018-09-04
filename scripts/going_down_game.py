# MIT License
# 
# Copyright (c) 2018 Chenrui Lei
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from tkinter import *
import time
import random
from collision_engine_2d import CollisionEngine2D, LineSegment2D, Point2D


class GameObject:
    def __init__(self, canvas, id):
        self.canvas = canvas
        self.canvas_height = canvas.winfo_height()
        self.canvas_width = canvas.winfo_width()
        self.id = id
        self.velocity = Point2D(0, 0)
        self.acceleration = Point2D(0, 350)#9.8)
        
    def update(self, t_interval, game_objects):
        dx = self.velocity.x * t_interval + \
            (1/2) * self.acceleration.x * t_interval**2
        dy = self.velocity.y * t_interval + \
            (1/2) * self.acceleration.y * t_interval**2
        self.canvas.move(self.id, dx, dy)
        d_velocity = Point2D(
            self.acceleration.x * t_interval,
            self.acceleration.y * t_interval
        )
        self.velocity += d_velocity
        
        
        
        
class Stick(GameObject):
    stick_height = 5

    def __init__(self, canvas, tl_cornor, length, color, speed=0):
        object_id = canvas.create_rectangle(tl_cornor[0],
                                          tl_cornor[1],
                                          tl_cornor[0]+length,
                                          tl_cornor[1]+Stick.stick_height,
                                          fill=color)
        GameObject.__init__(self, canvas, object_id)
        self.velocity = Point2D(0, -speed)
        self.acceleration = Point2D(0, 0)
            
            
        
        
class Ball(GameObject):
    def __init__(self, canvas, keys, color, central=None, radius=7):
        if central is None:
            central = Point2D(
                canvas.winfo_width()//2, canvas.winfo_height()//2
            )
        object_id = canvas.create_oval(
            central.x-radius, central.y-radius, 
            central.x+radius, central.y+radius, 
            fill=color
        )
        GameObject.__init__(self, canvas, object_id)
        
        self.canvas.bind_all(keys[0], self.jump)
        self.canvas.bind_all(keys[1], self.left)
        self.canvas.bind_all(keys[2], self.right)
        
    def update(self, t_interval, game_objects):
        last_ball_pos = self.canvas.coords(self.id)
        super(Ball, self).update(t_interval, game_objects)
        ball_pos = self.canvas.coords(self.id)
        
        # bottom boundary collision
        if ball_pos[1] < 0:
            self.canvas.move(self.id, 0, 0 - ball_pos[1])
            self.velocity.y = abs(self.velocity.y) * 0.8
            # print(ball_pos[1])
            return "end_game"
            
        # bottom boundary collision
        if ball_pos[3] > self.canvas_height:
            self.canvas.move(self.id, 0, self.canvas_height - ball_pos[3])
            self.velocity.y = -abs(self.velocity.y) * 0.8
            # print(ball_pos[3])
            return "end_game"
            
        # left boundary collision
        if ball_pos[0] < 0:
            self.canvas.move(self.id, 0 - ball_pos[0], 0)
            self.velocity.x = abs(self.velocity.x) * 0.8
            # print(ball_pos[0])
            
        # right boundary collision
        if ball_pos[2] > self.canvas_width:
            self.canvas.move(self.id, self.canvas_width - ball_pos[2], 0)
            self.velocity.x = -abs(self.velocity.x) * 0.8
            # print(ball_pos[2])
            
        for object in game_objects:
            if type(object) is Stick:
                stick_pos = self.canvas.coords(object.id)
                # print("before: ", stick_pos)
                # stick_pos[1] += object.velocity.y*t_interval
                # print("after: ", stick_pos)
                if self.is_collision(
                    ball_pos, last_ball_pos, stick_pos, Point2D(
                        0, object.velocity.y*t_interval
                    )
                ):
                    self.canvas.move(
                        self.id,  
                        0,
                        stick_pos[1] - ball_pos[3] + object.velocity.y*t_interval
                    )
                    self.velocity.y = object.velocity.y
            
    def is_collision(self, current_ball_pos, last_ball_pos, stick_pos, stick_movement):
        # detect collision
        point_movement = Point2D(
            current_ball_pos[0] - last_ball_pos[0],
            current_ball_pos[1] - last_ball_pos[1]
        )
        # print("point_movement =", point_movement)
        line_segment = LineSegment2D(
            Point2D(stick_pos[0], stick_pos[1]),
            Point2D(stick_pos[2], stick_pos[1])
        )
        # print("line_segment =", line_segment)
        point = Point2D(
            (last_ball_pos[0]+last_ball_pos[2])//2, 
            last_ball_pos[3]
        )
        # print("point =", point)
        if (last_ball_pos[3] <= stick_pos[1] and \
            current_ball_pos[3] >= stick_pos[1]+stick_movement.y) and \
        CollisionEngine2D.point_line_collision(
            point, point_movement, line_segment, 
            stick_movement#Point2D(0, 0)
        ):
            # print("result =", True)
            return True
        # print("result =", False)
        return False
        
            
    def jump(self, evt):
        self.velocity.y = -500
        
    def left(self, evt):
        self.velocity.x -= 100
        # self.acceleration.x = -100
        
    def right(self, evt):
        self.velocity.x += 100
        # self.acceleration.x = 100

        
        
        
class Game:
    font = ('calibri', 50)
    font_color = "#ddd"

    def __init__(self, width, height):
        # game setting
        self.update_time_interval = 0.01
        
        # tk setup
        self.tk = Tk()
        self.tk.title("Going Down Game")
        self.tk.resizable(0, 0)
        self.tk.wm_attributes("-topmost", 1)
        self.tk.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.win_closing = False

        # create canvas
        self.canvas_width = width
        self.canvas_height = height
        self.canvas = Canvas(self.tk, width=width, height=height,
                             bd=0, highlightthickness=0)
        self.canvas.pack()
        self.tk.update()

        self.canvas.bind_all('r', self.reset)

        self.reset(None)

    def reset(self, evt):
        self.canvas.delete("all")

        # create game objects
        self.game_objects = [
            Ball(
                self.canvas, 
                ['<space>', 'a', 'd'], 
                "red",
            ),
            Stick(
                self.canvas,
                (random.randint(0, 400), 400),
                random.randint(100, 300),
                "black"
            ),
        ]
        
        # print(type(self.game_objects[1]) is Stick)
        
        # for i in range(200):
        #     self.game_objects.append(
        #         Ball(
        #             self.canvas, 
        #             ['<space>', 'a', 'd'], 
        #             # [None, None, None], 
        #             "red",
        #             central=Point2D(
        #                 random.randint(8, self.canvas_width-8),
        #                 random.randint(8, self.canvas_height-8)
        #             )
        #         )
        #     )

        # # setup game status
        self.score = 0
        self.score_text_ids = []
        self.end_game = False
        self.last_update_time = None
        self.draw_score()
        
        # game management data
        self.stage = 0
        self.loop_num = -1
        self.skiped_starting = False

    def on_closing(self):
        self.win_closing = True
        self.tk.destroy()

    def update_score(self, points):
        self.score += points
        self.draw_score()
        # print(score)
    
    def draw_score(self):
        canvas = self.canvas
        for text_id in self.score_text_ids:
            canvas.delete(text_id)
        text_id = canvas.create_text(
            self.canvas_width//2,
            50, 
            text=str(self.score),
            font=Game.font, 
            fill=Game.font_color
        )
        self.score_text_ids.append(text_id)

    def update(self):
        if self.end_game:
            return
        self.game_management_update()
        self.game_objects_update()
        self.update_score(1)
        
        
    def game_objects_update(self):
        now = time.time()
        if self.last_update_time is not None:
            t_interval = now - self.last_update_time
        else:
            self.last_update_time = now
            return
            
        # update game objects
        for game_object in self.game_objects:
            if game_object.update(
                self.update_time_interval, 
                self.game_objects
            ) == 'end_game':
                self.end_game = True
            # game_object.update(t_interval)
            
        self.last_update_time = now
            
    def go_to_next_stage(self):
        self.stage += 1
        for object in self.game_objects:
            if type(object) is Stick:
                object.velocity.y = -self.stage * 100
                
    def game_management_update(self):
        if self.score % 1000 == 0:
            self.go_to_next_stage()
            
        if self.loop_num % (100//self.stage) == 0:
            self.game_objects.append(
                Stick(
                    self.canvas,
                    (random.randint(0, 400), 500),
                    random.randint((100//self.stage)+50, (300//self.stage)+50),
                    "black",
                    self.stage * 100
                )
            )
            if self.skiped_starting:
                self.canvas.delete(
                    self.game_objects.pop(1).id
                )
                self.loop_num = 1
                
        if self.loop_num == 200:
            self.skiped_starting = True
            self.loop_num = 1
        
    def run(self):
        # game start running here
        while not self.win_closing:
            self.loop_num += 1
            
            self.update()
            self.tk.update_idletasks()
            self.tk.update()
            
            time.sleep(self.update_time_interval)
            



if __name__ == "__main__":
    game = Game(500, 500)
    game.run()

from tkinter import *
from tkinter import messagebox
import time
import random
class Game:
    def __init__(self):
        self.points = 0
        self.is_running = False
        self.window = Tk()
        self.window.title("Space Worrior")
        self.window.resizable(0, 0)
        self.window.wm_attributes("-topmost", 1)
        self.canvas = Canvas(self.window, height=500, width=500)
        self.points_label_id = self.canvas.create_text(400, 10, text=f"Points: {self.points}")
        self.canvas.pack()
        self.asteroid_list = []
        self.ship = Ship(self)
    def start(self):
        self.is_running = True
        self.generate_astroid()
        self.generate_astroid()
        self.generate_astroid()
    def restart(self):
        for asteroid in self.asteroid_list:
            self.canvas.delete(asteroid.img_id)
        self.asteroid_list = []
        self.points = 0
        self.start()
    def quit(self):
        self.is_running = False
    def generate_astroid(self):
        new_astroid = Asteroid(self)
        self.asteroid_list.append(new_astroid) 

class Ship:
    def __init__(self, game):
        self.width = 38
        self.height = 90
        self.game = game
        self.img_list = []
        self.current_image = 0
        for x in range(1,11):
            img = PhotoImage(file=f'img/ship/ship-{x}.gif')
            self.img_list.append(img)
        self.img_id =  self.game.canvas.create_image(250, 400, image = self.img_list[self.current_image], anchor='nw')
        self.animate()
        self.game.canvas.bind_all('<space>', self.shoot)
        self.game.canvas.bind_all('<KeyPress-Left>', self.move_left)
        self.game.canvas.bind_all('<KeyPress-Right>', self.move_right)
        self.game.ship = self
    def animate(self):
        self.game.canvas.itemconfig(self.img_id, image=self.img_list[self.current_image])
        self.current_image = (self.current_image + 1) % 10
        self.game.window.after(50, self.animate)
    def shoot(self, event):
        coords = self.game.canvas.coords(self.img_id)
        Bullet(self.game, coords[0])
    def move_left(self, event):
        if self.game.is_running: 
            self.game.canvas.move(self.img_id, -5, 0)
    def move_right(self, event):
        if self.game.is_running:
            self.game.canvas.move(self.img_id, 5, 0)
    def get_coords(self):
        coords = self.game.canvas.coords(self.img_id)
        coords.append(coords[0] + self.width)
        coords.append(coords[1] + self.height)
        return {'x1' : coords[0], 'y1' : coords[1], 'x2' : coords[2], 'y2' : coords[3] }

class Bullet:
    def __init__(self, game, x_coord):
        self.width = 45
        self.height = 45
        self.game = game
        self.img_list = []
        self.current_image = 0
        for x in range(1,6):
            img = PhotoImage(file=f'img/bullet/bullet-{x}.gif')
            self.img_list.append(img)
        self.img_id = self.game.canvas.create_image(x_coord, 400, image = self.img_list[self.current_image], anchor='nw')
        self.moving = True
        self.animate()
        self.move_up()
    def animate(self):
        self.game.canvas.itemconfig(self.img_id, image=self.img_list[self.current_image])
        self.current_image = (self.current_image + 1) % 3
        self.game.window.after(50, self.animate)
    def move_up(self):
        if(not self.game.is_running):
            self.game.canvas.delete(self.img_id)
            del self
            return
        self.game.canvas.move(self.img_id, 0, -3 )
        if(self.moving):
            self.game.window.after(5, self.move_up)
            for index in range(0, len(self.game.asteroid_list) ):
                asteroid = self.game.asteroid_list[index]
                asteroid_coords = asteroid.get_coords()
                bullet_coords = self.get_coords()
                if checkCollision(asteroid_coords, bullet_coords):
                    self.game.canvas.delete(self.img_id)
                    self.game.canvas.delete(asteroid.img_id)
                    self.moving = False
                    asteroid.moving = False
                    del self.game.asteroid_list[index]
                    self.game.generate_astroid()
                    self.game.points += 1
                    self.game.canvas.itemconfig(self.game.points_label_id, text=f'Points: {self.game.points}')
                    return 
    def get_coords(self):
        coords = self.game.canvas.coords(self.img_id)
        coords.append(coords[0] + self.width)
        coords.append(coords[1] + self.height)
        return {'x1' : coords[0], 'y1' : coords[1], 'x2' : coords[2], 'y2' : coords[3] }

class Asteroid:
    def __init__(self, game):
        self.width = 47
        self.height = 130
        self.game = game
        self.img_list = []
        self.current_image = 0
        for x in range(1,8):
            img = PhotoImage(file=f'img/asteroid/asteroid-{x}.gif')
            self.img_list.append(img)
        random_x_pos = random.randint(10,490)
        random_y_pos = random.randint(-250,-40)
        self.img_id = self.game.canvas.create_image(random_x_pos, random_y_pos, image = self.img_list[self.current_image], anchor='nw')
        self.moving = True
        self.animate()
        self.move_down()
    def animate(self):
        self.game.canvas.itemconfig(self.img_id, image=self.img_list[self.current_image])
        self.current_image = (self.current_image + 1) % 7
        self.game.window.after(50, self.animate)
    def move_down(self):
        if(self.game.is_running and self.moving):
            self.has_hit_space_ship()
            self.has_hit_bottom()
            self.game.canvas.move(self.img_id, 0, 4)
            self.game.window.after(50, self.move_down)

        else:
            self.game.canvas.delete(self.img_id)
            for x in range(0,len(self.game.asteroid_list)):
                asteroid = self.game.asteroid_list[x]
                if asteroid.img_id == self.img_id:
                    del self.game.asteroid_list[x]
                    self.game.generate_astroid()
                    return
    def has_hit_space_ship(self):
        ship_coords = self.game.ship.get_coords()
        asteroid_coords = self.get_coords()
        
        if ship_coords and asteroid_coords and checkCollisionDown(asteroid_coords, ship_coords):
            self.game.is_running = False
            user_choice = messagebox.askyesno(title='Game Over', message='Do you want to restart?')
            if(user_choice == True):
                self.game.restart()
            else:
                self.game.window.destroy()
    def has_hit_bottom(self):
        coords = self.get_coords()
        if(not coords):
            return
        y2 = coords['y2']
        if y2 >= 580:
            self.moving = False
            self.game.points -= 1
            self.game.canvas.itemconfig(self.game.points_label_id, text=f'Points: {self.game.points}')
            
    def get_coords(self):
        coords = self.game.canvas.coords(self.img_id)
        if(not coords):
            return
        coords.append(coords[0] + self.width)
        coords.append(coords[1] + self.height)
        return {'x1' : coords[0], 'y1' : coords[1], 'x2' : coords[2], 'y2' : coords[3] }

def checkCollision(asteroid_coords, bullet_coords):
    if (bullet_coords['y1'] < asteroid_coords['y2']) and \
        ((bullet_coords['x1'] > asteroid_coords['x1'] and bullet_coords['x1'] < asteroid_coords['x2'])
        or (bullet_coords['x2'] > asteroid_coords['x1'] and bullet_coords['x2'] < asteroid_coords['x2'])
        ):
        return True
    return False
def checkCollisionDown(asteroid_coords, ship_coords):
    if (asteroid_coords['y2'] > ship_coords['y1']) and \
        ((ship_coords['x1'] > asteroid_coords['x1'] and ship_coords['x1'] < asteroid_coords['x2'])
        or (ship_coords['x2'] > asteroid_coords['x1'] and ship_coords['x2'] < asteroid_coords['x2'])
        ):
        return True
    return False
game = Game()
game.start()

mainloop()
# -*- coding: utf-8 -*-
"""
Created on Mon May 13 22:31:42 2019

@author: Dharmik joshi

Space war Game
"""


import turtle
import os
import random
import time
from tkinter.messagebox import *

turtle.speed(1)
turtle.bgcolor("black")
turtle.ht()
turtle.setundobuffer(1)#this save memory
turtle.tracer(0)
#turtle.bgpic("background.gif")
turtle.title("SPACE WAR")
turtle.bgpic("spacebackground.gif")
turtle.register_shape("spaceunit.gif")
turtle.register_shape("spacestone.gif")
turtle.register_shape("bullet.gif")
turtle.register_shape("red_bullet.gif")
turtle.register_shape("type_A.gif")


class Sprite(turtle.Turtle):
    def __init__(self,spriteshape,color,startx,starty):
        turtle.Turtle.__init__(self,shape=spriteshape)
        self.speed(0)
        self.penup()
        self.color(color)
        self.goto(startx,starty)
        self.speed = 1
        
    def move(self):
        self.fd(self.speed)# player will move to forward
        
        #boundry detection
        if self.xcor() > 290:
            self.setx(290)
            self.rt(60)
        if self.xcor() < -290:
            self.setx(-290)
            self.rt(60)
        if self.ycor() > 290:
            self.sety(290)
            self.rt(60)
        if self.ycor() < -290:
            self.sety(-290)
            self.rt(60)
            
    def is_collosion(self,other):
        if (self.xcor() >= (other.xcor() - 20)) and(self.xcor() <= (other.xcor() + 20)) and(self.ycor() >= (other.ycor() - 20)) and(self.ycor() <= (other.ycor() + 20)):
                return True
        else:
            return False
            
        
       
        
        
class Player(Sprite):
    def __init__(self,spriteshape,color,startx,starty):
        Sprite.__init__(self,spriteshape,color,startx,starty)
        self.shapesize(stretch_wid=0.6,stretch_len=1.1,outline=None)
        self.speed=4
        self.lives=3
        self.movement = 1
    def turn_left(self): 
        self.lt(45) #this will turn the left 45 degree
    def turn_right(self):
        self.rt(45) #this will turn the right 45 degree
    def accelerate(self):
        self.speed+=1
    def accelerate(self):
        self.speed+=1
    def decelerate(self):
        self.speed-=1

class Enemy(Sprite):
    def __init__(self,spriteshape,color,startx,starty):
        Sprite.__init__(self,spriteshape,color,startx,starty)    
        self.speed = 6
        self.setheading(random.randint(0,360))


class Ally(Sprite):
    def __init__(self,spriteshape,color,startx,starty):
        Sprite.__init__(self,spriteshape,color,startx,starty)    
        self.speed = 8
        self.setheading(random.randint(0,360))
       
    def move(self):
        self.fd(self.speed)# player will move to forward
        
        #boundry detection
        if self.xcor() > 290:
            self.setx(290)
            self.lt(60)
        if self.xcor() < -290:
            self.setx(-290)
            self.lt(60)
        if self.ycor() > 290:
            self.sety(290) 
            self.lt(60)
        if self.ycor() < -290:
            self.sety(-290)
            self.lt(60)
    
        

class Missile(Sprite):
    def __init__(self,spriteshape,color,startx,starty):
        Sprite.__init__(self,spriteshape,color,startx,starty)     
        self.shapesize(stretch_wid=0.2,stretch_len=0.4,outline=None)
        self.speed = 20
        self.status = "ready"
        self.hideturtle()
        
    def fire(self):
        if self.status == "ready":
            self.setheading(player.heading())
            self.showturtle()
            self.goto(player.xcor(),player.ycor())
            self.status = "firing"
    
    def move(self):
        
        if self.status == "ready":
            self.hideturtle()
        
        if self.status == "firing":
            self.fd(self.speed)
        #border check
        
        if self.xcor() > 290 or self.xcor() < -290 or self.ycor() > 290 or self.ycor() < -290:
            self.hideturtle()
            self.status = "ready"

class Particle(Sprite):
    def __init__(self,spriteshape,color,startx,starty):
        Sprite.__init__(self,spriteshape,color,startx,starty)     
        self.shapesize(stretch_wid=0.1,stretch_len=0.1,outline=None)
        self.frame = 0
        self.goto(-1000,-1000)
        
        
        
    def explode(self,startx,starty):
        self.frame=1
        self.goto(startx,starty)
        self.setheading(random.randint(0,360))
        
    def move(self):
        if self.frame>0:
            self.fd(10)
            self.frame+=1
        if self.frame>10:
            self.frame=0
            self.goto(-1000,-1000)
        
class Game():
    def __init__(self):
        self.level=1
        self.score=0
        self.state="playing"
        self.pen = turtle.Turtle()
        self.lives=3
        
    def draw_border(self):
        #draw border
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.pensize(3)
        self.pen.penup()
        self.pen.goto(-300,300)
        self.pen.pendown()
        for side in range(4):
            self.pen.fd(600)
            self.pen.rt(90)
        self.pen.penup()
        self.pen.ht()
        self.pen.pendown()
        
    def show_status(self):
        self.pen.undo()
        msg = "Score: %s"%(self.score)
        self.pen.penup()
        self.pen.goto(-300,310)
        self.pen.write(msg,font=("Arial",16,"normal"))
        
        
#create game object
game = Game()

#draw the game border
game.draw_border()

game.show_status()
        
#create my sprites
player = Player("triangle","white",0,0)

#enemy = Enemy("circle","red",-100,0)
missile = Missile("triangle","yellow",0,0)
#ally = Ally("square","blue",100,0)

enemies=[]
for i in range(9):
    enemies.append(Enemy("spacestone.gif","red",-100,0))
    
allies=[]
for i in range(6):
    allies.append( Ally("square","blue",100,0))
    
particles = []
for i in range(20):
    particles.append(Particle("circle","orange",0,0))

#keyboard binding
#when left key is pressed turn_left
turtle.onkey(player.turn_left,"Left")
turtle.onkey(player.turn_right,"Right")
turtle.onkey(player.accelerate,"Up")
turtle.onkey(player.decelerate,"Down")
turtle.onkey(missile.fire,"space")
turtle.listen()            

while True:
    
    if player.movement == 1:
        turtle.update()
        time.sleep(0.02)
        
        
        player.move() 
        #enemy.move()
        missile.move()
        #ally.move()
        
        for enemy in enemies:
            enemy.move()
            #check foe collision
            if player.is_collosion(enemy):
                x = random.randint(-250,250)
                y = random.randint(-250,250)
                enemy.goto(x,y)
                #increase score
                game.score-=10
                game.show_status()
                player.movement=0
        
    
            #check for collision with enemy and missile
            if missile.is_collosion(enemy):
                #play the sound
                #os.system("__.mp3&")
                missile.hideturtle()
                missile.status = "ready"
                x = random.randint(-250,250)
                y = random.randint(-250,250)
                enemy.goto(x,y)
                #increase score
                game.score+=10
                game.show_status()
                #do the explosion
                for particle in particles:
                    particle.explode(missile.xcor(),missile.ycor())
                    #particle.setheading(random.randint(0,360))
            
            
        for ally in allies:
            ally.move()
            #collision of missile and enemy with ally 
            if missile.is_collosion(ally):
                x = random.randint(-250,250)
                y = random.randint(-250,250)
                ally.goto(x,y)
                #decrease score
                game.score-=5
                game.show_status()
        
        
        for particle in particles:
            particle.move()
            
    else:
            
            player.shape("type_A.gif")
            for enemy in enemies:
                enemy.hideturtle()
            for ally in allies:
                ally.hideturtle()
                
            if askyesno('Confirm','Do you want to Continue ?'):
                player.movement = 1
                game.score = 0
                player.shape("triangle")
                for enemy in enemies:
                    enemy.showturtle()
                for ally in allies:
                    ally.showturtle()
            else:    
                break
    
    
    
delay = raw_input("Please enter to finish")




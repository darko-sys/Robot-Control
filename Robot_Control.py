#!/usr/bin/python
# A program with graphical interface for control over a 6-DOF robot.
# My robot has a servo in the base, which moves horizontally (servopin1)
# Servo 2,3,4 move the robots' members vertically, Servo5 rotates the claw,
# which is opened and closed by Servo 6.
# It's a chinese aluminium case robot I bought for about € 30 plus
# six metal gear servos which operate at about 5V.
# The interface supports input through keyboard (arrow and wasd keys), left/right
# arrow for servo choice, up/down for increase/decrease pulse wave (PW). PageUp/PageDown for
# increase/decrease of increase/decrease step. 
# It can also be controlled by a joystick/gamepad. I managed to connect a PS3 controller
# to my RasPi 4:
# Left stick (LS) horizontal axis controls servo1, vertical axis Servo 2;
# RS vertical axis controls Servo3, L1 and R1 control Servo4;
# L2 and R2 control Servo5, triangle and square close and open the claw.
# More comments follow at respective steps in the code.

import pigpio, time, pygame, subprocess
from numpy import copy

if subprocess.getoutput('pigs t') == "socket connect failed":#initiate pigpiod daemon, if it doesn't already run, start it. needed for accurate PWM on several GPIO pins
    subprocess.run("sudo pigpiod", shell=True, check=False)
    time.sleep(2)

minmum=[1150,1250,520,500,500,1200]#[770,500,500,500,500,1400] 			the minimum/maximum PW for each servo. 
maxmum=[2500,2150,1400,2500,2500,2050]#[2500,1250,1400,2500,2500,2050]	Settings depend on your robot and your needs.
neutral=[1650,1250,1050,1700,1500,1800]#[1650,1250,1050,1700,1500,1800]	I saved a preliminary values which work in these comments, am experimenting with the uncommented values.
inc=[50,50,50,50,100,100]					# increase steps used with keyboard control

servopin1 = 22
servopin2 = 23
servopin3 = 24
servopin4 = 25
servopin5 = 17
servopin6 = 27

servopwm=copy(neutral)	#used numpy for array copy. else leads to something like pointers and will not work with my code
tmp=copy(neutral)
active=1
axfactor = 6 #auxiliary variable: when using a gamepad, you can adjust the velocity of movement for each command given by axis: the further you push, the faster the movement. (Experimental)
done = False
clock = pygame.time.Clock() #maybe useful, if you want to reduce CPU load. Then you'd need to activate the created object, last lines of main loop below

def moveServo(act, pulse):	# a function to move the servos. It contains a smoothing algorithm, preventing all too sudden movements of the robot. experimental, not elaborated to satisfaction
    incTime=1.0/100.0
    servopwm[act-1] = pulse
    incMove=(pulse - tmp[act-1])/100
    if act == 1:
        for x in range(100):
            servo.set_servo_pulsewidth(servopin1, int(tmp[act-1]+x*incMove))
            time.sleep(incTime)
    elif act == 2:
        for x in range(100):
            servo.set_servo_pulsewidth(servopin2, int(tmp[act-1]+x*incMove))
            time.sleep(incTime)
    elif act == 3:
        for x in range(100):
            servo.set_servo_pulsewidth(servopin3, int(tmp[act-1]+x*incMove))
            time.sleep(incTime)
    elif act == 4:
        for x in range(100):
            servo.set_servo_pulsewidth(servopin4, int(tmp[act-1]+x*incMove))
            time.sleep(incTime)
    elif act == 5:
        for x in range(100):
            servo.set_servo_pulsewidth(servopin5, int(tmp[act-1]+x*incMove))
            time.sleep(incTime)
    elif act == 6:
        for x in range(100):
            servo.set_servo_pulsewidth(servopin6, int(tmp[act-1]+x*incMove))
            time.sleep(incTime)
    tmp[act-1]=pulse

def draw_interface():# function draws the graphic interface
        screen.fill(pygame.Color('white'))
        s1_rect = pygame.draw.rect(screen,pygame.Color('black'),[0,0,200,200],5)
        s2_rect = pygame.draw.rect(screen,pygame.Color('black'),[200,0,200,200],5)
        s3_rect = pygame.draw.rect(screen,pygame.Color('black'),[400,0,200,200],5)
        s4_rect = pygame.draw.rect(screen,pygame.Color('black'),[0,200,200,200],5)
        s5_rect = pygame.draw.rect(screen,pygame.Color('black'),[200,200,200,200],5)
        s6_rect = pygame.draw.rect(screen,pygame.Color('black'),[400,200,200,200],5)
        
        s1_text = pygame.font.Font.render(fnt,"Servo 1",1,pygame.Color('black'))
        pygame.Surface.blit(screen, s1_text, (100- s1_text.get_width() //2, 100 - s1_text.get_height() // 2-s1_text.get_height()+5))
        s1_text_pwm = pygame.font.Font.render(fnt,str(servopwm[0])+" us",1,pygame.Color('black'))
        pygame.Surface.blit(screen, s1_text_pwm, (100- s1_text_pwm.get_width() //2, 100 - s1_text_pwm.get_height() // 2+s1_text_pwm.get_height()+5))
        s1_text_inc = pygame.font.Font.render(fnt,"steps of "+str(inc[0])+" us",1,pygame.Color('black'))
        pygame.Surface.blit(screen,s1_text_inc,(100- s1_text_inc.get_width()//2,190- s1_text_inc.get_height()))
        s2_text = pygame.font.Font.render(fnt,"Servo 2",1,pygame.Color('black'))
        pygame.Surface.blit(screen, s2_text, (300- s2_text.get_width() //2, 100 - s1_text.get_height() // 2-s1_text.get_height()+5))
        s2_text_pwm = pygame.font.Font.render(fnt,str(servopwm[1])+" us",1,pygame.Color('black'))
        pygame.Surface.blit(screen, s2_text_pwm, (300- s2_text_pwm.get_width() //2, 100 - s2_text_pwm.get_height() // 2+s2_text_pwm.get_height()+5))
        s2_text_inc = pygame.font.Font.render(fnt,"steps of "+str(inc[1])+" us",1,pygame.Color('black'))
        pygame.Surface.blit(screen,s2_text_inc,(300- s2_text_inc.get_width()//2,190- s2_text_inc.get_height()))
        s3_text = pygame.font.Font.render(fnt,"Servo 3",1,pygame.Color('black'))
        pygame.Surface.blit(screen, s3_text, (500- s3_text.get_width() //2, 100 - s3_text.get_height() // 2-s3_text.get_height()+5))
        s3_text_pwm = pygame.font.Font.render(fnt,str(servopwm[2])+" us",1,pygame.Color('black'))
        pygame.Surface.blit(screen, s3_text_pwm, (500- s3_text_pwm.get_width() //2, 100 - s3_text_pwm.get_height() // 2+s3_text_pwm.get_height()+5))
        s3_text_inc = pygame.font.Font.render(fnt,"steps of "+str(inc[2])+" us",1,pygame.Color('black'))
        pygame.Surface.blit(screen,s3_text_inc,(500- s3_text_inc.get_width()//2,190- s3_text_inc.get_height()))
        s4_text = pygame.font.Font.render(fnt,"Servo 4",1,pygame.Color('black'))
        pygame.Surface.blit(screen, s4_text, (100- s4_text.get_width() //2, 300 - s4_text.get_height() // 2-s4_text.get_height()+5))
        s4_text_pwm = pygame.font.Font.render(fnt,str(servopwm[3])+" us",1,pygame.Color('black'))
        pygame.Surface.blit(screen, s4_text_pwm, (100- s4_text_pwm.get_width() //2, 300 - s4_text_pwm.get_height() // 2+s4_text_pwm.get_height()+5))
        s4_text_inc = pygame.font.Font.render(fnt,"steps of "+str(inc[3])+" us",1,pygame.Color('black'))
        pygame.Surface.blit(screen,s4_text_inc,(100- s4_text_inc.get_width()//2,390- s4_text_inc.get_height()))
        s5_text = pygame.font.Font.render(fnt,"Servo 5",1,pygame.Color('black'))
        pygame.Surface.blit(screen, s5_text, (300- s5_text.get_width() //2, 300 - s5_text.get_height() // 2-s5_text.get_height()+5))
        s5_text_pwm = pygame.font.Font.render(fnt,str(servopwm[4])+" us",1,pygame.Color('black'))
        pygame.Surface.blit(screen, s5_text_pwm, (300- s5_text_pwm.get_width() //2, 300 - s5_text_pwm.get_height() // 2+s5_text_pwm.get_height()+5))
        s5_text_inc = pygame.font.Font.render(fnt,"steps of "+str(inc[4])+" us",1,pygame.Color('black'))
        pygame.Surface.blit(screen,s5_text_inc,(300- s5_text_inc.get_width()//2,390- s5_text_inc.get_height()))
        s6_text = pygame.font.Font.render(fnt,"Servo 6",1,pygame.Color('black'))
        pygame.Surface.blit(screen, s6_text, (500- s6_text.get_width() //2, 300 - s6_text.get_height() // 2-s6_text.get_height()+5))
        s6_text_pwm = pygame.font.Font.render(fnt,str(servopwm[5])+" us",1,pygame.Color('black'))
        pygame.Surface.blit(screen, s6_text_pwm, (500- s6_text_pwm.get_width() //2, 300 - s6_text_pwm.get_height() // 2+s6_text_pwm.get_height()+5))
        s6_text_inc = pygame.font.Font.render(fnt,"steps of "+str(inc[5])+" us",1,pygame.Color('black'))
        pygame.Surface.blit(screen,s6_text_inc,(500- s6_text_inc.get_width()//2,390- s6_text_inc.get_height()))

def draw_active(act): # graphical issue: this section draws a red square into the box of the active servo
    if act == 1:
        active_servo = pygame.draw.rect(screen,pygame.Color('red'),[5,5,190,190],10)
    elif act == 2:
        active_servo = pygame.draw.rect(screen,pygame.Color('red'),[205,5,190,190],10)
    elif act==3:
        active_servo = pygame.draw.rect(screen,pygame.Color('red'),[405,5,190,190],10)
    elif act==4:
        active_servo = pygame.draw.rect(screen,pygame.Color('red'),[5,205,190,190],10)
    elif act==5:
        active_servo = pygame.draw.rect(screen,pygame.Color('red'),[205,205,190,190],10)
    elif act==6:
        active_servo = pygame.draw.rect(screen,pygame.Color('red'),[405,205,190,190],10)

servo = pigpio.pi()

if not servo.connected:
    exit()

servo.set_servo_pulsewidth(servopin1, neutral[0]) #default settings - will make your robot jump instantly to the settings, no smoothing!
servo.set_servo_pulsewidth(servopin2, neutral[1])
servo.set_servo_pulsewidth(servopin3, neutral[2])
servo.set_servo_pulsewidth(servopin4, neutral[3])
servo.set_servo_pulsewidth(servopin5, neutral[4])
servo.set_servo_pulsewidth(servopin6, neutral[5])

pygame.init() #pygame setup
screen = pygame.display.set_mode((600,400))
fnt = pygame.font.SysFont("Calibri",25)
pygame.display.set_caption("Servocontrol Display and Event Handler")
pygame.joystick.init()

joystick_count = pygame.joystick.get_count()
for i in range(joystick_count):
    joystick = pygame.joystick.Joystick(i)
    joystick.init()

try:#try-except checks whether a joystick is connected
    buttons = joystick.get_numbuttons()
    axes = joystick.get_numaxes()

    while not done:	#main loop
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done = True # exit this loop
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.type == pygame.K_d: #right arrow: change active servo to next
                    active += 1
                    if active > 6:
                        active = 1
                elif event.key == pygame.K_LEFT or event.type == pygame.K_a: #left arrow: change active servo
                    active -= 1
                    if active < 1:
                        active = 6
                elif event.key == pygame.K_UP or event.type == pygame.K_w:	#this is where movement is being initiated: active servo PW upped
                    servopwm[active-1] += inc[active-1]
                    if servopwm[active-1] > maxmum[active-1]:
                        servopwm[active-1] = maxmum[active-1]
                elif event.key == pygame.K_DOWN or event.type == pygame.K_s:
                    servopwm[active-1] -= inc[active-1]
                    if servopwm[active-1] < minmum[active-1]:
                        servopwm[active-1] = minmum[active-1]
                elif event.key == pygame.K_PAGEUP: #bigger increase steps
                    inc[active-1] += 25
                elif event.key == pygame.K_PAGEDOWN:
                    inc[active-1] -= 25
            elif event.type == pygame.JOYBUTTONDOWN: 	#first four buttons are the arrow buttons on PS3 controller
                for i in range(buttons):				#same meaning as keyboard arrows
                    button = joystick.get_button(i)
                    if i == 1:
                        if button == True:
                            inc[active-1] += 25
                    elif i==0:
                        if button == True:
                            inc[active-1] -= 25
                    elif i == 13:
                        if button == True:
                            servopwm[active-1] += inc[active-1]
                            if servopwm[active-1] > maxmum[active-1]:
                                servopwm[active-1] = maxmum[active-1]
                    elif i == 14:
                        if button == True:
                            servopwm[active-1] -= inc[active-1]
                            if servopwm[active-1] < minmum[active-1]:
                                servopwm[active-1] = minmum[active-1]
                    elif i == 15:
                        if button == True:
                            active -= 1
                            if active < 1:
                                active = 6
                    elif i == 16:
                        if button == True:
                            active += 1
                            if active > 6:
                                active = 1
                    elif i==4:							#this is L1, following R1; controls servo 5
                        if button == True:
                            active=5
                            servopwm[active-1] -= inc[active-1]
                            if servopwm[active-1] < minmum[active-1]:
                                servopwm[active-1] = minmum[active-1]
                    elif i==5:
                        if button==True:
                            active=5
                            servopwm[active-1] += inc[active-1]
                            if servopwm[active-1] > maxmum[active-1]:
                                servopwm[active-1] = maxmum[active-1]
                    elif i==3:							#triangle and square, controls servo 6, the claw
                        if button==True:
                            active=6
                            servopwm[active-1] += inc[active-1]
                            if servopwm[active-1] > maxmum[active-1]:
                                servopwm[active-1] = maxmum[active-1]
                    elif i==2:
                        if button==True:
                            active=6
                            servopwm[active-1] -= inc[active-1]
                            if servopwm[active-1] < minmum[active-1]:
                                servopwm[active-1] = minmum[active-1]
            elif event.type == pygame.JOYAXISMOTION:
                for i in range(axes):
                    axis = joystick.get_axis(i)
                    if i == 0:							#left stick, x-y
                        if axis <= 0.1 and >= -0.1:#if your joystick has a lot of jitter, increase this number; the axis buttons are almost never at zero when idle
                            pass
                        elif axis > 0.1:
                            active=1
                            servopwm[active-1] += axfactor * abs(axis)
                            if servopwm[active-1] > maxmum[active-1]:
                                servopwm[active-1] = maxmum[active-1]
                        elif axis < -0.1:
                            active=1
                            servopwm[active-1] -= axfactor * abs(axis)
                            if servopwm[active-1] < minmum[active-1]:
                                servopwm[active-1] = minmum[active-1]
                    elif i==1:							#left stick, u-d
                        if axis <= 0.1 and >= -0.1:
                            pass
                        elif axis < -0.1:					#move forward
                            active=2
                            servopwm[active-1] += axfactor * abs(axis)
                            if servopwm[active-1] > maxmum[active-1]:
                                servopwm[active-1] = maxmum[active-1]
                        elif axis> 0.1:
                            active=2
                            servopwm[active-1] -= axfactor * abs(axis)
                            if servopwm[active-1] < minmum[active-1]:
                                servopwm[active-1] = minmum[active-1]
                    elif i ==4:							#right stick, u-d
                        if axis <= 0.1 and >= -0.1:
                            pass
                        elif axis< -0.1:
                            active=3
                            servopwm[active-1] -= axfactor * abs(axis)
                            if servopwm[active-1] < minmum[active-1]:
                                servopwm[active-1] = minmum[active-1]
                        elif axis>0.1:
                            active=3
                            servopwm[active-1] += axfactor * abs(axis)
                            if servopwm[active-1] > maxmum[active-1]:
                                servopwm[active-1] = maxmum[active-1]
                    elif i==2:							#L2
                        if axis <= 0:
                            pass
                        elif axis>0:
                            active=4
                            servopwm[active-1] -= axfactor * abs(axis)
                            if servopwm[active-1] < minmum[active-1]:
                                servopwm[active-1] = minmum[active-1]
                    elif i==5:							#R2
                        if axis<=0:
                            pass
                        elif axis>0:
                            active=4
                            servopwm[active-1] += axfactor * abs(axis)
                            if servopwm[active-1] > maxmum[active-1]:
                                servopwm[active-1] = maxmum[active-1]

        draw_interface()
        draw_active(active)
        pygame.display.flip()
        if (servopwm[active-1] != tmp[active-1]): #if the active servo got a new value, the moveServo function is run
            moveServo(active, servopwm[active-1])
        clock.tick(5)
except NameError:
    print("No Joystick connected!")
    while not done:	#main loop
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done = True # exit this loop
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.type == pygame.K_d: #right arrow: change active servo to next
                    active += 1
                    if active > 6:
                        active = 1
                elif event.key == pygame.K_LEFT or event.type == pygame.K_a: #left arrow: change active servo
                    active -= 1
                    if active < 1:
                        active = 6
                elif event.key == pygame.K_UP or event.type == pygame.K_w:	#this is where movement is being initiated: active servo PW upped
                    servopwm[active-1] += inc[active-1]
                    if servopwm[active-1] > maxmum[active-1]:
                        servopwm[active-1] = maxmum[active-1]
                elif event.key == pygame.K_DOWN or event.type == pygame.K_s:
                    servopwm[active-1] -= inc[active-1]
                    if servopwm[active-1] < minmum[active-1]:
                        servopwm[active-1] = minmum[active-1]
                elif event.key == pygame.K_PAGEUP: #bigger increase steps
                    inc[active-1] += 25
                elif event.key == pygame.K_PAGEDOWN:
                    inc[active-1] -= 25

        draw_interface()
        draw_active(active)
        pygame.display.flip()
        if (servopwm[active-1] != tmp[active-1]): #if the active servo got a new value, the moveServo function is run
            moveServo(active, servopwm[active-1])
        clock.tick(5)
finally:
servo.stop
pygame.quit()

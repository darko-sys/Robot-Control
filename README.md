# Robot-Control
My elaboration of a program for control of a 6-DOF robot via a Raspberry Pi with graphical interface. It uses <a href="https://github.com/joan2937/pigpio">pigpio</a> for proper PWM management and  <a href="https://www.pygame.org/">pygame</a> for input management, be it by keyboard or by controller, in my case a <a href="https://pythonhosted.org/triangula/sixaxis.html">PS3 controller</a>.

My robot has a servo in the base, which moves horizontally (servopin1). Servo 2,3,4 move the robots' members vertically, Servo5 rotates the claw, which is opened and closed by Servo 6.

It's one of those chinese aluminium case robots I bought for about € 30 plus six metal gear servos which operate at about 5V. You need to provide power from an independent supply, the Pi will be overstrained! To be sure not to harm your Pi, you should use resistors on the signal wires. You need to wire the Pi and the power supply to the same ground level, else it will not work properly. <b><i>Mistakes in the wiring may easily result in destruction of your Pi.</i></b>

The interface supports input through keyboard (arrow keys), left/right arrow for servo choice, up/down for increase/decrease pulse wave (PW). PageUp/PageDown for increase/decrease of increase/decrease steps. 

It can also be controlled by a joystick/gamepad. I managed to connect a PS3 controller to my RasPi 4:
Left stick (LS) horizontal axis controls servo1, vertical axis Servo 2;
RS vertical axis controls Servo3, L1 and R1 control Servo4;
L2 and R2 control Servo5, triangle and square close and open the claw.
This introduction and more comments follow at respective steps in the code.

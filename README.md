# cs-capstone-sculpture
Source code for my computer science capstone project where I built an interactive sculpture using either the Arduino or Pyboard microcontroller.
# Software
The Micropython code should be compatible with Micropython v1.9.4 and v1.9.3. The arduino code should be compatible with Arduino v1.8.6 and v1.8.7.
# Hardware
The Micropython code was tested on Pyboard V1.1. The Arduino code was tested on the Arduino Mega2560 board or, specifically, the Dagu Redback Spider Board. The sculpture employed 4 servos, 2 buzzers, 1 on/off button, and 1 crash sensor.
# Sculpture
Reminiscent of arcade basketball games, the sculpture makes use of the idea of a finite state machine and it 
consists of a basketball court and hoop. The hoop sways back and forth as a player attempts
to bounce a small ball into the hoop to rack up points. Each game session lasts for 45 seconds. The score is tracked by a 
Read, Evaluate, Print, Loop(REPL) prompt on the computer attached to the sculpture. 

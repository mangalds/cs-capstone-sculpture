#include <Servo.h>
// Mini Basketball Finite State Machine
// Made by Delroy Mangal

//Sketch variables
Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;

//Timer variables
unsigned long startMillis;
unsigned long curMillis;
const unsigned long period = 45000;

//Servo variables
long lastFlippedTime = 0;
long interval = 2000;
int servoTracker = 0;
int startServos = 0;

//Pin assignments
const int OnButton = 2;
const int buzzer1 = 12;
const int buzzer2 = 30;
const int crashSensor = 22;


//Wait state variables
bool gameRunning = false;


//Game state variables
unsigned long gameTime = 0;
int score = 0;
int sensorState = 0; 
int lastSensorState = 0;




//Variables to represent state
const int WAITING = 0;
const int GAMING = 1;

//State variable and initial state
int state = WAITING;


//State 0: Wait until button is pressed
void wait() {
  //Stops rotation of servos
    servo1.write(95);
    servo2.write(95);
    servo3.write(95);
    servo4.write(95);
    startMillis = 0;

  //Starts game
    if(!digitalRead(OnButton)){
    gameRunning = true;
  }
  
  if(gameRunning == true){
    state = GAMING;
  }
}

//State 1: Playing the game.
void game() {
  tone(buzzer1, 550);
  tone(buzzer2, 550);
  delay(1000);
  noTone(buzzer1);
  noTone(buzzer2);
  
  startMillis = millis();
  
  while(gameRunning == true){
    curMillis = millis();

    //Keeps track of score
    sensorState = digitalRead(crashSensor);

    if(sensorState != lastSensorState){
    if (sensorState == HIGH) {
    
    } else {
      // if the current state is LOW then the button went from on to off:
      score++;
      Serial.print("score number: ");
      Serial.println(score);
    }
    delay(300);
  }
    lastSensorState = sensorState;

  //Gives initial direction for Servos
    if(startServos == 0){
      startServos = 1;
      servo1.write(120);
      servo2.write(120);
      servo3.write(45);
      servo4.write(45);
    }
    
  //Switches the direction the servos move towards depending on the servoTracker variable
    if(curMillis - lastFlippedTime >= interval){
      if(servoTracker == 0){
        servo1.write(45);
        servo2.write(45);
        servo3.write(120);
        servo4.write(120);
        lastFlippedTime = curMillis;
        servoTracker = 1;
      }
      else{
        servo1.write(120);
        servo2.write(120);
        servo3.write(45);
        servo4.write(45);
        lastFlippedTime = curMillis;
        servoTracker = 0;
      }
    }  

  //Winning condition
    if(score == 3) {
      gameRunning = false;
      tone(buzzer1, 550);
      tone(buzzer2, 550);
      delay(500);
      noTone(buzzer1);
      noTone(buzzer2);
      Serial.print("Final score: ");
      Serial.println(score);
      Serial.println("Congratulations! You won!"); 
      score = 0;
    }

  //Time is up  
    if(curMillis - startMillis >= period){
      gameRunning = false;
      tone(buzzer1, 550);
      tone(buzzer2, 550);
      delay(500);
      noTone(buzzer1);
      noTone(buzzer2);
      Serial.print("Final score: ");
      Serial.println(score); 
      Serial.println("Better luck next time.");
      score = 0;
    }
  }
  
  state = WAITING;
  
}

void setup() {
  // Configures servos, buzzers, sensor, and button  
  servo1.attach(10); //L
  servo2.attach(33); //R
  servo3.attach(35); //R
  servo4.attach(8); //L
  pinMode(OnButton, INPUT);
  pinMode(buzzer1, OUTPUT);
  pinMode(buzzer2, OUTPUT);
  pinMode(crashSensor, INPUT);
  Serial.begin(9600);
}

void loop() {
  // Loops through the wait state and game state
  if (state == WAITING) {
    wait();
  } else if (state == GAMING) {
    game();
  }
  else {
    state = WAITING; 
  }

}


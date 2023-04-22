volatile int counter = 0;
volatile int pulse_counter = 0;
volatile int stop_choice = 0;
const int interruptPin = 20;  //Naming pin20
unsigned long start_time = millis();
int pwm_normalX = 80;  //PWM for forward, backwards, left, right
int pwm_normalY = 80;
int pwm_rotate = 40;  //PWM for rotation
//motor A
int motorApin1 = 14;
int motorApin2 = 3;
//motor B
int motorBpin1 = 4;
int motorBpin2 = 5;
//motor C
int motorCpin1 = 6;
int motorCpin2 = 7;
//motor D
int motorDpin1 = 8;
int motorDpin2 = 9;
// Variables for ultrasonic sensors
// Define T and E for right sensor
const int trigPinX = 15;
const int echoPinX = 16;
// Define T and E for front sensor
const int trigPinY = 17;
const int echoPinY = 18;
// define duration and distance variables for both right and front sensors
// Set aim position (Xn,Yn)
float X_n = 25;  // target 81 to right wheel
float Y_n = 80;  // target 72 to front wheel
float thresh = 1;
float robot_radi = 11;
//float parsedInput;
void setup() {
  Serial.begin(9600);
  Serial.setTimeout(10);
  pinMode(interruptPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(interruptPin), interrupt_call, RISING);
  Serial.println("\n1. FORWARD");
  Serial.println("2. BACKWARD");
  Serial.println("3. LEFT");
  Serial.println("4. RIGHT");
  Serial.println("5. ANTI-CLOCKWISE");
  Serial.println("6. CLOCKWISE");
  Serial.println("7. STOP OPERATION");
  pinMode(motorApin1, OUTPUT);
  pinMode(motorApin2, OUTPUT);
  pinMode(motorBpin1, OUTPUT);
  pinMode(motorBpin2, OUTPUT);
  pinMode(motorCpin1, OUTPUT);
  pinMode(motorCpin2, OUTPUT);
  pinMode(motorDpin1, OUTPUT);
  pinMode(motorDpin2, OUTPUT);
  // define en pins
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(12, OUTPUT);
  pinMode(13, OUTPUT);
  // Initialize ultrasonic pins
  pinMode(trigPinX, OUTPUT);
  pinMode(echoPinX, INPUT);
  pinMode(trigPinY, OUTPUT);
  pinMode(echoPinY, INPUT);
}
void loop() {
  if (stop_choice == 1) {  //if loop to conduct 90 degrees turn only for rotations wiht stop_choice = 1
    while (millis() - start_time < 100000) {
      if (counter >= 158) {  //at counter = 158, robot turns 90 degrees
        moveStop();
        break;
      }
    }
  }
  start_time = millis();
  Serial.println("\nWhat do you want to do ? \n");
  while (Serial.available() == 0) {
  }
  int menuChoice = Serial.parseInt();
  switch (menuChoice) {
    case 1:
      moveForward();
      break;
    case 2:
      moveBackwards();
      break;
    case 3:
      moveLeft();
      break;
    case 4:
      moveRight();
      break;
    case 5:
      moveAntiClk();
      break;
    case 6:
      moveClk();
      break;
    case 7:
      moveStop();
      break;
    case 8:
    // Robot finds its location for first time to a rough position
      auto_positionY();
      delay(2000);
      auto_positionX();
      delay(2000);
    // Robot excecutes auto-position again to a more accurate position
      auto_positionY();
      delay(2000);
      auto_positionX();
      break;
    case 9:
      exit(0);
      break;
    default:
      Serial.println("Please choose a valid selection");
  }
}
void interrupt_call() {  // increase the counter to count the pulses of motor from encoder, when motors are turning
  counter++;
}
void moveStop() {  //stop all motor function
  stop_choice = 0;
  counter = 0;
  Serial.println("\nRobot stopped moving\n");
  analogWrite(10, 0);
  analogWrite(11, 0);
  analogWrite(12, 0);
  analogWrite(13, 0);
}
void moveForward() {
  stop_choice = 0;
  counter = 0;
  Serial.println("\nRobot moving forward\n");
  //Controlling speed (0 = off and 255 = max speed):
  analogWrite(10, pwm_normalY);  //ENA pin
  analogWrite(11, pwm_normalY);  //ENB pin
  //Controlling spin direction of motors:
  digitalWrite(motorApin1, LOW);
  digitalWrite(motorApin2, HIGH);
  digitalWrite(motorBpin1, LOW);
  digitalWrite(motorBpin2, HIGH);
}
void moveBackwards() {
  stop_choice = 0;
  counter = 0;
  Serial.println("\nRobot moving backwards\n");
  //Controlling speed (0 = off and 255 = max speed):
  analogWrite(10, pwm_normalY);  //ENA pin
  analogWrite(11, pwm_normalY);  //ENB pin
  //Controlling spin direction of motors:
  digitalWrite(motorApin1, HIGH);
  digitalWrite(motorApin2, LOW);
  digitalWrite(motorBpin1, HIGH);
  digitalWrite(motorBpin2, LOW);
}
void moveLeft() {
  stop_choice = 0;
  counter = 0;
  Serial.println("\nRobot moving left\n");
  //Controlling speed (0 = off and 255 = max speed):
  analogWrite(12, pwm_normalX);  //ENA pin
  analogWrite(13, pwm_normalX);  //ENB pin
  //Controlling spin direction of motors:
  digitalWrite(motorCpin1, HIGH);
  digitalWrite(motorCpin2, LOW);
  digitalWrite(motorDpin1, HIGH);
  digitalWrite(motorDpin2, LOW);
}
void moveRight() {
  stop_choice = 0;
  counter = 0;
  Serial.println("\nRobot moving right\n");
  //Controlling speed (0 = off and 255 = max speed):
  analogWrite(12, pwm_normalX);  //ENA pin
  analogWrite(13, pwm_normalX);  //ENB pin
  //Controlling spin direction of motors:
  digitalWrite(motorCpin1, LOW);
  digitalWrite(motorCpin2, HIGH);
  digitalWrite(motorDpin1, LOW);
  digitalWrite(motorDpin2, HIGH);
}
void moveAntiClk() {
  //change stop choice to 1
  stop_choice = 1;
  counter = 0;
  Serial.println("\nRobot rotating anti-clockwise\n");
  //Controlling speed (0 = off and 255 = max speed):
  analogWrite(10, pwm_rotate);  //ENA pin
  analogWrite(11, pwm_rotate);  //ENB pin
  analogWrite(12, pwm_rotate);  //ENA pin
  analogWrite(13, pwm_rotate);  //ENB pin
  //Controlling spin direction of motors:
  digitalWrite(motorApin1, HIGH);
  digitalWrite(motorApin2, LOW);
  digitalWrite(motorBpin1, LOW);
  digitalWrite(motorBpin2, HIGH);
  digitalWrite(motorCpin1, HIGH);
  digitalWrite(motorCpin2, LOW);
  digitalWrite(motorDpin1, LOW);
  digitalWrite(motorDpin2, HIGH);
}
void moveClk() {
  stop_choice = 1;
  counter = 0;
  Serial.println("\nRobot moving clockwise\n");
  //Controlling speed (0 = off and 255 = max speed):
  analogWrite(10, pwm_rotate);  //ENA pin
  analogWrite(11, pwm_rotate);  //ENB pin
  analogWrite(12, pwm_rotate);  //ENA pin
  analogWrite(13, pwm_rotate);  //ENB pin
  //Controlling spin direction of motors:
  digitalWrite(motorApin1, LOW);
  digitalWrite(motorApin2, HIGH);
  digitalWrite(motorBpin1, HIGH);
  digitalWrite(motorBpin2, LOW);
  digitalWrite(motorCpin1, LOW);
  digitalWrite(motorCpin2, HIGH);
  digitalWrite(motorDpin1, HIGH);
  digitalWrite(motorDpin2, LOW);
}
// Functions for distance measurement from ultrasonic sensors
float getDistanceX() {
  digitalWrite(trigPinX, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPinX, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPinX, LOW);
  float durationX = pulseIn(echoPinX, HIGH);
  float distanceX = (durationX * .0343) / 2;  //convert to cm
  Serial.print("Distance to right(X) : ");
  Serial.print(distanceX);
  Serial.println(" cm");
  return distanceX;
}
float getDistanceY() {
  digitalWrite(trigPinY, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPinY, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPinY, LOW);
  float durationY = pulseIn(echoPinY, HIGH);
  float distanceY = (durationY * .0343) / 2;  //convert to cm
  Serial.print("Distance to front(Y) : ");
  Serial.print(distanceY);
  Serial.println(" cm");
  return distanceY;
}
void auto_positionX() {
  while (X_n - thresh - robot_radi >= getDistanceX() || getDistanceX() >= X_n + thresh - robot_radi) {
    if (getDistanceX() > X_n + thresh - robot_radi) {
      moveRight();
    } else if (getDistanceX() < X_n - thresh - robot_radi) {
      moveLeft();
    } else {
      moveStop();
    }
  }
  moveStop();
}
void auto_positionY() {
  while (Y_n - thresh - robot_radi >= getDistanceY() || getDistanceY() >= Y_n + thresh - robot_radi) {
    if (getDistanceY() > Y_n + thresh - robot_radi) {
      moveForward();
      //Serial.print("check1");
    } else if (getDistanceY() < Y_n - thresh - robot_radi) {
      moveBackwards();
      //Serial.print("check2");
    } else {
      moveStop();
    }
  }
  moveStop();
}
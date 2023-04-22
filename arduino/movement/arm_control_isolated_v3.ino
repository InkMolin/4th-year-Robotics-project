// File: arm_control_isolated_v3.ino
// Author: Azeez Oyefeso
// Date: March 15, 2023
//
// Description: Converted integration code to just arm control code + added limit switch code

int menuChoice;

// Declare variables to store encoder position and desired position
int encoderPos = 0;
float desiredPosCM = 0;  // test with this set to 0.05 and when set to 0. should be zero anyway
int desiredPos = 0;      // to be changed
float cm2pos = 60.10017;

// Declare pins for the H-bridge
int in1 = 6;
int in2 = 7;
int motorPin = 9;

// Declare pins for the encoder
int encoderA = 2;
int encoderB = 3;
volatile int posi = 0;  // specify posi as volatile, since it will be used in interrupt triggered functions

// Declare variables for the PID controller // Change these params to not be global variables
double Kp = 2;  // Proportional gain
double Ki = 0;  // Integral gain
double Kd = 5;  // Derivative gain // Somewhat useless due to the typo

double error = 0;             // Current error
double lastError = 0;         // Previous error
double integral = 0;          // Integral accumulator
double derivative = 0;        // Derivative term
double output = 0;            // PID output
double stiction_offset = 55;  //55 // minimum value for pwm to allow motor to move

float parsedInput;

// needed for homing function
#include <ezButton.h>
ezButton limitSwitch(10);  // create ezButton object that attach to pin 7;

// timer for serial output
unsigned long previousMillis = 0; // stores the last time the LED was updated
const long interval = 50; // interval at which to blink (milliseconds)

unsigned long startTime; // stores the start time of the program

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(10);

  // Arm setup
  // Initialize the encoder and motor control pins
  pinMode(encoderA, INPUT);
  attachInterrupt(digitalPinToInterrupt(encoderA), readEncoder, RISING);
  pinMode(encoderB, INPUT);

  // Initialize motor control pins
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(motorPin, OUTPUT);

  //auto home of arm position
  autoHome();

  startTime = millis(); // record the start time of the program

}

void loop() {

  float input = parsedInput - 100;
  //Serial.println(input);
  myPID(input);

}

void readEncoder() {
  int b = digitalRead(encoderB);
  if (b > 0) {
    posi++;
  } else {
    posi--;
  }
}

void printSignals() {         // print some useful signals to observe in the serial plotter

  unsigned long currentMillis = millis(); // get the current time

  if (currentMillis - previousMillis >= interval) { // check if it's time to blink the LED
    previousMillis = currentMillis; // remember the last time the LED was updated

    Serial.print((currentMillis - startTime)); // print the elapsed time in seconds
    Serial.print(",");
    Serial.print(output);  // pwm output
    Serial.print(",");
    Serial.print(posi / cm2pos);  // turn the current pos to cm then print // Current postion
    Serial.print(",");
    Serial.print(parsedInput - 100);  // print the desired position in cm //Desired Position // does not bound the input printed
    Serial.print(",");
    Serial.println(error);
    
  }

}

void printCurrentPosition() {     // print some useful signals to observe in the serial plotter
  Serial.println(posi / cm2pos);  // turn the current pos to cm then print // Current postion
}

double controlSignalConstrain(double output) {  //limit bounds of the control signal
  int sign_;
  //non linearity to limit to abs(255)
  if (abs(output) >= 255) {
    sign_ = abs(output) / output;  // get the sign of output
    output = 255 * sign_;
  }
  //non linearity to limit to prevent under powering motor
  if (abs(output) <= stiction_offset) {
    sign_ = abs(output) / output;      // get the sign of output
    output = stiction_offset * sign_;  //minimum pwm value that allows the motor to move
  }

  return output;
}


int cm2pos_fun(float desiredPosCM) {
  double maxDistance = 18;  // alter this value if needed
  double minDistance = 0;
  if (desiredPosCM > maxDistance) {
    desiredPosCM = maxDistance;
  } else if (desiredPosCM < minDistance) {
    desiredPosCM = minDistance;
  }
  desiredPos = cm2pos * desiredPosCM;  // convert cm input to pos unit for calcluations/comparisons
  return desiredPos;
}

void moveArmUp() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  analogWrite(motorPin, output);
}

void moveArmDown() {
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  analogWrite(motorPin, abs(output));
}

void stopArm() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  analogWrite(motorPin, output);
}

void myPID(float menu_number) {
  desiredPos = cm2pos_fun(menu_number);
  printSignals();  //order: pwm output | Current Position | Desired Position | Error (in points unit)
 
  // Calculate the error between the current and desired positions
  error = desiredPos - posi;

  int error_threshold = 5;              // in pulse points units, small value to prevent set point jitter
  if (abs(error) <= error_threshold) {  //set motor to OFF if error is within threshold
    output = 0;
    stopArm();
  } else {
    // Calculate the integral term
    integral += error;

    // Calculate the derivative term
    derivative = error - lastError;  //Note: lastError is never stored

    // Calculate the PID output
    output = Kp * error + Ki * integral + Kd * derivative;
  }

  output = controlSignalConstrain(output);  // limit the magnitude of the control signal to minimum pwm to 255

  // Setting motot direction based on output sign
  if (output > 0) {
    moveArmUp();
  } else if (output < 0) {
    moveArmDown();
  }

  lastError = error;
}

void serialEvent() {                  //using interrupts, get input distance from serial port
  parsedInput = Serial.parseFloat();  // input should be in cm
}

void autoHome(){//LOW = Pressed, 
  limitSwitch.setDebounceTime(50);
  limitSwitch.loop(); //refreshing limit switch to get states

  int state = limitSwitch.getState();  
  if(state == LOW){//check if the arm is already at home//LOW = pressed
    Serial.println("Already homed");//comment after test
    return;
  }

  output = stiction_offset; // set to minimum speed

  moveArmUp();
  delay(200);

  while(!(limitSwitch.isPressed())){
    limitSwitch.loop(); // updates state of limit switch
    state = limitSwitch.getState();
    moveArmDown();
    //Serial.println(state);//test
    delay(50);// maybe unnecessary// used for slowing down the serial

  }

  output = 0;
  stopArm();

  //move arm up slightly
  output = stiction_offset;
  moveArmUp();
  delay(100);

  //finally stop arm
  output = 0;
  stopArm();

  posi = 0;
  delay(100);// wait some time after moving//can be removed

}
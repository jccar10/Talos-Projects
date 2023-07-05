/*
  Fade

  This example shows how to fade an LED on pin 9 using the analogWrite()
  function.

  The analogWrite() function uses PWM, so if you want to change the pin you're
  using, be sure to use another PWM capable pin. On most Arduino, the PWM pins
  are identified with a "~" sign, like ~3, ~5, ~6, ~9, ~10 and ~11.

  This example code is in the public domain.

  http://www.arduino.cc/en/Tutorial/Fade
*/

int L_led_fwd = 5;           // the PWM pin the LED is attached to
int L_led_bkd = 6;
int R_led_fwd = 9;
int R_led_bkd = 10;
int brightness = 0;    // how bright the LED is
int fadeAmount = 5;    // how many points to fade the LED by

String inString = "";
int inChar = 0;
int FL_drive;
int FR_drive;
int save_as_second = false;

// the setup routine runs once when you press reset:
void setup() {
  // declare pin 9 to be an output:
  pinMode(L_led_fwd, OUTPUT);
  pinMode(L_led_bkd, OUTPUT);
  pinMode(R_led_fwd, OUTPUT);
  pinMode(R_led_bkd, OUTPUT);
  analogWrite(L_led_fwd, 0);
  analogWrite(L_led_bkd, 0);
  analogWrite(R_led_fwd, 0);
  analogWrite(R_led_bkd, 0);
  Serial.begin(9600);
  while(!Serial); // wait for Serial to be active ... possibly always true?
  FL_drive = 127;
  FR_drive = 127;
}

unsigned long lastMessage;
const unsigned long MESSAGE_TIMEOUT = 1UL * 10000; // 10 seconds

// the loop routine runs over and over again forever:
void loop() {

  if (Serial.available()) {  // If serial data is available...
    lastMessage = millis();
    inChar = Serial.read();  // Save the latest byte
    inString += char(inChar);// Join the latest character to a growing string of recent chracters
        
    /// 3.2 When a comma is detected, save the current string as a number and assign it to one of the output variables
    if (inChar == ',') {
      if (save_as_second == false) { // If the most recent chracter is a comma, confirm that the current string is the first value.
        FL_drive = inString.toInt(); // Save the string as an integer in one of our two output variables
        inString = "";               // Reset the string
        save_as_second == true;      // Indicate that the next value detected is for the second thruster
      }
    }
    /// 3.3 When a semicolon is detected, save the current string as a number and assign it to the other output variables
    if (inChar == ';') {     // If the latest chracter is the end-of-line character...
      FR_drive = inString.toInt();// Assign the most recent number string to the second thruster
      inString = "";        // Reset the string
      save_as_second = false;// Indicate that the next value detected is for the first thruster

    
    // write the values
    
    }
  }

  if (millis() - lastMessage >= MESSAGE_TIMEOUT) {
    FL_drive = 127;
    FR_drive = 127;
  }

  // L_led:
  if (FL_drive > 127) {
    analogWrite(L_led_fwd, FL_drive-128);
    analogWrite(L_led_bkd, 0);
  } else {
    analogWrite(L_led_fwd, 0);
    analogWrite(L_led_bkd, 127-FL_drive);
  }

  if (FR_drive > 127) {
    analogWrite(R_led_fwd, FR_drive-128);
    analogWrite(R_led_bkd, 0);
  } else {
    analogWrite(R_led_fwd, 0);
    analogWrite(R_led_bkd, 127-FR_drive);
  }
  
 
}

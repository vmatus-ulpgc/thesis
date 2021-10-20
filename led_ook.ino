Add#include "LowPower.h"
#include <OneWire.h>
#include <DallasTemperature.h>

#define headerSize 5
#define samplingTime 4.0/30
#define SLEEPTIME 60
int     state = 0;
int     counterHeader = 0;
int     counterByte = 0;
int     cycleCounter = 0;
unsigned int data = 0;
const int sensPin = 9;
OneWire ow_obj(sensPin);
DallasTemperature tempSens(&ow_obj);


void setup() {
  // put your setup code here, to run once:
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN,0);
  tempSens.begin();
  Serial.begin(9600);
  Serial.println("\nBegin:");
}

void waitForIt(){
  for(int i = 0; i < SLEEPTIME; i++){
    Serial.println("me dormi");
    LowPower.idle(SLEEP_1S, ADC_OFF, TIMER2_OFF, TIMER1_OFF, TIMER0_OFF, 
                SPI_OFF, USART0_OFF, TWI_OFF);
    
    }
  }


void loop() {
  //Action
  switch(state){
    case 0: //header
      digitalWrite(LED_BUILTIN,1);
      Serial.print("H");
      counterHeader++;

      if(counterHeader>=headerSize){
        counterHeader=0;
        state=1;
      }
      
      break;
      
    case 1: //send first 0
      digitalWrite(LED_BUILTIN,0);
      Serial.print("L");
      state=2;
      break;
      
    case 2: //send first subByte
      digitalWrite(LED_BUILTIN,(data<<counterByte)&0b10000000);
      Serial.print(((data<<counterByte)&0b10000000)>>7);
      counterByte++;

      if(counterByte>=4){
        state=3;
      }
      
      break;
    case 3: //send second 0
      digitalWrite(LED_BUILTIN,0);
      Serial.print("L");
      state=4;
      break;
    case 4: //send second subByte
      digitalWrite(LED_BUILTIN,(data<<counterByte)&0b10000000);
      Serial.print(((data<<counterByte)&0b10000000)>>7);
      counterByte++;

      if(counterByte>=8){
        counterByte=0;

        state=5;
        //Serial.println("");
        //if(data++>=256) data=0;
        
        tempSens.requestTemperatures();
        data = tempSens.getTempCByIndex(0);
        //Serial.print("\tSent... New temp. = ");
        //Serial.println(data);
      }
      break;
    case 5: // sleep cycle
      digitalWrite(LED_BUILTIN,0);
      if(cycleCounter == SLEEPTIME-1){
        state = 0;
        cycleCounter = 0;
        } else {
        cycleCounter++;
        //Serial.print("me dormi");
    //LowPower.idle(SLEEP_1S, ADC_OFF, TIMER2_OFF, TIMER1_OFF, TIMER0_OFF, SPI_OFF, USART0_OFF, TWI_OFF);
    LowPower.powerDown(SLEEP_1S, ADC_OFF, BOD_OFF);
        }
      break;
    default:
      break;
  }

  if(state != 5)  delay(samplingTime*1000);


}

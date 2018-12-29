/*
    This is a demo to test gas library
    This code is running on Xadow-mainboard, and the I2C slave is Xadow-gas
    There is a ATmega168PA on Xadow-gas, it get sensors output and feed back to master.
    the data is raw ADC value, algorithm should be realized on master.

    please feel free to write email to me if there is any question

    Jacky Zhang, Embedded Software Engineer
    qi.zhang@seeed.cc
    17,mar,2015
*/

#include <Wire.h>
#include "MutichannelGasSensor.h"

void setup()
{
    Serial.begin(115200);  // start serial for output
    //Serial.println("power on!");
    gas.begin(0x04);//the default I2C address of the slave is 0x04
    gas.powerOn();
    //Serial.print("Firmware Version = ");
    //Serial.println(gas.getVersion());
}

void loop()
{
    float c;

    c = gas.measure_NH3();
    if(c>=0) 
    Serial.print(c);


    c = gas.measure_CO();
    if(c>=0)
    Serial.print(",Q") ;
    Serial.println(c);
    





    delay(1000);
 
}

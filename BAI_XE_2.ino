#include <SPI.h>
#include <MFRC522.h>
#define RST_PIN         9           // Configurable, see typical pin layout above
#define SS_PIN          10
#include <Wire.h>
#include <Servo.h>
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27,16,2); 

MFRC522 mfrc522(SS_PIN, RST_PIN);   // Create MFRC522 instance.

String lua;
String myString;

Servo cua_ra;
char rdata;

int readsuccess;
byte readcard[4];
char str[32] = "";
String StrUID, user;
//------------------------------------------
void senddata()
{
   readsuccess = getid();
  if(readsuccess)
  {
    user_data();
    Serial.println( (String) "DATA,DATE,TIME," + StrUID +',' + user + ',' + "Out" );
    if(user=="Warning. Wrong Card") {}
    else mo_cua();
  }
}
void mo_cua()
{
   // Serial.println("mocua");
    cua_ra.write(90); 
    LCD_TRUE();
    for(int i=0;i<2;i++)
       {
         digitalWrite(5,LOW);       
         delay(100); 
         digitalWrite(5,~LOW);       
         delay(100);  
       } 
       delay(3200);
    cua_ra.write(0); 
   // Serial.println("dongcua");
}
void user_data()
{
    if(StrUID=="17D1A44B")       user="Le Nguyen Dat";
    else if(StrUID=="504CF130")  user="Nguyen Thi Muoi";
    else                       
    {  
       user="Warning. Wrong Card" ;
       LCD_FALSE();
       for(int i=0;i<4;i++)
       {
         digitalWrite(5,LOW);       
         delay(500); 
         digitalWrite(5,~LOW);       
         delay(500);  
       }         
    }
}
int getid(){  
  if(!mfrc522.PICC_IsNewCardPresent()){
    return 0;
  }
  if(!mfrc522.PICC_ReadCardSerial()){
    return 0;
  }
 
 // Serial.println("THE UID OF THE SCANNED CARD IS:");
  for(int i=0;i<4;i++)
      {
        readcard[i]=mfrc522.uid.uidByte[i]; //storing the UID of the tag in readcard
        array_to_string(readcard, 4, str);
        StrUID = str;
      }
  mfrc522.PICC_HaltA();
  return 1;
}
// --------------------------------------------------------------------
void array_to_string(byte array[], unsigned int len, char buffer[])
{
    for (unsigned int i = 0; i < len; i++)
    {
        byte nib1 = (array[i] >> 4) & 0x0F;
        byte nib2 = (array[i] >> 0) & 0x0F;
        buffer[i*2+0] = nib1  < 0xA ? '0' + nib1  : 'A' + nib1  - 0xA;
        buffer[i*2+1] = nib2  < 0xA ? '0' + nib2  : 'A' + nib2  - 0xA;
    }
    buffer[len*2] = '\0';
}

void LCD(){
  //  lcd.clear();
    lcd.setCursor(0,0);
    lcd.print("     Please     ");
    lcd.setCursor(0,1);
    lcd.print("Check your card ");
}
void LCD_TRUE()
{
    lcd.clear();
    lcd.setCursor(5,0);
    lcd.print("Goodbye");
    lcd.setCursor(0,1);
    lcd.print("See you again  ");
}
void LCD_FALSE()
{
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print("    Wrong Card   ");
    lcd.setCursor(0,1);
    lcd.print("Check again    ");
    
}
void LCD_BAO_CHAY(){
    
    lcd.setCursor(0,0);
    lcd.print("****Warning*** ");
    lcd.setCursor(0,1);
    lcd.print("Canh Bao Co Chay");
}
void setup() {
  // put your setup code here, to run once:
    Serial.begin(9600);
    cua_ra.attach(6);
    pinMode(5,OUTPUT);
    pinMode(7,INPUT);
    cua_ra.write(0);    
    
    lcd.init();                      // initialize the lcd 
    lcd.backlight();
    lcd.clear();
    
    SPI.begin();      // Init SPI bus
    mfrc522.PCD_Init(); // Init MFRC522 card
    delay(250);
    LCD(); 
    delay(250);
}

void loop() {
  if(digitalRead(7)==LOW)
  {
    LCD_BAO_CHAY();
    digitalWrite(5,LOW);
    cua_ra.write(90);
  }
  else
  {
      LCD();
      digitalWrite(5,HIGH);
  }
   
   senddata();
}

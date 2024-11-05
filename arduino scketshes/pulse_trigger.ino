#include<SPI.h>
#include <Ethernet2.h>

unsigned int localPort = 5000; //Assign a Port to talk over
char packetBuffer[UDP_TX_PACKET_MAX_SIZE];
String datReq; //String for our data
int packetSize; //Size of Packet
EthernetUDP Udp; //Define UDP Object

byte mac[] = {  0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED }; // Мак адрес
byte ip[] = {  192, 168, 127, 111 }; // IP адрес
EthernetServer server(80);
String readString = String(15);  // Парсим запрос к серверу (ардуино)

int pulse_width = 50; // us
int flag_pulse = 0;
int web_flag = 1;
unsigned int delay_us = 0;

void setup()
{
 Ethernet.begin(mac, ip);
 server.begin();
 Udp.begin(localPort);
 SPI.begin(); 
 pinMode(A1, OUTPUT);
 digitalWrite(A1, LOW);   //  set pin A0 low
}

void pulse(){
  digitalWrite(A1, HIGH); // set pin A0 high
  delay_us = pulse_width - 3; // us
  delayMicroseconds(delay_us);
  digitalWrite(A1, LOW); // set pin A0 low
}

void UDP_communication(){
  int value = 0;
  packetSize = Udp.parsePacket(); //Read theh packetSize

  if(packetSize>0){ //Check to see if a request is present
    
    Udp.read(packetBuffer, UDP_TX_PACKET_MAX_SIZE); //Reading the data request on the Udp
    String datReq(packetBuffer); //Convert packetBuffer array to string datReq
  
    Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
    value = datReq.substring(2).toInt();
    datReq = datReq.substring(0, 2);
  
    if (datReq == "t"){ // time
      Udp.print("t=");
      Udp.print(pulse_width);
      Udp.endPacket();
      }
    else if (datReq == "p"){ // pulse
      pulse();
      flag_pulse = 0; 
      Udp.print("ok");
      Udp.endPacket();
      }
    else if (datReq == "c"){ // check
      Udp.print("ok");
      Udp.endPacket();
      }
    else if (datReq == "wf"){ // web flag
      if (value == 0){web_flag = 0;}
      else if (value == 1){web_flag = 1;}
      Udp.print("wf=");
      Udp.print(int(round(value)));
      Udp.endPacket();
      }
    else if (datReq == "s="){ // set pulse time
      pulse_width = value;
      Udp.print("ok");
      Udp.endPacket();
      }
  }
  memset(packetBuffer, 0, UDP_TX_PACKET_MAX_SIZE);
}



void web_server()
{   
 EthernetClient client = server.available();
 if (client)
 {
  // Проверяем подключен ли клиент к серверу
  while (client.connected())
  {
   char c = client.read();
   if (readString.length() < 30) {
   readString += c;
   }


   if (c == '\n') { 

   if(readString.indexOf("p=1") > 0) {
       if (flag_pulse) {
        pulse();
        }
       flag_pulse = 0;    
   }
   else if(readString.indexOf("p=0") > 0) {;
       flag_pulse = 1;
   }
    
     
   client.println("HTTP/1.1 200 OK");
   client.println("Content-Type: text/html");
   client.println("Refresh: 5");
   client.println();
   client.println("<!DOCTYPE html>");
   client.println("<html><meta charset='UTF-8'>");
   client.println("<style>.tab1 {background-color:#F5F5F5;border-radius: 5px;margin: auto;}</style>"
                  "<br><TABLE class='tab1' align='center' width='200' BORDER='1' cellspacing='0' cellpadding='10'>"
                 "<td><center><b>PULSE GENERATOR </b></td><tr><td><center>");
   client.println("<h1>tau = ");
   client.println(pulse_width);
   client.println(" us</h1>");
   if (flag_pulse){
      client.println("<input type=button value=PULSE onmousedown=location.href='\?p=1\'>"); 
   }
   else{
      client.println("<input type=button value=READY onmousedown=location.href='\?p=0\'>");
   }
   client.println("</td></table></center>");
   client.println("</html>");
   readString="";
   client.stop();   
   
   }
  }
 }
}

void loop()
{
  UDP_communication();
  if (web_flag == 1){
    web_server();
  }
 }


  

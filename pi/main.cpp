//use g++ -std=c++11 -o main main.cpp -lwiringPi

#include <iostream>
#include <unistd.h>
#include <stdio.h>
#include <wiringPi.h>
#include <wiringSerial.h>
#include <thread>
#include <cstring>
#include <string>
#include <string.h>
#define BAUDRATE 9600
#define UART_INPUT_MAX_SIZE 1024
#define PORT "/dev/ttyS0"

class Data{
    public:
        float latitude;
        float longitude;
        float elevation;
        int satellites;
        float v_x;
        float v_y;
        float v_z;
        float a_x;
        float a_y;
        float a_z;
        float m_x;
        float m_y;
        float m_z;
};

class Serial{
    private:
        int id;
    public:
        Serial();
        int init_serial();
        std::string listen();
        int write(std::string msg);
};

int Serial::init_serial(){
    id = serialOpen("/dev/ttyS0", BAUDRATE);
    if(id == -1){
        printf("Error, unable to open serial device.\n");
    }
    return id;
}

std::string Serial::listen(){
    std::cout << "Waiting for connection..." << std::endl;
    while(true){
        char uartInput[UART_INPUT_MAX_SIZE+1];
        int uartInputIndex = 0;
        memset(uartInput, 0, UART_INPUT_MAX_SIZE+1);
        while(serialDataAvail(id) > -1 && uartInputIndex < UART_INPUT_MAX_SIZE+1){
            uartInput[uartInputIndex] = serialGetchar(id);
            if(0 == uartInput[uartInputIndex]){
                break;
            }
            ++uartInputIndex;
        }

        if(uartInputIndex > 0){
            std::string s(uartInput);
            return s;
        }
    }
}

int Serial::write(std::string msg){
    serialPuts(id, msg.c_str());
}

Serial::Serial(){
    init_serial();
    std::string str = Serial::listen();
    if(str != "pc_connect"){
        printf("Error, Connection corruption.\n");
        exit(1);
    }
    write("pi_connect");
    printf("Connected to PC.\n");

    
}

int main(){
	wiringPiSetup();
    Serial uart;

    return 0;
}


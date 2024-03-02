
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <plc.hpp>

namespace testcpplink{
    int testplc()
    {
        ___Config_Init();
        //unsigned long int i = 0;
        //while(true){
        //    ___Config_Run(i);
        //    sleep(0.01);
        //    i++;
        //}
        for(unsigned long int i = 0; i<2; i++){
            ::__ID0_0 = 7;
            ___Config_Run(i);
            printf("udint_output %d\n\r", ::__QD0_0);
            sleep(0.01);
        }
        return 0;
    }
}

int main(int argc,char **argv){
    testcpplink::testplc();
}
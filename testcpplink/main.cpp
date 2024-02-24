
#include <stdio.h>
#include <string.h>
#include <plc.hpp>

namespace testcpplink{
    int testplc()
    {
        Config_Init();

        for(unsigned long int i = 0; i<2; i++){
            ::__ID0_0 = 7;
            Config_Run(i);
            printf("udint_output %d\n\r", ::__QD0_0);
        }
        return 0;
    }
}

int main(int argc,char **argv){
    testcpplink::testplc();
}
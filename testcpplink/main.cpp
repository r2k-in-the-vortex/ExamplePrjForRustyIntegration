
#include <stdio.h>
#include <string.h>

extern "C"{
    extern int udint_output;
    extern int udint_input;
    extern void Config_Run(unsigned long int tick);
    extern void Config_Init(void);
}


int main(int argc,char **argv)
{
    Config_Init();

    for(unsigned long int i; i<2; i++){
        udint_input = 7;
        Config_Run(i);
        printf("udint_output %d\n\r", udint_output);
    }
    return 0;
}
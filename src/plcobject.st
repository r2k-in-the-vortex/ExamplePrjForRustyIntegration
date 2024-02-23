FUNCTION PLC : INT
    VAR
        asd : ULINT;
    END_VAR

    asd := udint_input + 1;
    asd := asd + 1;
    asd := asd + 1;
    asd := asd + 1;
    asd := asd + 1;
    asd := asd + 1;
    asd := asd + 1;
    udint_output := asd + 1;

END_FUNCTION

FUNCTION Config_Run : INT
    VAR_INPUT
        tick : ULINT;
    END_VAR
    PLC();
    
    boolean_output := boolean_input;
END_FUNCTION

FUNCTION Config_Init : INT
    ;
END_FUNCTION

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
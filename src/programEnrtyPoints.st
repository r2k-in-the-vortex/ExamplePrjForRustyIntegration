// this is called cyclically
FUNCTION ___Config_Run : INT
    VAR_INPUT
        tick : ULINT;
    END_VAR
    // ___CopyInputs() calles generated code, do not touch
    ___CopyInputs();
    // here call your project entry point
    PLC();
    // ___CopyOutputs() calles generated code, do not touch
    ___CopyOutputs();
END_FUNCTION

// if there is any pre-runtime setup do be done, do it from this, this is called once before cyclic run starts
FUNCTION ___Config_Init : INT
    ;
END_FUNCTION
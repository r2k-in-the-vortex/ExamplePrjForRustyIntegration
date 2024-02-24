VAR_GLOBAL
    boolean_input       AT %IX0.0 : BOOL; (* some input *)
    boolean_output      AT %QX0.0 : BOOL; (* some output *)
    byte_input          AT %IB0.0 : BYTE; (* some input *)
    byte_output         AT %QB0.0 : BYTE; (* some output *)
    uint_input          AT %IW0.0 : INT; (* some input *)
    uint_output         AT %QW0.0 : WORD; (* some output *)
    udint_input         AT %ID0.0 : DWORD; (* some input *)
    udint_output        AT %QD0.0 : DWORD; (* some output *)
    ulint_input         AT %IL0.0 : LWORD; (* some input *)
    ulint_output        AT %QL0.0 : LWORD; (* some output *)

    
    uint_m1             AT %MW0.0 : WORD; (* some input *)
    uint_m2             AT %MW1.0 : WORD; (* some output *)
    udint_m1            AT %MD0.0 : DWORD; (* some input *)
    udint_m2            AT %MD1.0 : DWORD; (* some output *)
    ulint_m1            AT %ML0.0 : LWORD; (* some input *)
    ulint_m2            AT %ML1.0 : LWORD; (* some output *)

    testvar             : S_somestruct;
END_VAR
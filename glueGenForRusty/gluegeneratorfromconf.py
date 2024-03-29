import sys
import json
import os

__gluevarsGenerateTemplate = """
//-----------------------------------------------------------------------------
// Copyright 2015 Thiago Alves
// This file is part of the OpenPLC Software Stack.
//
// OpenPLC is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// OpenPLC is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with OpenPLC.  If not, see <http://www.gnu.org/licenses/>.
//------
//
// This file is responsible for gluing the variables from the IEC program to
// the OpenPLC memory pointers. It is automatically generated by the
// glue_generator program. PLEASE DON'T EDIT THIS FILE!
// Thiago Alves, May 2016
//-----------------------------------------------------------------------------

#include "iec_std_lib.h"
#include <stdint.h>
extern "C"{{
{0}
    extern void ___Config_Run(unsigned long int tick);
    extern void ___Config_Init(void);
}}

TIME __CURRENT_TIME;
extern unsigned long long common_ticktime__;

//Internal buffers for I/O and memory. These buffers are defined in the
//auto-generated glueVars.cpp file
#define BUFFER_SIZE		1024

//Booleans
IEC_BOOL *bool_input[BUFFER_SIZE][8];
IEC_BOOL *bool_output[BUFFER_SIZE][8];

//Bytes
IEC_BYTE *byte_input[BUFFER_SIZE];
IEC_BYTE *byte_output[BUFFER_SIZE];

//Analog I/O
IEC_UINT *int_input[BUFFER_SIZE];
IEC_UINT *int_output[BUFFER_SIZE];

//32bit I/O
IEC_DINT *dint_input[BUFFER_SIZE];
IEC_DINT *dint_output[BUFFER_SIZE];

//64bit I/O
IEC_LINT *lint_input[BUFFER_SIZE];
IEC_LINT *lint_output[BUFFER_SIZE];

//Memory
IEC_UINT *int_memory[BUFFER_SIZE];
IEC_DINT *dint_memory[BUFFER_SIZE];
IEC_LINT *lint_memory[BUFFER_SIZE];

//Special Functions
IEC_LINT *special_functions[BUFFER_SIZE];



void glueVars()
{{
{1}
}}

void updateTime()
{{
	__CURRENT_TIME.tv_sec  += common_ticktime__ / 1000000000ULL;
	__CURRENT_TIME.tv_nsec += common_ticktime__ % 1000000000ULL;

	if (__CURRENT_TIME.tv_nsec >= 1000000000ULL)
	{{
		__CURRENT_TIME.tv_nsec -= 1000000000ULL;
		__CURRENT_TIME.tv_sec += 1;
	}}
}}"""

__cgenerateTemplate = """
#include <stdint.h>
extern "C"{{
{0}
    extern void ___Config_Run(unsigned long int tick);
    extern void ___Config_Init(void);
}}
"""
__generateTemplate = """
VAR_GLOBAL
{0}END_VAR

FUNCTION ___CopyInputs : INT
{1}END_FUNCTION

FUNCTION ___CopyOutputs : INT
{2}END_FUNCTION
"""

def IEC2Ctype(typename: str) -> str:
    sizedict = {
        "bit": 1,
        "byte": 8,
        "word": 16,
        "dword": 32,
        "lword": 64
    }
    typedict = {
        1: "uint8_t",
        8: "uint8_t",
        16: "uint16_t",
        32: "uint32_t",
        64: "uint64_t"
    }
    size = sizedict[typename.lower()]
    ctype = typedict[size]
    return ctype, size

def stLinkvar(item: dict) -> str:
    IQM = {
        "Input" : "I",
        "Output" : "Q",
        "Memory" : "M"
    }
    stSize = {
        1 : "X",
        8 : "B",
        16 : "W",
        32 : "D",
        64 : "L",
    }
    iqm = IQM[item["direction"]]
    s = stSize[item["size"]]
    a0 = item["address"][0]
    a1 = item["address"][1]
    return f"__{iqm}{s}{a0}_{a1}"

def stDeclare(item: dict) -> str:
    stlinkvar = item["stlinkvar"]
    itype = item["type"].upper().replace("BIT", "BOOL")
    return f"{stlinkvar} : {itype};"

def stInputRead(item: dict) -> str:
    stlinkvar = item["stlinkvar"]
    name = item["name"]
    return f"{name} := {stlinkvar};"

def stOutputWrite(item: dict) -> str:
    stlinkvar = item["stlinkvar"]
    name = item["name"]
    return f"{stlinkvar} := {name};"

def glueVarSet(item: dict) -> str:
    a0 = item["address"][0]
    a1 = item["address"][1]
    direction = item["direction"]
    stlinkvar = item["stlinkvar"]
    size = item["size"]
    reginputs = {
        1 : "bool_input",
        8 : "byte_input",
        16 : "int_input",
        32 : "dint_input",
        64 : "lint_input",
    }
    regoutputs = {
        1 : "bool_output",
        8 : "byte_output",
        16 : "int_output",
        32 : "dint_output",
        64 : "lint_output",
    }
    regmemory = {
        16 : "int_memory",
        32 : "dint_memory",
        64 : "lint_memory",
    }
    match direction:
        case "Input":
            register = reginputs[size]
        case "Output":
            register = regoutputs[size]
        case "Memory":
            register = regmemory[size]
    cSize = {
        1 : "IEC_BOOL",
        8 : "IEC_BYTE",
        16 : "IEC_UINT",
        32 : "IEC_DINT",
        64 : "IEC_LINT",
    }
    ctype = cSize[size]
    if size == 1:
        return f"{register}[{a0}][{a1}] = ({ctype} *)&{stlinkvar};"
    else:
        return f"{register}[{a0}] = ({ctype} *)&{stlinkvar};"

def ParseConfFile(confffile: str) -> dict:
    f = open(confffile)
    conf = json.load(f)
    f.close()
    items = conf["HardwareConfiguration"]

    for item in items:
        ctype, size = IEC2Ctype(item[0]["type"])
        name = item[0]["name"]
        item[0]["size"] = size
        stlinkvar = stLinkvar(item[0])
        item[0]["stlinkvar"] = stlinkvar
        item[0]["cdeclaration"] = f"extern {ctype} {stlinkvar};"
        item[0]["stdeclaration"] = stDeclare(item[0])
        item[0]["inread"] = stInputRead(item[0])
        item[0]["outwrite"] = stOutputWrite(item[0])
        item[0]["gluevarstatement"] = glueVarSet(item[0])
    return conf

def IdentText(text: str) -> str:
    ret = ""
    for line in text.splitlines():
        ret += "    " + line + os.linesep
    return ret

def GenerateVariableDeclaforC(conf: dict) -> str:
    lines = ""
    for item in conf["HardwareConfiguration"]:
        lines += item[0]["cdeclaration"] + os.linesep
    declare = IdentText(lines)
    return __cgenerateTemplate.format(declare)

def GenerateGlueVarforC(conf: dict) -> str:
    lines = ""
    for item in conf["HardwareConfiguration"]:
        lines += item[0]["cdeclaration"] + os.linesep
    declare = IdentText(lines)
    lines = ""
    for item in conf["HardwareConfiguration"]:
        lines += item[0]["gluevarstatement"] + os.linesep
    assign = IdentText(lines)
    return __gluevarsGenerateTemplate.format(declare, assign)

def GenerateGluefileforST(conf: dict) -> str:
    lines = ""
    for item in conf["HardwareConfiguration"]:
        lines += item[0]["stdeclaration"] + os.linesep
    declare = IdentText(lines)
        
    lines = ""
    for item in conf["HardwareConfiguration"]:
        if item[0]["direction"] in ["Input", "Memory"]:
            lines += item[0]["inread"] + os.linesep
    inread = IdentText(lines)
        
    lines = ""
    for item in conf["HardwareConfiguration"]:
        if item[0]["direction"] in ["Output", "Memory"]:
            lines += item[0]["outwrite"] + os.linesep
    outwrite = IdentText(lines)

    return __generateTemplate.format(declare, inread, outwrite)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("4 arguments required, conf.json path, st output file path, hpp output file path, gluevars.cpp path")
        exit

    confffile = sys.argv[1]
    stoutfile = sys.argv[2]
    coutfile = sys.argv[3]
    goutluefile = sys.argv[4]

    res = ParseConfFile(confffile)
    
    cfile = GenerateVariableDeclaforC(res)
    stfile = GenerateGluefileforST(res)
    gluefile = GenerateGlueVarforC(res)
    f1 = open(stoutfile, "w")
    f1.write(stfile)
    f1.close()
    f2 = open(coutfile, "w")
    f2.write(cfile)
    f2.close()
    f2 = open(goutluefile, "w")
    f2.write(gluefile)
    f2.close()
    
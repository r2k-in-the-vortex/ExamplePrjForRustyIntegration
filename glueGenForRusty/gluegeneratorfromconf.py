import sys
import json
import os

__cgenerateTemplate = """
#include <stdint.h>
extern "C"{{
{0}
    extern void Config_Run(unsigned long int tick);
    extern void Config_Init(void);
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
    return conf

def IdentText(text: str) -> str:
    ret = ""
    for line in text.splitlines():
        ret += "    " + line + os.linesep
    return ret

def GenerateGluefileforC(conf: dict) -> str:
    lines = ""
    for item in conf["HardwareConfiguration"]:
        lines += item[0]["cdeclaration"] + os.linesep
    declare = IdentText(lines)
    return __cgenerateTemplate.format(declare)

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
    if len(sys.argv) != 4:
        print("3 arguments required, conf.json path, st output file path, hpp output file path")
        exit

    confffile = sys.argv[1]
    stoutfile = sys.argv[2]
    coutfile = sys.argv[3]

    res = ParseConfFile(confffile)
    
    cfile = GenerateGluefileforC(res)
    stfile = GenerateGluefileforST(res)
    f1 = open(stoutfile, "w")
    f1.write(stfile)
    f1.close()
    f2 = open(coutfile, "w")
    f2.write(cfile)
    f2.close()
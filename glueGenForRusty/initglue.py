import sys

__generateTemplate = """
VAR_GLOBAL
    {0}
END_VAR

FUNCTION ___CopyInputs : INT
    {1}
END_FUNCTION

FUNCTION ___CopyOutputs : INT
    {2}
END_FUNCTION
"""

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("1 argument required, output .st file path")
        exit

    outfile = sys.argv[1]

    f = open(outfile, "w")
    f.write(__generateTemplate.format("", ";", ";"))
    f.close()
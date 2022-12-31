import base64, string, random
from easyui import *

functionName = ['print', '[]', "''",
    random.randint(10000,200000), 'len',
    'input', 'iter', 'round', 'zip', 'vars',
    'tuple', 'type', '__import__', 'super',
    'sum', 'str', 'set', 'slice', 'sorted',
    'filter', 'frozenset', 'getattr', 'exec']

splitSize = 12
varSize = 200
floodNumber = 6
obfuscateOperationNumber = 1

#https://www.geeksforgeeks.org/python-generate-random-string-of-given-length/
def getRandomString(len):
    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase +
                             string.digits, k=len))

def getRandomStringB85(len):
    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase +
                             string.digits + "+#)=}{)'", k=len))

def getRandomStringArray(size):
    res = []
    for i in range(size):
        rdn = getRandomString(varSize)
        while str(rdn[:1]).isnumeric():
            rdn = getRandomString(varSize)
        res.append(rdn)
    return res

def encrypt(txt:str):
    return base64.b85encode(txt.encode("ascii")).decode("ascii")

def split(text, size):
    return [text[i:i + size] for i in range(0, len(text), size)]

def obfuscate(_input):
    result = ""
    finalLine = '%execvar%(%importvar%("base64").b85decode('

    importVar = ""
    execVar = ""

    fileContentB64 = encrypt(_input)
    fileSplitted = split(fileContentB64, splitSize)

    randomStringArray = getRandomStringArray(len(fileSplitted))

    pos = 0
    resultArray = []

    for chunk in fileSplitted:
        resultArray.append(f'{randomStringArray[pos]}="{chunk}"')
        if pos == 0:
            finalLine += randomStringArray[pos]
        else:
            finalLine += "+" + randomStringArray[pos]
        pos += 1
    
    random.shuffle(resultArray)

    res = ""
    for line in resultArray:
        guys = []
        guys.append(line)
        for i in range(floodNumber):
                randomVar = getRandomStringArray(1)[0]
                funcName = random.choice(functionName)
                if funcName == "''":
                    funcName = '"' + getRandomStringB85(splitSize) + '"'
                if funcName == '__import__':
                    importVar = randomVar
                if funcName == 'exec':
                    execVar = randomVar
                guys.append(f"{randomVar}={funcName}")
        
        random.shuffle(guys)

        baka = ""
        for element in guys:
            baka += element + ";"
        
        res += baka + "\n"

    finalLine = finalLine.replace("%execvar%", execVar).replace("%importvar%", importVar)
    finalLine += "))"

    res += finalLine
    return res

if __name__ == "__main__":
    Console.clear()
    print(Colors.pink + Center.XCenter(Ascii.get("CODE FLOODER", AsciiType.BANNER)))
    fileToObf = Console.input("Please Drag Your Python File To Confuse", PrintType.CLEAN)

    fileContentStr = open(fileToObf.replace('"', ""), "r").read()
    for i in range(obfuscateOperationNumber):
        print('Obfuscated ' + str(i) + " times")
        fileContentStr = obfuscate(fileContentStr)
    with open("result.py", "a+") as file:
        file.write(fileContentStr)
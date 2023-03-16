import re, json, sys

def media(lista):
    if len(lista)==0:
        return 0
    return sum(lista)/len(lista)

def treatCSV(filename):
    regex = re.compile(r"(\w+)(?:{(\d+)})?(?:{(\d+,\d+)})?((?:::\w+)+)?")
    funcoes = {"sum":sum, "media":media, "max":max, "min":min}

    def treatValue(key, splittedLine, jsonObject, index, indexFields):
        value = splittedLine[index]
        fieldName = key['nomeCampo']
        if len(key['lista'])>0:
            numVals = int(key['lista'])
            jsonObject[fieldName] = []
            for val in splittedLine[index::index+numVals+1]:
                jsonObject[fieldName].append(int(val))
            index += numVals
        elif len(key['listaIntervalada'])>0:
            numValsMin,numValsMax = key['listaIntervalada'].split(",")
            numValsMin = int(numValsMin)
            numValsMax = int(numValsMax)

            jsonObject[fieldName] = []
            for val in splittedLine[index:index+numValsMax]:
                if len(val) == 0:
                    break
                jsonObject[fieldName].append(int(val))
            index += numValsMax
        else:
            jsonObject[fieldName] = value
            index += 1

        if len(key['funcaoAgregacao'])>0 and fieldName in jsonObject.keys():
            funcs = key['funcaoAgregacao'].split("::")

            for func in funcs:
                if len(func) > 0:
                    jsonObject[fieldName + "_" + func] = funcoes[func](jsonObject[fieldName])

            jsonObject.pop(fieldName)

        indexFields += 1

        return index, indexFields

    with open(filename, "r") as csvFile:
        lines = csvFile.readlines()
        header = lines[0]
        fields = []

        for mtch in regex.findall(header):
            fields.append({"nomeCampo":mtch[0], "lista":mtch[1], "listaIntervalada":mtch[2], "funcaoAgregacao":mtch[3]})


        result = []

        for line in lines[1::]:
            splittedLine = [field.strip('\n') for field in line.split(",")]
            
            jsonObject = {}
            index,indexFields = 0,0
            l = len(splittedLine)
            l2 = len(fields)
            while index < l and indexFields < l2:
                index, indexFields = treatValue(fields[indexFields], splittedLine, jsonObject, index, indexFields)

            result.append(jsonObject)

    with open(filename.replace("csv","json"),"w") as jsonFile:
        json.dump(result, jsonFile, ensure_ascii=False, indent=True)


def main():
    if len(sys.argv) < 2:
        print("Erro: Deve dar como argumento o nome do ficheiro csv a ler")
        return 1

    treatCSV(sys.argv[1])

if __name__ == "__main__":
    main()

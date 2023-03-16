[
 {
  "import": ""
 },
 {
  "import": "def media(lista):"
 },
 {
  "import": "    if len(lista)==0:"
 },
 {
  "import": "        return 0"
 },
 {
  "import": "    return sum(lista)/len(lista)"
 },
 {
  "import": ""
 },
 {
  "import": "def treatCSV(filename):"
 },
 {
  "import": "    regex = re.compile(r\"(\\w+)(?:{(\\d+)})?(?:{(\\d+",
  "re": "\\d+)})?((?:::\\w+)+)?\")"
 },
 {
  "import": "    funcoes = {\"sum\":sum",
  "re": " \"media\":media",
  "json": " \"max\":max",
  "sys": " \"min\":min}"
 },
 {
  "import": ""
 },
 {
  "import": "    def treatValue(key",
  "re": " splittedLine",
  "json": " jsonObject",
  "sys": " index"
 },
 {
  "import": "        value = splittedLine[index]"
 },
 {
  "import": "        fieldName = key['nomeCampo']"
 },
 {
  "import": "        if len(key['lista'])>0:"
 },
 {
  "import": "            numVals = int(key['lista'])"
 },
 {
  "import": "            jsonObject[fieldName] = []"
 },
 {
  "import": "            for val in splittedLine[index::index+numVals+1]:"
 },
 {
  "import": "                jsonObject[fieldName].append(int(val))"
 },
 {
  "import": "            index += numVals"
 },
 {
  "import": "        elif len(key['listaIntervalada'])>0:"
 },
 {
  "import": "            numValsMin",
  "re": "numValsMax = key['listaIntervalada'].split(\"",
  "json": "\")"
 },
 {
  "import": "            numValsMin = int(numValsMin)"
 },
 {
  "import": "            numValsMax = int(numValsMax)"
 },
 {
  "import": ""
 },
 {
  "import": "            jsonObject[fieldName] = []"
 },
 {
  "import": "            for val in splittedLine[index:index+numValsMax]:"
 },
 {
  "import": "                if len(val) == 0:"
 },
 {
  "import": "                    break"
 },
 {
  "import": "                jsonObject[fieldName].append(int(val))"
 },
 {
  "import": "            index += numValsMax"
 },
 {
  "import": "        else:"
 },
 {
  "import": "            jsonObject[fieldName] = value"
 },
 {
  "import": "            index += 1"
 },
 {
  "import": ""
 },
 {
  "import": "        if len(key['funcaoAgregacao'])>0 and fieldName in jsonObject.keys():"
 },
 {
  "import": "            funcs = key['funcaoAgregacao'].split(\"::\")"
 },
 {
  "import": ""
 },
 {
  "import": "            for func in funcs:"
 },
 {
  "import": "                if len(func) > 0:"
 },
 {
  "import": "                    jsonObject[fieldName + \"_\" + func] = funcoes[func](jsonObject[fieldName])"
 },
 {
  "import": ""
 },
 {
  "import": "            jsonObject.pop(fieldName)"
 },
 {
  "import": ""
 },
 {
  "import": "        indexFields += 1"
 },
 {
  "import": ""
 },
 {
  "import": "        return index",
  "re": " indexFields"
 },
 {
  "import": ""
 },
 {
  "import": "    with open(filename",
  "re": " \"r\") as csvFile:"
 },
 {
  "import": "        lines = csvFile.readlines()"
 },
 {
  "import": "        header = lines[0]"
 },
 {
  "import": "        fields = []"
 },
 {
  "import": ""
 },
 {
  "import": "        for mtch in regex.findall(header):"
 },
 {
  "import": "            fields.append({\"nomeCampo\":mtch[0]",
  "re": " \"lista\":mtch[1]",
  "json": " \"listaIntervalada\":mtch[2]",
  "sys": " \"funcaoAgregacao\":mtch[3]})"
 },
 {
  "import": ""
 },
 {
  "import": ""
 },
 {
  "import": "        result = []"
 },
 {
  "import": ""
 },
 {
  "import": "        for line in lines[1::]:"
 },
 {
  "import": "            splittedLine = [field.strip('\\n') for field in line.split(\"",
  "re": "\")]"
 },
 {
  "import": "            print(splittedLine)"
 },
 {
  "import": "            "
 },
 {
  "import": "            jsonObject = {}"
 },
 {
  "import": "            index",
  "re": "indexFields = 0",
  "json": "0"
 },
 {
  "import": "            l = len(splittedLine)"
 },
 {
  "import": "            l2 = len(fields)"
 },
 {
  "import": "            while index < l and indexFields < l2:"
 },
 {
  "import": "                index",
  "re": " indexFields = treatValue(fields[indexFields]",
  "json": " splittedLine",
  "sys": " jsonObject"
 },
 {
  "import": ""
 },
 {
  "import": "            result.append(jsonObject)"
 },
 {
  "import": ""
 },
 {
  "import": "    with open(filename.replace(\"csv\"",
  "re": "\"json\")",
  "json": "\"w\") as jsonFile:"
 },
 {
  "import": "        json.dump(result",
  "re": " jsonFile",
  "json": " ensure_ascii=False",
  "sys": " indent=True)"
 },
 {
  "import": ""
 },
 {
  "import": ""
 },
 {
  "import": "def main():"
 },
 {
  "import": "    if len(sys.argv) < 1:"
 },
 {
  "import": "        print(\"Erro: Deve dar como argumento o nome do ficheiro csv a ler\")"
 },
 {
  "import": "        return 1"
 },
 {
  "import": ""
 },
 {
  "import": "    treatCSV(sys.argv[0])"
 },
 {
  "import": ""
 },
 {
  "import": "if __name__ == \"__main__\":"
 },
 {
  "import": "    main()"
 }
]
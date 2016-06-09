import pandas as pd
import itertools
import json


def main():
    df = pd.read_excel('ffta.xlsx', 'jobTree')
    writeSankeyJson(df)
    # testCombineList()


def testCombineList():
    a = ['a', 'b', 'b', 'a']
    b = ['b', 'c']
    c = combineList(a, b)
    print(c)


def combineList(a, b):
    result = []
    # result = list(set(a + b))
    for x in itertools.chain.from_iterable([a, b]):
        if x not in result:
            result.append(x)
    print(result)
    return result


def writeSankeyJson(df):
    raceList = df['race'].unique()
    print(raceList)
    finalJsonObject = {}
    for race in raceList:
        dfRace = df[df['race']==race]

        nodeDistinctList = generateNodeDistinctList(dfRace)
        replaceDict = {v: i for i, v in enumerate(nodeDistinctList)}
        dfRace['source'].replace(replaceDict, inplace=True)
        dfRace['target'].replace(replaceDict, inplace=True)

        resultJson = generateJsonObject(dfRace, nodeDistinctList)
        finalJsonObject[race]=resultJson
    f = open('fftaRace.json', 'w')
    json.dump(finalJsonObject, f)


def generateNodeDistinctList(df):
    sourceList = df['source'].tolist()
    targetList = df['target'].tolist()
    result = combineList(sourceList, targetList)
    return result




def generateJsonObject(dfResult, nodeDistinctList):
    nodeArray = [{"name": x} for x in nodeDistinctList]
    # links array, array of dictionary [{'from':tableName1, 'to':tableName2, 'value':1}]
    linksJsonStr = dfResult.to_json(orient='records')
    linksJson = json.loads(linksJsonStr)
    resultJson = {"nodes": nodeArray, "links": linksJson}
    return resultJson


if __name__ == '__main__':
    main()
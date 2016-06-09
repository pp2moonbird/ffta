import pandas as pd
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
    # result = list(set(a) | set(b))
    result = list(set(a + b))
    return result


def writeSankeyJson(df):
    df['source'] = df['race'] + '-' + df['source']
    df['target'] = df['race'] + '-' + df['target']

    nodeDistinctList = generateNodeDistinctList(df)
    replaceDict = {v: i for i, v in enumerate(nodeDistinctList)}
    df['source'].replace(replaceDict, inplace=True)
    df['target'].replace(replaceDict, inplace=True)


    resultJson = generateJsonObject(df, nodeDistinctList)
    f = open('ffta.json', 'w')
    json.dump(resultJson, f)


def generateNodeDistinctList(df):
    sourceList = df['source'].tolist()
    targetList = df['target'].tolist()
    result = combineList(sourceList, targetList)
    return result




def generateJsonObject(dfResult, nodeDistinctList):
    nodeArray = [{"name": x.split('-')[1], "race": x.split('-')[0]} for x in nodeDistinctList]
    # links array, array of dictionary [{'from':tableName1, 'to':tableName2, 'value':1}]
    linksJsonStr = dfResult.to_json(orient='records')
    linksJson = json.loads(linksJsonStr)
    resultJson = {"nodes": nodeArray, "links": linksJson}
    return resultJson


if __name__ == '__main__':
    main()
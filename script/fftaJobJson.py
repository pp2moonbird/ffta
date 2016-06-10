import pandas as pd
import itertools
import json


def main():
    df = pd.read_excel('ffta.xlsx', 'jobTree')
    writeCombinedSankeyJson(df)
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

# all races are in same nodes array and links array, front end will get right nodes array and links
def writeCombinedSankeyJson(df):
	df['source'] = df['race'] + '-' + df['source']
	df['target'] = df['race'] + '-' + df['target']

	nodeDistinctList = generateNodeDistinctList(df)
	replaceDict = {v: i for i, v in enumerate(nodeDistinctList)}
	df['source'].replace(replaceDict, inplace=True)
	df['target'].replace(replaceDict, inplace=True)


	resultJson = generateCombinedJsonObject(df, nodeDistinctList, replaceDict)
	f = open('fftaCombined.json', 'w')
	json.dump(resultJson, f)


def generateCombinedJsonObject(dfResult, nodeDistinctList, replaceDict):
	nodeArray = [{"name": x.split('-')[1], "race": x.split('-')[0], "id":replaceDict[x]} for x in nodeDistinctList]
	# links array, array of dictionary [{'from':tableName1, 'to':tableName2, 'value':1}]
	linksJsonStr = dfResult.to_json(orient='records')
	linksJson = json.loads(linksJsonStr)
	resultJson = {"nodes": nodeArray, "links": linksJson}
	return resultJson


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
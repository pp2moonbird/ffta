# coding=utf-8
from bs4 import BeautifulSoup, element, NavigableString
import requests
import os.path
import pandas as pd
import numpy as np
import json
raceList = ['Human', 'Viera', 'Moogle', 'Bangaa', 'NuMou']
baseFolder = '../raw/'
htmlList = ['http://ffta.ffsky.cn/human.htm',
            'http://ffta.ffsky.cn/viera.htm',
            'http://ffta.ffsky.cn/mog.htm',
            'http://ffta.ffsky.cn/banga.htm',
            'http://ffta.ffsky.cn/nnmo.htm'
            ]
linkDict = dict(zip(raceList, htmlList))
fileList = [baseFolder + race + '.html' for race in raceList]
fileDict = dict(zip(raceList, fileList))

def main():
    saveRawHTML()


    dfMapping = pd.read_excel('fftaJobNameMapping.xlsx')
    dfMapping.drop_duplicates()
    jobList = dfMapping['job'].tolist()
    chineseJobList = dfMapping['chineseJobName'].tolist()
    mappingDict = dict(zip(jobList, chineseJobList))
    print(mappingDict)
    print(dfMapping)


    # investigateNavigableString(tables)
    # investigateTag(tables)
    # testOneRace()

    # resultList = [
    #                 {
    #                     'name':race,
    #                     'jobs':jobList
    #                             [
    #                                 {
    #                                     'jobName': jobName,
    #                                     'df': skillDF
    #                                 }
    #                             ]
    #                 }
    #             ]


    resultList = []
    for race in raceList:
        # race.name
        raceResultDict = {'name': race}

        file = fileDict[race]
        bs = BeautifulSoup(open(file), 'html.parser')
        tables = bs.find_all('table')

        jobList = []
        for table in tables:
            jobDict = {}

            job = extraJob(table)
            df = extractSkillToDf(table)
            #race.jobs[].jobName
            jobDict['jobName'] = job
            #race.jobs[].df
            jobDict['df'] = df
            jobList.append(jobDict)

        # race.jobs
        raceResultDict['jobs'] = jobList
        resultList.append(raceResultDict)



    for race in resultList:
        if race['name'] == 'Human':
            for job in race['jobs']:
                if job['jobName'] == u'青魔道士（青魔法）':
                    blueDf = job['df']
                    dfNormal = blueDf.ix[:3]
                    dfMonster = blueDf.ix[6:]
                    dfMonster['Description'] = dfMonster['CostOfAP']
                    dfMonster['Weapon'] = dfMonster['skillType']
                    dfMonster['CostOfAP'] = np.NaN
                    dfMonster['skillType'] = np.NaN
                    blueDf = pd.concat([dfNormal, dfMonster])
                    job['df'] = blueDf;
                    break;
            break;

    # extractJobMappingRaw(resultList)

    # transform df to json object
    for race in resultList:
        for job in race['jobs']:
            #job['jobName'] = race['name'] + '-' + job['jobName'] # TODO cutomize key
            job['jobName'] = mappingDict[job['jobName']]
            job['race'] = race['name']
            df = job['df']
            dfJsonStr = df.to_json(orient='records')
            dfJson = json.loads(dfJsonStr)
            job['df'] = dfJson

    # add sankeyDataJson
    jobTreeJson = json.load(open('fftaRaceSplit.json'))

    for raceObject in resultList:
        raceName = raceObject['name']
        for jobTreeObject in jobTreeJson:
            if jobTreeObject['race'] == raceName:
                raceObject['sankeyData'] = jobTreeObject['sankeyData']
                break


    f = open('fftaSkill.json', 'w')
    json.dump(resultList, f)

    # get blue mage


    # print


def extractJobMappingRaw(resultList):
    raceJobListForMapping = []
    for r in resultList:
        raceName = r['name']
        print(r['name'])
        for j in r['jobs']:
            jobName = j['jobName']
            raceJobListForMapping.append({'race': raceName, 'job': jobName})
            print('\t' + j['jobName'])
    dfRaceJobMapping = pd.DataFrame(raceJobListForMapping)
    print(dfRaceJobMapping)
    dfRaceJobMapping.to_csv('raceJobMapping.csv', encoding='utf-8')


#
    # # modify blue mage
	#

	#
    # # print blueDf
    # # blueDf.to_csv('blue.csv', encoding='utf-8')
	#
    # # result Dict {race:jobDict{job:df}} -> [{name:race, jobDictList:[{job:jobDf}]}]
    # resultList = []
    # for race in resultDict:
	#
	#
	#
    #     linksJsonStr = dfResult.to_json(orient='records')
	 #    linksJson = json.loads(linksJsonStr)
	#
    #     raceDict = {'name':race}




    # dict & df -> json

    # json -> d3 -> html

def testOneRace():
    dfList = []
    race = 'Human'
    file = fileDict[race]
    bs = BeautifulSoup(open(file), 'html.parser')
    tables = bs.find_all('table')
    for table in tables:
        job = extraJob(table)
        df = extractSkillToDf(table)
        dfList.append(df)
    df = pd.concat(dfList)
    df.to_csv('sample2.csv', encoding='utf-8')


def extraJob(table):
    childTags = [c for c in table.contents if type(c) == element.Tag]
    job = childTags[0].text.strip()
    return job


def extractSkillToDf(table):
    childTags = [c for c in table.contents if type(c) == element.Tag]
    job = childTags[0].text.strip()
    skillTags = childTags[2:]
    header = ['skillName', 'CostOfAP', 'skillType', 'Description', 'Weapon']
    skillList = []
    for skill in skillTags:
        rawStringList = skill.text.strip().split('\n')
        rawStringList = [s.strip() for s in rawStringList]
        mydict = dict(zip(header, rawStringList))
        skillList.append(mydict)
    df = pd.DataFrame(skillList, columns=header)
    return df


def investigateTag(tables):
    table = tables[0]
    tagChilds = [c for c in table.contents if type(c) == element.Tag]
    print(tagChilds[0])

    print(tagChilds[0].text.strip())

    print(tagChilds[1])

    print(tagChilds[1].text.strip().split('\s'))

    tds = tagChilds[1].find_all('td')
    tdtextarray = [td.text for td in tds if type(td) == element.Tag]
    print (tdtextarray)
    s = pd.Series(tdtextarray)
    print (s)


def investigateNavigableString(tables):
    table = tables[0]
    contents = table.contents
    typeList = []
    valueList = []
    lenList = []
    for c in contents:
        ctype = type(c)
        if type(c) == NavigableString:
            value = str(c).strip()
            length = len(value)

        else:
            value = c.text.strip()
            length = len(value)
        if length > 0:
            typeList.append(ctype)
            valueList.append(value)
            lenList.append(length)
    df = pd.DataFrame({"type": typeList, 'value': valueList, 'len': lenList})
    print(df)
    df.to_csv('sample.csv', encoding='utf-8')


#
    #         # print(type(c))
    #         if(type(c) == element.Tag): # TODO only Tag has real value
    #             print(c)
    #             counter = counter + 1
	#
    #     print(t.contents[0])
	#
    #     print(counter)
    #     #print (t.children)
    #     print('#############')
    # #print(tables)


def saveRawHTML():


    for race in fileDict:
        f = fileDict[race]
        # print(f, os.path.isfile(f))
        if(not os.path.isfile(f)):
            r = requests.get(linkDict[race])
            r.encoding='utf-8'  #TODO why need explictily set encoding?
            # print(r.text)
            with open(f, "a+") as f:
                f.write(r.text.encode('utf-8'))

if __name__ == '__main__':
    main()
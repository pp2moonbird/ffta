from bs4 import BeautifulSoup, element
import requests
import os.path
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
    print(raceList)
    saveRawHTML()

    race = 'Human'
    file = fileDict[race]
    bs = BeautifulSoup(open(file), 'html.parser')
    tables = bs.find_all('table')
    for t in tables:
        counter = 0;
        for c in t.contents:

            # print(type(c))
            if(type(c) == element.Tag): # TODO only Tag has real value
                print(c)
                counter = counter + 1

        print(t.contents[0])

        print(counter)
        #print (t.children)
        print('#############')
    #print(tables)


def saveRawHTML():


    for race in fileDict:
        f = fileDict[race]
        print(f, os.path.isfile(f))
        if(not os.path.isfile(f)):
            r = requests.get(linkDict[race])
            r.encoding='utf-8'  #TODO why need explictily set encoding?
            # print(r.text)
            with open(f, "a+") as f:
                f.write(r.text)

if __name__ == '__main__':
    main()
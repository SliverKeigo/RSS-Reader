# -*- coding: utf-8 -*-
import os
import json
import time
import feedparser

######################################################################################
displayDay=14 # 抓取多久前的内容
displayMax=5 # 每个RSS最多抓取数
weeklyKeyWord="" # 周刊过滤关键字

rssBase={
    "阮一峰":{
        "url":"http://www.ruanyifeng.com/blog/atom.xml",
        "type":"weekly",
        "timeFormat":"%Y-%m-%dT%H:%M:%SZ",
        "nameColor":"#1f883d"
    },
    "Anthony Fu":{
        "url":"https://antfu.me/feed.xml",
        "type":"weekly",
        "timeFormat":"%a, %d %b %Y %H:%M:%S GMT",
        "nameColor":"#1f883d"
    }
}
######################################################################################

rssAll=[]
info=json.loads('{}')
info["published"]=int(time.time())
info["rssBase"]=rssBase
rssAll.append(info)

displayTime=info["published"]-displayDay*86400

print("====== Now timestamp = %d ======"%info["published"])
print("====== Start reptile Last %d days ======"%displayDay)

for rss in rssBase:
    print("====== Reptile %s ======"%rss)
    rssDate = feedparser.parse(rssBase[rss]["url"])
    i=0
    for entry in rssDate['entries']:
        if i>=displayMax:
            break
        if 'published' in entry:
            published=int(time.mktime(time.strptime(entry['published'], rssBase[rss]["timeFormat"])))

            if entry['published'][-5]=="+":
                published=published-(int(entry['published'][-5:])*36)

            if rssBase[rss]["type"]=="weekly" and (weeklyKeyWord not in entry['title']):
                continue

            if published>info["published"]:
                continue

            if published>displayTime:
                onePost=json.loads('{}')
                onePost["name"]=rss
                onePost["title"]=entry['title']
                onePost["link"]=entry['link']
                onePost["published"]=published
                rssAll.append(onePost)
                print("====== Reptile %s ======"%(onePost["title"]))
                i=i+1
        else:
            published = None
            print("Warning: 'published' key not found in entry")

            
print("====== Start sorted %d list ======"%(len(rssAll)-1))
rssAll=sorted(rssAll,key=lambda e:e.__getitem__("published"),reverse=True)

if not os.path.exists('docs/'):
    os.mkdir('docs/')
    print("ERROR Please add docs/index.html")

listFile=open("docs/rssAll.json","w")
listFile.write(json.dumps(rssAll))
listFile.close()
print("====== End reptile ======")
######################################################################################

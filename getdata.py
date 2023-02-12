from flask import Flask,render_template,request
import requests,json
import os
import os
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

app = Flask(__name__)

@app.route('/', methods=('GET', 'POST'))
def e1():
    if request.method == 'POST':
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        api_key="your api key"
        api_service_name = "youtube"
        api_version = "v3"

        # Get credentials and create an API client
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=api_key)

        req = youtube.search().list(
            part="snippet",
            maxResults=9,
            q=request.form['search'],
            order=request.form['order'],
            type="video"
        )
        response = req.execute()
        # print(response)
        
        resTitle=[]
        resDesc=[]
        resTag=[]
        for i in response["items"]:
            resTitle.append(i["snippet"]["title"])
            resDesc.append(i["snippet"]["description"])
            req=requests.get("https://www.googleapis.com/youtube/v3/videos?key="+api_key+"&fields=items(snippet(tags))&part=snippet&id="+i["id"]["videoId"])
            vid=json.loads(req.content)
            if 'tags' in vid["items"][0]["snippet"]:
                resTag.append(list(vid["items"][0]["snippet"]["tags"])) 
        #############################################

        tagss=resTag

        d={}
        for i in range(len(tagss)):
            for j in range(len(tagss[i])):
                d[tagss[i][j]]=0

        for i in range(len(tagss)):
            for j in range(len(tagss[i])):
                d[tagss[i][j]]+=1

        d1=[]
        sorted_x = sorted(d.items(), key=lambda kv: kv[1])
        for i in range(len(sorted_x)-1,0,-1):
            d1.append(sorted_x[i])

        txt=[]
        for i in range(len(tagss)):
            for j in range(len(tagss[i])):
                s=tagss[i][j].split(" ")
                for k in s:
                    txt.append(k)
        # print(txt)

        dtxt={}
        for i in range(len(txt)):
            dtxt[txt[i]]=0
        
        for i in range(len(txt)):
            dtxt[txt[i]]+=1

        dd=[]
        sorted_x = sorted(dtxt.items(), key=lambda kv: kv[1])
        for i in range(len(sorted_x)-1,0,-1):
            dd.append(sorted_x[i])
        ################################################
        return render_template("frontend.html",titles=resTitle,descriptions=resDesc,tags=resTag,d1I=d1,ddI=dd)

    return render_template("frontend.html",titles="",descriptions="",tags="",d1I="",ddI="")
import requests
from server import conf
import database

ANILIST_USER_ID = 5964458
MEDIA_TYPE = "anime"   # anime or manga

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0"
}

data1 = {
    "query": "query($userId:Int,$userName:String,$type:MediaType){MediaListCollection(userId:$userId,userName:$userName,type:$type){lists{name isCustomList isCompletedList:isSplitCompletedList entries{...mediaListEntry}}user{id name avatar{large}mediaListOptions{scoreFormat rowOrder animeList{sectionOrder customLists splitCompletedSectionByFormat theme}mangaList{sectionOrder customLists splitCompletedSectionByFormat theme}}}}}fragment mediaListEntry on MediaList{id mediaId status score progress progressVolumes repeat priority private hiddenFromStatusLists customLists advancedScores notes updatedAt startedAt{year month day}completedAt{year month day}media{id title{userPreferred romaji english native}coverImage{extraLarge large}type format status(version:2)episodes volumes chapters averageScore popularity isAdult countryOfOrigin genres bannerImage startDate{year month day}}}",
    "variables": {"userId": ANILIST_USER_ID, "type": f"{MEDIA_TYPE.upper()}"},
}
response = requests.post(
    "https://graphql.anilist.co", headers=headers, json=data1
)
rj = response.json()

feeds = []

types = ["completed", "watching", "dropped", "planning", "paused"]

for i in rj["data"]["MediaListCollection"]["lists"]:
    if MEDIA_TYPE == "anime":
        for _ in range(4):
            for item in rj["data"]["MediaListCollection"]["lists"][_]["entries"]:
                dict_ = {}
                print(item)
                dict_["title"] = item["media"]["title"]["english"]
                if item["media"]["title"]["english"] is None:
                    dict_["title"] = item["media"]["title"]["romaji"]
                dict_["media_id"] = item["mediaId"]
                dict_["status"] = item["status"].lower()
                dict_["score"] = item["score"]
                dict_["progress"] = item["progress"]
                if MEDIA_TYPE == "anime":
                    dict_["total"] = item["media"]["episodes"]
                elif MEDIA_TYPE == "manga":
                    dict_["total"] = item["media"]["chapters"]
                dict_["image"] = item["media"]["coverImage"]["large"]
                dict_["notes"] = ""
                dict_["isAdult"] = item["media"]["isAdult"]
                feeds.append(dict_)
                print(dict_)
    elif MEDIA_TYPE == "manga":
        for _ in range(4):
            for item in rj["data"]["MediaListCollection"]["lists"][_]["entries"]:
                dict_ = {}
                print(item)
                dict_["title"] = item["media"]["title"]["english"]
                if item["media"]["title"]["english"] is None:
                    dict_["title"] = item["media"]["title"]["romaji"]
                dict_["media_id"] = item["mediaId"]
                dict_["status"] = item["status"].lower()
                dict_["score"] = item["score"]
                dict_["progress"] = item["progressVolumes"]
                if MEDIA_TYPE == "anime":
                    dict_["total"] = item["media"]["episodes"]
                elif MEDIA_TYPE == "manga":
                    dict_["total"] = item["media"]["chapters"]
                dict_["image"] = item["media"]["coverImage"]["large"]
                dict_["notes"] = ""
                dict_["isAdult"] = item["media"]["isAdult"]
                feeds.append(dict_)
                print(dict_)

for x in feeds:
    print(x)
    database.xenylist.initiate()
    database.xenylist.add_media(MEDIA_TYPE, x['title'], x['media_id'], x['status'], x['score'], x['progress'], x['total'], x['image'], x['notes'], x['isAdult'])


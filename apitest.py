import requests
import json


api_key = ""
api_secret = ""
face_set_token = ""
cur_face = []
facetable = {}
debug = False


if debug:
    api_key = "Ydwy6NbL5aIFUKzCHw1rTaKKLR9FhFi9"
    api_secret = "A7yzxG2uAz6-qoiFEaARNoKQ1IYxeJx5"
    face_set_token = "0b5377515fb5ad4b7675b2198d7df62e"
    cur_face = [
        "95d74bdd9ef1261aa62b8cfb3b4c8d20",
        "7c7784f6da841c6d88e416dbd064b61a",
        "2a0b532a191912f6d305d4342b16e028"
    ]
    facetable = {
        "7c7784f6da841c6d88e416dbd064b61a": "Zheng Yang",
        "95d74bdd9ef1261aa62b8cfb3b4c8d20": "Mingyu Liang",
        "2a0b532a191912f6d305d4342b16e028": "Guangli Peng"
    }
else:
    api_key = "lR-9MWp_bEhjwM0vFJH_kUZQE3iz8YMJ"
    api_secret = "Sza524ezHL0Wu66LCutFvp1l5LmlamDB"
    face_set_token = "4fd81ee2f881be369fc0fc26d8cb07fb"
    cur_face = [
        "fadd954074d00b733e29493c6feb1e1d",
        "fa9cc66c3a581baba8e88596e823e6cc",
        "235b4f68f403e9f4b9248474e0ec919d"
    ]
    facetable = {
        "fadd954074d00b733e29493c6feb1e1d": "Zheng Yang",
        "fa9cc66c3a581baba8e88596e823e6cc": "Guangli Peng",
        "235b4f68f403e9f4b9248474e0ec919d": "Mingyu Liang"
    }

def cmp_face(file1, file2):
    url = "https://api-cn.faceplusplus.com/facepp/v3/compare"

    files = {
        'image_file1': ('file1', open(file1, 'rb'), 'image/jpg', {'Expires': '0'}),
        'image_file2': ('file2', open(file1, 'rb'), 'image/jpg', {'Expires': '0'})
    }
    data = {
        'api_key': api_key,
        'api_secret': api_secret
    }
    r = requests.post(url, files=files, data=data)
    ret = json.loads(r.text)
    print "confidence: {}".format(ret["confidence"])


def build_face_set():
    url = "https://api-cn.faceplusplus.com/facepp/v3/faceset/create"
    data = {
        'api_key': api_key,
        'api_secret': api_secret
    }
    r = requests.post(url, data=data)
    print r.text

def detect_fact(file):
    url = "https://api-cn.faceplusplus.com/facepp/v3/detect"
    data = {
        'api_key': api_key,
        'api_secret': api_secret
    }
    files = {
        'image_file': ('file1', open(file, 'rb'), 'image/jpg', {'Expires': '0'})
    }
    r = requests.post(url, files=files, data=data)
    print r.text


def add_face_to_set(faces):
    url = "https://api-cn.faceplusplus.com/facepp/v3/faceset/addface"
    data = {
        'api_key': api_key,
        'api_secret': api_secret,
        'faceset_token': face_set_token,
        'face_tokens': ",".join(faces)
    }
    r = requests.post(url, data=data)
    print r.text

def search_face(file):
    url = "https://api-cn.faceplusplus.com/facepp/v3/search"
    data = {
        'api_key': api_key,
        'api_secret': api_secret,
        'faceset_token': face_set_token,
    }
    files = {
        'image_file': ('file1', open(file, 'rb'), 'image/jpg', {'Expires': '0'})
    }
    r = requests.post(url, files=files, data=data)
    ret = json.loads(r.text)
    # print ret
    try:
        thresholds = ret["thresholds"]
        for res in ret['results']:
            if res["confidence"] < thresholds['1e-3']:
                print "Stranger is detected"
            elif res["confidence"] < thresholds['1e-4']:
                print "{} is detected".format(facetable[res["face_token"]])
            else :
                print "{} is highly detected".format(facetable[res["face_token"]])
    except KeyError as err:
        print ret
        print "No face is detected"
     #print "{} is detected with {}".format(ret["thresholds"])

if __name__ == "__main__":
    search_face("./uploads/1.jpg")
    # add_face_to_set(cur_face)
    # detect_fact("./uploads/yz.jpg")
    # detect_fact("./uploads/pgl.jpg")
    # detect_fact("./uploads/lmy.jpg")
    # cmp_face("./uploads/1.jpg", "./uploads/5.jpg")
    # build_face_set()
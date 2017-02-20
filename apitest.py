import requests

def test():
    url = "https://api-cn.faceplusplus.com/facepp/v3/compare"
    api_key = "Ydwy6NbL5aIFUKzCHw1rTaKKLR9FhFi9"
    api_secret = "A7yzxG2uAz6-qoiFEaARNoKQ1IYxeJx5"
    files = {
        'image_file1': ('file1', open("./uploads/1.jpg", 'rb'), 'image/jpg', {'Expires': '0'}),
        'image_file2': ('file2', open("./uploads/2.jpg", 'rb'), 'image/jpg', {'Expires': '0'})
    }
    data = {
        'api_key' : api_key,
        'api_secret' : api_secret
    }
    r = requests.post(url, files=files, data= data)
    print r.text

if __name__ == "__main__":
    test()
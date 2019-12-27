import requests
url = "https://tcc.taobao.com/cc/json/mobile_tel_segment.htm?"
parameter_dict = {"tel":17764591649}
r = requests.get(url, headers={}, params=parameter_dict)
print(r.text)
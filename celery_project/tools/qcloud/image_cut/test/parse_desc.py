# coding=utf-8
import requests
import re

desc = 'http://dsc.taobaocdn.com/i6/530/131/536139663070/TB1QJyGPpXXXXcnXVXX8qtpFXlX.desc%7Cvar%5Edesc%3Bsign%5Ee068e613625da70fdd91c12c82ade062%3Blang%5Egbk%3Bt%5E1486490191'
desc = 'http://dsc.taobaocdn.com/i6/531/190/539195036509/TB14ey2PpXXXXacXXXX8qtpFXlX.desc%7Cvar%5Edesc%3Bsign%5E1bf754abefba938484e46b5a0ab3d07d%3Blang%5Egbk%3Bt%5E1486490262'
desc = 'http://dsc.taobaocdn.com/i5/530/481/537488383098/TB1s19HPpXXXXa0XVXX8qtpFXlX.desc%7Cvar%5Edesc%3Bsign%5E125ad8c80d546d78ec21117194c1839e%3Blang%5Egbk%3Bt%5E1486490224'
r = requests.get(desc)

image_list = re.findall(r"<img.*?>", r.text, re.M)
for image in image_list:
    # print image
    m = re.match(r".*src=[\'|\"](.*\.jpg)[\'|\"]", image)

    if m is not None:
        print m.group(1)

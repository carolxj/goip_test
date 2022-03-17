import hashlib
import requests
import json
import logging
from Crypto.Cipher import ARC4, AES

def calc_client_session(username, password, cnonce, url_resource):
    m = hashlib.md5()
    m.update(username.encode())
    m.update(password.encode())
    m.update(cnonce.encode())
    m.update(url_resource.encode())
    print(m.hexdigest())
    return m.hexdigest()

def calc_req_auth(username, password, server_session, url_resource, seq):
    m = hashlib.md5()
    m.update(username.encode())
    m.update(password.encode())
    m.update(server_session.encode())
    m.update(str(seq).encode())
    m.update(url_resource.encode())
    return m.hexdigest()

def calc_key(username, password, client_session, server_session, seq):
    m = hashlib.md5()
    m.update(username.encode())
    m.update(password.encode())
    m.update(client_session.encode())
    m.update(server_session.encode())
    m.update(str(seq).encode())
    return m.hexdigest()

def rc4_enc(key, data):
    cipher = ARC4.new(key.encode())
    return cipher.encrypt(data.encode())

def aes_ecb_enc(key, data):
    bs = AES.block_size
    pad = lambda s: s + b"\0" * (bs - len(s) % bs)
    cipher = AES.new(key.encode(), AES.MODE_ECB)
    return cipher.encrypt(pad(data.encode()))

logging.info("#############################test start###########################")

username = "root"
password = "root"
expires = 60
cnonce = "123456"
url = "http://192.168.1.57"
url_resource = "/crypt_sess.json"

client_session = calc_client_session(username, password, cnonce, url_resource)
print('clitnt_session')
crypt_params = {
        'username': username,
        'cnonce': cnonce,
        'expires': expires,
        'auth': client_session,
        'crypt': 'aes-ecb'
        }
requests_addr = url + url_resource
req = requests.get(requests_addr, params=crypt_params)
response = req.json()
logging.info(requests_addr)

print(response)

if response['code'] != 0:
    print(response['desc'])
    exit(1)

server_session = response['session']
expires = response['expires']

seq = 10
url_resource = "/goip_remove_sms.html"
body = '{"tids":[0]}'
auth = calc_req_auth(username, password, server_session, url_resource, seq)
key = calc_key(username, password, client_session, server_session, seq)
#data = rc4_enc(key, body)
data = aes_ecb_enc(key, body)

params = {
        'session': server_session,
        'seq': seq,
        'auth': auth
        }
req = requests.post(url + "/goip_remove_sms.html", params=params, data=data)
print(params,data)
response = req.json()
print(response)

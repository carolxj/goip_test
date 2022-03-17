import sys,os
import urllib.request
import urllib.error
import urllib.parse
import json
import time

url_path = "/goform/goform_set_cmd_process?goformId=setDeviceConfig&configOption=setFirstMnc&save=1&admin=admin&pwd=admin"
host = "192.168.40.1:9090"
delay_time = 5*60

def usage():
  print("Usage:", sys.argv[0], "[delay_time [host]]\n")
  
def sendUrl(url, tmo=30):
  try:
    html = urllib.request.urlopen(url, timeout=tmo)
    hcode = html.getcode()
    
    rspdat = html.read().decode("utf-8")
    print("response data: " + rspdat)
    
    rspjson = json.loads(rspdat)
    jcode = rspjson["resultdd"]
    if (0 == jcode):
      print("response OK!")
    else:
      print("response error:", jcode)
    
  except urllib.error.URLError as e:
    print(e.reason)
    
  except json.decoder.JSONDecodeError:
    print("json decode error!")
    
  except:
    print("unkonw exception!")

usage()

if (len(sys.argv) > 1):
  delay_time = int(sys.argv[1])
  
if (len(sys.argv) > 2):
  host = sys.argv[2]

print("Delay time:", delay_time)
print("Host:", host)

print("\nPrint any key to continue?")
os.system("pause")

operators = ["46000", "46001", "46003"]
test_cnt = 0

while True:
  operator = operators[test_cnt % len(operators)]
  url = "http://" + host + url_path + "&configValue=" + operator;
  
  print("\nSwitch to operator[%s] %d..." %(operator, test_cnt+1))
  print(url)
  sendUrl(url, 30)
  
  time.sleep(delay_time)
  test_cnt += 1
  
os.system("pause")

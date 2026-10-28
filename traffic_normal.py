import random, time, urllib.request

URL = "http://127.0.0.1:8080/"
DURATION = 180  # seconds

end = time.time() + DURATION
count = 0
while time.time() < end:
    try:
        urllib.request.urlopen(URL, timeout=3).read()
        count += 1
    except Exception as e:
        print("err", e)
    time.sleep(random.uniform(0.2, 2.0))
print("done, requests:", count)

import threading, time, urllib.request

URL = "http://127.0.0.1:8080/"
THREADS = 20
DURATION = 20  # seconds, keep short

def worker(end):
    while time.time() < end:
        try:
            urllib.request.urlopen(URL, timeout=2).read()
        except Exception:
            pass

end = time.time() + DURATION
ts = [threading.Thread(target=worker, args=(end,)) for _ in range(THREADS)]
[t.start() for t in ts]
[t.join() for t in ts]
print("http flood done")

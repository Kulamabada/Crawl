import queue
import urllib.request as rq
import re
import threading as th

def url_na_tekst(url):
    try: tekst = rq.urlopen(url)
    except: return ''
    else: return ''.join([linia.decode("utf-8") for linia in tekst])

def licznik(tekst): return tekst.count('Python')

def pom(url, distance, action, linki, wynik):
    linki.put(url)
    tekst = url_na_tekst(url)
    wynik.put((url, action(tekst)))
    if distance == 0: return
    links = re.findall(r"\<a.*href=\"http[^\"]*\"", tekst)
    for link in links:
        link = re.findall(r"\"http[^\"]*\"", link)[0].replace("\"", "")
        if link[-1] != '/': link += '/'
        if link not in linki.queue:
            t = th.Thread(target = pom, args = (link, distance - 1, action, linki, wynik))
            t.start()

def crawl(url, distance, action):
    linki = queue.Queue()
    wynik = queue.Queue()
    pom(url, distance, action, linki, wynik)
    return wynik

result = crawl("https://zapisy.ii.uni.wroc.pl/", 2, licznik)

count = 0
suma = 0

while True:
    try:
        url, res = result.get(True, 3)
        print(url, ":", res)
        count += 1
        suma += res
    except queue.Empty:
        break

print(count)
print("suma =", suma)

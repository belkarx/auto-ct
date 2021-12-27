def getInfo(soup):
    info = soup.findAll('div',attrs={'class':'info'})
    data = ""

    for x in info:
        for y in x.findAll('p'):
            data += str(y)
    data = [x.lstrip() for x in data.splitlines()[1::2]]

    days = data[::2]
    info = data[1::2]

    d = {x:y for x, y in zip(days, info)}
    return d

def getRest(soup):
    rest = []
    info = getInfo(soup)
    for x in info:
        if 'REST' in info[x]:
            rest.append(x.capitalize())
    return rest

#util
def getLinks(soup):
    links = soup.findAll('div',attrs={'class':'videos'})

    a = []
    p = ""
    for x in links:
        b = x.findAll('a')
        d = x.findAll('p')
        for y in b:
            a.append(y['href'])
        for y in d:
            p += str(y)

    p = [x.lstrip() for x in p.splitlines()[1::2]]
    links = {x:y for x, y in zip(p, a)}
    return links

#util for synthepsWC
def getEps(soup):
    data = ""
    videos = soup.findAll('div',attrs={'class':'videos'})
    for x in videos:
        a = x.findAll('a')
        for y in a:
            video = y.findAll('div',attrs={'class':'video'})
            for z in video:
                data += str(z.findAll('p'))
    data = [x.lstrip() for x in data.splitlines()[1::2]]
    return data
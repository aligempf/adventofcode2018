import urllib2

class InputValueReceiver:

    def __init__(self, url="", fileLocation="", args=[]):
        if not url and not args and not fileLocation:
            raise NameError
        if url:
            with open("cookie_values.txt") as cookieFile:
                cookies = cookieFile.readline()[:-1]
            opener = urllib2.build_opener()
            opener.addheaders.append(("Cookie", cookies))
            rawInputValues = opener.open(url).read().split("\n")
        elif fileLocation:
            with open(fileLocation) as fin:
                rawInputValues = fin.read().split("\n")
        elif args:
            rawInputValues = args

        intInputValues = map(self.safeInt, rawInputValues)
        self.inputValues = filter(lambda a: not a is None, intInputValues)

    def safeInt(self, a):
        try:
            return int(a)
        except:
            pass

import urllib2

def safeInt(a):
    try:
        return int(a)
    except:
        return None

def safeString(a):
    try:
        return str(a)
    except:
        return None

class InputValueReceiver:

    def __init__(self, url="", fileLocation="", args=[], sanitiser=safeString):
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

        self.inputValues = self.sanitiseInput(rawInputValues, sanitiser)

    def sanitiseInput(self, rawInputValues, sanitiser):
        # sanitiser is a function that returns the input in the correct type if valid
        # or None if invalid, taking in a single parameter
        sanitisedInputValues = map(sanitiser, rawInputValues)
        return filter(lambda a: not a is None, sanitisedInputValues)

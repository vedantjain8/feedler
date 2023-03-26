def cleanString(s):
    import re
    r = re.sub(r'[^\w]', ' ', s)
    s = re.sub(' +', ' ', r)
    return str(s)

def listToString(s):
    str1 = ""
    for ele in s:
        str1 += ele
    return str(str1)
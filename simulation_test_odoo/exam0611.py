# exo 1

def mot_le_plus_long(phrase):
    phrase = phrase.split()
    longueur = 0
    result = ''

    for word in phrase:
        new = ""
        for letter in word:
            if 97 <= ord(letter) <= 122 or 65 <= ord(letter) <= 90 or 48 <= ord(letter) <= 57:
            # if 'a' <= letter <= 'z' or 'A' <= letter <= 'Z' or '0' <= letter <= '9':
                new += letter
            else:
                letter = ""
        if len(new) > longueur:
            longueur = len(new)
            result = new
    return result

# print(mot_le_plus_long("le chat&!! dort"))
# print(mot_le_plus_long("Python est génial !!!"))


# exo 2

def lettres_encadrees(s):
    patern = "+"
    res = "true"
    if s[0] != patern:
        return "false"
    for i,char in enumerate(s):
        if char != patern:
            if s[i-1] and s[i+1] == patern:
                res = "true"
                continue
            else:
                return "false"
    return res

# print(lettres_encadrees("++a+b+"))
# print(lettres_encadrees("+d+=+s+"))
# print(lettres_encadrees("f++d+"))


# exo 3

def intersection(tab):
    t1,t2  = tab
    t1 = t1.split(", ")
    t2 = t2.split(", ")
    res = []
    for i in t1:
        if i not in res and i in t2:
            res.append(i)
    for i in t2:
        if i not in res and i in t1:
            res.append(t2[i])
    return ",".join(res)

# print(intersection(["1, 3, 9, 10, 17, 18", "1, 4, 9, 10"]))
# print(intersection(["1, 3, 4, 7, 13", "1, 2, 4, 13, 15"]))


#exo 4



#exo 5

def compresser(s):
    pass
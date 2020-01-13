import re

str = "ist    fällig"

#Search for a sequence that starts with "he", followed by two (any) characters, and an "o":

x = re.search("ist *f[ä,a]e?llig", str)
print(x)
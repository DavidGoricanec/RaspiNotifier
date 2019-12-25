import re

str = "Prüfung"

#Search for a sequence that starts with "he", followed by two (any) characters, and an "o":

x = re.search("Pr[ü,u]e?fung", str)
print(x)
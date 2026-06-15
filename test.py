import re



pattern=re.compile(r"^(((?!25?[6-9])[12]\d|[1-9])?\d\.?\b){4}$")


print(pattern.match("a"))
print(pattern.match("0.0.0.0"))
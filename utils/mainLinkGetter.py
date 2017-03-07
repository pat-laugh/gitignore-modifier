import sys, re

p = re.compile(r'([^.]*)\.gitignore')

for line in sys.stdin:
    m = p.match(line)
    if (m):
        s = m.group(1)
        print("'%s' : '%s'," % (s.lower(), s))
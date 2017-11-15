from lxml import html
from urllib import urlencode
import requests,re,sys

QUERY_TYPES = [{'type': 'displayname', 'name': 'Display Name', 'short': 'name'}, 
        {'type': 'email', 'name': 'Email', 'short': 'email'},
        {'type': 'email', 'name': 'Net-ID', 'convert': lambda x: x + \
            '@utdallas.edu', 'short': 'net-ID'}]


def getStandings(name, dirType):
    base = 'http://www.utdallas.edu/directory/includes/directories.class.php?'
    query = {'dirType': dirType, 'dirSearch': name, 'dirMajor': 'CS'}

    page = requests.get(base + urlencode(query))
    tree = html.fromstring(page.content)

    names = tree.xpath('//*[@id="page1"]/h5/text()')
    standings = [s.split(',')[0] for s in tree.xpath(
        '//*[@id="page1"]/p/text()[1]')]

    res = [[names[i], standings[i]] for i in range(len(names))]
    return res

print('Select search parameter type: ')
for i in range(len(QUERY_TYPES)):
    print('  (' + str(i + 1) + ') ' + QUERY_TYPES[i]['name'])

error = 'Please input valid number from 1 to ' + str(len(QUERY_TYPES))
num = -1
while num == -1:
    try:
        num = int(raw_input())
        if num < 1 or num > len(QUERY_TYPES):
            print(error)
            num = -1
        else:
            num -= 1
    except:
        print(error)


sys.stdout.write('Input ' + QUERY_TYPES[num]['short'] + \
        's (separated by commas): ')

result = []
for n in re.split(r'\s*,\s*', raw_input()):
    if 'convert' in QUERY_TYPES[num]:
        n = QUERY_TYPES[num]['convert'](n)
    result += getStandings(n, QUERY_TYPES[num]['type'])

for r in sorted(result, key=lambda x: x[0]):
    print(r[0] + ": " + r[1])



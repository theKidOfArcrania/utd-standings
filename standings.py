from lxml import html
from urllib import urlencode
import requests,re,sys

def getStandings(name):
    base = 'http://www.utdallas.edu/directory/includes/directories.class.php?'
    query = {'dirType': 'displayname', 'dirSearch': name, 'dirMajor': 'CS'}

    page = requests.get(base + urlencode(query))
    tree = html.fromstring(page.content)

    names = tree.xpath('//*[@id="page1"]/h5/text()')
    standings = [s.split(',')[0] for s in tree.xpath(
        '//*[@id="page1"]/p/text()[1]')]

    res = [[names[i], standings[i]] for i in range(len(names))]
    return res

sys.stdout.write('Input names (separated by commas): ')

result = []
for n in re.split(r'\s*,\s*', raw_input()):
    result += getStandings(n)


for r in sorted(result, key=lambda x: x[0]):
    print(r[0] + ": " + r[1])



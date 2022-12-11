import os,re

if not os.path.isdir('new'):
    os.makedirs('new')

def gethtmldirs():
    return filter(lambda i:i.endswith('.html')or
                         i.endswith('.htm'),
                  os.listdir('.'))

def addstatic(htmlname):
    with open(htmlname) as f:
        s = f.read()
        if len(re.findall('{% load static %}',s))==0:
            s = '{% load static %}\n'+s
        s = re.sub(r'((src|href)=)(")([^":]+?\.)(css|js|png|jpg|gif)(")','''\g<1>\g<3>{% static "\g<4>\g<5>" %}\g<6>''',s)
        s = re.sub(r'((src|href)=)(")([^":]+?\.)(css|js|png|jpg|gif)(\?[^"/]+?)(")','''\g<1>\g<3>{% static "\g<4>\g<5>" %}{{data|default:'\g<6>'}}\g<7>''',s)
        with open('new/'+htmlname,'w') as t:
            t.write(s)

if __name__ == '__main__':
    for htmlname in gethtmldirs():
        addstatic(htmlname)

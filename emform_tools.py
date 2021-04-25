import json

def clean_unicode(umsg):
    s = ''

    inquote = False
    for c in umsg:
        ucode = ord(c)
        if (ucode > 128):
            s += hex(ucode) +';'
        elif c == '"':
            inquote = not inquote
            s += c
        elif (c == '\n') and inquote:
            s += "\\n"
        else:
            s += c
    return s

def read_form(form_file, verbose=False):

    f = open(form_file, encoding='utf-8', mode='r')
    jsontxt = f.read()
    f.close()

    clean_txt = clean_unicode(jsontxt)

    # print("Debug: emform_tools.py: clean_txt=", clean_txt)

    if verbose:
        print(clean_txt)

    d = json.loads(clean_txt)

    return d

if __name__ == '__main__':
    txtdict = read_form("student.json", True)
    print('Dict=', txtdict)
    print("\n\ntxtdict['FE0']=", txtdict["FE0"])
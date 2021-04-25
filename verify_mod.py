"""
Verification module version 2 (Apr 24th, 2021).
"""

codefile = 'codebook.csv'


def verify(id, verf_code, codebook):
    '''
    :param id: string of id, e.g., kubo@memory.com
    :param verf_code: string of verification code, e.g., x!9876A3$5%
    :param codebook: function mapping id to correct verf_code
    :return: True/False
    '''

    found = codebook(id)
    if found is None:
        print('verify: id {} is not in the codebook.'.format(id))
        return False

    _, cvc = found.split()

    verf_bool = False
    if cvc is not None:
        verf_bool = (verf_code.strip() == cvc.strip())

    # print("codebookf: result=", verf_bool)
    return verf_bool


def codebookf(txtin):
    global codefile

    vcode = None

    with open(codefile, 'r') as f:
        for line in f:
            email, code1, code2 = line.split(',')
            if email.strip() == txtin:
                vcode =  code1.strip() + ' ' + code2.strip()
                break

    return vcode


def read_student_verf(verf_file):

    student_vcode = None
    with open(verf_file, 'r') as f:
        student_vcode = f.read()

    return student_vcode


if __name__ == '__main__':

    ids = ['tatpong@kku.ac.th', 'tatpong@gmail.com', 'jitti.s@kkumail.com',
            'kroek@kkumail.com', 'don_art@kkumail.com', 'IamNew@nowhere.com']
    codes = ["4601", "2686", "7045", "1246", "3101"]

    for id in ids:
        for c in codes:
            print(id, ': c=', c, "check=", verify(id, c, codebookf))

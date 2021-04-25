"""
Predecessor: grading_policy3.py (from LCA 2019)
Crated: Dec 26th, 2020
Updated: Apr 21st, 2021 
    * fix is_number for cases: 2 vs 2. vs 2.0, so that "line 2." does not match "line 2"
For: unifying the autograder. This policy handles numerical answers
with specified tolerance.
"""

import re

def find_diff(txt1, txt2):
    pos = -1
    N1 = len(txt1)
    N2 = len(txt2)
    N = N1

    if N1 != N2:
        N = min(N1, N2)
        pos = N

    # Search for difference
    align_emph = ''

    for i in range(N):

        if txt1[i] != txt2[i]:
            pos = i

            break

        align_emph += '_'

    align_emph += '#'
    alpha1 = (None, -1)
    if pos < N1:
        alpha1 = (txt1[pos], ord(txt1[pos]))

    alpha2 = (None, -1)
    if pos < N2:
        alpha2 = (txt2[pos], ord(txt2[pos]))


    return pos, alpha1, alpha2, align_emph


def is_number(txt):
    '''
    :param txt: e.g., 'Q1', '23', '25.0', '28j', '30.5j'
    :return:
        None for textual string
        number (without j) for a number
        e.g., 'Q1' -> None, '23' -> 23, '25.0' -> 25.0,
            '28j' -> 28, '30.5j' -> 30.5
    '''
    # r = re.match('-?[0-9]+\.?[0-9]*j?', txt)
    r = re.match('-?[0-9]+\.?[0-9]+j?', txt)  # fix case of 2. vs 2 vs 2.0

    found = False
    if r:

        # Found match
        sb, se = r.span(0)

        if se < ( len(txt) ):

            # It does not match to the end, e.g., 152A
            # So, this does not count
            found = False
        else:

            # It matches to the end, e.g., 200 or 150j
            found = True

    return found


def compare_num(snum1, snum2, tol):
    # BREAK HERE
    # number term

    if snum1[-1] != 'j' and snum2[-1] != 'j':

        # Real numbers
        diff = float(snum1) - float(snum2)

    elif snum1[-1] == 'j' and snum2[-1] == 'j':

        # Imaginary numbers
        diff = float(snum1[:-1]) - float(snum2[:-1])

    else:

        # One is real. Another is imaginary.
        return False

    if -tol < diff < tol:
        return True

    return False

def rev_chunk(txt, i):
    striped = txt.strip()
    sep_positions = [-1] + [i for i in range(len(striped)) if striped[i] == ' ']
    chunk_pos = sep_positions[i] + 1
    return chunk_pos

def check_answer(txtline1, txtline2, ntol):

    details = {'diff_emph': '', 'pos': '', 'a1': '', 'a2': ''}

    # Text match
    is_matched = (txtline1 == txtline2)
    if is_matched:
        return True, details

    # Breaking a line to chucks
    TL1 = txtline1.split()
    TL2 = txtline2.split()
    N1 = len(TL1)
    N2 = len(TL2)

    txt_offset = 0
    a1 = ''
    a2 = ''
    emph = '#'

    if N1 != N2: # different numbers of chucks
        # Find difference
        N = min(N1, N2)
        pos = N
        for i in range(N):
            if TL1[i] != TL2[i]:
                if is_number(TL1[i]) and is_number(TL2[i]):
                    is_matched = compare_num(TL1[i], TL2[i], ntol)
                    if not is_matched:
                        pos = i
                        a1 = TL1[i]
                        a2 = TL2[i]
                        emph = '#'*len(TL1[i])
                        break
                else:
                    pos = i
                    a1 = TL1[i]
                    a2 = TL2[i]
                    emph = '#' * len(TL1[i])
                    break
        #end for i

        txt_pos = len(txtline1)
        if pos < N:
            txt_pos = rev_chunk(txtline1, pos)

        elif N1 > N2:
            a1 = TL1[pos]
            emph = '#' * len(TL1[pos])
            txt_pos = rev_chunk(txtline1, pos)

        else:
            a2 = TL2[pos]

        # end if

        details['diff_emph'] = "_" * txt_pos + emph
        details['pos'] = txt_pos
        details['a1'] = a1
        details['a2'] = a2

        return False, details

    # end if N1 != N2

    # Check every term for numbers of chunks are matched
    is_matched = True
    pos = 0

    for i in range(N1):

        if is_number(TL1[i]) and is_number(TL2[i]):

            is_matched = compare_num(TL1[i], TL2[i], ntol)
            if not is_matched:
                pos = i
                a1 = TL1[i]
                a2 = TL2[i]
                emph = '#' * len(TL1[i])
                break

        else:

            # Text term
            if TL1[i] == TL2[i]:
                continue
            else:
                is_matched = False
                pos = i
                txt_offset, a1, a2, emph= find_diff(TL1[i], TL2[i])
                break
            # end if text term
        # end if-else is_number
    # end for i

    txt_pos = rev_chunk(txtline1, pos)
    details['diff_emph'] = '_'* txt_pos + emph * (not is_matched)
    details['pos'] = txt_pos + txt_offset
    details['a1'] = a1
    details['a2'] = a2

    return is_matched, details


if __name__ == '__main__':
    txt1 = 'Test number compare 14.055 and 15.09 on numerical tol with diff ident'
    txt2 = 'Test number compare 14.05 and 15.085 on numerical tol with diff ident'
    match, d = check_answer(txt1, txt2, 0.01)
    print('Case 1: matched')
    print(match)
    print(d)

    txt1 = 'Test number compare 14.2 and 15.09 on numerical tol with diff ident'
    txt2 = 'Test number compare 14.05 and 15.085 on numerical tol with diff ident'
    match, d = check_answer(txt1, txt2, 0.01)
    print('\nCase 2: exceed tol:', match)
    print(txt2)
    print(txt1)
    print(d['diff_emph'])
    print(d['pos'], ': a1=', d['a1'], '; a2=', d['a2'])
    # print(txt1[:d['pos']])

    txt1 = 'Test number compare 14.05555 and 15.09 on numerical tolerance with diff ident'
    txt2 = 'Test number compare 14.05 and 15.085 on numerical tol with diff ident'
    match, d = check_answer(txt1, txt2, 0.01)
    print('\nCase 3: txt unmatch:', match)
    print(txt2)
    print(txt1)
    print(d['diff_emph'])
    print(d['pos'], ': a1=', d['a1'], '; a2=', d['a2'])
    # print(txt1[:d['pos']])

    txt1 = 'Test number compare 14.05 and 15.09 on a numerical tolerance with diff ident'
    txt2 = 'Test number compare 14.05 and 15.085 on numerical tolerance with diff ident'
    match, d = check_answer(txt1, txt2, 0.1)
    print('\nCase 4: different token:', match)
    print(txt2)
    print(txt1)
    print(d['diff_emph'])
    print(d['pos'], ': a1=', d['a1'], '; a2=', d['a2'])
    print(txt1[:d['pos']])


    txt1 = 'That is it.'
    txt2 = "That's it."
    match, d = check_answer(txt1, txt2, 0.1)
    print('\nCase 5: different token:', match)
    print(txt2)
    print(txt1)
    print(d['diff_emph'])
    print(d['pos'], ': a1=', d['a1'], '; a2=', d['a2'])
    print(txt1[:d['pos']])


    txt1 = 'That is it.'
    txt2 = "   That's it."
    match, d = check_answer(txt1, txt2, 0.1)
    print('\nCase 6: leading spaces:', match)
    print(txt2)
    print(txt1)
    print(d['diff_emph'])
    print(d['pos'], ': a1=', d['a1'], '; a2=', d['a2'])
    print(txt1[:d['pos']])

    txt1 = 'That is it'
    txt2 = "That is it ."
    match, d = check_answer(txt1, txt2, 0.1)
    print('\nCase 7: chunk trailing:', match)
    print(txt2)
    print(txt1)
    print(d['diff_emph'])
    print(d['pos'], ': a1=', d['a1'], '; a2=', d['a2'])
    print(txt1[:d['pos']])

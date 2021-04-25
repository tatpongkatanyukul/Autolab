import re
from numgraders import check_answer, find_diff


def clean_whitespace(dirty_text):
    clean_text = re.sub(' +', ' ', dirty_text)
    # remove excessive white spaces
    return clean_text


def clean_newline(dirty_text):
    clean_text = re.sub('\r\r', '\r', dirty_text)
    clean_text = re.sub('\r', '\n', clean_text)

    # to be fixed (need to do it in while loop)
    clean_text = re.sub('\n\n', '\n', clean_text)
    clean_text = re.sub('\n\n', '\n', clean_text)
    clean_text = clean_whitespace(clean_text)

    return clean_text

def trim_ending(dirty_text):
    if len(dirty_text) == 0:
        return dirty_text

    clean_text = dirty_text
    if dirty_text[-1] == '\n':
        clean_text = dirty_text[:-1]

    return clean_text

def numtol_policy(student_out, ref_ans, fullscore, report, attrib):
    tol = float(attrib)

    # Clean texts
    student_out = clean_newline(student_out)
    student_out = trim_ending(student_out)
    student_out = student_out.strip()

    ref_ans = clean_newline(ref_ans)
    ref_ans = trim_ending(ref_ans)
    ref_ans = ref_ans.strip()

    # Grading test_out c.f. gt_ans
    student_lines = student_out.split('\n')
    ref_lines = ref_ans.split('\n')

    Nref = len(ref_lines)
    Nstu = len(student_lines)
    M = min(Nref, Nstu)

    if report == 'Show' or report == 'Silence':
        print('numtol_policy: # reference lines: {}'.format(Nref))
        print('numtol_policy: # submitted lines: {}'.format(Nstu))

    point = 0
    for i in range(M):

        s = student_lines[i].strip()
        r = ref_lines[i].strip()

        match, details = check_answer(s, r, tol)
        if match:
            point += 1

        if report == 'Show':
            print('numtol_policy: details: line', i)
            print('numtol_policy: * reference :', r)
            print('numtol_policy: * student   :', s)

            if not match:
#                pos, a_stu, a_ref, diff_emph = find_diff(student_lines[i], ref_lines[i])
                print('numtol_policy: * difference:', details['diff_emph'])
                print('numtol_policy: * 1st diff (at ', details['pos'],
                      ') stu=', details['a1'],
                      '; ref=', details['a2'], sep='')

    return fullscore * point / Nref


def parline_policy(student_out, ref_ans, fullscore, report):
    # Clean texts
    student_out = clean_newline(student_out)
    student_out = trim_ending(student_out)
    student_out = student_out.strip()

    ref_ans = clean_newline(ref_ans)
    ref_ans = trim_ending(ref_ans)
    ref_ans = ref_ans.strip()

    # Grading test_out c.f. gt_ans
    student_lines = student_out.split('\n')
    ref_lines = ref_ans.split('\n')

    Nref = len(ref_lines)
    Nstudent = len(student_lines)
    M = min(Nref, Nstudent)

    if report == 'Show' or report == 'Silence':
        print('parline_policy: # reference lines: {}'.format(Nref))
        print('parline_policy: # submitted lines: {}'.format(Nstudent))

    point = 0
    for i in range(M):
        match = (student_lines[i] == ref_lines[i])
        if match:
            point += 1

        if report == 'Show':
            print('parline_policy: details: match = ', student_lines[i] == ref_lines[i])
            print('parline_policy: * reference :', ref_lines[i])
            print('parline_policy: * student   :', student_lines[i])

            if not match:
                pos, a_stu, a_ref, diff_emph = find_diff(student_lines[i], ref_lines[i])
                print('parline_policy: * difference:', diff_emph)
                print('parline_policy: * 1st diff (at ', pos,
                      ') stu=', a_stu,
                      '; ref=', a_ref, sep='')


    return fullscore * point / Nref

def exact_policy(student_out, ref_ans, fullscore, report):
    clean_student = clean_newline(student_out)
    clean_ref = clean_newline(ref_ans)

    # Check file in notepad++ with [view] > [show symbol] > [show all characcters]
    # f = open('debug' + Px + 'out.txt', 'w')
    # f.write(clean_student)
    #
    # f = open('debug' + Px + 'gt.txt', 'w')
    # f.write(clean_ref)
    test_score = 0

    if clean_student == clean_ref:
        test_score = fullscore

    if report == 'Show':
        print('exact_policy: match score =', test_score)
        print('exact_policy: * reference:', clean_ref)
        print('exact_policy: * student:', clean_student)

    return test_score

if __name__ == '__main__':
    ref = 'V1 = 24.5 V; I1 = 0.032 A\nV2 = 36.8 V; I2 = -0.150 A'
    outs = []
    outs.append('V1 = 24.5 V; I1 = 0.032 A\nV2 = 36.8 V; I2 = -0.150 A')
    outs.append('V1 = 24.51 V; I1 = 0.031 A\nV2 = 36.8 V; I2 = -0.150 A')
    outs.append('V1 = 24.51 V; I1 = 0.031 A\nV2 = 36.9 V; I2 = -0.149 A')
    outs.append('V1 = 24 V; I1 = 0.031 A\nV2 = 36.9 V; I2 = -0.149 A')
    outs.append('V1 = 24 V; I1 = 0.03 A\nV2 = 37 V; I2 = -0.149 A')
    outs.append('V1 =  V; I1 = 0.03 A\nV2 = 37V; I2 = -0.149 A')

    for i, o in enumerate(outs):
        s1 = numtol_policy(o, ref, 10, "None", "0.05")
        s2 = parline_policy(o, ref, 10, "Show")
        s3 = exact_policy(o, ref, 10, "None")
        print(o)
        print(i, ': numtol={}, parline={}, exact={}'.format(s1, s2, s3))
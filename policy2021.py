import re
from numgraders import check_answer, find_diff
from base_policies import clean_newline, trim_ending


def numtol_policy2(student_out, ref_ans, fullscore, report, attrib, neg_handling=True):
    tol = float(attrib)

    # Clean texts
    student_out = clean_newline(student_out)
    student_out = trim_ending(student_out)
    student_out = student_out.strip()

    ref_ans = clean_newline(ref_ans)
    ref_ans = trim_ending(ref_ans)
    ref_ans = ref_ans.strip()

    if neg_handling:
        # Handling negative sign
        student_out = re.sub("- ", "-", student_out)
        ref_ans = re.sub("- ", "-", ref_ans)

    # Grading test_out c.f. gt_ans
    student_lines = student_out.split('\n')
    ref_lines = ref_ans.split('\n')

    Nref = len(ref_lines)
    Nstu = len(student_lines)
    M = min(Nref, Nstu)

    print('numtol_policy2: report mode', report, '; tol:', tol, '; neg handling:', neg_handling)

    if (report == 'Show') or (report == 'Silence') or (report == 'HidNum'):
        print('numtol_policy2: # reference lines: {}'.format(Nref))
        print('numtol_policy2: # submitted lines: {}'.format(Nstu))

    point = 0
    for i in range(M):

        s = student_lines[i].strip()
        r = ref_lines[i].strip()

        match, details = check_answer(s, r, tol)
        if match:
            point += 1

        if report == 'Show':
            print('numtol_policy2: details: line', i)
            print('numtol_policy2: * reference :', r)
            print('numtol_policy2: * student   :', s)

            if not match:
                pos, a_stu, a_ref, diff_emph = find_diff(student_lines[i], ref_lines[i])
                print('numtol_policy2: * difference:', details['diff_emph'])
                print('numtol_policy2: * 1st diff (at ', details['pos'],
                      ') stu=', details['a1'],
                      '; ref=', details['a2'], sep='')
            ## end if not match

        elif report == 'HidNum':
            print('numtol_policy2: details: line', i)
            print('numtol_policy2: * student   :', s)

            if not match:
                pos, a_stu, a_ref, diff_emph = find_diff(student_lines[i], ref_lines[i])
                print('numtol_policy2: * difference:', details['diff_emph'])
                #print('numtol_policy: * 1st diff (at ', details['pos'],
                #      ') stu=', details['a1'],
                #      '; ref=', details['a2'], sep='')
            ## end if not match

        
        # end if Show elif HidNum



    return fullscore * point / Nref


if __name__ == '__main__':
    ref = 'V1 = 24.5 V; I1 = 0.032 A\nV2 = 36.8 V; I2 = -0.150 A'
    outs = []
    outs.append('V1 = 24.5 V; I1 = 0.032 A\nV2 = 36.8 V; I2 = -0.150 A')
    outs.append('V1 = -24.51 V; I1 = 0.031 A\nV2 = 36.8 V; I2 = -0.150 A')
    outs.append('V1 = - 24.51 V; I1 = 0.031 A\nV2 = 36.9 V; I2 = -0.149 A')
    outs.append('V1 = 24 V; I1 = 0.031 A\nV2 = 36.9 V; I2 = - 0.149 A')
    outs.append('V1 = 24 V; I1 = 0.03 A\nV2 = 37 V; I2 = -0.149 A')
    outs.append('V1 = 24.5 V; I1 = 0.032 A\nV2 = 36.8 V; I2 = - 0.150 A')
    outs.append('V1 = 24.5 V; I1 = 0.032 A\nV2 = 36.8 V; I2 = -0.150 A')
    outs.append('V1 = 24.5 V; I1 = 0.032 A\nV2 = 36.8 V; I2 = 0.150 A')


    print('\n\n')
    for i, o in enumerate(outs):
        s1 = numtol_policy2(o, ref, 10, "Show", "0.05")
        print('----')
        s2 = numtol_policy2(o, ref, 10, "HidNum", "0.05")

        print(o)
        print(i, ': numtol2(none)={}, (hidnum)={}'.format(s1, s2))
        print()
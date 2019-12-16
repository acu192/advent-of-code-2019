val = '59787832768373756387231168493208357132958685401595722881580547807942982606755215622050260150447434057354351694831693219006743316964757503791265077635087624100920933728566402553345683177887856750286696687049868280429551096246424753455988979991314240464573024671106349865911282028233691096263590173174821612903373057506657412723502892841355947605851392899875273008845072145252173808893257256280602945947694349746967468068181317115464342687490991674021875199960420015509224944411706393854801616653278719131946181597488270591684407220339023716074951397669948364079227701367746309535060821396127254992669346065361442252620041911746738651422249005412940728'

offset = int(val[:7])

val = [int(c) for c in val]


REPEAT = 10000


vals_end = [val[i % len(val)] for i in range(offset, len(val) * REPEAT)]

assert len(vals_end) == len(val) * REPEAT - offset


"""
Because the offset is more than half way through the entire list, we can play a trick to make the computation faster
because all the coefficients involved in this part of the list are `1`. Essentially the values in this part of the
list just get summed together, so we can do this cleverly.

The code below is just a hack to only work in this particular case.
"""


def next_phase_hack(vals_end):
    vals_end_next = []

    s = 0

    for v in reversed(vals_end):
        s += v
        vals_end_next.append(int(str(s)[-1]))

    return vals_end_next[::-1]  # reverse it


for i in range(100):
    vals_end = next_phase_hack(vals_end)
    vals_str_8 = ''.join([str(v) for v in vals_end[:8]])
    print('Phase', i+1, ':', vals_str_8)


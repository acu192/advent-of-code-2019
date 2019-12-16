val = '59787832768373756387231168493208357132958685401595722881580547807942982606755215622050260150447434057354351694831693219006743316964757503791265077635087624100920933728566402553345683177887856750286696687049868280429551096246424753455988979991314240464573024671106349865911282028233691096263590173174821612903373057506657412723502892841355947605851392899875273008845072145252173808893257256280602945947694349746967468068181317115464342687490991674021875199960420015509224944411706393854801616653278719131946181597488270591684407220339023716074951397669948364079227701367746309535060821396127254992669346065361442252620041911746738651422249005412940728'
#val = '12345678'
#val = '80871224585914546619083218645595'

offset = int(val[:7])

val = [int(c) for c in val]


REPEAT = 1 # 10000



def pattern(n, length):
    # HARDCODING THE PATTERN TO BE MOST EFFICIENT

    curr_index = n-1   # first 0 patch gets shifted by one to the left

    while curr_index < length:
        for _ in range(n):
            if curr_index < length:
                yield curr_index, 1
            curr_index += 1

        curr_index += n   # skip the zero patch

        for _ in range(n):
            if curr_index < length:
                yield curr_index, -1
            curr_index += 1

        curr_index += n   # skip the zero patch


cache = {}

def calc_digit(phase, pos):
    key = (phase, pos)

    if key in cache:
        return cache[key]

    if phase == 0:
        pos = pos % len(val)
        ans = val[pos]
        cache[key] = ans
        return ans

    pat = pattern(pos+1, len(val) * REPEAT)

    s = 0

    for i, p in pat:
        d = calc_digit(phase-1, i)
        s += d * p

    ans = int(str(s)[-1])
    cache[key] = ans

    return ans


for i in range(8):
    #print(offset+i)
    #d = calc_digit(100, offset+i)
    d = calc_digit(100, i)
    print('got', d)


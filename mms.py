# Original code in JavaScript by HypCos 
# https://github.com/hypcos/notation-explorer/blob/master/MM3.js

import re
import traceback

class Cache:
    def __init__(self):
        self.cache = {}
    def get(self, key):
        return self.cache.get(key)
    def set(self, key, value):
        self.cache[key] = value
    def has(self, key):
        return key in self.cache
    def clear(self):
        self.cache.clear()   

row_indices = Cache()
correspondence = Cache()

def row_index_increase(v, i): #v + ω^i
    c = v.copy()
    while len(c) <= i:
        c.append(0)
    c[i] += 1
    for j in range(i):
        c[j] = 0
    return c

def row_index_compare(a, b):
    if len(a) > len(b):
        return 1
    if len(a) < len(b):
        return -1
    for i in range(len(a) - 1, -1, -1):
        if a[i] > b[i]:
            return 1
        if a[i] < b[i]:
            return -1
    return 0

def get_row_index(m, xy):
    x, y = xy
    if x >= len(m) or x < 0 or y < 0:
        return []
    ri = []
    if row_indices.has(str(m[x])):
        ri = row_indices.get(str(m[x]))
    else:
        for i in range(len(m[x])):
            if not i:
                ri.append([1])
            else:
                j = i
                while j > 0 and extract(m, [x, j - 1]) == extract(m, [x, i]):
                    j -= 1
                ri.append(row_index_increase(ri[i - 1], i - j))
        row_indices.set(str(m[x]), ri)
    if y < len(ri):
        return ri[y]
    lnz = len(ri) - 1
    return row_index_increase(ri[lnz] if lnz >= 0 else [], y - lnz - 1)

def corresponding_entry(m, rx, xy): #In theory I could also omit rx (root x) since you can calculate it from the matrix m, but that would make it unnecessarily complicated...
    x, y = xy
    cs = -1
    if correspondence.has(str([m, xy])):
        cs = correspondence.get(str([m, xy]))
    else:
        if x < rx[0]:
            cs = -1
        elif x == rx[0]:
            cs = y
        else:
            cs = corresponding_entry(m, rx, parent(m, xy))
        correspondence.set(str([m, xy]), cs)
    return cs

def parent_check(m, xy):
    x, y = xy
    if not y:
        return [x - 1, 0]
    else:
        p = parent(m, [x, y - 1])[0]
        i = y
        while extract(m, [p, i]) < extract(m, xy) - 1 or row_index_compare(get_row_index(m, [p, i]), get_row_index(m, xy)) > 0:
            i -= 1
        return [p, i]

def parent(m, xy):
    if not extract(m, xy):
        return [-1, xy[1]]
    xyp = xy
    while extract(m, xyp) != extract(m, xy) - 1:
        xyp = parent_check(m, xyp)
    return xyp

def expand(m, n):
    if str(m).casefold() == 'limit':
        mat = [[], [1]]
        for i in range(n):
            mat[1].append(1)
        return mat
    mat = dcopy(m)
    lnzx = len(m) - 1
    if not zero(m, lnzx): #Is last column non 0?
        lnzy = len(m[lnzx]) - 1
        lnz = extract(m, [lnzx, lnzy])
        root_checks = []
        index = [lnzx, lnzy]
        while index[1] >= 0: #Get root checks
            while extract(m, index) != lnz - 1:
                index = parent(m, index)
            while len(root_checks) <= index[0]:
                root_checks.append([])
            root_checks[index[0]].insert(0, index[1])
            index[1] -= 1
        column_weigths = [1] + [len(column) for column in root_checks]
        if column_weigths[len(column_weigths) - 1] == 1: #Last column with root checks only has 1? Then that's the root
            root = parent(m, [lnzx, lnzy])
        else: #Find the root
            r = len(column_weigths) - 2
            while column_weigths[r] >= column_weigths[len(column_weigths) - 1]:
                r -= 1
            root = [r, root_checks[r][0]]
        w, h = [lnzx - root[0], lnzy - root[1]] #Width and height of bad part
        mat[lnzx][lnzy] -= 1
        for y, val in enumerate(m[root[0]][root[1]:]):
            if lnzy + y < len(mat[lnzx]):    
                mat[lnzx][lnzy + y] = val
            else:
                mat[lnzx].append(val)
        for i in range(1, n + 1): #Actual expansion
            reference = []
            y1, y2 = 0, 0
            while y2 <= root[1] + h * i: #Build reference array
                cmp = row_index_compare(get_row_index(mat, [root[0], y1 + 1]), get_row_index(mat, [root[0] + w * i, y2]))
                if cmp > 0 or y1 >= root[1]:
                    while len(reference) <= y1:
                        reference.append(-1)
                    reference[y1] = y2
                    y2 += 1
                else:
                    y1 += 1
            for dx in range(1, w + 1): #Copy Bad Part and ascend
                x = root[0] + dx
                while len(mat) <= x + w * i:
                    mat.append([])
                target_column = mat[x + w * i] = []
                last_magma = -1
                for y, val in enumerate(mat[x]):
                    asc = corresponding_entry(mat, root, [x, y])
                    if asc >= 0:
                        if asc <= root[1] and not row_index_compare(get_row_index(mat, [root[0], asc]), get_row_index(mat, [x, y])):
                            for j in range((reference[asc - 1] if asc - 1 >= 0 else -1) + 1, reference[asc] + 1):
                                target_column.append(val - extract(mat, [root[0], asc]) + extract(mat, [root[0] + w * i, j]))
                            last_magma = asc
                        else:
                            if last_magma >= 0:
                                target_column.append(val - extract(mat, [root[0], last_magma]) + extract(mat, [root[0] + w * i, reference[last_magma]]))
                            else:
                                target_column.append(val - extract(mat, [root[0], 0]) + extract(mat, [root[0] + w * i, 0]))
                    else:
                        target_column.append(val)
    mat.pop()
    return clean(mat, 0)

def compare_columns(c1, c2):
    col1 = c1.copy()
    col2 = c2.copy()
    col1.append(0)
    col2.append(0)
    for i in range(len(col1)):
        if col1[i] < col2[i]:
            return -1
        if col1[i] > col2[i]:
            return 1
        if col1[i] == col2[i] == 0:
            return 0

def compare(m1, m2):
    if str(m1).casefold() == 'limit':
        if str(m2).casefold() == 'limit':
            return 0
        return 1
    if str(m2).casefold() == 'limit':
        return -1
    mat1 = dcopy(m1)
    mat2 = dcopy(m2)
    mat1.append([-1])
    mat2.append([-1])
    for i in range(len(mat1)):
        if compare_columns(mat1[i], mat2[i]) < 0:
            return -1
        if compare_columns(mat1[i], mat2[i]) > 0:
            return 1
        if compare_columns(mat1[i], mat2[i]) == 0 and mat1[i] == [-1]:
            return 0

def type(m):
    if str(m).casefold() == 'limit':
        return 4 #Notation Limit
    if not len(m):
        return 0 #Zero Ordinal
    prev_col0 = -1
    for col in clean(m, 1):
        if col[0] > prev_col0 + 1:
            return -3 #Nonstandard: some column's first entry is bigger than the previous column's first entry + 1
        prev_col0 = col[0]
        prev_entry = -1
        for entry in col:
            if prev_entry > -1 and entry > prev_entry:
                return -2 #Nonstandard: some column contains entries bigger than the previous one
            prev_entry = entry
    c = 'limit'
    n = 0
    while 1:
        d = expand(c, n)
        cmp = compare(d, m)
        if not cmp:
            return 3 #Subsystem Limit
        elif cmp > 0:
            c = d
            break
        n += 1
    while 1:
        n = 0
        while 1:
            d = expand(c, n)
            cmp = compare(d, m)
            if not cmp:
                if not compare_columns(m[-1], [0]):
                    return 1 #Successor
                return 2 #Limit
            elif cmp > 0:
                c = d
                break
            if len(d) >= len(m) and compare(d[:len(m)], m) < 0:
                return -1 #Nonstandard
            n += 1

def increase_column(c, inc):
    if inc < 1:
        return col
    col = c.copy() 
    while len(col) > 0 and col[-1] < inc:
        col.pop()
    col.append(inc)
    return col  

def mat_to_seq(m):
    if str(m).casefold() == 'limit':
        return [1, 'ω']
    mat = clean(m, 0)
    seq = []
    for i in range(len(mat)):
        if zero(mat, i):
            seq.append(1)
            continue
        sn = 2
        col = [1]
        test = mat[:i]
        while compare_columns(col, mat[i]): # != 0
            col = increase_column(col, 1)
            inc = 2
            while type(test + [col]) < 0:
                col = increase_column(col, inc)
                inc += 1
            sn += 1
        seq.append(sn)
    return seq

def dcopy(m): #Since copy.deepcopy() is slow as f***, I implemented it myself
    cpy = []
    for c in m:
        cpy.append(c.copy())
    return cpy
    
def clean(m, display):
    if str(m).casefold() == 'limit':
        return 'limit'
    mat = dcopy(m)
    for column in mat:
        while len(column) > 0 and column[-1] == 0:
            column.pop()
        if display and column == []:
            column.append(0)
    return mat 

def extract(m, xy):
    x, y = xy
    if x > len(m) - 1 or x < 0 or y < 0:
        return -1
    if y > len(m[x]) - 1:
        return 0
    return m[x][y]
    
def zero(m, x):
    if extract(m, [x, 0]) < 1:
        return 1
    return 0

def string_to_mat(s):
    if s.casefold() == 'limit':
        return s
    rows = re.findall(r'\((.*?)\)', s)
    m = [list(map(int, row.split(',')) if row != '' else []) for row in rows]    
    return m

def mat_to_string(m):
    if str(m).casefold() == 'limit':
        return m
    return ''.join(['(' + ','.join(map(str, row)) + ')' for row in m])

def seq_to_string(s):
    return ','.join([str(e) for e in s])

mode = 0
while 1:
    try:
        if mode == 0:
            mode = int(input('Please select a mode to continue\n\n1: Expand MMS matrix\n2: Convert MMS matrix to MMS sequence\n3: Convert MMS sequence to MMS matrix\n4: Credits\n\nType the mode number and press enter: '))
            if mode > 4 or mode < 1:
                raise Exception
        if mode == 1:
            text = input('\nEnter the MMS matrix to expand\n(type "limit" to expand the limit matrix, type "." to return to mode selection)\n')
            if text == '.':
                mode = 0
                continue
            n = input('\nEnter the number of expansions (leave empty for 5): ')
            if n == '':
                n = 6
            else:
                n = int(n) + 1
            m = clean(string_to_mat(text), 0)
            t = type(m)
            if t < 0:
                print('Matrix type: Nonstandard')
                continue
            if not t:
                print('Matrix type: Zero')
                continue
            if t == 1:
                print('Matrix type: Successor')
                print(mat_to_string(clean(expand(m, 0), 1)))
                continue
            if t == 2:
                print('Matrix type: Limit')
            if t == 3:
                print('Matrix type: Subsystem Limit')
            if t == 4:
                print('Matrix type: Notation Limit')
            for i in range(n):
                print(f'{n}: {mat_to_string(clean(expand(m, i), 1))}')
            print('. . .')
        if mode == 2:
            text = input('\nEnter the MMS matrix to be converted\n(type "limit" to convert the limit matrix, type "." to return to mode selection)\nWARNING: CONVERSION MAY TAKE UP TO OR EVEN LONGER THAN 1 MINUTE!\n')
            if text == '.':
                mode = 0
                continue
            m = clean(string_to_mat(text), 0)
            t = type(m)
            if t < 0:
                print('Nonstandard')
                continue
            print(seq_to_string(mat_to_seq(m)))
        if mode == 3:
            mode = 0
            print('\nNot yet implemented ¯\\_(ツ)_/¯\n')
        if mode == 4:
            mode = 0
            print('\nOriginal code in JavaScript by HypCos\nhttps://github.com/hypcos/notation-explorer/blob/master/MM3.js\n\nPython implementation, matrix type checking and conversion from and to sequence by AleX-1337\nhttps://github.com/YT-AleX-1337/MMS\n')
    except KeyboardInterrupt:
        print('\n\nBye!')
        exit()
    except Exception as e:
        mode = 0
        print('\n', repr(e), '\nTraceback:\n', ''.join(traceback.format_tb(e.__traceback__)))
        print('Something went wrong. Either the input is invalid or the code is broken (._.)\n')
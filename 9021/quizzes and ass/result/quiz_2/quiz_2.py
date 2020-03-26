# Written by *** and Eric Martin for COMP9021


def rule_encoded_by(rule_nb):
    '''
    "rule_nb" is supposed to be an integer between 0 and 15.
    '''
    values = [int(d) for d in f'{rule_nb:04b}']
    return {(p // 2, p % 2): values[p] for p in range(4)}

def describe_rule(rule_nb):
    '''
    "rule_nb" is supposed to be an integer between 0 and 15.
    '''
    rule = rule_encoded_by(rule_nb)
    print('The rule encoded by', rule_nb, 'is: ', rule)
    print()
    for r in rule: 
        print(f'After {r[0]} followed by {r[1]}, we draw {rule[r]}')



def draw_line(rule_nb, first, second, length):
    '''
    "rule_nb" is supposed to be an integer between 0 and 15.
    "first" and "second" are supposed to be the integer 0 or the integer 1.
    "length" is supposed to be a positive integer (possibly equal to 0).

    
    Draws a line of length "length" consisting of 0's and 1's,
    that starts with "first" if "length" is at least equal to 1,
    followed by "second" if "length" is at least equal to 2,
    and with the remaining "length" - 2 0's and 1's determined by "rule_nb".
    '''
    rule = rule_encoded_by(rule_nb)
    if length > 2:
        l = [first,second]
        l.append(rule[(first,second)])
        l.append(rule[(second,l[2])])
        
        for i in range(4, length):
            l.append(rule[l[i - 2],l[i - 1]])  
        print(''.join([str(e) for e in l]))
    elif length == 1:
        print(first)
    elif length == 2:
        print(first,second,sep = '')
    elif length == 0:
        return None
        
    


def uniquely_produced_by_rule(line):
    '''
    "line" is assumed to be a string consisting of nothing but 0's and 1's.

    Returns an integer n between 0 and 15 if the rule encoded by n is the
    UNIQUE rule that can produce "line"; otherwise, returns -1.
    '''
    
    uniquely_rule = {}
    length = len(line)
    for i in range(length - 2):
        if (int(line[i]),int(line[i + 1])) not in uniquely_rule.keys():
            uniquely_rule[(int(line[i]),int(line[i + 1]))] = int(line[i + 2])
        else:
            #判断values是否相同
            if uniquely_rule[(int(line[i]),int(line[i + 1]))] == int(line[i + 2]):
                pass
            else:
                return -1
    if len(uniquely_rule) == 4:
        pass
    else:
        return -1
    
    t = uniquely_rule[(0,0)]*2**3 + uniquely_rule[(0,1)]*2**2 +uniquely_rule[(1,0)]*2**1 +uniquely_rule[(1,1)]
    return t
                
        
        
    
    
    
    
    
    
    
    

    

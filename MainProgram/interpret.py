#####################################################################
#
# CAS CS 320, Spring 2015
# Joe Zhou
# jzhou94@bu.edu
# interpret.py
#

exec(open("parse.py").read())

Node = dict
Leaf = str

def subst(s, a):
    #  Takes a substitution s and replace all variables in the abstract
    #    syntax tree a with any applicable substitutions using s
    if type(a) == Leaf:
        if a == 'End':
            return a
    elif type(a) == Node:
        for labelA in a:
            if labelA == 'Variable':
                for labelS in s:
                    if a["Variable"][0] == labelS:
                        return s[labelS]
            else:
                children = a[labelA]
                for x in range(0, len(children)):
                    v = subst(s, children[x])
                    children[x] = v
            return a



def unify(a, b):
    #  Takes two syntax trees a, b, and return the smallest
    #    substitution such that subst(s, a) == subst(s, b)
    s = {}
    if type(a) != Node and type(b) != Node and equal(a, b):
        return {}
    x = 0
    for labelA in a:
        y = 0
        for labelB in b:
            if x == y:
                if labelA == 'Variable':
                    s.update({a["Variable"][0]:b})
                if labelB == 'Variable':
                    s.update({b["Variable"][0]:a})
                childrenA = a[labelA]
                childrenB = b[labelB]
                if labelA == labelB and len(childrenA) == len(childrenB):
                    for z in range(0, len(childrenA)):
                        t = unify(childrenA[z], childrenB[z])
                        for labelT in t:
                            s.update({labelT:t[labelT]})
            y = y + 1
        x = x + 1
        return s
                
        

def equal(a, b):
    # Determines if two abstract syntax trees are equivalent
    e = True
    if type(a) != Node and type(b) != Node:
        if a != b:
            return False
        else:
            return True
    x = 0
    for labelA in a:
        y = 0
        for labelB in b:
            if x == y:
                if labelA != labelB:
                    e = False
                childrenA = a[labelA]
                childrenB = b[labelB]
                if len(childrenA) != len(childrenB):
                    e = False
                else:
                    for z in range(0, len(childrenA)):
                        e = e and equal(childrenA[z], childrenB[z])
            y = y + 1
        x = x + 1
    return e
            

def build(m, d):
    #  Builds abstract syntax tree
    if d == "End":
        return m
    if type(d) == Node:
        for labelD in d:
            if labelD == "Function":
                children = d[labelD]
                function = children[0]["Variable"][0]
                inputP = children[1]
                outputE = children[2]
                rest = children[3]
    
                if function not in m:
                    m[function] = [(inputP, outputE)]
                    m2 = build(m, rest)
                    return m2
                else:
                    m[function] = m[function] + [(inputP, outputE)]
                    m2 = build(m, rest)
                    return m2

def evaluate(m, env, e):
    #  Evaluates elements of abstract syntax tree
    #  i.e. if f(x) = test then f(test) = test
    if type(e) == Node:
        for label in e:
            children = e[label]

            if label == "ConInd":
                c = children[0]
                e1 = children[1]
                e2 = children[2]
                v1 = evaluate(m, env, e1)
                v2 = evaluate(m, env, e2)
                return {"ConInd": [c, v1, v2]}

            elif label == "ConBase":
                return e
            elif label == "Number":
                n = children[0]
                return n
            elif label == "Variable":
                x = children[0]
                v = env[x]
                return v
            elif label == "Plus":
                e1 = children[0]
                e2 = children[1]
                n1 = evaluate(m, env, e1)
                n2 = evaluate(m, env, e2)
                return n1 + n2
            elif label == "Apply":
                f = children[0]["Variable"][0]
                e1 = children[1]
                v1 = evaluate(m, env, e1)
                for (p, e2) in m[f]:
                    for labelV in v1:
                        for labelP in p:
                            if labelP == 'Variable':
                                return v1
                            if labelV == labelP and v1[labelV][0] == p[labelP][0]:
                                s = unify(p, v1)
                                if s is not None:
                                    env.update(s)
                                    v2 = evaluate(m, env, e2)
                                    return v2


def interact(s):
    # Build the module definition.
    m = build({}, parser(grammar, 'declaration')(s))

    # Interactive loop.
    while True:
        # Prompt the user for a query.
        s = input('> ') 
        if s == ':quit':
            break
        
        # Parse and evaluate the query.
        e = parser(grammar, 'expression')(s)
        if not e is None:
            print(evaluate(m, {}, e))
        else:
            print("Unknown input.")

#eof

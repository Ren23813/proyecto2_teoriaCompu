import copy
from itertools import chain, combinations

def _powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def chomsky(variables, terminales, simboloInicial, producciones):

    # copias
    V = copy.deepcopy(variables)
    T = copy.deepcopy(terminales)
    P = copy.deepcopy(producciones)

    # crear So único
    base = "So"
    idx = 0
    new_start = base
    while new_start in V or new_start in P:
        idx += 1
        new_start = f"{base}{idx}"
    V.append(new_start)
    P.setdefault(new_start, []).append([simboloInicial])


    # normalizar epsilon
    for A in list(P.keys()):
        new_rules = []
        for rhs in P[A]:
            if isinstance(rhs, list) and len(rhs) == 1 and rhs[0] == '?':
                new_rules.append([])
            else:
                new_rules.append(list(rhs))
        P[A] = new_rules


    # hallar nullable
    nullable = set()
    changed = True
    while changed:
        changed = False
        for A, rules in P.items():
            if A in nullable:
                continue
            for rhs in rules:
                if len(rhs) == 0 or all(sym in nullable for sym in rhs):
                    nullable.add(A)
                    changed = True
                    break

    # expandir producciones eliminando referencias a nullable
    P_expanded = {}
    for A, rules in P.items():
        bag = set()
        for rhs in rules:
            if len(rhs) == 0:
                if A == new_start:
                    bag.add(tuple([]))
                continue
            idxs = [i for i, sym in enumerate(rhs) if sym in nullable]
            for mask in _powerset(idxs):
                mask = set(mask)
                new_rhs = [sym for i, sym in enumerate(rhs) if i not in mask]
                if len(new_rhs) == 0:
                    if A == new_start:
                        bag.add(tuple([]))
                else:
                    bag.add(tuple(new_rhs))
        P_expanded[A] = [list(x) for x in bag]
    P = P_expanded

    # asegurar claves para todas las variables conocidas
    for a in V:
        P.setdefault(a, [])

    # eliminar producciones unarias 
    vars_set = set(V)
    unit_graph = {A: set() for A in P.keys()}
    for A, rules in P.items():
        for rhs in rules:
            if len(rhs) == 1 and rhs[0] in vars_set:
                unit_graph.setdefault(A, set()).add(rhs[0])


    unit_closure = {A: set() for A in P.keys()}
    for A in P.keys():
        stack = list(unit_graph.get(A, []))
        seen = set()
        while stack:
            x = stack.pop()
            if x in seen:
                continue
            seen.add(x)
            unit_closure[A].add(x)
            for y in unit_graph.get(x, []):
                if y not in seen:
                    stack.append(y)

    P_no_units = {}
    for A in P.keys():
        s = set()
        for rhs in P[A]:
            if not (len(rhs) == 1 and rhs[0] in vars_set):
                s.add(tuple(rhs))
        for B in unit_closure.get(A, []):
            for rhs in P.get(B, []):
                if not (len(rhs) == 1 and rhs[0] in vars_set):
                    s.add(tuple(rhs))
        P_no_units[A] = [list(x) for x in s]
    P = P_no_units


    # crear variables para terminales >=2
    term_var = {}
    for t in T:
        cand = f"T_{t}"
        k = 0
        while cand in V:
            k += 1
            cand = f"T_{t}{k}"
        term_var[t] = cand
        V.append(cand)
        P.setdefault(cand, [])
        if [t] not in P[cand]:
            P[cand].append([t])


    # reemplazar terminales >= 2
    for A in list(P.keys()):
        new_rules = []
        for rhs in P[A]:
            if len(rhs) >= 2:
                new_rules.append([term_var[sym] if sym in T else sym for sym in rhs])
            else:
                new_rules.append(list(rhs))
        P[A] = new_rules


    # binarización
    cnt = 1
    P_bin = {}
    for A in list(P.keys()):
        P_bin.setdefault(A, [])
        for rhs in P[A]:
            if len(rhs) <= 2:
                P_bin[A].append(list(rhs))
            else:
                symbols = list(rhs)
                head = A
                while len(symbols) > 2:
                    newX = f"X_{cnt}"
                    cnt += 1
                    while newX in V:
                        newX = f"X_{cnt}"
                        cnt += 1
                    V.append(newX)
                    P_bin.setdefault(head, []).append([symbols[0], newX])
                    head = newX
                    symbols = symbols[1:]
                P_bin.setdefault(head, []).append([symbols[0], symbols[1]])
    P = P_bin


    # eliminar no-productivas
    productive = set()
    changed = True
    while changed:
        changed = False
        for A, rules in P.items():
            if A in productive:
                continue
            for rhs in rules:
                ok = True
                for s in rhs:
                    if s in T:
                        continue
                    if s not in productive:
                        ok = False
                        break
                if ok:
                    productive.add(A)
                    changed = True
                    break

    # filtrar por productivas
    P = {A: [r for r in rules if all((s in T) or (s in productive) for s in r)]
         for A, rules in P.items() if A in productive}


    V = [v for v in V if v in P]

    # eliminar no-alcanzables
    reachable = set()
    stack = [new_start]
    while stack:
        cur = stack.pop()
        if cur in reachable:
            continue
        if cur not in P:
            continue
        reachable.add(cur)
        for rhs in P[cur]:
            for s in rhs:
                if s in P and s not in reachable:
                    stack.append(s)

    P = {A: rules for A, rules in P.items() if A in reachable}
    V = [v for v in V if v in P]

    for A in list(P.keys()):
        seen = set()
        dedup = []
        for rhs in P[A]:
            tup = tuple(rhs)
            if tup not in seen:
                seen.add(tup)
                dedup.append(list(rhs))
        P[A] = dedup
    return (V, T, new_start, P)

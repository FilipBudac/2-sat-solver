from collections import defaultdict

SINGLE_LITERAL_CLAUSE = 1
TWO_LITERAL_CLAUSE = 2

FILENAME = 'input2.txt'


def inv_literal(lit):
    return lit * -1


def cons_graphs(clauses):
    adj = defaultdict(list)
    t_adj = defaultdict(list)
    for clause in clauses:
        clause_type = len(clause)
        if clause_type == SINGLE_LITERAL_CLAUSE:
            lit = clause[0]

            adj[inv_literal(lit)].append(lit)

            t_adj[lit].append(inv_literal(lit))
        elif clause_type == TWO_LITERAL_CLAUSE:
            f_lit, s_lit = clause

            adj[inv_literal(f_lit)].append(s_lit)
            adj[inv_literal(s_lit)].append(f_lit)

            t_adj[s_lit].append(inv_literal(f_lit))
            t_adj[f_lit].append(inv_literal(s_lit))

    return adj, t_adj


def f_dfs(v, adj, visited, order):
    visited.add(v)
    for n in adj[v]:
        if n not in visited:
            f_dfs(n, adj, visited, order)
    order.append(v)


def s_dfs(v, group, t_adj, comp):
    comp[v] = group
    for n in t_adj[v]:
        if n not in comp:
            s_dfs(n, group, t_adj, comp)


def solve_2sat(n_literals, adj, t_adj):
    order = []
    visited = set()
    for i in range(1, n_literals + 1):
        if i not in visited:
            f_dfs(i, adj, visited, order)

    group = 0
    comp = {}
    for i in range(n_literals):
        v = order[n_literals - i - 1]
        if v not in comp:
            s_dfs(v, group, t_adj, comp)
            group += 1

    assigns = {}
    for i in range(1, n_literals // 2 + 1):
        if comp[i] == comp[inv_literal(i)]:
            return False, {}
        assigns[i] = comp[i] > comp[inv_literal(i)]

    return True, assigns


def main():
    with open(FILENAME) as file:
        n_literals, _ = list(map(int, file.readline().split()))
        clauses = [list(map(int, line.split()))[:-1] for line in file]

    adj, t_adj = cons_graphs(clauses)
    is_satisfiable, assigns = solve_2sat(n_literals * 2, adj, t_adj)

    print(is_satisfiable, assigns)


if __name__ == '__main__':
    main()

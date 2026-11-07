"""Subproblema adversario de asignacion de recursos por turnos.

El jugador MAX asigna unidades a la empresa; MIN representa al competidor
que puede disputar unidades. Cada turno cambia el saldo de recursos.
"""
def legal_actions(state):
    # state = (remaining_turns, available_units, score)
    turns, units, score = state
    if turns <= 0 or units <= 0:
        return [0]
    return list(range(0, min(3, units) + 1))

def terminal(state):
    return state[0] <= 0 or state[1] <= 0

def transition(state, action, player):
    turns, units, score = state
    # MAX gana 2 puntos por unidad asignada; MIN reduce 2 puntos por unidad disputada.
    delta = 2 * action if player == 1 else -2 * action
    return (turns - 1, units - action, score + delta)

def utility(state):
    return state[2] + state[1] * 0.5

def minimax(state, depth, player=1):
    if depth == 0 or terminal(state):
        return utility(state), 1
    values, nodes = [], 1
    for action in legal_actions(state):
        value, visited = minimax(transition(state, action, player), depth-1, -player)
        values.append(value); nodes += visited
    return (max(values) if player == 1 else min(values)), nodes

def alphabeta(state, depth, alpha=float("-inf"), beta=float("inf"), player=1):
    if depth == 0 or terminal(state):
        return utility(state), 1, 0
    nodes, pruned, values = 1, 0, []
    for action in legal_actions(state):
        value, visited, cut = alphabeta(transition(state, action, player),
                                        depth-1, alpha, beta, -player)
        nodes += visited; pruned += cut; values.append(value)
        if player == 1:
            alpha = max(alpha, value)
        else:
            beta = min(beta, value)
        if beta <= alpha:
            pruned += max(0, len(legal_actions(state)) - len(values))
            break
    return (max(values) if player == 1 else min(values)), nodes, pruned

def compare(depth=6, available_units=10):
    initial = (depth, available_units, 0)
    value1, nodes1 = minimax(initial, depth)
    value2, nodes2, pruned = alphabeta(initial, depth)
    return {"minimax_value": value1, "alphabeta_value": value2,
            "minimax_nodes": nodes1, "alphabeta_nodes": nodes2, "pruned": pruned,
            "same_value": value1 == value2}

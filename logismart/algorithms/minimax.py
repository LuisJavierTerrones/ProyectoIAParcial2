
"""Minimax y poda alfa-beta para la asignación de recursos."""


def legal_actions(state):
    turns, units, score = state

    if turns <= 0 or units <= 0:
        return [0]

    return list(range(0, min(3, units) + 1))


def terminal(state):
    turns, units, score = state
    return turns <= 0 or units <= 0


def transition(state, action, player):
    turns, units, score = state

    if action not in legal_actions(state):
        raise ValueError("Acción no válida.")

    delta = 2 * action if player == 1 else -2 * action

    return (
        turns - 1,
        units - action,
        score + delta
    )


def utility(state):
    turns, units, score = state
    return score + units * 0.5


def minimax(state, depth, player=1):
    if depth <= 0 or terminal(state):
        return utility(state), 1

    values = []
    nodes = 1

    for action in legal_actions(state):
        next_state = transition(state, action, player)

        value, visited = minimax(
            next_state,
            depth - 1,
            -player
        )

        values.append(value)
        nodes += visited

    if player == 1:
        return max(values), nodes

    return min(values), nodes


def alphabeta(state, depth, alpha=float("-inf"),
              beta=float("inf"), player=1):

    if depth <= 0 or terminal(state):
        return utility(state), 1, 0

    nodes = 1
    pruned = 0
    values = []

    actions = legal_actions(state)

    for action in actions:
        next_state = transition(state, action, player)

        value, visited, cut = alphabeta(
            next_state,
            depth - 1,
            alpha,
            beta,
            -player
        )

        nodes += visited
        pruned += cut
        values.append(value)

        if player == 1:
            alpha = max(alpha, value)
        else:
            beta = min(beta, value)

        if beta <= alpha:
            pruned += len(actions) - len(values)
            break

    if player == 1:
        return max(values), nodes, pruned

    return min(values), nodes, pruned


def compare(depth=6, available_units=10):
    """Compara ambos algoritmos y obtiene la acción inicial recomendada."""

    if depth < 1:
        raise ValueError("La profundidad debe ser al menos 1.")

    if available_units < 0:
        raise ValueError("Los recursos disponibles no pueden ser negativos.")

    initial = (depth, available_units, 0)

    value1, nodes1 = minimax(initial, depth)

    value2, nodes2, pruned = alphabeta(initial, depth)

    # Obtener la mejor acción inicial para MAX.
    actions = legal_actions(initial)
    action_values = []

    for action in actions:
        next_state = transition(initial, action, 1)

        value, _ = minimax(
            next_state,
            depth - 1,
            -1
        )

        action_values.append((value, action))

    best_value, best_action = max(
        action_values,
        key=lambda item: item[0]
    )

    return {
        "minimax_value": value1,
        "alphabeta_value": value2,
        "minimax_nodes": nodes1,
        "alphabeta_nodes": nodes2,
        "pruned": pruned,
        "same_value": value1 == value2,
        "best_action": best_action,
        "allocated_resources": best_action,
        "remaining_units": available_units - best_action
    }

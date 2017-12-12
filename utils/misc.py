def load_state(filename):
    """
    Loads last imported state and returns it as a set for efficient existence queries.
    """
    ids = []
    with open(filename, 'r', encoding='utf-8') as state_file:
        ids = state_file.read().splitlines()
    return set(ids)

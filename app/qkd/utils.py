### Helper Functions

def compare_keys(alice_key, bob_key):
    """
        Compares two keys and returns the number and percentage of matches
    """
    if len(alice_key) != len(bob_key):
        raise ValueError("Key lengths must match.")
    matches = sum(a == b for a, b in zip(alice_key, bob_key))
    match_rate = matches / len(alice_key)
    return matches, match_rate

def print_key_summary(alice_key, bob_key):
    """
        Prints a summary of how well Alice and Bob's keys match
    """
    matches, match_rate = compare_keys(alice_key, bob_key)
    print("Matching Bits:", matches)
    print("Match Rate: {:.2%}".format(match_rate))

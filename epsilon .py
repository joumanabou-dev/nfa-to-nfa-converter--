# Maya lina gadda group 02 security
# boufroukh djemana group 01 security
# benzid oumeima group 02 security


# ε-NFA to NFA Conversion
# Symbol used for epsilon
EPSILON = "ε"
EPSILON_INPUTS = ["e", "eps", "epsilon", "ε"]

#  Function 1
# Check if the NFA contains any epsilon transitions


def check_for_epsilon_transitions(nfa):
    for state in nfa["states"]:
        if state in nfa["transitions"] and EPSILON in nfa["transitions"][state]:
            return True
    return False


#  Function 2
# Calculate epsilon-closure of ONE state


def calculate_epsilon_closure(nfa, start_state):
    closure = set()
    stack = [start_state]
    while stack:
        current = stack.pop()
        if current not in closure:
            closure.add(current)
            transitions_from_current = nfa["transitions"].get(current, {})
            if EPSILON in transitions_from_current:
                for next_state in transitions_from_current[EPSILON]:
                    stack.append(next_state)
    return sorted(list(closure))


#  Function 3
# Calculate epsilon-closure for ALL states


def calculate_all_epsilon_closures(nfa):
    closures = {}
    for state in nfa["states"]:
        closures[state] = calculate_epsilon_closure(nfa, state)
    return closures


#  Function 4
# Create new transitions without epsilon


def calculate_new_transitions(nfa, closures):
    new_transitions = {}
    for state in nfa["states"]:
        new_transitions[state] = {}
        for symbol in nfa["symbols"]:
            reachable_states = set()
            for c_state in closures[state]:
                transitions_from_c_state = nfa["transitions"].get(c_state, {})
                if symbol in transitions_from_c_state:
                    for target in transitions_from_c_state[symbol]:
                        reachable_states.update(closures[target])
            new_transitions[state][symbol] = sorted(list(reachable_states))
    return new_transitions


#  Function 5
# Find new final states after removing epsilon


def determine_new_final_states(nfa, closures):
    new_finals = set()
    for state in nfa["states"]:
        for f in nfa["final_states"]:
            if f in closures[state]:
                new_finals.add(state)
                break
    return sorted(list(new_finals))


# Read NFA from the user


def read_nfa():
    print("\nEnter NFA information\n")

    # Read states
    while True:
        states_input = input("States (space-separated): ").split()
        if not states_input:
            print(" State list cannot be empty. Try again.")
            continue

        states = list(dict.fromkeys(states_input))
        if len(states) < len(states_input):
            print("⚠ Duplicate states were removed:", set(states_input) - set(states))
        break

    # Enter alphabet symbols
    while True:
        symbols_input = input("Alphabet symbols (space-separated): ").split()
        if not symbols_input:
            print(" Alphabet cannot be empty. Try again.")
            continue

        symbols = list(dict.fromkeys(symbols_input))
        if len(symbols) < len(symbols_input):
            print(
                "⚠ Duplicate symbols were removed:", set(symbols_input) - set(symbols)
            )
        break

    # Enter  start state
    while True:
        start_state = input("Start state: ")
        if start_state not in states:
            print(f" Start state '{start_state}' is not in state list. Try again.")
        else:
            break

    # Enter  final states
    while True:
        final_states_input = input("Final states (space-separated): ").split()

        # Check for empty input
        if not final_states_input:
            print(
                "⚠ Warning: No final states entered. The automaton will accept NO strings."
            )
            choice = input("Continue anyway? (y/n): ").strip().lower()
            if choice == "y":
                final_states = []
                break
            else:
                continue

        invalid_finals = [f for f in final_states_input if f not in states]
        if invalid_finals:
            print(f" Final states {invalid_finals} are not in state list. Try again.")
        else:
            final_states = list(dict.fromkeys(final_states_input))
            if len(final_states) < len(final_states_input):
                print(
                    " Duplicate final states were removed:",
                    set(final_states_input) - set(final_states),
                )
            break

    # Enter transitions
    transitions = {}
    print("\nEnter transitions: state symbol state")
    print("Use e / eps / epsilon / ε for epsilon")
    print("Type 'done' to finish\n")

    while True:
        line = input("Transition: ").strip()

        # Handle epsilon input
        if line == "":
            print("⚠ Empty input. Type 'done' to finish or enter a transition.")
            continue

        if line.lower() == "done":
            break

        parts = line.split()
        if len(parts) != 3:
            print(" Format error. Use: state symbol state")
            continue

        from_state, symbol, to_state = parts

        if symbol.lower() in EPSILON_INPUTS:
            symbol = EPSILON

        if symbol != EPSILON and symbol not in symbols:
            print(" Symbol not in alphabet")
            continue

        if from_state not in states:
            print(f" Unknown from-state '{from_state}'")
            continue

        if to_state not in states:
            print(f" Unknown to-state '{to_state}'")
            continue

        if from_state not in transitions:
            transitions[from_state] = {}
        if symbol not in transitions[from_state]:
            transitions[from_state][symbol] = set()

        if to_state in transitions[from_state][symbol]:
            print(
                f" Duplicate transition ignored: {from_state} --({symbol})--> {to_state}"
            )
        else:
            transitions[from_state][symbol].add(to_state)

    # convert sets to lists
    for from_state in transitions:
        for symbol in transitions[from_state]:
            transitions[from_state][symbol] = sorted(
                list(transitions[from_state][symbol])
            )

    return {
        "states": states,
        "symbols": symbols,
        "start_state": start_state,
        "final_states": final_states,
        "transitions": transitions,
    }


# Display the new NFA without epsilon
def display_nfa(nfa, new_transitions, new_final_states):
    print("\n" + "=" * 50)
    print("NFA without ε-transitions")
    print("=" * 50)

    print("States:", nfa["states"])
    print("Alphabet:", nfa["symbols"])
    print("Start state:", nfa["start_state"])
    print("Final states:", new_final_states)

    print("\nTransition Table:")
    header = "State".center(6) + " | "
    for s in nfa["symbols"]:
        header += f"{s:^12} | "
    print(header)
    print("-" * len(header))

    for state in nfa["states"]:
        row = f"{state:^6} | "
        for s in nfa["symbols"]:
            if new_transitions[state].get(s):
                row += f"{str(new_transitions[state][s]):^12} | "
            else:
                row += f"{'Ø':^12} | "
        print(row)


def main():
    print("=" * 50)
    print("ε-NFA to NFA Converter (Student Version)")
    print("=" * 50)

    while True:
        nfa = read_nfa()

        if not check_for_epsilon_transitions(nfa):
            print("\nℹ No ε-transitions found.")
            print("This is already a valid NFA.")
        else:
            closures = calculate_all_epsilon_closures(nfa)
            print("\nEpsilon Closures:")
            for state in closures:
                print(f"ε-closure({state}) = {closures[state]}")

            new_transitions = calculate_new_transitions(nfa, closures)
            new_final_states = determine_new_final_states(nfa, closures)

            display_nfa(nfa, new_transitions, new_final_states)

            print("\n ε-transitions removed successfully!")

        choice = input("\nDo you want to convert another NFA? (y/n): ").strip().lower()
        if choice != "y":
            print("\nExiting. Goodbye!")
            break


# Run Program
if __name__ == "__main__":
    main()

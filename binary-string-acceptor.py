from __future__ import annotations
import re

def is_binary(string: str) -> bool:
    if len(re.findall(r'\b[01]+\b', string)):
        return True
    return False

def has_whitespace(string: str) -> bool:
    if len(re.findall(r'\s*', string)) > 0:
        return True
    return False

def trimmer(list_str: list[str]) -> str:
    result = ""
    for string in list_str:
        result += string
    return result

# Raised when the symbol being matched is not part of the language set.
class NonBinarySymbolException(Exception):
    pass

class EmptyStartStateException(Exception):
    pass

class EmptyFinalStateException(Exception):
    pass

class NonBinaryStringException(Exception):
    pass

def transition_state(state: State, symbol: str) -> State:
    if re.match('0', symbol):
        return state.zero_state
    if re.match('1', symbol):
        return state.one_state
    raise NonBinarySymbolException('Non-binary symbols encountered!')

class State:
    def __init__(self, name: str, zero_state: State = None, one_state: State = None) -> None:
        self.name: str = name
        if zero_state is None:
            self.zero_state: State = self
        if one_state is None:
            self.one_state: State = self
        self.zero_state: State = zero_state
        self.one_state: State = one_state
    
    def set_zero_state(self, state: State) -> None:
        self.zero_state = state

    def set_one_state(self, state: State) -> None:
        self.one_state = state

class DFA:
    def __init__(self, name: str, start_state: State = None, final_state: State = None) -> None:
        self.name = name
        if start_state is None:
            raise EmptyStartStateException('The start state is empty!')
        if final_state is None:
            raise EmptyFinalStateException('The final state is empty!')
        self.current_state: State = start_state
        self.start_state: State = start_state
        self.final_state: State = final_state
    
    def change_state(self, symbol: str) -> None:
        new_state: State = transition_state(self.current_state, symbol)
        self.current_state = new_state

    def evaluate(self, string: str) -> bool:
        for symbol in string:
            self.change_state(symbol)
            print(self.current_state.name)
        if self.current_state is self.final_state:
            return True
        return False

def check_string(dfa: DFA, string: str) -> bool:
    if is_binary(string) == False:
        raise NonBinaryStringException("The string provided is non-binary!")
    if has_whitespace(string):
        return dfa.evaluate(trimmer(string.split()))
    return dfa.evaluate(string)

q0: State = State('q0')
q1: State = State('q1')
q2: State = State('q2')

q0.set_zero_state(q0)
q0.set_one_state(q1)

q1.set_zero_state(q2)
q1.set_one_state(q2)

q2.set_zero_state(q1)
q2.set_one_state(q0)

dfa: DFA = DFA("Simple Model", q0, q2)
print(check_string(dfa, "11001011"))

import abc
from dataclasses import dataclass
from enum import Enum
from collections import defaultdict, deque

class Signal(Enum):
    Zero = 0
    Low = 1
    High = 2

@dataclass
class Message:
    signal: Signal
    source: str
    destination: str

class Module(abc.ABC):
    def __init__(self, name: str, destinations: list[str]):
        ...
    def accept(self, message: Message) -> list[Message]:
        ...
    @property
    def active(self) -> bool:
        ...

class Void(Module):
    def __init__(self, name: str = "", destinations: list[str] = []):
        ...
    def accept(self, message: Message) -> list[Message]:
        return []
    @property
    def active(self) -> bool:
        return False

class FlipFlop(Module):
    def __init__(self, name: str, destinations: list[str]):
        self.state = False
        self.destinations = destinations
        self.name = name

    def accept(self, message: Message) -> list[Message]:
        if message.signal == Signal.Low:
            self.state = not self.state
            if self.state:
                return [Message(Signal.High, self.name, d) for d in self.destinations]
            else:
                return [Message(Signal.Low, self.name, d) for d in self.destinations]
        return []
    
    @property
    def active(self) -> bool:
        return self.state
    
    def __repr__(self):
        return f"FlipFlop({self.name}, {dict([(d, Signal.High if self.state else Signal.Low) for d in self.destinations])}"


    
class Conjunction(Module):
    def __init__(self, name: str, destinations: list[str]):
        self.states = {d: Signal.Low for d in destinations}
        self.destinations = destinations
        self.name = name

    def accept(self, message: Message) -> list[Message]:
        self.states[message.source] = message.signal
        if all([s == Signal.High for s in self.states.values()]):
            return [Message(Signal.Low, self.name, d) for d in self.destinations]
        return [Message(Signal.High, self.name, d) for d in self.destinations]
    
    @property
    def active(self) -> bool:
        return any([s == Signal.High for s in self.states.values()])
    
    def __repr__(self):
        return f"Conjunction({self.name}, {self.states})"
    
class Broadcast(Module):
    def __init__(self, name: str, destinations: list[str]):
        self.destinations: list[str] = destinations
        self.name: str = name

    def accept(self, message: Message) -> list[Message]:
        return [Message(message.signal, self.name, d) for d in self.destinations]
    
    @property
    def active(self) -> bool:
        return False
    
    def __repr__(self):
        return f"Broadcast({self.name})"
    

def state_non_zero(modules: dict[str, Module], itterations: int):
    if itterations == 0:
        return True
    for m in modules.values():
        if m.active:
            return True
    return False

def solve(filename: str):
    modules: defaultdict[str, Module] = defaultdict(Void)
    with open(filename) as file:
        for line in file:
            name, destinations = line.strip().split(" -> ")
            if name.startswith("&"):
                modules[name[1:]] = Conjunction(name[1:], destinations.split(", "))
            elif name.startswith("%"):
                modules[name[1:]] = FlipFlop(name[1:], destinations.split(", "))
            elif name == "broadcaster":
                modules[name] = Broadcast(name, destinations.split(", "))
    
    button_push = Message(Signal.Low, "button", "broadcaster")
    times: list[int] = []
    states: deque[list[Message]] = deque([])

    while True:
        signals: list[Message] = modules["broadcaster"].accept(button_push)
        times.append(0)
        while len(signals) > 0:
            states.appendleft(signals)
            times[-1] += 1
            signals = []
            for s in states[0]:
                signals.extend(modules[s.destination].accept(s))
        if state_non_zero(modules, len(times)):
            break
    print(times)
    for s in states:
        print(s)


        



    

if __name__ == "__main__":
    solve("test1.txt")

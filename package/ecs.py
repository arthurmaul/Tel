from dataclasses import dataclass, field
from itertools import count

data = dataclass (kw_only=True, slots=True)
new = lambda T: field (default_factory=T)
ID = count ()

cells: dict[int, dict[int, int]] = dict ()
markers: dict[int, set[int]] = dict ()
components: dict[int, list[object]] = dict ()
indices: dict[int, list[object]] = dict ()
labels: dict[str, int] = dict()

def cell (label: str = None) -> int:
    if label and label in labels: return labels[label]
    identifier: int = next (ID)
    if label: labels[label] = identifier
    cells[identifier] = dict ()
    return identifier

def storage (identifier: int) -> int:
    components[identifier] = list ()
    indices[identifier] = list ()
    return identifier

def despawn (identifier: int) -> None:
    pass

def mark (marker: int, target: int) -> callable:
    if not marker in markers: markers[marker] = set ()
    markers[marker].add (target)
    return mark

def unmark (marker: int, target: int) -> callable:
    markers[marker].remove (target)
    return unmark

def attach (target: int, component: int, data: object) -> callable:
    mark (component, target)
    cells[target][component] = len (components[component])
    components[component].append (data)
    indices[component].append (target)
    return attach

def detach (target: int, component: int) -> callable:
    unmark (component, target)
    row = cells[target].pop(component); column = components[component]
    if row != (len(column) - 1):
        last = indices[component][-1]
        indices[row],indices[last]=last,row
        column[row],column[last]=column[last],column[row]
    components[component].pop ()
    indices[component].pop ()
    return detach

def assign (target: int, component: int, data: object) -> callable:
    components[component][cells[target][component]] = data
    return assign

def the (target: int, component: int) -> object:
    return components[component][cells[target][component]]

def inherit (left: int, right: int) -> callable:
    return inherit

def clone (cell: int, label: str = None) -> int:
    pass

def search (*terms: tuple[int]) -> list[tuple]:
    pass


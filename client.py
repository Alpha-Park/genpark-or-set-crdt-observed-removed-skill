import time
import uuid

class ORSetCRDT:
    """Observed-Removed Set (Add-Wins OR-Set) CRDT."""
    def __init__(self):
        # elements mapped to set of active addition tags
        self.add_set = set() # (element, tag)
        self.rem_set = set() # (element, tag)

    def add(self, element: str, tag: str = None) -> str:
        if tag is None:
            tag = f"{time.time()}_{uuid.uuid4().hex[:6]}"
        self.add_set.add((element, tag))
        return tag

    def remove(self, element: str) -> int:
        # Mark all observed tags for this element as removed
        removed_count = 0
        for e, tag in list(self.add_set):
            if e == element:
                self.rem_set.add((e, tag))
                removed_count += 1
        return removed_count

    def read(self) -> list[str]:
        active = {e for e, tag in self.add_set if (e, tag) not in self.rem_set}
        return sorted(list(active))

    def get_state(self) -> dict:
        return {
            "add_set": list(self.add_set),
            "rem_set": list(self.rem_set)
        }

    def merge(self, other_state: dict):
        for item in other_state.get("add_set", []):
            self.add_set.add(tuple(item))
        for item in other_state.get("rem_set", []):
            self.rem_set.add(tuple(item))

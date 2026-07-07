import bisect
from typing import List, Tuple, Optional

class Resource:
    def __init__(self, name: str, working_hours: List[Tuple[int, int]]):
        self.name = name
        self.working_hours = sorted(working_hours)
        self.busy = []          # занятые интервалы [(start, end), ...]

    def occupy(self, start: int, end: int):
        bisect.insort(self.busy, (start, end))
        merged = []
        for s, e in self.busy:
            if not merged or s > merged[-1][1]:
                merged.append([s, e])
            else:
                merged[-1][1] = max(merged[-1][1], e)
        self.busy = [(s, e) for s, e in merged]

    def find_free_slot(self, duration: int, earliest_start: int = 0) -> Optional[Tuple[int, int]]:
        for ws, we in self.working_hours:
            if we <= earliest_start:
                continue
            cur_start = max(ws, earliest_start)
            if cur_start >= we:
                continue
            next_start = cur_start
            for bs, be in self.busy:
                if be <= cur_start:
                    continue
                if bs >= we:
                    break
                if bs > next_start:
                    if bs - next_start >= duration:
                        return (next_start, next_start + duration)
                next_start = max(next_start, be)
            if next_start < we and we - next_start >= duration:
                return (next_start, next_start + duration)
        return None
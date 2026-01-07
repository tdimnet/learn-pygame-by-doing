import time
from __future__ import annotations
from dataclasses import dataclass, field
from collections import deque
from contextlib import contextmanager
from typing import Deque, Dict, Iterator, Optional



@dataclass
class Stat:
    samples: Deque[float] = field(default_factory=lambda: deque(maxlen=120))
    last_ms: float = 0.0

    def add(self, ms: float) -> None:
        self.last_ms = ms
        self.samples.append(ms)

    @property
    def avg_ms(self) -> float:
        if not self.samples:
            return 0.0

        return sum(self.samples) / len(self.samples)

    @property
    def max_ms(self) -> float:
        return max(self.samples) if self.samples else 0.0


class Profiler:
    def __init__(self, enabled: bool = True) -> None:
        self.enabled = enabled
        self._stats: Dict[str, Stat] = {}
        self._frame_start: Optional[float] = None
        self.frame_ms: float = 0.0

    def toggle(self) -> None:
        pass

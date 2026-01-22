import time
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
        self.enabled = not self.enabled

    def reset_frame(self) -> None:
        if not self.enabled:
            return
        self._frame_start = time.perf_counter()

    def end_frame(self) -> None:
        if not self.enabled or self._frame_start is None:
            return
        self.frame_ms = (time.perf_counter() - self._frame_start) * 1000.0

    @contextmanager
    def section(self, name: str) -> Iterator[None]:
        if not self.enabled:
            yield
            return
        t0 = time.perf_counter()
        try:
            yield
        finally:
            ms = (time.perf_counter() - t0) * 1000.0
            self._stats.setdefault(name, Stat()).add(ms)

    def snapshot(self) -> list:
        """Returns a sorted list of stats for displaying purposes"""
        items = []
        for name, st in self._stats.items():
            items.append((name, st.last_ms, st.avg_ms, st.max_ms))
        items.sort(key=lambda x: x[2], reverse=True)
        return items

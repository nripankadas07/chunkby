"""Core chunkby implementation."""
from __future__ import annotations

from collections import deque
from typing import Callable, Deque, Iterable, Iterator, List, Tuple, TypeVar

T = TypeVar("T")

__all__ = [
    "ChunkbyError",
    "batch_by",
    "chunk",
    "drop",
    "nth",
    "pairwise",
    "partition",
    "take",
    "window",
]


class ChunkbyError(ValueError):
    """Raised on invalid arguments to chunkby helpers."""


def chunk(it: Iterable[T], size: int) -> Iterator[List[T]]:
    """Yield consecutive lists of length ``size``. Last chunk may be shorter."""
    if size <= 0:
        raise ChunkbyError(f"size must be positive, got {size}")
    buf: List[T] = []
    for item in it:
        buf.append(item)
        if len(buf) == size:
            yield buf
            buf = []
    if buf:
        yield buf


def window(it: Iterable[T], size: int, step: int = 1) -> Iterator[Tuple[T, ...]]:
    """Yield sliding windows of length ``size`` with stride ``step``.

    The last window may be shorter than ``size`` only if the iterator is
    exhausted before the window fills. By default we drop the trailing
    incomplete window — pass ``step=size`` for a strict, non-overlapping
    chunker that's equivalent to :func:`chunk`.
    """
    if size <= 0:
        raise ChunkbyError(f"size must be positive, got {size}")
    if step <= 0:
        raise ChunkbyError(f"step must be positive, got {step}")
    buf: Deque[T] = deque(maxlen=size)
    skip = 0
    for item in it:
        if skip > 0:
            skip -= 1
            continue
        buf.append(item)
        if len(buf) == size:
            yield tuple(buf)
            if step >= size:
                buf.clear()
                skip = step - size
            else:
                for _ in range(step):
                    if buf:
                        buf.popleft()


def batch_by(it: Iterable[T], key: Callable[[T], object]) -> Iterator[List[T]]:
    """Yield runs of items whose ``key(item)`` is the same as the previous's.

    Conceptually like :func:`itertools.groupby` but materialised into lists.
    """
    batch: List[T] = []
    last_key: object = object()  # sentinel
    for item in it:
        k = key(item)
        if batch and k != last_key:
            yield batch
            batch = []
        batch.append(item)
        last_key = k
    if batch:
        yield batch


def partition(it: Iterable[T], pred: Callable[[T], bool]) -> Tuple[List[T], List[T]]:
    """Return ``(matching, not_matching)``. Iterates ``it`` once."""
    yes: List[T] = []
    no: List[T] = []
    for item in it:
        (yes if pred(item) else no).append(item)
    return yes, no


def pairwise(it: Iterable[T]) -> Iterator[Tuple[T, T]]:
    """Yield ``(a, b), (b, c), (c, d) …`` overlapping pairs."""
    iterator = iter(it)
    try:
        prev = next(iterator)
    except StopIteration:
        return
    for current in iterator:
        yield (prev, current)
        prev = current


def take(it: Iterable[T], n: int) -> List[T]:
    """Return the first ``n`` items as a list."""
    if n < 0:
        raise ChunkbyError(f"n must be non-negative, got {n}")
    out: List[T] = []
    for i, item in enumerate(it):
        if i >= n:
            break
        out.append(item)
    return out


def drop(it: Iterable[T], n: int) -> Iterator[T]:
    """Yield items after the first ``n``."""
    if n < 0:
        raise ChunkbyError(f"n must be non-negative, got {n}")
    iterator = iter(it)
    for _ in range(n):
        try:
            next(iterator)
        except StopIteration:
            return
    for item in iterator:
        yield item


_MISSING = object()


def nth(it: Iterable[T], n: int, default: T = _MISSING) -> T:  # type: ignore[assignment]
    """Return the ``n``-th element (0-indexed) or ``default``.

    If no ``default`` is given and the iterable is too short, raises
    :class:`ChunkbyError`.
    """
    if n < 0:
        raise ChunkbyError(f"n must be non-negative, got {n}")
    for i, item in enumerate(it):
        if i == n:
            return item
    if default is _MISSING:
        raise ChunkbyError(f"iterable shorter than {n + 1} items")
    return default

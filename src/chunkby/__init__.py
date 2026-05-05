"""chunkby — iterator helpers, zero dependencies.

Public API:

* :func:`chunk` — split into fixed-size lists.
* :func:`window` — sliding windows of size ``n``, optional ``step``.
* :func:`batch_by` — start a new batch whenever a predicate flips.
* :func:`partition` — split into two iterables by predicate.
* :func:`pairwise` — overlapping pairs ``(a, b), (b, c), …``.
* :func:`take` — first ``n``.
* :func:`drop` — skip first ``n``.
* :func:`nth` — element at index ``n`` or ``default``.
* :class:`ChunkbyError` — raised on invalid arguments.
"""
from __future__ import annotations

from ._core import (
    ChunkbyError,
    batch_by,
    chunk,
    drop,
    nth,
    pairwise,
    partition,
    take,
    window,
)

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

__version__ = "0.1.0"

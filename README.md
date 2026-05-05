# chunkby

Iterator helpers for Python 3.10+. Zero dependencies.

`chunk`, `window`, `batch_by`, `partition`, `pairwise`, `take`, `drop`, `nth`.

## Install

```bash
pip install chunkby
```

## Quick start

```python
from chunkby import chunk, window, batch_by, partition, pairwise, take, drop, nth

list(chunk([1,2,3,4,5], 2))                # [[1,2],[3,4],[5]]
list(window([1,2,3,4], 2))                 # [(1,2),(2,3),(3,4)]
list(window([1,2,3,4,5,6], 3, step=3))     # [(1,2,3),(4,5,6)]
list(batch_by([1,1,2,2,1], lambda x: x))   # [[1,1],[2,2],[1]]
partition([1,2,3,4], lambda x: x%2==0)     # ([2,4], [1,3])
list(pairwise([1,2,3,4]))                  # [(1,2),(2,3),(3,4)]
take([1,2,3,4,5], 3)                       # [1,2,3]
list(drop([1,2,3,4,5], 3))                 # [4,5]
nth([10,20,30], 1)                         # 20
```

All errors raise `ChunkbyError` (a `ValueError` subclass).

## License

MIT.

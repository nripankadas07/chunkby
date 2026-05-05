"""Tests for chunkby."""
import pytest

from chunkby import (
    ChunkbyError, batch_by, chunk, drop, nth, pairwise, partition, take, window,
)


class TestChunk:
    def test_basic(self):
        assert list(chunk([1, 2, 3, 4, 5], 2)) == [[1, 2], [3, 4], [5]]

    def test_exact(self):
        assert list(chunk([1, 2, 3, 4], 2)) == [[1, 2], [3, 4]]

    def test_empty(self):
        assert list(chunk([], 3)) == []

    def test_size_one(self):
        assert list(chunk([1, 2, 3], 1)) == [[1], [2], [3]]

    def test_invalid_size(self):
        with pytest.raises(ChunkbyError):
            list(chunk([1, 2], 0))


class TestWindow:
    def test_size_2(self):
        assert list(window([1, 2, 3, 4], 2)) == [(1, 2), (2, 3), (3, 4)]

    def test_step_2(self):
        assert list(window([1, 2, 3, 4, 5], 2, step=2)) == [(1, 2), (3, 4)]

    def test_step_equals_size(self):
        assert list(window([1, 2, 3, 4, 5, 6], 3, step=3)) == [(1, 2, 3), (4, 5, 6)]

    def test_too_short(self):
        # Iterable shorter than window size yields nothing.
        assert list(window([1], 3)) == []

    def test_invalid_size(self):
        with pytest.raises(ChunkbyError):
            list(window([1], 0))

    def test_invalid_step(self):
        with pytest.raises(ChunkbyError):
            list(window([1, 2], 2, step=0))


class TestBatchBy:
    def test_runs(self):
        out = list(batch_by([1, 1, 2, 2, 1], lambda x: x))
        assert out == [[1, 1], [2, 2], [1]]

    def test_predicate(self):
        items = [1, 2, 4, 5, 7, 8]
        out = list(batch_by(items, lambda x: x % 2))
        assert out == [[1], [2, 4], [5, 7], [8]]

    def test_empty(self):
        assert list(batch_by([], lambda x: x)) == []


class TestPartition:
    def test_basic(self):
        evens, odds = partition([1, 2, 3, 4], lambda x: x % 2 == 0)
        assert evens == [2, 4]
        assert odds == [1, 3]

    def test_all_match(self):
        a, b = partition([1, 2, 3], lambda x: x > 0)
        assert a == [1, 2, 3]
        assert b == []

    def test_empty(self):
        a, b = partition([], lambda x: True)
        assert a == [] and b == []


class TestPairwise:
    def test_basic(self):
        assert list(pairwise([1, 2, 3, 4])) == [(1, 2), (2, 3), (3, 4)]

    def test_two(self):
        assert list(pairwise([1, 2])) == [(1, 2)]

    def test_one(self):
        assert list(pairwise([1])) == []

    def test_empty(self):
        assert list(pairwise([])) == []


class TestTakeDropNth:
    def test_take(self):
        assert take([1, 2, 3, 4], 2) == [1, 2]

    def test_take_more_than_available(self):
        assert take([1, 2], 5) == [1, 2]

    def test_take_zero(self):
        assert take([1, 2, 3], 0) == []

    def test_take_negative(self):
        with pytest.raises(ChunkbyError):
            take([1, 2], -1)

    def test_drop(self):
        assert list(drop([1, 2, 3, 4], 2)) == [3, 4]

    def test_drop_more_than_available(self):
        assert list(drop([1, 2], 5)) == []

    def test_drop_negative(self):
        with pytest.raises(ChunkbyError):
            list(drop([1, 2], -1))

    def test_nth(self):
        assert nth([10, 20, 30], 1) == 20

    def test_nth_default(self):
        assert nth([10, 20], 5, default=-1) == -1

    def test_nth_no_default_raises(self):
        with pytest.raises(ChunkbyError):
            nth([1, 2], 5)

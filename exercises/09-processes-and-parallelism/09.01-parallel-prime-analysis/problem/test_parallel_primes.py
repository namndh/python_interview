import pytest

from parallel_primes import PrimeSummary, analyze_chunk, is_prime, parallel_prime_summary


@pytest.mark.parametrize(
    "value,expected",
    [(-1, False), (0, False), (1, False), (2, True), (3, True), (4, False), (97, True), (99, False)],
)
def test_is_prime(value: int, expected: bool) -> None:
    assert is_prime(value) is expected


def test_analyze_chunk() -> None:
    assert analyze_chunk([1, 2, 3, 4, 11]) == PrimeSummary(5, 3, 11)
    assert analyze_chunk([]) == PrimeSummary(0, 0, None)


def test_parallel_summary_combines_chunks() -> None:
    values = list(range(2, 30))
    assert parallel_prime_summary(values, max_workers=2, chunk_size=4) == PrimeSummary(
        item_count=28,
        prime_count=10,
        largest_prime=29,
    )


def test_empty_input_and_configuration() -> None:
    assert parallel_prime_summary([], max_workers=1, chunk_size=1) == PrimeSummary(0, 0, None)
    with pytest.raises(ValueError):
        parallel_prime_summary([2], max_workers=0)
    with pytest.raises(ValueError):
        parallel_prime_summary([2], chunk_size=0)

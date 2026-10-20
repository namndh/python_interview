import itertools

import pytest

from lazy_pipeline import Pipeline, RecordError, batched, read_records, windowed


def test_read_records_is_lazy_and_tracks_physical_line_numbers() -> None:
    records = read_records(iter(['{"id": 1}', "", "not-json"]))
    assert next(records) == {"id": 1}
    with pytest.raises(RecordError) as error:
        next(records)
    assert error.value.line_number == 3
    assert error.value.text == "not-json"


def test_windowed_supports_infinite_iterators() -> None:
    result = list(itertools.islice(windowed(itertools.count(), 3), 3))
    assert result == [(0, 1, 2), (1, 2, 3), (2, 3, 4)]


def test_batched_includes_partial_tail() -> None:
    assert list(batched(iter(range(5)), 2)) == [(0, 1), (2, 3), (4,)]


@pytest.mark.parametrize("function", [windowed, batched])
def test_grouping_rejects_non_positive_size(function: object) -> None:
    with pytest.raises(ValueError):
        list(function([], 0))  # type: ignore[operator]


def test_pipeline_is_lazy_composable_and_one_shot() -> None:
    consumed: list[int] = []

    def source():
        for value in itertools.count():
            consumed.append(value)
            yield value

    pipeline = Pipeline(source()).map(lambda value: value * 2).filter(lambda value: value % 4 == 0).take(3)
    assert consumed == []
    assert list(pipeline) == [0, 4, 8]
    assert consumed == [0, 1, 2, 3, 4]
    assert list(pipeline) == []

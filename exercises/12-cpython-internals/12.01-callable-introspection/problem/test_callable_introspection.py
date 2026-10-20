import pytest

from callable_introspection import analyze_callable, mutable_default_parameters

MODULE_VALUE = 10


def test_analyzes_code_object_and_instructions() -> None:
    captured = 3

    def calculate(value: int) -> int:
        temporary = value + captured
        return max(temporary, MODULE_VALUE)

    analysis = analyze_callable(calculate)
    assert analysis.positional_argument_count == 1
    assert "temporary" in analysis.local_names
    assert analysis.free_variables == ("captured",)
    assert {"max", "MODULE_VALUE"} <= analysis.globals_loaded
    counts = dict(analysis.opcode_counts)
    assert counts["RETURN_VALUE"] == 1
    assert sum(counts.values()) > 5


def test_reports_cell_variables_without_counting_nested_bytecode() -> None:
    def outer(seed: int):
        state = seed

        def inner() -> int:
            return state + 1

        return inner

    analysis = analyze_callable(outer)
    assert analysis.cell_variables == ("state",)
    assert analysis.free_variables == ()


def test_rejects_non_python_functions() -> None:
    with pytest.raises(TypeError):
        analyze_callable(len)


def test_finds_positional_and_keyword_only_mutable_defaults() -> None:
    def example(one=[], two=(), *, three={}, four=None, five=set()):  # noqa: B006
        return one, two, three, four, five

    assert mutable_default_parameters(example) == ("one", "three", "five")

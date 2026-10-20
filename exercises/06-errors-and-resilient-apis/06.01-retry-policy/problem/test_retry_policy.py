import pytest

from retry_policy import RetryEvent, RetryExhausted, RetryPolicy, run_with_retry


@pytest.mark.parametrize(
    "kwargs",
    [
        {"attempts": 0},
        {"initial_delay": -1},
        {"multiplier": 0.5},
        {"max_delay": 0},
    ],
)
def test_policy_validates_configuration(kwargs: dict[str, object]) -> None:
    with pytest.raises(ValueError):
        RetryPolicy(**kwargs)  # type: ignore[arg-type]


def test_retries_with_capped_exponential_backoff() -> None:
    calls = 0
    sleeps: list[float] = []
    events: list[RetryEvent] = []

    def operation() -> str:
        nonlocal calls
        calls += 1
        if calls < 4:
            raise OSError(f"failure {calls}")
        return "ok"

    result = run_with_retry(
        operation,
        RetryPolicy(attempts=4, initial_delay=1, multiplier=3, max_delay=5),
        retry_on=(OSError,),
        sleep=sleeps.append,
        on_retry=events.append,
    )
    assert result == "ok"
    assert sleeps == [1, 3, 5]
    assert [event.attempt for event in events] == [1, 2, 3]


def test_non_retryable_error_propagates_immediately() -> None:
    with pytest.raises(ValueError, match="bad input"):
        run_with_retry(
            lambda: (_ for _ in ()).throw(ValueError("bad input")),
            RetryPolicy(),
            retry_on=(OSError,),
            sleep=lambda _: None,
        )


def test_exhaustion_chains_final_error_without_final_sleep() -> None:
    sleeps: list[float] = []
    with pytest.raises(RetryExhausted) as error:
        run_with_retry(
            lambda: (_ for _ in ()).throw(OSError("down")),
            RetryPolicy(attempts=2, initial_delay=1),
            retry_on=(OSError,),
            sleep=sleeps.append,
        )
    assert isinstance(error.value.__cause__, OSError)
    assert error.value.attempts == 2
    assert sleeps == [1]

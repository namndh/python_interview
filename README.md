# Senior/Principal Python Interview Practice

This repository contains a fourteen-day practice program. Each day is designed for
one focused two-hour session and lives under `exercises/`.

Every exercise contains:

- `problem/readme.md`: requirements, constraints, and discussion prompts.
- `problem/<topic>.py`: the starter implementation with TODOs.
- `problem/test_<topic>.py`: executable acceptance tests.

Install pytest and run one day at a time, for example:

```bash
python -m pytest exercises/01-python-data-model/01.01-value-objects/problem -q
```

The starter implementations are deliberately incomplete, so tests should fail
until the exercise is solved. Avoid reading future tests as an implementation
recipe: begin with the requirements, design the API, and use tests as feedback.

## Daily routine

1. Spend 15 minutes answering the warm-up and prediction questions aloud.
2. Spend 70 minutes implementing the required behavior.
3. Spend 25 minutes running tests, debugging, and adding your own tests.
4. Spend 10 minutes answering the design and trade-off questions aloud.

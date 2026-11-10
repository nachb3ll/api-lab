# API lab

## Install and run

Use Python 3.10 or newer. Create and activate a virtual environment, then install the dependencies:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Run the full suite with `pytest -v`. The tests call the QuickPizza demo API at `https://quickpizza.grafana.com`.

## Input domain model: POST /api/ratings

| Characteristic | Blocks | Values in the test |
|---|---|---|
| C1: stars value | below 1; 1 to 5 (base); above 5 | 0 and 6: `test_stars_out_of_range`; base 3: `test_base_choice_is_saved` |
| C2: stars type | whole number (base); decimal; text; missing | 3.5: `test_decimal_stars_are_refused`; "3": `test_text_stars_are_refused`; omitted: `test_missing_stars_are_refused` |
| C3: pizza | exists (base); does not exist | fixture-created pizza: `test_base_choice_is_saved`; 999999999: `test_unknown_pizza_is_refused` |
| C4: token | own token (base); none; wrong | fixture token: `test_base_choice_is_saved`; no header: `test_rating_without_token_is_refused`; malformed token: `test_rating_with_wrong_token_is_refused` |

The base choice suite uses one test for the base blocks, then one test for every non-base block while keeping the other characteristics at their base. That is 1 + 2 + 3 + 1 + 2 = 9 cases for this model. All combinations would require 3 × 4 × 2 × 3 = 72 cases.

## Tests

Each test states its goal in a comment, checks the response status and important response data, and uses fixtures for the data it needs. Tests create their own practice users and only change ratings they created. The fixtures share one HTTP session so the load-balancer cookie is kept throughout each run.

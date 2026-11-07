from hypothesis import given, strategies as st
from car_insurance_premium_parser import (
    normalize_registration,
    total_claim_amount,
    driver_age,
)


@given(st.text() | st.none())
def test_normalize_registration_no_crash(s):
    try:
        normalize_registration(s)
    except Exception as e:
        assert False, f"normalize_registration crashed with: {e!r}"


@given(st.text() | st.none())
def test_total_claim_amount_no_crash(s):
    try:
        total_claim_amount(s)
    except Exception as e:
        assert False, f"total_claim_amount crashed with: {e!r}"


@given(st.text() | st.none())
def test_driver_age_no_crash(s):
    try:
        driver_age(s)
    except Exception as e:
        assert False, f"driver_age crashed with: {e!r}"


@given(
    st.text("abcdefghijklmnopqrstuvwxyz", min_size=2, max_size=2),
    st.integers(1, 99),
    st.text("abcdefghijklmnopqrstuvwxyz", min_size=1, max_size=2),
    st.integers(1, 9999),
    st.sampled_from([" ", "-", ".", " - "]),
)
def test_normalize_registration_valid_plates(state, rto, series, num, sep):
    raw = f" {state}{sep}{rto:02d}{sep}{series}{sep}{num:04d} "
    expected = f"{state.upper()}{rto:02d}{series.upper()}{num:04d}"
    assert normalize_registration(raw) == expected


@given(st.lists(st.integers(min_value=0, max_value=100000), min_size=1, max_size=8))
def test_total_claim_amount_valid_list(amounts):
    text = ";".join(str(a) for a in amounts)
    assert total_claim_amount(text) == sum(amounts)


@given(
    st.integers(1, 28),
    st.integers(1, 12),
    st.integers(1926, 2040),
)
def test_driver_age_valid_and_future_dates(day, month, year):
    dob = f"{day:02d}/{month:02d}/{year:04d}"
    result = driver_age(dob, current_year=2026)
    if 1906 <= year <= 2026:
        assert result == 2026 - year
    else:
        assert result is None

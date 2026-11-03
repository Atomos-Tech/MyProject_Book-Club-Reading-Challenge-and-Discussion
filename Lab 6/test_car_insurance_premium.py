import pytest
from car_insurance_premium import annual_premium, no_claim_bonus, claim_payout


# annual_premium tests

def test_sedan_no_claims():
    assert annual_premium("sedan", 30, 0, False) == 9600


def test_unknown_car_type():
    with pytest.raises(ValueError, match="unknown car type"):
        annual_premium("convertible", 30, 0, False)


def test_driver_under_18():
    with pytest.raises(ValueError, match="driver too young"):
        annual_premium("hatchback", 17, 0, False)


def test_young_driver_with_anti_theft():
    # hatchback 8000 + 4000 (age < 25) = 12000, 0 claims (-2400) = 9600, anti-theft (-500) = 9100
    assert annual_premium("hatchback", 21, 0, True) == 9100


def test_senior_driver_high_claims():
    # suv 15000 + 2000 (age >= 60) = 17000, claims > 2 (*2) = 34000
    assert annual_premium("suv", 65, 3, False) == 34000


# no_claim_bonus tests

def test_no_bonus():
    assert no_claim_bonus(0) == 0


def test_negative_claim_free_years():
    with pytest.raises(ValueError, match="invalid years"):
        no_claim_bonus(-1)


def test_bonus_5_or_more_years():
    assert no_claim_bonus(5) == 50


def test_bonus_3_to_4_years():
    assert no_claim_bonus(3) == 35


def test_bonus_1_to_2_years():
    assert no_claim_bonus(1) == 20


# claim_payout tests

def test_payout_negative_damage():
    with pytest.raises(ValueError, match="invalid amount"):
        claim_payout(-500, 20000, 1000, False)


def test_payout_total_loss():
    assert claim_payout(8000, 25000, 1000, True) == 25000


def test_payout_below_deductible():
    assert claim_payout(800, 25000, 1000, False) == 0


def test_payout_capped_at_insured_value():
    assert claim_payout(30000, 25000, 1000, False) == 25000


def test_payout_normal_claim():
    assert claim_payout(10000, 25000, 1000, False) == 9000

import pytest
from car_insurance_premium import annual_premium, no_claim_bonus, claim_payout


# annual_premium branch tests

def test_unknown_car_type():
    with pytest.raises(ValueError, match="unknown car type"):
        annual_premium("convertible", 30, 0, False)


def test_driver_under_18():
    with pytest.raises(ValueError, match="driver too young"):
        annual_premium("hatchback", 17, 0, False)


def test_young_driver_zero_claims_anti_theft():
    # age < 25 true, claims == 0 true, has_anti_theft true
    assert annual_premium("hatchback", 18, 0, True) == 9100


def test_middle_age_zero_claims_no_anti_theft():
    # age < 25 false, age >= 60 false, claims == 0 true, has_anti_theft false
    assert annual_premium("sedan", 25, 0, False) == 9600


def test_middle_age_1_or_2_claims():
    # covers branch where claims != 0 and claims <= 2 (16->18)
    assert annual_premium("sedan", 30, 1, False) == 12000
    assert annual_premium("hatchback", 59, 2, True) == 7500


def test_senior_driver_more_than_2_claims():
    # age >= 60 true, claims > 2 true
    assert annual_premium("suv", 60, 3, False) == 34000


# no_claim_bonus branch tests

def test_negative_claim_free_years():
    with pytest.raises(ValueError, match="invalid years"):
        no_claim_bonus(-1)


def test_bonus_5_or_more_years():
    assert no_claim_bonus(5) == 50
    assert no_claim_bonus(8) == 50


def test_bonus_3_to_4_years():
    assert no_claim_bonus(3) == 35
    assert no_claim_bonus(4) == 35


def test_bonus_1_to_2_years():
    assert no_claim_bonus(1) == 20
    assert no_claim_bonus(2) == 20


def test_no_bonus():
    assert no_claim_bonus(0) == 0


# claim_payout branch tests

def test_payout_negative_damage():
    with pytest.raises(ValueError, match="invalid amount"):
        claim_payout(-100, 20000, 1000, False)


def test_payout_negative_deductible():
    with pytest.raises(ValueError, match="invalid amount"):
        claim_payout(5000, 20000, -100, False)


def test_payout_total_loss():
    assert claim_payout(8000, 25000, 1000, True) == 25000


def test_payout_within_deductible():
    assert claim_payout(800, 25000, 1000, False) == 0
    assert claim_payout(1000, 25000, 1000, False) == 0


def test_payout_exceeds_insured_value():
    assert claim_payout(30000, 25000, 1000, False) == 25000


def test_payout_normal_and_boundary():
    assert claim_payout(10000, 25000, 1000, False) == 9000
    assert claim_payout(26000, 25000, 1000, False) == 25000

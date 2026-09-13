from app.services.deal_engine import DealEngine

def test_strong_deal():

    engine = DealEngine()

    result = engine.assess(
        property_data={
            "price": 900000,
            "area": 100,
        },
        investment={
            "score": 85,
        },
        valuation={
            "available": True,
            "valuation_score": 90,
            "upside_percent": 20,
            "confidence": 0.9,
        },
        growth={
            "score": 80,
            "confidence": 0.8,
        },
        risk={
            "score": 20,
            "confidence": 0.9,
        },
        intelligence={
            "infrastructure": {
                "score": 85,
            },
            "pricing": {
                "priced_comparables": 8,
            },
        },
        comparables={
            "count": 8,
        },
    )

    assert result["available"] is True
    assert result["deal_score"] >= 80
    assert result["decision"] == "strong"
    assert result["confidence"] >= 0.8
    assert result["risks"] == []

def test_insufficient_evidence():

    engine = DealEngine()

    result = engine.assess(
        property_data={},
        investment={},
        valuation={
            "available": False,
            "confidence": 0.2,
        },
        growth={
            "score": 40,
            "confidence": 0.2,
        },
        risk={
            "score": 80,
            "confidence": 0.2,
        },
        intelligence={
            "infrastructure": {},
            "pricing": {
                "priced_comparables": 0,
            },
        },
        comparables={
            "count": 0,
        },
    )

    assert result["available"] is False or (
        result["decision"]
        in {
            "insufficient_evidence",
            "unattractive",
            "weak",
        }
    )

    assert "No priced comparable evidence is available" in (
        result["risks"]
    )

def test_deal_score_is_bounded():

    engine = DealEngine()

    result = engine.assess(
        property_data={
            "price": 1000000,
            "area": 100,
        },
        investment={
            "score": 100,
        },
        valuation={
            "available": True,
            "valuation_score": 100,
            "upside_percent": 30,
            "confidence": 1.0,
        },
        growth={
            "score": 100,
            "confidence": 1.0,
        },
        risk={
            "score": 0,
            "confidence": 1.0,
        },
        intelligence={
            "infrastructure": {
                "score": 100,
            },
            "pricing": {
                "priced_comparables": 10,
            },
        },
        comparables={
            "count": 10,
        },
    )

    assert 0 <= result["deal_score"] <= 100


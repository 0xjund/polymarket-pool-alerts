import pytest
from monitor import detect_changes

def test_detect_new_market_high_liquidity():
    """Test that new markets with >50k liquidity trigger alerts"""
    markets = [
        {
            'id': 'test_123',
            'title': 'Test_market',
            'liquidity': 60000,
            'volume': 100000
    }
]

    alerts = detect_changes(markets, threshold_percent=50)

    # 1 new market
    assert len(alerts) == 1
    assert alerts[0]['type'] == 'new_market'
    assert alerts[0]['current_liquidity'] == 60000

def test_detect_new_market_low_liquidity():
    """Test that new markets with <50k liquidity don't trigger alerts"""
    markets = [
        {
        'id': 'test_456',
        'title': 'Small market',
        'liquidity': 10000,
        'volume': 5000        
        }
    ]

    alerts = detect_changes(markets, threshold_percent=50)
    
    # No new alerts
    assert len(alerts) == 0

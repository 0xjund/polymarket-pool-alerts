from typing import List, Dict, Tuple
from database import get_previous_snapshot

def detect_change(markets: List[Dict], threshold_percent: float = 50.0) -> List[Dict]
    """
    Detect significant changes in the market

    Args:
        markets: Current market data from Polymarket API
        threshold_perecent: Percentage change to trigger alert(default is 50%)

    Returns:
        List of markets with significant changes

    """

    alerts = []

    for market in markets:
        market_id = market['id']
        current_liquidity = market.get('liquidity', 0)
        current_volume = market.get('volume', 0)

        # Get previous snapshot from db
        previous = get_previous_snapshot(market_id)

        if not previous:
            # First time seeing the market and no previous data is available
            #  Show new markets with high liquidity
            if current_liquidity > 50000: # New market with > 50k liquidity 
                alerts.append({
                                  'market_id': market_id,
                                  'title': market.get('title', 'Unknown'),
                                  'type': 'new market',
                                  'current_liquidity': current_liquidity,
                                  'current_volume': current_volume
                              })
                continue 
                        
    # Calculate changes
    prev_liqudity = previous['liquidity']
    prev_volume = previous['volume']

    # Avoid dividing by zero
    if prev_liqudity > 0:
        liquidity_change_pct = ((current_liquidity - prev_liqudity) / prev_liqudity) * 100
    else:
        liquidity_change_pct = 0

    if prev_volume > 0:
        volume_change_pct = ((current_volume - prev_volume) / prev_volume) * 100
    else:
        volume_change_pct = 0

    # Check the changes to see if the exceeded the threshold
    if abs(liquidity_change_pct) >= threshold_percent:
        alerts.append({
                          'market_id': market_id,
                          'title': market.get('title', 'Unknown'),
                          'type': 'liquidity_change',
                          'previous_liquidity': prev_liqudity,
                          'current_liquidity': current_liquidity,
                          'change_percent': liquidity_change_pct,
                          'previous_timestamp': previous['timestamp']
                      })

    if abs(volume_change_pct) >= threshold_percent:
        alerts.append({
                              'market_id': market_id,
                              'title': market.get('title', 'Unknown'),
                              'type': 'liquidity_change',
                              'previous_liquidity': prev_liqudity,
                              'current_liquidity': current_liquidity,
                              'change_percent': liquidity_change_pct,
                              'previous_timestamp': previous['timestamp']
                          })

    if abs(volume_change_pct) >= threshold_percent:
        alerts.append({
                            'market_id': market_id,
                            'title': market.get('title', 'Unknown'),
                            'type': 'volume_change',
                            'previous_volume': prev_volume,
                            'current_volume': current_volume,
                            'change_percent': volume_change_pct,
                            'previous_timestamp': previous['timestamp']
                              })

return alerts

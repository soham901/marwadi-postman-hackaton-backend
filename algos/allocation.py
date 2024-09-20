from dataclasses import dataclass

@dataclass
class Hospital:
    name: str
    volume: int
    per_unit_cost: float
    distance: float

def process_allocation(request_volume: int, hospitals: list[Hospital], streagy='greedy' | 'distance' | 'cost') -> float:
    if request_volume < 0: 
        request_volume = 0

    suppliers = []
    if streagy == 'distance':
        hospitals = sorted(hospitals, key=lambda x: x.distance)
    elif streagy == 'greedy':
        hospitals = sorted(hospitals, key=lambda x: x.distance / x.volume, reverse=True)
    elif streagy == 'cost':
        hospitals = sorted(hospitals, key=lambda x: x.per_unit_cost)
    else:
        print('Invalid strategy')
        return 0.0, []
    total_cost = 0.0

    for item in hospitals:
        if request_volume <= 0:
            break
        
        take_volume = min(request_volume, item.volume)
        
        suppliers.append((item, take_volume))
        
        total_cost += item.per_unit_cost * take_volume
        
        request_volume -= take_volume

    return total_cost, suppliers

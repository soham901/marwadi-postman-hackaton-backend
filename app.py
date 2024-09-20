from flask import Flask, request, jsonify
from algos.allocation import Hospital, process_allocation
from geopy.distance import geodesic

app = Flask(__name__)


@app.route('/allocate', methods=['POST'])
def allocate():
    try:
        data = request.json
        request_volume = data['request_volume']
        hospitals_data = data['hospitals']
        distance_priority = data.get('distance_priority', True)
        
        hospitals = [
            Hospital(name=h['name'], volume=h['volume'], per_unit_cost=h['per_unit_cost'], distance=h['distance'])
            for h in hospitals_data
        ]
        
        # for request in requests:
        total_cost, suppliers = process_allocation(request_volume=request_volume, hospitals=hospitals, distance_priority=distance_priority)
    
        allocation_details = [
            {
                'name': supplier.name,
                'volume_taken': volume_taken,
                'distance': supplier.distance,
                'per_unit_cost': supplier.per_unit_cost,
                'total_cost': volume_taken * supplier.per_unit_cost,
            }
            for supplier, volume_taken in suppliers
        ]
        
        response = {
            'total_cost': total_cost,
            'allocation_details': allocation_details
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)


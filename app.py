from flask import Flask, request, jsonify
from algos.allocation import Hospital, process_allocation
from geopy.distance import geodesic

app = Flask(__name__)


# requests = []
# hospitals = [
#     Hospital(name='Jamnagar', volume=2, per_unit_cost=100, distance=10, location=(22.4707, 70.0577)),
#     Hospital(name='Ahmedabad', volume=15, per_unit_cost=200, distance=30, location=(23.0225, 72.5714)),
#     Hospital(name='Bombay', volume=100, per_unit_cost=50, distance=50, location=(19.0760, 72.8777))
# ]


# def calculate_distance(location_a, location_b):
#     return geodesic(location_a, location_b).kilometers


# @app.route("/request", methods=['POST'])
# def add_request():
#     try:
#         data = request.json
#         volume = data['volume']
#         request_location = tuple(data['location'])
        
#         for hospital in hospitals:
#             hospital.distance = calculate_distance(request_location, hospital.location)
        
#         total_cost, suppliers = process_allocation(request_volume=volume, hospitals=hospitals, distance_priority=True)
        
#         allocation_details = [
#             {
#                 'name': supplier.name,
#                 'volume_taken': volume_taken,
#                 'per_unit_cost': supplier.per_unit_cost,
#                 'total_cost': volume_taken * supplier.per_unit_cost,
#                 'distance': supplier.distance
#             }
#             for supplier, volume_taken in suppliers
#         ]
        
#         requests.append({
#             'volume': volume,
#             'location': request_location,
#             'total_cost': total_cost,
#             'allocation_details': allocation_details
#         })
        
#         return jsonify({
#             'total_cost': total_cost,
#             'allocation_details': allocation_details
#         }), 200
    
#     except Exception as e:
#         return jsonify({'error': str(e)}), 400



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


import httpx
from enum import Enum

API_URL = "https://healthcareinfra.soham901.me"


class Strategy(str, Enum):
    greedy = "greedy"
    distance = "distance"
    cost = "cost"


user_data = {"email": "testuser@example.com", "password": "testpassword"}

api_user_data = {"email": "string", "password": "string"}

hospitals_data = [
    {
        "name": "Rajkot hospital",
        "address": "rajkot",
        "latitude": 22.308155,
        "longitude": 70.800705,
    },
    {
        "name": "Ahmedabad hospital",
        "address": "ahmedabad",
        "latitude": 23.033863,
        "longitude": 72.585022,
    },
    {
        "name": "Jaipur hospital",
        "address": "jaipur",
        "latitude": 26.907524,
        "longitude": 75.739639,
    },
]

medicines_data = [
    {
        "name": "Paracetamol",
        "description": "Pain reliever",
        "quantity": 100,
        "price_per_unit": 150,
        "hospital_id": 1,
    },
    {
        "name": "Paracetamol",
        "description": "Pain reliever",
        "quantity": 200,
        "price_per_unit": 100,
        "hospital_id": 2,
    },
    {
        "name": "Paracetamol",
        "description": "Pain reliever",
        "quantity": 50,
        "price_per_unit": 50,
        "hospital_id": 3,
    },
]

request_scenarios = [
    {
        "hospital_id": 1,
        "name": "Paracetamol",
        "quantity": 5,
        "strategy": Strategy.distance,
    },
    {
        "hospital_id": 1,
        "name": "Paracetamol",
        "quantity": 10,
        "strategy": Strategy.cost,
    },
    {
        "hospital_id": 1,
        "name": "Paracetamol",
        "quantity": 15,
        "strategy": Strategy.greedy,
    },
    {
        "hospital_id": 2,
        "name": "Paracetamol",
        "quantity": 300,
        "strategy": Strategy.distance,
    },  # Test over-allocation
]


def setup_test_environment():
    print("Setting up test environment...")

    # Register and login
    response = httpx.post(f"{API_URL}/register", json=api_user_data)
    if response.status_code != 201:
        raise Exception(f"Failed to register api user: {response.text}")
    print("API User registered successfully")

    # Register and login
    response = httpx.post(f"{API_URL}/register", json=user_data)
    if response.status_code != 201:
        raise Exception(f"Failed to register normal user: {response.text}")
    print("User registered successfully")

    response = httpx.post(f"{API_URL}/login", json=user_data)
    if response.status_code != 200:
        raise Exception(f"Failed to login: {response.text}")
    access_token = response.json()["access_token"]
    print("Logged in successfully")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "accept": "application/json",
        "Content-Type": "application/json",
    }

    # Add hospitals
    for hospital in hospitals_data:
        response = httpx.post(f"{API_URL}/hospitals/", json=hospital, headers=headers)
        if response.status_code != 201:
            raise Exception(
                f"Failed to add hospital {hospital['name']}: {response.text}"
            )
        print(f"Added hospital: {hospital['name']}")

    # Add medicines
    for medicine in medicines_data:
        response = httpx.post(f"{API_URL}/medicines/", json=medicine, headers=headers)
        if response.status_code != 200:
            raise Exception(
                f"Failed to add medicine for hospital {medicine['hospital_id']}: {response.text}"
            )
        print(
            f"Added medicine {medicine['name']} for hospital {medicine['hospital_id']}"
        )

    return headers


def create_request_and_get_allocation(headers, request_data):
    print(f"\nCreating request: {request_data}")
    response = httpx.post(f"{API_URL}/requests/", json=request_data, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to create medicine request: {response.text}")
    print("Medicine request created successfully")

    response = httpx.get(f"{API_URL}/allocations/", headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve allocations: {response.text}")
    allocations = response.json()
    print("Allocation result:")
    print(allocations[-1])  # Print the latest allocation
    return allocations[-1]


def run_tests():
    try:
        headers = setup_test_environment()

        for scenario in request_scenarios:
            allocation = create_request_and_get_allocation(headers, scenario)

            # Additional checks based on the scenario
            if scenario["strategy"] == Strategy.distance:
                assert allocation["suppliers"][0]["distance"] == min(
                    h["distance"] for h in allocation["suppliers"]
                ), "Distance strategy failed"
            elif scenario["strategy"] == Strategy.cost:
                assert allocation["suppliers"][0]["per_unit_cost"] == min(
                    h["per_unit_cost"] for h in allocation["suppliers"]
                ), "Cost strategy failed"

            if scenario["quantity"] > sum(m["quantity"] for m in medicines_data):
                assert (
                    sum(s["volume_allocated"] for s in allocation["suppliers"])
                    < scenario["quantity"]
                ), "Over-allocation not handled correctly"

        print("\nAll tests completed successfully!")

    except Exception as e:
        print(f"Error during test execution: {str(e)}")


if __name__ == "__main__":
    run_tests()

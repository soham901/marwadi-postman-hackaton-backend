# Healthcare Resource Allocation System

## Project Overview

This project focuses on optimizing healthcare resource allocation using different strategies like cost, distance, and greedy approaches. It addresses the critical issue of resource shortages in healthcare, especially during emergencies.

## Features

- **Resource Allocation**: Allocates hospital resources (e.g., oxygen, beds) using a strategy-based approach (distance, cost, greedy).
- **Real-Time Data**: Tracks hospital resources in real-time and optimizes resource distribution based on the selected strategy.
- **Supplier Management**: Manages and tracks the volume allocated to each hospital and the associated costs.
- **Predictive Analysis**: Utilizes geolocation data for distance-based allocations and cost calculations.
- **Emergency Response**: Prioritizes resource allocation during emergencies using real-time data.
- **Traffic Handling**: Each request is processed as a background job to efficiently manage high traffic and ensure smooth performance.

## Tech Stack

- **Backend**: FastAPI (Python), running background jobs for resource allocation.
- **Frontend**: Next.js (React-based framework) for the admin dashboard and visualization.
- **Database**: PostgreSQL for storing hospital and resource data.
- **API Testing**: Postman for collabrating and testing APIs, Open API (Swagger UI).
- **Reverse Proxy**: Caddy, managing HTTPS and serving the app.
- **Distance Calculation**: Geopy library for calculating distances between hospitals.
- **ORM**: SQLModel, simplifying database queries and operations.
- **CI/CD**: GitHub Actions for continuous integration and deployment.
- **Hosting**: AWS EC2 for cloud infrastructure.

## Allocation Strategy Options

- **Greedy**: Allocates resources based on the highest value (e.g., cost per distance) in descending order.
- **Distance-Based**: Prioritizes hospitals closest to the resource.
- **Cost-Based**: Focuses on the least expensive options for resource allocation.

## Links

- **Postman Workspace**: [Postman Workspace](https://app.getpostman.com/join-team?invite_code=45048bec-261c-44e9-ab1c-3b29ceba48b9)
- **Backend Repository**: [GitHub - Backend](https://github.com/soham901/marwadi-postman-hackaton-backend)
- **Frontend Repository**: [GitHub - Frontend](https://github.com/EhsaasChaudhary/sanjivani)
- **API Documentation (Swagger UI)**: [API Docs](https://healthcareinfra.soham901.me/docs)

# Rescue Radar API

This is the Flask API for the Rescue Radar project. It serves data from a locally maintained Petfinder SQLite database.

## Endpoints

- `/api/animals` – Get all animals  
  Optional query param: `?type=Dog`  

- `/api/breeds/count` – Get breed counts by type  
  Example: `/api/breeds/count?type=Dog`

- `/api/organizations` – Get all organizations

## Getting Started

1. Create a virtual environment (optional but recommended)
2. Install dependencies:

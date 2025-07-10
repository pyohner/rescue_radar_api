# Rescue Radar API

This is the Flask API for the Rescue Radar project. It serves data from a locally maintained Petfinder SQLite database.

Only collects data from the Orlando, FL, area.

## Endpoints

- `/api/animals` – Get all animals  
  Optional query param: `?type=Dog`  

- `/api/breeds/count` – Get breed counts by type  
  Example: `/api/breeds/count?type=Dog`

- `/api/organizations` – Get all organizations

- `/api/animals/daily-counts` – Get daily counts of animals (optionally filtered by type)

- `/api/animals/size-distribution` – Get size distribution for a type

- `/api/animals/type-distribution` – Get distribution by animal type

- `/api/animals/environment-stats` – Get summed environment data (children, dogs, cats) by type

- `/api/animals/readiness` – Get readiness stats (spayed/neutered, house-trained, shots current) by type

- `/api/organizations/animal-counts` – Get animal counts per organization

- `/api/animals/todays-rescues` – Get summary and top organization for the latest rescue date

## Getting Started

1. Create a virtual environment (optional but recommended)

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root:

   ```env
   DATABASE_PATH=C:/Your/Database/Path/petfinder_data.db
   ```

4. Run the API server:

   ```bash
   python api_server.py
   ```

The server will start on `http://localhost:5000`.

## Notes

- Ensure the SQLite database is up-to-date and contains the `animals` and `organizations` tables.
- Add `.env` to `.gitignore` to avoid committing local paths or secrets.

## Related Repositories

- [Rescue Radar App (Frontend)](https://github.com/pyohner/rescue_radar_app)
- [Petfinder Data Collector](https://github.com/pyohner/petfinder-data-collector)

## License

This project is licensed under the MIT License.
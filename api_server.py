from flask import Flask, jsonify, request
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
DB_FILE = "C:/Users/yohnep25/PycharmProjects/databases/petfinder_data.db"


def query_db(query, args=(), one=False):
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.execute(query, args)
        rows = cur.fetchall()
        return (rows[0] if rows else None) if one else rows


@app.route("/api/animals", methods=["GET"])
def get_animals():
    animal_type = request.args.get("type")
    if animal_type:
        rows = query_db("""
            SELECT a.*, o.name AS organization_name
            FROM animals a
            LEFT JOIN organizations o ON a.organization_id = o.id
            WHERE a.type = ?
        """, (animal_type,))
    else:
        rows = query_db("""
            SELECT a.*, o.name AS organization_name
            FROM animals a
            LEFT JOIN organizations o ON a.organization_id = o.id
        """)
    return jsonify([dict(row) for row in rows])


@app.route("/api/breeds/count", methods=["GET"])
def get_breed_counts():
    animal_type = request.args.get("type", "Dog")
    rows = query_db("""
        SELECT primary_breed, COUNT(*) as count
        FROM animals
        WHERE type = ?
        GROUP BY primary_breed
        ORDER BY count DESC
    """, (animal_type,))
    return jsonify([dict(row) for row in rows])


@app.route("/api/organizations", methods=["GET"])
def get_organizations():
    rows = query_db("SELECT * FROM organizations")
    return jsonify([dict(row) for row in rows])


@app.route("/api/animals/daily-counts")
def daily_counts():
    animal_type = request.args.get("type")  # e.g., 'Dog', 'Cat', etc.

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    if animal_type:
        cur.execute("""
            SELECT substr(published_at, 1, 10) AS date, COUNT(*) AS count
            FROM animals
            WHERE published_at IS NOT NULL AND type = ?
            GROUP BY date
            ORDER BY date
        """, (animal_type,))
    else:
        cur.execute("""
            SELECT substr(published_at, 1, 10) AS date, COUNT(*) AS count
            FROM animals
            WHERE published_at IS NOT NULL
            GROUP BY date
            ORDER BY date
        """)

    data = cur.fetchall()
    conn.close()

    return jsonify([
        {"date": row[0], "count": row[1]} for row in data
    ])


@app.route("/api/animals/size-distribution")
def size_distribution():
    animal_type = request.args.get("type")
    rows = query_db("""
        SELECT size, COUNT(*) as count
        FROM animals
        WHERE type = ?
        GROUP BY size
        ORDER BY count DESC
    """, (animal_type,))
    return jsonify([dict(row) for row in rows])


@app.route("/api/animals/type-distribution")
def type_distribution():
    rows = query_db("""
        SELECT type, COUNT(*) as count
        FROM animals
        GROUP BY type
        ORDER BY count DESC
    """)
    return jsonify([dict(row) for row in rows])


@app.route("/api/animals/environment-stats")
def environment_stats():
    animal_type = request.args.get("type")
    rows = query_db("""
        SELECT
            SUM(environment_children) as children,
            SUM(environment_dogs) as dogs,
            SUM(environment_cats) as cats
        FROM animals
        WHERE type = ?
    """, (animal_type,))
    return jsonify(dict(rows[0]) if rows else {})


@app.route("/api/animals/readiness")
def readiness():
    animal_type = request.args.get("type")
    rows = query_db("""
        SELECT
            SUM(spayed_neutered) as spayed_neutered,
            SUM(house_trained) as house_trained,
            SUM(shots_current) as shots_current
        FROM animals
        WHERE type = ?
    """, (animal_type,))
    return jsonify(dict(rows[0]) if rows else {})


@app.route("/api/organizations/animal-counts")
def org_animal_counts():
    rows = query_db("""
        SELECT o.name, COUNT(a.id) as count
        FROM organizations o
        JOIN animals a ON o.id = a.organization_id
        GROUP BY o.name
        ORDER BY count DESC
    """)
    return jsonify([dict(row) for row in rows])


@app.route("/api/animals/todays-rescues")
def todays_rescues():
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        # 1. Get the most recent published_at date (date-only)
        cur.execute("SELECT MAX(substr(published_at, 1, 10)) FROM animals")
        latest_date = cur.fetchone()[0]
        if not latest_date:
            return jsonify({"message": "No data available"}), 404

        # 2. Get animals published on that date
        cur.execute("""
            SELECT a.*, o.name AS organization_name
            FROM animals a
            LEFT JOIN organizations o ON a.organization_id = o.id
            WHERE substr(a.published_at, 1, 10) = ?
        """, (latest_date,))
        all_today = cur.fetchall()

        if not all_today:
            return jsonify({"message": "No animals found for latest date"}), 404

        # 3. Animal type breakdown
        type_counts = {}
        org_counts = {}
        org_type_counts = {}

        for row in all_today:
            animal_type = row["type"]
            org_id = row["organization_id"]
            org_name = row["organization_name"]

            type_counts[animal_type] = type_counts.get(animal_type, 0) + 1

            if org_id:
                org_counts[org_id] = org_counts.get(org_id, {"name": org_name, "count": 0})
                org_counts[org_id]["count"] += 1

        # 4. Find top org
        top_org_id = max(org_counts.items(), key=lambda x: x[1]["count"])[0]
        top_org_name = org_counts[top_org_id]["name"]
        top_org_total = org_counts[top_org_id]["count"]

        # 5. Breakdown of types for top org
        for row in all_today:
            if row["organization_id"] == top_org_id:
                org_type_counts[row["type"]] = org_type_counts.get(row["type"], 0) + 1

        return jsonify({
            "date": latest_date,
            "total": len(all_today),
            "typeBreakdown": type_counts,
            "topOrganization": {
                "id": top_org_id,
                "name": top_org_name,
                "total": top_org_total,
                "typeBreakdown": org_type_counts
            }
        })


if __name__ == "__main__":
    app.run(debug=True)

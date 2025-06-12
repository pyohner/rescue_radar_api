from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)
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
        rows = query_db("SELECT * FROM animals WHERE type = ?", (animal_type,))
    else:
        rows = query_db("SELECT * FROM animals")
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

if __name__ == "__main__":
    app.run(debug=True)

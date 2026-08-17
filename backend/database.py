import sqlite3

DATABASE = "naturelens.db"

def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS observations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            name TEXT NOT NULL,
            scientific_name TEXT,
            category TEXT,
            confidence INTEGER,
            description TEXT,
            ecological_role TEXT,
            interesting_fact TEXT,
            look_closer TEXT,
            nature_mission TEXT,
            mission_type TEXT,
            xp_reward INTEGER DEFAULT 10,
            connection_message TEXT,
            safety_note TEXT,
            latitude REAL,
            longitude REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    columns = {row["name"] for row in conn.execute("PRAGMA table_info(observations)")}
    if "user_id" not in columns:
        conn.execute("ALTER TABLE observations ADD COLUMN user_id TEXT NOT NULL DEFAULT 'legacy'")
    conn.commit()
    conn.close()

def save_observation(data, user_id):
    conn = get_connection()
    cursor = conn.execute("""
        INSERT INTO observations (
            user_id, name, scientific_name, category, confidence, description,
            ecological_role, interesting_fact, look_closer, nature_mission,
            mission_type, xp_reward, connection_message, safety_note,
            latitude, longitude
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id, data.get("name"), data.get("scientific_name"),
        data.get("category"), data.get("confidence"), data.get("description"),
        data.get("ecological_role"), data.get("interesting_fact"),
        data.get("look_closer"), data.get("nature_mission"),
        data.get("mission_type"), data.get("xp_reward", 10),
        data.get("connection_message"), data.get("safety_note"),
        data.get("latitude"), data.get("longitude")
    ))
    conn.commit()
    observation_id = cursor.lastrowid
    conn.close()
    return observation_id

def get_observations(user_id):
    conn = get_connection()
    rows = conn.execute("""
        SELECT * FROM observations
        WHERE user_id = ?
        ORDER BY created_at DESC
    """, (user_id,)).fetchall()
    conn.close()
    return [dict(row) for row in rows]

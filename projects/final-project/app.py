#!/usr/bin/env python3
"""
Моя Коллекция — итоговый проект курса DevOps для детей
REST API для хранения списка любимых вещей.
"""
import os, sqlite3
from flask import Flask, jsonify, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
DB_PATH = os.environ.get("DB_PATH", "collection.db")


def get_db():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    return db


def init_db():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            name    TEXT NOT NULL,
            emoji   TEXT DEFAULT '📦',
            comment TEXT DEFAULT ''
        )
    """)
    db.commit()
    db.close()


@app.route("/")
def home():
    return jsonify({
        "сервис":  os.environ.get("APP_NAME", "МояКоллекция"),
        "версия":  "1.0",
        "маршруты": [
            "GET    /items         — все предметы",
            "GET    /items/<id>    — один предмет",
            "POST   /items         — добавить предмет",
            "PUT    /items/<id>    — изменить предмет",
            "DELETE /items/<id>    — удалить предмет",
        ]
    })


@app.route("/items", methods=["GET"])
def list_items():
    db = get_db()
    rows = db.execute("SELECT * FROM items ORDER BY id").fetchall()
    db.close()
    return jsonify({"items": [dict(r) for r in rows], "всего": len(rows)})


@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    db = get_db()
    row = db.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
    db.close()
    if row is None:
        return jsonify({"ошибка": f"Предмет {item_id} не найден"}), 404
    return jsonify(dict(row))


@app.route("/items", methods=["POST"])
def add_item():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"ошибка": "Нужно поле 'name'"}), 400
    db = get_db()
    cur = db.execute(
        "INSERT INTO items (name, emoji, comment) VALUES (?, ?, ?)",
        (data["name"], data.get("emoji", "📦"), data.get("comment", ""))
    )
    db.commit()
    row = db.execute("SELECT * FROM items WHERE id = ?", (cur.lastrowid,)).fetchone()
    db.close()
    return jsonify(dict(row)), 201


@app.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    data = request.get_json() or {}
    db = get_db()
    row = db.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
    if row is None:
        db.close()
        return jsonify({"ошибка": f"Предмет {item_id} не найден"}), 404
    db.execute("UPDATE items SET name=?, emoji=?, comment=? WHERE id=?",
               (data.get("name", row["name"]),
                data.get("emoji", row["emoji"]),
                data.get("comment", row["comment"]),
                item_id))
    db.commit()
    updated = db.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
    db.close()
    return jsonify(dict(updated))


@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    db = get_db()
    row = db.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
    if row is None:
        db.close()
        return jsonify({"ошибка": f"Предмет {item_id} не найден"}), 404
    db.execute("DELETE FROM items WHERE id = ?", (item_id,))
    db.commit()
    db.close()
    return jsonify({"удалено": dict(row)})


if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("APP_PORT", 8080))
    print(f"🚀 Запущен: http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)

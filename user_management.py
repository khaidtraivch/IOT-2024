from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DATABASE = 'user_management.db'

# Khởi tạo cơ sở dữ liệu và tạo bảng người dùng
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL UNIQUE,
                        email TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Thêm người dùng
@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return jsonify({'id': user_id, 'username': username, 'email': email}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'User with this username or email already exists'}), 409

# Sửa thông tin người dùng
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET username = ?, email = ?, password = ? WHERE id = ?", (username, email, password, user_id))
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'id': user_id, 'username': username, 'email': email}), 200

# Xóa người dùng
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'message': 'User deleted successfully'}), 200

# Xem danh sách người dùng
@app.route('/users', methods=['GET'])
def list_users():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email FROM users")
    users = cursor.fetchall()
    conn.close()
    return jsonify([{'id': u[0], 'username': u[1], 'email': u[2]} for u in users])

if __name__ == '__main__':
    init_db()  # Khởi tạo cơ sở dữ liệu
    app.run(debug=True)

const apiUrl = "http://127.0.0.1:5000/users";

// Hiển thị danh sách người dùng
async function loadUsers() {
    const response = await fetch(apiUrl);
    const users = await response.json();
    const userList = document.getElementById("userList");
    userList.innerHTML = '';

    users.forEach(user => {
        const li = document.createElement("li");
        li.innerHTML = `
            ${user.username} (${user.email})
            <button class="edit" onclick="editUser(${user.id}, '${user.username}', '${user.email}')">Edit</button>
            <button onclick="deleteUser(${user.id})">Delete</button>
        `;
        userList.appendChild(li);
    });
}

// Thêm hoặc sửa người dùng
document.getElementById("userForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    const userId = document.getElementById("userId").value;
    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const method = userId ? "PUT" : "POST";
    const url = userId ? `${apiUrl}/${userId}` : apiUrl;

    await fetch(url, {
        method: method,
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, email, password }),
    });

    document.getElementById("userForm").reset();
    document.getElementById("userId").value = '';
    loadUsers();
});

// Xóa người dùng
async function deleteUser(id) {
    await fetch(`${apiUrl}/${id}`, { method: "DELETE" });
    loadUsers();
}

// Chỉnh sửa người dùng
function editUser(id, username, email) {
    document.getElementById("userId").value = id;
    document.getElementById("username").value = username;
    document.getElementById("email").value = email;
}

// Tải danh sách người dùng khi trang được tải
document.addEventListener("DOMContentLoaded", loadUsers);

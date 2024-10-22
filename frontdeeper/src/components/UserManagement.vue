<template>
  <div class="container mt-5">
    <div class="header">
      <h2>Users Management</h2>
      <button type="button" class="btn-create" @click="openModal">
        + Create User
      </button>
    </div>
    <div class="table-container">
      <h3 class="table-title">List of Users</h3>
      <div class="table-responsive">
        <table class="table">
          <thead>
            <tr>
              <th>UserName</th>
              <th>Roles</th>
              <th>Timezone</th>
              <th>Is Active?</th>
              <th>Last updated at</th>
              <th>Created at</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.username">
              <td>
                <router-link
                  :to="{
                    name: 'AboutUser',
                    params: { username: user.username },
                  }"
                  class="user-link"
                >
                  {{ user.username }}
                </router-link>
              </td>
              <td>
                <span v-for="role in user.roles" :key="role"
                  >{{ role }}<br
                /></span>
              </td>
              <td>{{ user.preferences.timezone }}</td>
              <td>{{ user.active ? "Yes" : "No" }}</td>
              <td>{{ formatDate(user.updated_ts) }}</td>
              <td>{{ formatDate(user.created_ts) }}</td>
              <td>
                <div class="btn-group">
                  <button
                    type="button"
                    class="btn btn-primary"
                    @click="confirmEditUser(user)"
                  >
                    Edit
                  </button>
                  <button
                    type="button"
                    class="btn btn-danger"
                    @click="confirmDeleteUser(user.username)"
                  >
                    Delete
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <FormCreateUser
      v-if="isModalVisible"
      :isVisible="isModalVisible"
      :onClose="closeModal"
      :userData="selectedUser"
      :isEditing="isEditing"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import userService from "../services/usersService";
import FormCreateUser from "./FormCreateUser.vue";
import Swal from "sweetalert2"; // Importa SweetAlert2

const users = ref([]);
const isModalVisible = ref(false);
const selectedUser = ref(null);
const isEditing = ref(false);

const formatDate = (timestamp) => {
  const date = new Date(timestamp * 1000);
  return date.toLocaleString();
};

const fetchUsers = async () => {
  try {
    const response = await userService.getUsers();
    users.value = response.data;
  } catch (error) {
    console.error("Error fetching users:", error);
  }
};

// Nueva función para confirmar la edición del usuario
const confirmEditUser = (user) => {
  Swal.fire({
    title: "Are you sure you want to edit this user?",
    text: "You can change the user details.",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    confirmButtonText: "Yes, edit it!",
  }).then((result) => {
    if (result.isConfirmed) {
      editUser(user); // Si el usuario confirma, llama a la función editUser
    }
  });
};

// Nueva función para confirmar la eliminación del usuario
const confirmDeleteUser = (username) => {
  Swal.fire({
    title: "Are you sure?",
    text: `You won't be able to revert this!`,
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#d33",
    cancelButtonColor: "#3085d6",
    confirmButtonText: "Yes, delete it!",
  }).then(async (result) => {
    if (result.isConfirmed) {
      await deleteUser(username);
    }
  });
};

const editUser = (user) => {
  selectedUser.value = user;
  isEditing.value = true;
  isModalVisible.value = true;
};

const deleteUser = async (username) => {
  try {
    await userService.deleteUser(username);
    await fetchUsers();
  } catch (error) {
    console.error("Error deleting user:", error);
  }
};

const openModal = () => {
  selectedUser.value = null;
  isEditing.value = false;
  isModalVisible.value = true;
};

const closeModal = () => {
  isModalVisible.value = false;
  selectedUser.value = null;
  isEditing.value = false;
};

// Llamar a fetchUsers al montar el componente
onMounted(fetchUsers);
</script>

<style>
.container {
  max-width: 1100px;
  margin: 0 auto;
  background-color: #f5f5f5;
  border-radius: 10px;
  padding: 30px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  font-family: "Inter", sans-serif;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

h2 {
  font-size: 28px;
  font-weight: 600;
  color: #333;
}

.btn-create {
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 10px 15px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-create:hover {
  background-color: #218838;
}

.table-container {
  margin-top: 30px;
}

.table-title {
  font-size: 22px;
  font-weight: 500;
  color: #555;
  margin-bottom: 15px;
}

.table {
  width: 100%;
  border-collapse: collapse;
  background-color: white;
  border-radius: 10px;
  overflow: hidden;
}

.table th,
.table td {
  padding: 15px 20px;
  text-align: left;
  vertical-align: middle;
  font-size: 16px;
}

.table th {
  background-color: #007bff;
  color: white;
  font-weight: 600;
}

.table td {
  color: #333;
  border-bottom: 1px solid #ddd;
}

.table-striped tbody tr:nth-of-type(odd) {
  background-color: #f9f9f9;
}

.user-link {
  color: #007bff;
  text-decoration: none;
  font-weight: 500;
}

.user-link:hover {
  text-decoration: underline;
}

.btn-group {
  display: flex;
  gap: 10px;
}

.btn {
  padding: 8px 12px;
  font-size: 14px;
  border-radius: 5px;
  cursor: pointer;
  border: none;
  transition: background-color 0.3s ease;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.btn-danger {
  background-color: #dc3545;
  color: white;
}

.btn-danger:hover {
  background-color: #c82333;
}

@media (max-width: 768px) {
  .container {
    padding: 20px;
  }

  .table-responsive {
    overflow-x: auto;
  }
}
</style>

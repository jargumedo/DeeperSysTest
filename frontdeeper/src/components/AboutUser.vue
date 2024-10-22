<template>
  <div class="container">
    <button type="button" class="btn btn-secondary back-btn" @click="goBack">
      Back to Home
    </button>
    <div class="user-details" v-if="user.username">
      <h2>User Details for {{ user.username }}</h2>
      <div class="details">
        <p><strong>Roles:</strong> {{ user.roles.join(", ") }}</p>
        <p><strong>Timezone:</strong> {{ user.preferences.timezone }}</p>
        <p>
          <strong>Status:</strong> {{ user.active ? "Active" : "Inactive" }}
        </p>
        <p><strong>Created at:</strong> {{ formatDate(user.created_ts) }}</p>
        <p>
          <strong>Last updated at:</strong> {{ formatDate(user.updated_ts) }}
        </p>
      </div>

      <div class="btn-group">
        <button type="button" class="btn btn-primary" @click="confirmEditUser">
          Edit
        </button>
        <button
          type="button"
          @click="confirmDeleteUser(user.username)"
          class="btn btn-danger"
        >
          Delete
        </button>
      </div>

      <!-- Modal para editar usuario -->
      <FormCreateUser
        v-if="isModalVisible"
        :isVisible="isModalVisible"
        :onClose="closeModal"
        :userData="user"
        :isEditing="true"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import userService from "../services/usersService";
import FormCreateUser from "./FormCreateUser.vue";
import Swal from "sweetalert2"; // Importa SweetAlert2

const route = useRoute();
const router = useRouter();
const user = ref({
  username: "",
  roles: [],
  preferences: {
    timezone: "",
  },
  active: false,
  created_ts: "",
  updated_ts: "",
});
const isModalVisible = ref(false);

const fetchUserDetails = async () => {
  try {
    const response = await userService.getUser(route.params.username);
    user.value = response.data || {
      username: "",
      roles: [],
      preferences: {
        timezone: "",
      },
      active: false,
      created_ts: "",
      updated_ts: "",
    };
  } catch (error) {
    console.error("Error fetching user details:", error);
  }
};

const formatDate = (timestamp) => {
  const date = new Date(timestamp * 1000);
  return date.toLocaleString();
};

// Nueva función para confirmar la edición del usuario
const confirmEditUser = () => {
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
      openEditModal(); // Si el usuario confirma, abre el modal
    }
  });
};

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

const deleteUser = async (username) => {
  try {
    await userService.deleteUser(username);
    router.push("/");
    Swal.fire("Deleted!", "User has been deleted.", "success");
  } catch (error) {
    console.error("Error deleting user:", error);
    Swal.fire("Error!", "There was an error deleting the user.", "error");
  }
};

const openEditModal = () => {
  isModalVisible.value = true;
};

const closeModal = () => {
  isModalVisible.value = false;
};

const goBack = () => {
  router.push("/");
};

onMounted(fetchUserDetails);
</script>

<style scoped>
html,
body {
  height: 100%;
  margin: 0;
  font-family: "Roboto", sans-serif;
  background-color: #f3f4f6;
}

.container {
  position: relative;
  max-width: 700px;
  margin: auto;
  padding: 20px;
}

.back-btn {
  position: absolute;
  top: 20px;
  left: 20px;
  padding: 10px 15px;
  background-color: #6b7280;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.back-btn:hover {
  background-color: #4b5563;
  transform: translateY(-2px);
}

.user-details {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin-top: 80px;
  padding: 30px;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
  transition: transform 0.3s ease-in-out;
}

h2 {
  margin-bottom: 25px;
  color: #111827;
  font-size: 24px;
  font-weight: 600;
}

.details {
  width: 100%;
  margin-bottom: 25px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 20px;
  background-color: #f9fafb;
}

.details p {
  margin: 12px 0;
  font-size: 16px;
  color: #374151;
}

strong {
  color: #111827;
  font-weight: 500;
}

.btn-group {
  display: flex;
  justify-content: center;
  gap: 15px;
}

.btn {
  padding: 12px 20px;
  font-size: 16px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary {
  background-color: #3b82f6;
  color: white;
}

.btn-primary:hover {
  background-color: #2563eb;
  transform: translateY(-2px);
}

.btn-danger {
  background-color: #ef4444;
  color: white;
}

.btn-danger:hover {
  background-color: #dc2626;
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .container {
    width: 90%;
  }

  .details p {
    font-size: 14px;
  }
}
</style>

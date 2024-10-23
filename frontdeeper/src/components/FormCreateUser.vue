<template>
  <div v-if="isVisible" class="modal">
    <div class="modal-content">
      <span class="close" @click="closeModal">&times;</span>
      <h2 class="modal-title">{{ isEditing ? "Edit User" : "Create User" }}</h2>
      <form @submit.prevent="submitForm">
        <div class="form-group">
          <label for="username">Username:</label>
          <input
            v-model="formUser.username"
            type="text"
            id="username"
            required
            class="form-control"
          />
        </div>
        <div class="form-group">
          <label for="password">Password:</label>
          <input
            v-model="formUser.password"
            type="password"
            id="password"
            required
            class="form-control"
          />
        </div>
        <div class="form-group">
          <label>Roles:</label><br />
          <label>
            <input type="checkbox" value="admin" v-model="formUser.roles" />
            Admin
          </label>
          <label>
            <input type="checkbox" value="manager" v-model="formUser.roles" />
            Manager
          </label>
          <label>
            <input type="checkbox" value="tester" v-model="formUser.roles" />
            Tester
          </label>
        </div>
        <div class="form-group">
          <label for="timezone">Timezone:</label>
          <input
            v-model="formUser.preferences.timezone"
            type="text"
            id="timezone"
            required
            class="form-control"
          />
        </div>
        <div class="btn-group">
          <button type="submit" class="btn btn-primary">
            {{ isEditing ? "Edit" : "Create" }}
          </button>
          <button type="button" @click="closeModal" class="btn btn-secondary">
            Cancel
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, defineProps } from "vue";
import userService from "../services/usersService";
import { useRouter } from "vue-router";

const props = defineProps({
  isVisible: Boolean,
  onClose: Function,
  userData: Object,
  isEditing: Boolean,
});

const router = useRouter();
const formUser = ref({
  username: "",
  password: "",
  roles: [], // Inicialmente un arreglo vacío para los roles seleccionados
  preferences: { timezone: "" },
});

// Rellena el formulario con los datos del usuario si se está editando
watch(
  () => props.userData,
  (newValue) => {
    if (newValue) {
      formUser.value = { ...newValue };
    }
  },
  { immediate: true }
);

const closeModal = () => {
  if (typeof props.onClose === "function") {
    props.onClose();
  }
};

const submitForm = async () => {
  try {
    if (props.isEditing) {
      await userService.updateUser(props.userData.username, formUser.value);
    } else {
      await userService.addUser(formUser.value);
    }
    closeModal();
    router.push("/");
  } catch (error) {
    console.error("Error submitting form:", error);
  }
};
</script>

<style scoped>
.modal {
  display: flex;
  position: fixed;
  z-index: 1000;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: white;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  width: 100%;
  max-width: 500px;
  position: relative;
  transition: all 0.3s ease;
  animation: slide-down 0.3s ease-out;
}

@keyframes slide-down {
  from {
    transform: translateY(-20%);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.modal-title {
  margin-bottom: 20px;
  text-align: center;
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
}

.close {
  cursor: pointer;
  position: absolute;
  top: 10px;
  right: 15px;
  font-size: 24px;
  color: #999;
  transition: color 0.3s ease;
}

.close:hover {
  color: #333;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  font-size: 0.9rem;
  color: #555;
  margin-bottom: 5px;
  display: block;
}

.form-control {
  width: 100%;
  padding: 10px;
  font-size: 0.95rem;
  border: 1px solid #ccc;
  border-radius: 5px;
  transition: border-color 0.3s ease;
}

.form-control:focus {
  border-color: #007bff;
  outline: none;
}

.btn-group {
  display: flex;
  justify-content: space-between;
}

.btn {
  padding: 10px 15px;
  font-size: 1rem;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background-color: #5a6268;
}
</style>

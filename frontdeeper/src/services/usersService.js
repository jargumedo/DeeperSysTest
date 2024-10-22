import axios from "axios";

const API_URL = "http://localhost:4000";

export default {
  getUsers() {
    return axios.get(`${API_URL}/api/users`);
  },
  getUser(username) {
    return axios.get(`${API_URL}/api/users/${username}`);
  },
  addUser(user) {
    return axios.post(`${API_URL}/users`, user);
  },
  updateUser(username, user) {
    return axios.post(`${API_URL}/update/${username}`, user);
  },
  deleteUser(username) {
    return axios.post(`${API_URL}/delete/${username}`);
  },
};

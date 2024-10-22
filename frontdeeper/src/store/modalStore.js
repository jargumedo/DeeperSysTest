// stores/modalStore.js
import { defineStore } from "pinia";

export const useModalStore = defineStore("modal", {
  state: () => ({
    isModalVisible: false,
  }),
  actions: {
    openModal() {
      this.isModalVisible = true;
    },
    closeModal() {
      this.isModalVisible = false;
    },
  },
});

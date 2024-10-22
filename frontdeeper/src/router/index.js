import { createRouter, createWebHashHistory } from "vue-router";
import UserManagement from "@/components/UserManagement.vue";
import AboutUser from "@/components/AboutUser.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: UserManagement,
  },
  {
    path: "/users/:username",
    name: "AboutUser",
    component: AboutUser,
    props: true,
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;

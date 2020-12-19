import Vue from "vue";
import Router from "vue-router";
//레이아웃
//로그인
import main from "@/views/main/main.vue";

const router = new Router({
    mode: "history",
    linkExactActiveClass: "active",
    routes: [
        //로그인
        {
            path: "/",
            name: "main",
            components: {
                main: main
            }
        }
    ]
});
Vue.use(Router);
router.beforeEach((to, from, next) => {
    //무조건 메인으로
    if (to.path !== "/") {
        next("/");
    } else {
        next();
    }
})

export default router;
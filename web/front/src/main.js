import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import Antd from "ant-design-vue";
import "ant-design-vue/dist/antd.less";
import VueCookies from 'vue-cookies';
import VueRx from "vue-rx";
import VuejsClipper from "vuejs-clipper/dist/vuejs-clipper.umd";
import "vuejs-clipper/dist/vuejs-clipper.css";
Vue.use(VueCookies);
Vue.use(VueRx);
Vue.use(VuejsClipper);
Vue.config.productionTip = false;

Vue.use(Antd);
new Vue({
    router,
    render: h => h(App),
}).$mount("#app");
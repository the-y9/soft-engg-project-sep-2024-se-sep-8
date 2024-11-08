import router from './router.js'
import navbar from './components/navbar.js'



router.beforeEach((to, from, next) => {
    const authToken = localStorage.getItem('auth-token');
    const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
    const requiredRole = to.meta.role;
    const role = localStorage.getItem('role')
    if (!authToken && to.name!=='login' && to.name!=='register' && to.name!=='home') {
         next({name:'login'})
    }
    else if (requiresAuth && requiredRole !== role) {
        next('/unauthorized');
    }
    else{
        next()
    }
})


router.afterEach((to, from) => {
    if (to.matched.length === 0) {
        router.replace({ name: '404_page' });
    }
});

new Vue({
    el: '#app',
    template: `<div>
    <navbar :key='has_changed'/>
    <router-view /> </div>`,
    router,
    components:{
        navbar,
    },
    data:{
        has_changed: true,
    },
    watch:{
        $route(to,from){
            this.has_changed = !this.has_changed
        }
    }
})
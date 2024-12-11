import router from './router.js'
import navbar from './components/navbar.js'


router.beforeEach((to, from, next) => {
    const authToken = localStorage.getItem('auth-token');
    const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
    const requiredRole = to.meta.role;
    const role = localStorage.getItem('role')
    if (!authToken && to.name!=='Login' && to.name!=='Register' && to.name!=='Home') {
         next({name:'Login'})
    }
    else if (requiresAuth && requiredRole !== role && to.name!=='Login') {
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
        // $route(to,from){
        //     this.has_changed = !this.has_changed
        // },
        $route: {
            immediate: true,
            handler(to, from) {
                this.has_changed = !this.has_changed;
                document.title = to.name;
            }
        },
    }
})
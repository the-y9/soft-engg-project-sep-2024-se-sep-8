import home from './components/home.js'
import login from './components/login.js'
import Not_found_page from './components/Not_found_page.js'

const routes = [
    { path:'/' , component : home , name:'home'},
    { path:'/login', component: login , name:'login'},
    { path: '/404_page' , component: Not_found_page , name:'404_page'}
] 

export default new VueRouter({
    routes,
})
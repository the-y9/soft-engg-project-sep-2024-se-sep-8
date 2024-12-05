export default {
    template: `
 
    <nav class="navbar">
        <a href="#" class="navbar-brand">Project Tracker</a>
        <div class="nav-links">
            <router-link v-if="!role && $route.path!='/'" class="nav-link" to="/">Home</router-link>
            <router-link v-if="role=='student' && $route.path=='/'" class="nav-link" to="/student_dashboard">Dashboard</router-link>
            <router-link v-if="!is_login && $route.path!='/login'" class="nav-link" to="/login">Login</router-link>
            <router-link v-if="!is_login && $route.path!='/register'" class="nav-link" to="/register">Register</router-link>
            <button  v-if="is_login" class="nav-link" @click='logout'>Logout</button>

        </div>
    </nav>
    `,
    data(){
        return {
            role: localStorage.getItem('role'),
            is_login: localStorage.getItem('auth-token'),
            username:''
        }
    },


    methods:{
        logout(){
            localStorage.removeItem('auth-token')
            localStorage.removeItem('role')
            localStorage.removeItem('email')
            this.$router.push({path:'/login'})
        }
    }
}
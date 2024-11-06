export default {
    template: `
 
    <nav class="navbar navbar-expand-lg " style="background-color: #F5B7B1;">
  
    <a class="navbar-brand " href="#">LibraryApp</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    
    <div class="collapse navbar-collapse justify-content-end " id="navbarNav">
      <ul class="navbar-nav" v-if="!is_login">
        <li class="nav-item">
          <router-link class="nav-link" to="/login">Login</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/register">Register</router-link>
        </li>
      </ul>

      <ul class="navbar-nav" v-if="is_login">
        <li class="nav-item">
          <router-link class="nav-link" to="/">Home</router-link>
        </li>
        <li class="nav-item" v-if="role=='admin'">
          <router-link class="nav-link" to="/request_and_issue_book"">Requests</router-link>
        </li>
        <li class="nav-item" v-if="role=='user'">
          <router-link class="nav-link" to="/my_books">My Books</router-link>
        </li>
        <li class="nav-item" v-if="role=='admin'">
        <router-link class="nav-link" to="/all_logs" >Logs</router-link>
        </li>
        <li class="nav-item" v-if="role=='user'">
          <router-link class="nav-link" to="/logs" >My Logs</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/profile">Profile</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/search">Search</router-link>
        </li>
        <li class="nav-item">
         <button class="nav-link" @click='logout' >Logout</button>
        </li>
      </ul>
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
            // this.$router.push({path:'/login'})
        }
    }
}

export default {
    template: `
      <div class="login-page">
        <div class="login-container">

          <img :src="image" alt="Profile Picture" class="profile-pic" />
          <div class="error-message text-danger text-center">{{ error }}</div>  
          <h1 class="login-title">Please Login</h1>
          
          <div class="form-group">
            <label for="username" class="form-label">Email</label> 
            <input type="text" class="form-control" id="email" v-model="cred.email" placeholder="Enter your email">
          </div>
          
          <div class="form-group">
            <label for="user_password" class="form-label">Password</label>
            <input type="password" class="form-control" id="user_password" v-model="cred.password" placeholder="Enter your password">
          </div>
          
          <button class="btn btn-primary login-button" @click="login">Login</button>
          
          <p class="register-link text-center">
            Don't have an account? <router-link to="/register">Register</router-link>
          </p>
        </div>
      </div>`,
      
    data() {
      return {
        cred: {
          email: null,
          password: null,
        },
        error: null,
        image : "static/images/user.png",
      }
    },
    
    methods: {
      async login() {
        try {
          const res = await fetch('/user-login', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.cred),
          })
          const data = await res.json()
          if (res.ok) {
            localStorage.setItem('auth-token', data.token)
            localStorage.setItem('role', data.role)
            localStorage.setItem('email', data.email)
            localStorage.setItem('user_id', data.id)
            if (data.role == "student"){
            this.$router.push({ path: '/student_dashboard' })
            }
            else if (data.role == "admin" || data.role == "instructor" || data.role == "ta" ){
                this.$router.push({ path: '/instructor_dashboard' })
            }
          } else {
            this.error = data.message
          }
        } catch (error) {
          console.log("Error is := " ,error)
        }
      }
    }
  }
  
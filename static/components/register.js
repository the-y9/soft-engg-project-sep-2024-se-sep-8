export default {
    template: `
    <div class="register-page">
    <div class="register-container">
        <img :src="image" alt="Profile Picture" class="profile-pic" />
        <div class="error-message text-danger text-center">{{ error }}</div>
        <h1 class="register-title">Register</h1>

        <div class="form-group">
            <label for="username" class="form-label">Username</label>
            <input type="text" class="form-control" id="username" v-model="cred.username" placeholder="Enter your username">
        </div>

        <div class="form-group">
            <label for="email" class="form-label">Email</label>
            <input type="text" class="form-control" id="email" v-model="cred.email" placeholder="Enter your email">
        </div>

        <div class="form-group">
            <label for="password" class="form-label">Password</label>
            <input type="password" class="form-control" id="password" v-model="cred.password" placeholder="Enter your password">
        </div>

        <button class="btn btn-primary register-button" @click="register">Register</button>

        <p class="login-link text-center">
            Already have an account? <router-link to="/login">Login</router-link>
        </p>
    </div>
</div>
`,

    data(){
        return{
            cred:{
                username:null,
                email:null,
                password:null,
            },
            error:null,
            image:"static/images/user.png",
        }
    },

    methods:{
        async register(){
            const res = await fetch('/user-signup', { 
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(this.cred),
        })
        const data = await res.json()
        if(res.ok){
            localStorage.setItem('auth-token', data.token)
            localStorage.setItem('role', data.role)
            this.$router.push({path:'/'})
        }
        else {
            this.error = data.message
        }
        }

    }
}


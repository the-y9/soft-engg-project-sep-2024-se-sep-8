export default {
    template: `
 <div>
    <nav class="navbar">
        <a href="#" class="navbar-brand">Project Tracker</a>
        <div class="nav-links">
            <router-link v-if="$route.path!='/'" class="nav-link" to="/">Home</router-link>
            <router-link v-if="role=='student' && $route.path=='/'" class="nav-link" to="/student_dashboard">Dashboard</router-link>
            <button v-if="is_login" class="nav-link" @click="fetchNotifications">
            <i class="fa fa-bell"></i> Notifications
            </button>
            <router-link v-if="!is_login && $route.path!='/login'" class="nav-link" to="/login">Login</router-link>
            <router-link v-if="!is_login && $route.path!='/register'" class="nav-link" to="/register">Register</router-link>

            <button  v-if="is_login" class="nav-link" @click='logout'>Logout</button>

        </div>
    </nav>
    <div v-if="showModal" class="modal-overlay">
        <div class="modal">
          <div class="modal-header">
            <h3>Notifications</h3>
            <button class="close-button" @click="closeModal">&times;</button>
          </div>
          <div class="modal-body">
            <ul v-if="notifications.length > 0">
              <li v-for="notification in notifications" :key="notification.id" class="notification-item">
                {{ notification.message }}
              </li>
            </ul>
            <p v-else>No notifications available.</p>
          </div>
        </div>
      </div>
    </div>
    `,
    data(){
        return {
            role: localStorage.getItem('role'),
            is_login: localStorage.getItem('auth-token'),
            username:'',
            showModal: false, // Controls the visibility of the modal
            notifications: []
        }
    },


    methods:{
        logout(){
            localStorage.removeItem('auth-token')
            localStorage.removeItem('role')
            localStorage.removeItem('email')
            this.$router.push({path:'/login'})
        },

        async fetchNotifications() {
            try {
                user_id = localStorage.getItem('user_id')
              this.showModal = true; // Open the modal
              const res = await fetch('/notifications/team/${user_id}', {
                method: 'GET',
                headers: {
                  'Authorization': `Bearer ${localStorage.getItem('auth-token')}`,
                  'Content-Type': 'application/json',
                },
              });
      
              if (res.ok) {
                this.notifications = await res.json();
              } else {
                console.error('Failed to fetch notifications.');
              }
            } catch (error) {
              console.error('Error fetching notifications:', error);
            }
          },
      
          closeModal() {
            this.showModal = false; // Close the modal
          },


    }
}
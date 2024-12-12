export default {
  template: `
 <div>
    <div>
    <nav class="navbar">
      <a href="#" class="navbar-brand">Project Tracker</a>
      <div class="nav-links">
        <!-- Notifications Button -->
        <button v-if="is_login & role === 'student'" class="nav-link" @click="toggleNotifications">
          <i class="fa fa-bell"></i> Notifications
        </button>
        
        <router-link v-if="!is_login" class="nav-link" to="/login">Login</router-link>
        <router-link v-if="!is_login" class="nav-link" to="/register">Register</router-link>
        <router-link v-if="is_login & role === 'student' & $route.path != '/student_dashboard'" class="nav-link" to="/student_dashboard">Dashboard</router-link>
        <router-link v-if="is_login & role != 'student' & $route.path != '/instructor_dashboard'" class="nav-link" to="/instructor_dashboard">Dashboard</router-link>
        <router-link v-if="is_login & role === 'student'" class="nav-link" to="/commit_history">Commit History</router-link>
        <router-link v-if="is_login & role != 'student' & $route.path != '/project'" class="nav-link" to="/project">Projects</router-link>
        <button v-if="is_login" class="nav-link" @click="logout">Logout</button>
      </div>
    </nav>

    <!-- Notifications Dropdown -->
    <div class="notifications-dropdown" v-if="showNotifications && role === 'student'">
      <div class="dropdown-header">
        <h4>Notifications</h4>
      </div>
      <ul class="dropdown-body">
        <li v-for="notification in notifications" :key="notification.id" class="notification-item">
          {{ notification.message }}
        </li>
      </ul>
      <div v-if="notifications.length === 0" class="dropdown-empty">
        No notifications available.
      </div>
    </div>
  </div>
    </nav>
    </div>
    `,

  data() {
    return {
      role: localStorage.getItem('role'),
      is_login: !!localStorage.getItem('auth-token'), // Ensure boolean
      username: '',
      notifications: [],
      commitHistory: [],
      team:'',
      teamData: [],
      showNotifications: false, // Track dropdown visibility
    };
  },

  methods: {
    
    logout() {
      localStorage.removeItem('auth-token');
      localStorage.removeItem('role');
      localStorage.removeItem('email');
      localStorage.removeItem('user_id');
      this.$router.push({ path: '/login' });
    },

    async toggleNotifications() {
      if (this.showNotifications) {
        this.showNotifications = false; // Close the dropdown if it's open
        return;
      }

      try {
        console.log("fetchNotifications triggered");
        const id = localStorage.getItem('user_id');
        const res = await fetch(`/notifications/user/${id}`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('auth-token')}`,
            'Content-Type': 'application/json',
          },
        });

        if (res.ok) {
          this.notifications = await res.json();
          console.log("Notifications fetched:", this.notifications);
        } else {
          console.error('Failed to fetch notifications.');
        }
      } catch (error) {
        console.error('Error fetching notifications:', error);
      }

      this.showNotifications = true; // Open the dropdown
    },

    async fetchCommitHistory() {
      try {
        console.log("fetchCommitHistory triggered");
        const projectId = localStorage.getItem('project_id');
        const teamid = localStorage.getItem('team_id');
        const res = await fetch(`/projects/${projectId}/teams/${teamid}`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('auth-token')}`,
            'Content-Type': 'application/json',
          },
        });

        if (res.ok) {
          this.commitHistory = await res.json();
          this.teamData = this.commitHistory.team;
          console.log("Commit history fetched:", this.teamData.name);
        } else {
          console.error('Failed to fetch commit history.');
        }
      } catch (error) {
        console.error('Error fetching commit history:', error);
      }

      // Show the modal after fetching data
      const modal = new bootstrap.Modal(document.getElementById('commitHistoryModal'));
      modal.show();
    },
  },
};

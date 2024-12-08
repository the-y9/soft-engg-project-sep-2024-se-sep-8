export default {
  template: `
    <div class="notification-page">
      <section class="page-header">
        <div class="header-content">
          <h1 class="hero-title">Notification System</h1>
          <p class="hero-subtitle">Create and send notifications to students with ease.</p>
        </div>
      </section>        
      <section class="notification-form">
        <div class="notification-target text-center mb-4">
          <h4 style="font-weight:bold" v-if="teamName">Team: {{ teamName }}</h4>
          <h4 style="font-weight:bold" v-if="memberName">Member: {{ memberName }}</h4>
        </div>
          <form @submit.prevent="createNotification">
            <div class="form-group">
              <label for="notification-title" class="form-label">Notification Title</label>
              <input type="text" id="notification-title" v-model="notificationTitle" class="form-control" placeholder="Enter notification title" required />
            </div>
            
            <div class="form-group">
              <label for="notification-message" class="form-label">Notification Message</label>
              <textarea id="notification-message" v-model="notificationMessage" class="form-control" placeholder="Enter your message" required></textarea>
            </div>

            <button type="submit" class="create-button btn btn-primary">Send Notification</button>
          </form>
      </section>
    </div>
  `,

  data() {
    return {
      teamId: null,
      teamName: null,
      memberId: null,
      memberName: null,
      notificationTitle: '',
      notificationMessage: ''
    }
  },

  created() {
    this.teamId = this.$route.query.team_id;
    this.teamName = this.$route.query.team_name;
    this.memberId = this.$route.query.member_id;
    this.memberName = this.$route.query.member_name;
    console.log(this.teamId, this.memberId);
  },

  methods: {
    async createNotification() {
      if (this.notificationTitle && this.notificationMessage) {
        try {
          const response = await fetch('/notifications', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authentication-Token': localStorage.getItem('auth-token')
            },
            body: JSON.stringify({
              // Backend: if team_id and member_id both are present send to member only, otherwise send to entire team.
              teamId: this.teamId,
              memberId: this.memberId,
              notificationTitle: this.notificationTitle,
              notificationMessage: this.notificationMessage
            })
          });

          if (!response.ok) {
            throw new Error('Failed to send notification.');
          }
          this.$router.go(-1);
          alert('Notification Sent');
        } catch (error) {
          console.error('Error sending notification:', error);
          alert('Failed to send notification. Please try again.');
        }
      } else {
        alert('Please fill out all fields.');
      }
    }
  }
};

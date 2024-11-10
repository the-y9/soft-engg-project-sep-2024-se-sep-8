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
        <form @submit.prevent="createNotification">
          <div class="form-group">
            <label for="notification-title" class="form-label">Notification Title</label>
            <input type="text" id="notification-title" v-model="notificationTitle" class="form-control" placeholder="Enter notification title" required />
          </div>
          
          <div class="form-group">
            <label for="notification-message" class="form-label">Notification Message</label>
            <textarea id="notification-message" v-model="notificationMessage" class="form-control" placeholder="Enter your message" required></textarea>
          </div>
          
          <div class="form-group">
            <label for="recipients" class="form-label">Select Recipients</label>
            <select id="recipients" v-model="selectedRecipient" class="form-control" required>
              <option v-for="student in students" :key="student.id" :value="student.id">{{ student.name }}</option>
            </select>
          </div>

          <button type="submit" class="create-button">Send Notification</button>
        </form>
      </section>
    </div>`,

    data() {
        return {
            notificationTitle: '',
            notificationMessage: '',
            selectedRecipient: null,
            students: [
                { id: 1, name: 'Student A' },
                { id: 2, name: 'Student B' },
                { id: 3, name: 'Student C' }
            ]
        }
    },

    methods: {
        createNotification() {
            if (this.notificationTitle && this.notificationMessage && this.selectedRecipient) {
                alert(`Notification titled "${this.notificationTitle}" sent to recipient ID: ${this.selectedRecipient}`);
                // Logic for sending the notification can be added here (e.g., API call)
            } else {
                alert('Please fill out all fields.');
            }
        }
    }
}
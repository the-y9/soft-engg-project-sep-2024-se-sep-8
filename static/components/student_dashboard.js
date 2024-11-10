export default {
    template: `
     <div class="student-dashboard-page">
      <section class="page-header">
        <div class="header-content">
          <h1 class="hero-title">Student Dashboard</h1>
          <p class="hero-subtitle">View your project milestones, upload documents, and check feedback.</p>
        </div>
      </section>

      <section class="milestone-content">
        <div v-for="milestone in milestones" :key="milestone.id" class="milestone-card">
          <div class="milestone-header">
            <h3 class="milestone-title">{{ milestone.name }}</h3>
            <p class="milestone-deadline">Deadline: {{ milestone.deadline }}</p>
          </div>
          <div class="progress-container">
            <div class="progress-bar" :style="{ width: milestone.progress + '%' }"></div>
          </div>
          <p class="progress-text">Progress: {{ milestone.progress }}%</p>

          <div class="form-group">
            <label :for="'upload-' + milestone.id" class="form-label">Upload Document</label>
            <input type="file" :id="'upload-' + milestone.id" @change="uploadDocument($event, milestone.id)" class="form-control" />
          </div>

          <div class="button-group">
            <button class="feedback-button" @click="viewFeedback(milestone.id)">View Feedback</button>
          </div>
        </div>
      </section>

      <div class="chatbot-icon" @click="openChatbot">
        <img src="static/images/chatbot.png" alt="Chatbot" />
      </div>
    </div>`,

    data() {
        return {
            milestones: [
                { id: 1, name: 'Milestone 1', deadline: '2024-11-15', progress: 50 },
                { id: 2, name: 'Milestone 2', deadline: '2024-11-30', progress: 30 },
                { id: 3, name: 'Milestone 3', deadline: '2024-12-10', progress: 0 }
            ]
        }
    },

    methods: {
        uploadDocument(event, milestoneId) {
            const file = event.target.files[0];
            if (file) {
                alert(`Document uploaded for milestone ID: ${milestoneId}`);
                // Logic for handling file upload can be added here
            }
        },

        viewFeedback(milestoneId) {
            alert(`Viewing feedback for milestone ID: ${milestoneId}`);
            // Logic for viewing feedback can be added here
        },

        openChatbot() {
            alert('Chatbot opened');
            // Logic for opening the chatbot interface can be added here
        }
    }
}
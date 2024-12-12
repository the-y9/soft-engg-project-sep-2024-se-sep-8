export default {
  template: `
    <div class="student-dashboard-page">
      <section class="page-header">
        <div class="header-content">
          <h1 class="hero-title">Student Dashboard</h1>
          <p class="hero-subtitle">View your project milestones, upload documents, and check feedback.</p>
        </div>
      </section>

      <!-- Project Selection -->
      <center>
      <div class="form-group">
      
        <section class="project-selection">
          <label for="project-select" class="form-label" style="color: white;">Select a Project:</label>
          <select id="project-select" class="form-select" v-model="selectedProjectId">
            <option value="" disabled>Select a project</option>
            <option v-for="project in projects" :key="project.project_id" :value="project.project_id">{{ project.project_title }}</option>
          </select>
          <button class="btn btn-primary mt-3" @click="submitProject">Submit</button>
        </section>
        
      </div>
      </center>

      <!-- Milestone Display -->
      <section v-if="milestones.length && selectedProjectId" class="milestone-content">
        <h2>Milestones for Selected Project</h2>
        <div v-for="milestone in milestones" :key="milestone.id" class="milestone-card">
          <div class="milestone-header">
            <h3 class="milestone-title">{{ milestone.name }}</h3>
            <p class="milestone-deadline">Deadline: {{ milestone.deadline }}</p>
          </div>
          <p><b>Task Name: </b>{{milestone.taskName}}</p>
          <p><b>Description:</b> {{milestone.description}}</p>

          <div class="form-group">
            <label :for="'upload-' + milestone.id" class="form-label">Upload Document</label>
            <input type="file" :id="'upload-' + milestone.id" @change="uploadDocument($event, milestone.id)" class="form-control" />
          </div>
        </div>
      </section>

      <!-- Chatbot Section -->
      <div class="chatbot-icon" @click="toggleChatbot">
        <img src="static/images/chatbot.png" alt="Chatbot" />
      </div>

      <div class="modal fade" id="chatbotModal" tabindex="-1" aria-labelledby="chatbotModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-lg modal-dialog-centered">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="chatbotModalLabel">Chatbot</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <div class="messages" id="messages" style="height: 300px; overflow-y: auto; border: 1px solid #ddd; padding: 10px; border-radius: 5px;">
                <div v-for="entry in chatHistory.Chat_History" :key="entry.id">
                  <div class="message user-message p-2 mb-2 rounded bg-primary text-white">{{ entry.User }}</div>
                  <div class="message bot-message p-2 mb-2 rounded bg-light" v-html="entry.bot"></div>
                </div>
              </div>
              <div class="input-group mt-3">
                <input type="text" id="user-input" v-model="chatHistory.current_message" @keydown.enter="sendMessage" placeholder="Type your message" class="form-control" />
                <button class="btn btn-primary" @click="sendMessage">Send</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>`,

  data() {
    return {
      projects: [], // List of projects
      selectedProjectId: '', // Selected project ID
      milestones: [], // Milestones for selected project
      chatbotOpen: false,
      chatHistory: {
        Chat_History: [],
        current_message: ''
      },
      team_id : '',
      milestoneId: '',
      user_id : localStorage.getItem('user_id')
    };
  },

  mounted() {
    this.fetchProjects(); // Fetch projects when the page loads
  },

  methods: {
    // Fetch all projects
    async fetchProjects() {
      try {
        
        const response = await fetch(`/get_user_details/${this.user_id}`, { method: 'GET' });
        if (!response.ok) {
          throw new Error('Failed to fetch projects');
        }
        const data = await response.json();
        this.projects = data['teams_and_projects']; // Set the projects data
        this.team_id = data['team_id'];
      } catch (error) {
        console.error('Error fetching projects:', error);
        alert('Failed to load projects');
      }
    },

    // Submit selected project to fetch milestones
    async submitProject() {
      if (!this.selectedProjectId) {
        alert('Please select a project.');
        return;
      }
      localStorage.setItem('project_id', this.selectedProjectId);

      try {
        const response = await fetch(`/projects/${this.selectedProjectId}`, { method: 'GET' });
        if (!response.ok) {
          throw new Error('Failed to fetch milestones');
        }
        const data = await response.json();
        this.milestones = data.milestones; // Set the milestones data
      } catch (error) {
        console.error('Error fetching milestones:', error);
        alert('Failed to load milestones');
      }
    },

    async uploadDocument(event, milestoneId) {
      const file = event.target.files[0];
      if (file) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('filename', file.name);
        try {
          const response = await fetch(`/upload/${this.team_id}/${this.user_id}/${milestoneId}`, { method: 'POST', body: formData });
          if (!response.ok) {
            throw new Error('Failed to upload file');
          }
          alert(`Document uploaded successfully for milestone ID: ${milestoneId}`);
        } catch (error) {
          console.error('Error uploading document:', error);
          alert('Failed to upload document');
        }
      }
    },

    viewFeedback(milestoneId) {
      alert(`Viewing feedback for milestone ID: ${milestoneId}`);
    },

    toggleChatbot() {
      const chatbotModal = new bootstrap.Modal(document.getElementById('chatbotModal'));
      chatbotModal.toggle();
    },

    async sendMessage() {
      if (this.chatHistory.current_message.trim() !== '') {
        const userMessage = this.chatHistory.current_message;

        try {
          const response = await fetch('/chatbot', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.chatHistory)
          });

          const data = await response.json();
          if (!response.ok) {
            throw new Error(data.message || 'Failed to get bot response.');
          }

          this.chatHistory.Chat_History.push({
            User: userMessage,
            bot: this.renderMarkdown(data.bot_response)
          });

          this.chatHistory.current_message = '';
          this.updateChatDisplay();
        } catch (error) {
          console.error('Error getting bot response:', error);
        }
      }
    },

    renderMarkdown(markdownText) {
      try {
        const md = window.markdownit();
        return md.render(markdownText);
      } catch (error) {
        console.error('Markdown rendering failed:', error);
        return markdownText;
      }
    },

    updateChatDisplay() {
      this.$nextTick(() => {
        const messagesContainer = document.getElementById('messages');
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
      });
    }
  }
};

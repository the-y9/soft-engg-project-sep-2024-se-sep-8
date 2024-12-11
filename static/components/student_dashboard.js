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
          <button class="feedback-button btn btn-info" @click="viewFeedback(milestone.id)">View Feedback</button>
        </div>
      </div>
    </section>

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
          milestones: [
              { id: 1, name: 'Milestone 1', deadline: '2024-11-15', progress: 50 },
              { id: 2, name: 'Milestone 2', deadline: '2024-11-30', progress: 30 },
              { id: 3, name: 'Milestone 3', deadline: '2024-12-10', progress: 0 }
          ],
          chatbotOpen: false,
          chatHistory: {
              Chat_History: [],
              current_message: ''
          }
      }
  },
  mounted() {
    this.fetchMilestones();
  },

  methods: {
    async uploadDocument(event, milestoneId) {
      const file = event.target.files[0];
      if (file) {
          const formData = new FormData();
          formData.append('file', file);
          formData.append('filename', file.name);
          formData.append('related_milestone', milestoneId);
          formData.append('uploaded_by', this.getUserId()); // Replace this with your logic to fetch user ID
          formData.append('team_id', this.getTeamId()); // Replace this with your logic to fetch team ID

          try {
              const response = await fetch('/upload', {
                  method: 'POST',
                  body: formData,
              });

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

  async fetchMilestones() {
    try {
      const response = await fetch('/milestone',{
        method: 'GET'
      }); // Adjust endpoint as per your API
      if (!response.ok) {
        throw new Error('Failed to fetch milestones');
      }
      const data = await response.json();
      this.milestones = data.milestones; // Update milestones with backend data
    } catch (error) {
      console.error('Error fetching milestones:', error);
      alert('Failed to load milestones');
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
              const md = window.markdownit(); // Initialize markdown-it
              return md.render(markdownText); // Render Markdown to HTML
          } catch (error) {
              console.error('Markdown rendering failed:', error);
              return markdownText; // Fallback to plain text
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

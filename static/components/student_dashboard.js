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
                <div class="message bot-message p-2 mb-2 rounded bg-light">{{ entry.bot }}</div>
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

      toggleChatbot() {
          const chatbotModal = new bootstrap.Modal(document.getElementById('chatbotModal'));
          chatbotModal.toggle();
      },

      async sendMessage() {
          if (this.chatHistory.current_message.trim() !== '') {

              // Add user message to chat
              const userMessage = this.chatHistory.current_message;

              // Send chat history with current message to backend
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

                  // Update the last entry with the bot's response
                  this.chatHistory.Chat_History.push({ User: userMessage, bot: data.bot_response });
                  
                  // Clear the current message
                  this.chatHistory.current_message = '';
                  console.log(this.chatHistory);

                  // Update chat display
                  this.updateChatDisplay();
              } catch (error) {
                  console.error('Error getting bot response:', error);
                  alert('Failed to get bot response. Please try again.');
              }
          }
      },

      updateChatDisplay() {
          this.$nextTick(() => {
              const messagesContainer = document.getElementById('messages');
              messagesContainer.scrollTop = messagesContainer.scrollHeight;
          });
      }
  }
}

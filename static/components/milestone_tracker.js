export default {
    template: `
     <div class="milestone-tracker-page">
      <section class="page-header">
        <div class="header-content">
          <h1 class="hero-title">Milestone Tracker</h1>
          <p class="hero-subtitle">Track progress for each team and review their milestone submissions.</p>
        </div>
      </section>

      <section class="tracker-content">
        <div v-for="team in teams" :key="team.id" class="team-section">
          <h2 class="team-name">Team: {{ team.name }}</h2>
          <div v-for="milestone in team.milestones" :key="milestone.id" class="milestone-card">
            <h3 class="milestone-title">Milestone: {{ milestone.name }}</h3>
            <p class="milestone-status">Status: {{ milestone.status }}</p>
            <button class="analyze-button" @click="analyzeDocument(milestone.id)">Analyze Document with AI</button>
            <button class="view-button" @click="viewDocument(milestone.id)">View Document</button>
          </div>
        </div>
      </section>
    </div>`,

    data() {
        return {
            teams: [
                {
                    id: 1,
                    name: 'Team Alpha',
                    milestones: [
                        { id: 101, name: 'Milestone 1', status: 'Submitted' },
                        { id: 102, name: 'Milestone 2', status: 'In Progress' }
                    ]
                },
                {
                    id: 2,
                    name: 'Team Beta',
                    milestones: [
                        { id: 201, name: 'Milestone 1', status: 'Submitted' },
                        { id: 202, name: 'Milestone 2', status: 'Pending' }
                    ]
                }
            ]
        }
    },

    methods: {
        analyzeDocument(milestoneId) {
            alert(`Analyzing document for milestone ID: ${milestoneId}`);
            // Logic for analyzing the document using an API can be added here
        },

        viewDocument(milestoneId) {
            alert(`Viewing document for milestone ID: ${milestoneId}`);
            // Logic for viewing the document can be added here
        }
    }
}
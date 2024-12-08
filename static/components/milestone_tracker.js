export default {
  template: `
   <div class="milestone-tracker-page">
  <section class="page-header">
    <div class="container">
      <div class="row">
        <div class="col text-center">
          <h1 class="display-4">Milestone Tracker</h1>
          <p class="lead">Track progress for each team and review their milestone submissions.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="container">
    <div v-for="team in teams" :key="team.id" class="team-section my-4">
      <h2 class="team-name h4">Team: {{ team.name }}</h2>
      <div v-for="(milestone,index) in team.milestones" :key="milestone.id" class="milestone-card card p-3 mb-3">
        <h3 class="milestone-title h5">Milestone {{ index + 1 }}: {{ milestone.name }}</h3>
        <p class="milestone-status mb-2">Status: {{ milestone.status }}</p>
        <div class="d-flex">
          <button class="btn btn-primary btn-sm me-2 px-2 py-1" @click="analyzeDocument(team.id, milestone.id)">
            Analyze Document with AI
          </button>
          <button class="btn btn-secondary btn-sm px-2 py-1" @click="viewDocument(team.id, milestone.id)">
            View Document
          </button>
        </div>
        <p v-if="milestone.analysisResult" class="analysis-result mt-2">{{ milestone.analysisResult }}</p>
      </div>
    </div>
  </section>
</div>
`,

  data() {
      return {
          projectId: this.$route.params.id,
          teams: [
            {
                id: 1,
                name: 'Team Alpha',
                milestones: [
                    { id: 1, name: 'Milestone 1', status: 'Submitted' },
                    { id: 2, name: 'Milestone 2', status: 'In Progress' }
                ]
            },
            {
                id: 2,
                name: 'Team Beta',
                milestones: [
                    { id: 1, name: 'Milestone 1', status: 'Submitted' },
                    { id: 2, name: 'Milestone 2', status: 'Pending' }
                ]
            }
        ]
      }
  },

  async beforeCreate() {
      try {
          const response = await fetch(`/projects/${this.$route.params.project_id}/teams`);
          const data = await response.json();

          if (!response.ok) {
              throw new Error(data.message || "Failed to fetch team information.");
          }

          this.teams = data;
      } catch (error) {
          console.error("Error fetching team information:", error);
          alert("Failed to load team information.");
      }
  },

  methods: {
      async analyzeDocument(teamId, milestoneId) {
          try {
              const response = await fetch(`/teams/${teamId}/milestones/${milestoneId}/analyze`, {
                  method: 'POST',
                  headers: {
                      'Content-Type': 'application/json',
                      'Authentication-Token': localStorage.getItem('auth-token')
                  },
                  body: JSON.stringify({ projectId: this.projectId })
              });

              const result = await response.json();

              if (!response.ok) {
                  throw new Error(result.message || "Failed to analyze document.");
              }

              alert(`Analysis Result: ${result.analysis}`);
          } catch (error) {
              console.error("Error analyzing document:", error);
              alert("Failed to analyze document. Please try again.");
          }
      },

      async viewDocument(teamId, milestoneId) {
          try {
              const response = await fetch(`/teams/${teamId}/milestones/${milestoneId}/document`, {
                  method: 'GET',
                  headers: {
                      'Content-Type': 'application/json',
                      'Authentication-Token': localStorage.getItem('auth-token')
                  }
              });

              const blob = await response.blob();
              const url = URL.createObjectURL(blob);
              window.open(url, '_blank');
          } catch (error) {
              console.error("Error viewing document:", error);
              alert("Failed to view document. Please try again.");
          }
      }
  }
}

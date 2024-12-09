export default {
  template: `
  <div class="content row justify-content-center">
    <div class="col-12 col-md-6 text-center">
      <h3 class='p-3 m-3'>Student Performance Prediction</h3>
      
      <div class="form-group">
          <label for="projectSelect" class="p-2 m-2 d-block text-center">Select Project</label>
          <select v-model="selectedProjectId" @change="updateTeams" class="form-control" id="projectSelect">
              <option disabled value="">Choose Project</option>
              <option v-for="project in projects" :key="project.id" :value="project.id">{{ project.name }}</option>
          </select>
      </div>
      
      <div class="form-group">
          <label for="teamSelect" class="p-2 m-2 d-block text-center">Select Team</label>
          <select v-model="selectedTeamId" class="form-control" id="teamSelect" :disabled="!selectedProjectId">
              <option disabled value="">Choose Team</option>
              <option v-for="team in availableTeams" :key="team.id" :value="team.id">{{ team.name }}</option>
          </select>
      </div>
      
      <button class="btn btn-primary mb-2" @click="predictPerformance">Predict Performance</button>
    </div>

    <div v-if="result" class="results-table">
      <h4 class="bg-success text-white p-2">Prediction Results</h4>
      <table class="table table-bordered">
        <thead>
          <tr>
            <th>Student ID</th>
            <th>Task Completion (%)</th>
            <th>Coding Activity (Hours)</th>
            <th>Predicted Performance</th>
            <th>Support Recommendation</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>{{ result.studentId }}</td>
            <td>{{ result.taskCompletion }}</td>
            <td>{{ result.codingActivity }}</td>
            <td>{{ result.predictedPerformance }}</td>
            <td>{{ result.supportRecommendation }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  `,
  
  data() {
      return {
          selectedProjectId: '',
          selectedTeamId: '',
          projects: [],
          availableTeams: [],
          students: [
              { id: '21fx' },
              { id: '22fx' },
              { id: '23fx' }
          ],
          result: null
      };
  },

  async beforeCreate() {
    try {
      const response = await fetch('/projects');
      const data = await response.json();
      if (!response.ok) {
          throw new Error(data.message || "Failed to fetch projects.");
      }
      this.projects = data;
  } catch (error) {
      console.error("Error fetching projects:", error);
      alert("Failed to load projects.");
  }
  },

  methods: {

      updateTeams() {
          const project = this.projects.find(proj => proj.id === this.selectedProjectId);
          this.availableTeams = project ? project.teams : [];
          this.selectedTeamId = '';
      },

      async predictPerformance() {
          const selectedTeam = this.availableTeams.find(team => team.id === this.selectedTeamId);
          if (selectedTeam) {
              try {
                  const response = await fetch('/predict_performance', {
                      method: 'POST',
                      headers: {
                          'Content-Type': 'application/json',
                          'Authentication-Token': localStorage.getItem('auth-token')
                      },
                      body: JSON.stringify({
                          owner: selectedTeam.repo_owner,
                          repo: selectedTeam.repo_name
                      })
                  });

                  const data = await response.json();
                  if (!response.ok) {
                      throw new Error(data.message || 'Failed to predict performance.');
                  }
                  console.log(data);
                  // this.result = {
                  //     taskCompletion: data.taskCompletion,
                  //     codingActivity: data.codingActivity,
                  //     predictedPerformance: data.predictedPerformance,
                  //     supportRecommendation: data.supportRecommendation
                  // };
              } catch (error) {
                  console.error('Error predicting performance:', error);
                  alert('Failed to predict performance. Please try again.');
              }
          }
      }
  }
};

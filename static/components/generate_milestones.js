export default {
    template: `
    <div class="container my-5 text-center">
      <h5 class="font-weight-bold">Enter Project Statement</h5>
      <textarea v-model="projectStatement" class="form-control border my-3" rows="4" placeholder="Enter the detailed description of the project..."></textarea>
      <button @click="generateMilestones" class="btn btn-success">Generate Milestones</button>

      <!-- Display generated milestones -->
      <div v-if="milestones.length" class="mt-4 mb-5 pb-5">
        <h5>Generated Milestones</h5>
        <ul class="list-group mt-3">
          <li v-for="(milestone, index) in milestones" :key="index" class="list-group-item">
            {{ milestone }}
          </li>
        </ul>
      </div>
    </div>
    `,
      
    data() {
        return{
        projectStatement: '',
        milestones: []
      }},
    
    methods: {
        generateMilestones() {
          // Dummy data for generated milestones
          this.milestones = [
            "Define project scope and objectives",
            "Complete initial research and planning",
            "Develop project prototype",
            "Conduct testing and evaluation",
            "Finalize and deliver project",
            "Finalize and deliver project",
            "Finalize and deliver project"
          ];
    
          // Backend API call (uncomment to enable backend integration)
          /*
          fetch('https://your-backend-url.com/api/generate-milestones', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ projectStatement: this.projectStatement })
          })
          .then(response => response.json())
          .then(data => {
            this.milestones = data.milestones;
          })
          .catch(error => {
            console.error('Error:', error);
          });
          */
        }
      }
  }
  
export default {
  template: `
   <div class="instructor-dashboard">

    <section class="dashboard-header">
      <div class="dashboard-title">
        <h1 class="hero-title">Instructor Dashboard</h1>
        <p class="hero-subtitle">Manage your project milestones and analyze documents effortlessly.</p>
      </div>
    </section>

    <section class="dashboard-options">
      <center>
      <div class="dashboard-cards">
        <div class="dashboard-card" @click="goToCreateProject">
          <img src="static/images/milestone.webp" alt="Create Milestone" class="dashboard-image" />
          <h3 class="dashboard-card-title">Create Project and Milestones</h3>
          <p class="dashboard-card-description">Plan and define your project and milestones with ease.</p>
        </div>
        <div class="dashboard-card" @click="openProjectModal">
          <img src="static/images/track_milestone.webp" alt="Milestone Tracker" class="dashboard-image" />
          <h3 class="dashboard-card-title">Milestone Tracker</h3>
          <p class="dashboard-card-description">Track and monitor the progress of your milestones in real-time.</p>
        </div>
        <div class="dashboard-card" @click="openTeamTrackerModal">
            <img src="static/images/team_tracker.webp" alt="Team Tracker" class="dashboard-image" />
            <h3 class="dashboard-card-title">Team Tracker</h3>
            <p class="dashboard-card-description">Track and monitor the progress of your teams.</p>
        </div>
      </div>
      </center>
    </section>

    <!-- Modal for Project Selection -->
    <div class="modal" id="selectProjectModal" tabindex="-1" aria-labelledby="selectProjectModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="selectProjectModalLabel">Select a Project</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
              <div class="list-group">
                <button v-for="project in projects" :key="project.id" type="button" class="list-group-item list-group-item-action" :class="{'active': project.id === selectedProjectId}" @click="selectProject(project.id)">
                  {{ project.name }}
                </button>
              </div>
          </div>
          <div class="modal-footer justify-content-center">
            <button type="button" class="btn btn-primary" @click="goToMilestoneTracker" :disabled="!selectedProjectId">Track Milestones</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal for Team Tracker -->
      <div class="modal" id="selectTeamModal" tabindex="-1" aria-labelledby="selectTeamModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="selectTeamModalLabel">Select a Project and Team</h5>
            </div>
            <div class="modal-body">
                <div class="form-group mb-3">
                  <label for="projectSelect">Project</label>
                  <select class="form-control" id="projectSelect" v-model="selectedProjectId" @change="updateTeams">
                    <option value="" disabled selected>Select a project</option>
                    <option v-for="project in projects" :key="project.id" :value="project.id">{{ project.name }}</option>
                  </select>
                </div>
                <div class="form-group mb-3">
                  <label for="teamSelect">Team</label>
                  <select class="form-control" id="teamSelect" v-model="selectedTeamId" :disabled="!selectedProjectId">
                    <option value="" disabled selected>Select a team</option>
                    <option v-for="team in availableTeams" :key="team.id" :value="team.id">{{ team.name }}</option>
                  </select>
                </div>
            </div>
            <div class="modal-footer justify-content-center">
              <button type="button" class="btn btn-primary" @click="goToTeamTracker" :disabled="!selectedTeamId">Track Team</button>
            </div>
          </div>
        </div>
      </div>
  </div>`,
  
  data() {
      return {
          options: [
              { id: 1, title: "Create Project and Milestones", description: "Plan and define your project and milestones with ease.", image: "static/images/milestone.webp" },
              { id: 2, title: "Milestone Tracker", description: "Track and monitor the progress of your milestones in real-time.", image: "static/images/track_milestone.webp" },
              { id: 3, title: "Notification", description: "You can create Notifications From Here.", image: "static/images/doc_analyzer.webp" },
              { id: 4, title: "Team Tracker", description: "Track and monitor the progress of your teams.", image: "static/images/team_tracker.webp" }
          ],
          projects: [
            {
                id: 1,
                name: 'Project Alpha',
                teams: [{ id: 1, name: 'Team A' }, { id: 2, name: 'Team B' }],
                startDate: '2024-01-01',
                endDate: '2024-06-30',
                milestones: [
                    { id: 101, name: 'Milestone 1', status: 'Completed' },
                    { id: 102, name: 'Milestone 2', status: 'In Progress' }
                ]
            },
            {
                id: 2,
                name: 'Project Beta',
                teams: [{ id: 3, name: 'Team C' }],
                startDate: '2024-03-01',
                endDate: '2024-08-15',
                milestones: [
                    { id: 201, name: 'Milestone 1', status: 'Pending' }
                ]
            }
        ],
          selectedProjectId: null,
          selectedTeamId: null,
          availableTeams: [],
          modal: null
      }
  },

  async beforeCreate(){
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
      goToCreateProject() {
          this.$router.push('/project/create');
      },
      goToMilestoneTracker() {
          if (this.selectedProjectId) {
              this.modal.hide();
              this.$router.push(`/milestone_tracker/${this.selectedProjectId}`);
              this.selectedProjectId = null; // Reset the selected project after navigation
          }
      },
      openProjectModal() {
          this.modal = new bootstrap.Modal(document.getElementById('selectProjectModal'));
          this.modal.show();
      },
      selectProject(projectId) {
          this.selectedProjectId = projectId;
      },
      openTeamTrackerModal() {
        this.modal = new bootstrap.Modal(document.getElementById('selectTeamModal'));
        this.modal.show();
      },
      updateTeams() {
        const project = this.projects.find(proj => proj.id === this.selectedProjectId);
        this.availableTeams = project ? project.teams : [];
        this.selectedTeamId = null; // Reset the selected team when the project changes
      },
      goToTeamTracker() {
          if (this.selectedProjectId && this.selectedTeamId) {
              this.modal.hide();
              this.$router.push(`/team_tracker/${this.selectedProjectId}/${this.selectedTeamId}`);
              this.selectedProjectId = null; // Reset the selected project after navigation
              this.selectedTeamId = null;    // Reset the selected team after navigation
          }
      }
  }
};

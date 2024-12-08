export default {
    template: `
     <div class="container my-4">
      <section class="text-center mb-4">
        <h1 class="display-4">Project List</h1>
        <p class="lead">Manage projects, track their progress, and access detailed overviews.</p>
      </section>

      <section class="row">
        <div v-for="project in projects" :key="project.id" class="col-md-6 col-lg-4 mb-4">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">{{ project.name }}</h5>
              <p class="card-text">Teams: {{ project.teams.length }}</p>
              <p class="card-text">
                <small class="text-muted">
                  Start Date: {{ project.startDate }} | End Date: {{ project.endDate }}
                </small>
              </p>
              <p class="card-text">Milestones: {{ project.milestones.length }}</p>
            </div>
            <div class="card-footer text-end">
              <button
                class="btn btn-primary btn-sm me-2"
                v-if="isAdmin"
                @click="editProject(project.id)"
              >
                Edit
              </button>
              <button
                class="btn btn-danger btn-sm me-2"
                v-if="isAdmin"
                @click="deleteProject(project.id)"
              >
                Delete
              </button>
              <router-link :to="'/project/' + project.id" class="btn btn-secondary btn-sm">
                <i class="fas fa-external-link-alt"></i> Details
              </router-link>
            </div>
          </div>
        </div>
      </section>
    </div>`,

    data() {
        return {
            isAdmin: true, // Simulates admin status; change to false for non-admin view
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
            ]
        };
    },

    created() {
        this.fetchProjects();
    },

    methods: {
        async fetchProjects() {
            try {
                const response = await fetch('/projects'); // Replace with your API endpoint
                const data = await response.json();

                if (!response.ok) {
                    throw new Error(data.message || 'Failed to fetch projects.');
                }

                this.projects = data.projects; // Assumes the API returns { projects: [...] }
            } catch (error) {
                console.error('Error fetching projects:', error);
                alert('Failed to load projects. Please try again later.');
            }
        },

        editProject(projectId) {
            // Redirect to the edit page for the specific project
            this.$router.push(`/project/${projectId}`);
        },

        async deleteProject(projectId) {
            if (confirm(`Are you sure you want to delete project ID: ${projectId}?`)) {
                try {
                    const response = await fetch(`/projects/${projectId}`, {
                        method: 'DELETE',
                        headers: {
                          'Content-Type': 'application/json',
                          'Authentication-Token': localStorage.getItem('auth-token')
                        },
                    });

                    const data = await response.json();

                    if (!response.ok) {
                        throw new Error(data.message || 'Failed to delete project.');
                    }

                    // Remove the project from the list after successful deletion
                    this.projects = this.projects.filter(project => project.id !== projectId);
                    alert('Project deleted successfully.');
                } catch (error) {
                    console.error('Error deleting project:', error);
                    alert('Failed to delete project. Please try again.');
                }
            }
        }
    }
};

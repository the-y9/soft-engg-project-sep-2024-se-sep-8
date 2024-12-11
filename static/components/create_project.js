export default {
  template: `
   <div class="container my-5 create-milestone-page">
    <section class="text-center mb-4">
      <h1 class="display-4">Create Project</h1>
      <p class="lead text-muted">Define your project and set milestones with ease.</p>
    </section>

    <section>
      <form @submit.prevent="createProject" class="shadow p-4 rounded">
        <div class="mb-4">
          <label for="project-heading" class="form-label fw-bold">Project Title</label>
          <input 
            type="text" 
            id="project-heading" 
            v-model="projectHeading" 
            class="form-control" 
            placeholder="Enter project title" 
            required 
          />
        </div>

        <div class="mb-4">
          <label for="project-description" class="form-label fw-bold">Project Description</label>
          <textarea 
            id="project-description" 
            v-model="projectDescription" 
            class="form-control" 
            placeholder="Enter project description" 
            rows="3"
            required
          ></textarea>
        </div>

        <div class="mb-4">
              <label for="project-start-date" class="form-label fw-bold">Start Date</label>
              <input 
                type="date" 
                id="project-start-date" 
                v-model="projectStartDate" 
                class="form-control" 
                required 
              />
        </div>
        <div class="mb-4">
              <label for="project-end-date" class="form-label fw-bold">End Date</label>
              <input 
                type="date" 
                id="project-end-date" 
                v-model="projectEndDate" 
                class="form-control" 
                required 
              />
        </div>

        <div class="d-grid gap-2 mb-4">
          <button 
            type="button" 
            class="btn btn-outline-primary ai-button" 
            @click="fetchMilestonesFromAI"
          >
            Generate AI suggested milestones
          </button>
          <div v-if="aiResponse.length != 0" class="alert alert-info mt-2">
            <strong>AI Response:</strong>
            <ul>
              <li v-for="(milestone, index) in aiResponse" :key="index">
                Task : {{ milestone.task }};  
                <br>
                Description : {{ milestone.description }}
                <br>
              </li>
            </ul>
          </div>
        </div>

        <div v-for="(milestone, index) in milestones" :key="index" class="card mb-4 milestone-card">
          <div class="card-header d-flex justify-content-between align-items-center bg-light">
            <h5 class="mb-0 text-primary">Milestone {{ index + 1 }}</h5>
            <button 
              type="button" 
              class="btn-close" 
              aria-label="Remove" 
              @click="removeMilestone(index)"
            ></button>
          </div>
          <div class="card-body">
            <div class="mb-3">
              <label :for="'milestone-task-' + index" class="form-label fw-bold">Task</label>
              <input 
                type="text" 
                :id="'milestone-task-' + index" 
                v-model="milestone.task" 
                class="form-control" 
                placeholder="Enter task name" 
                required 
              />
            </div>
            <div class="mb-3">
              <label :for="'milestone-desc-' + index" class="form-label fw-bold">Description</label>
              <textarea 
                :id="'milestone-desc-' + index" 
                v-model="milestone.description" 
                class="form-control" 
                placeholder="Enter task description" 
                rows="3"
                required
              ></textarea>
            </div>
            <div class="mb-3">
              <label :for="'milestone-deadline-' + index" class="form-label fw-bold">Deadline</label>
              <input 
                type="date" 
                :id="'milestone-deadline-' + index" 
                v-model="milestone.deadline" 
                class="form-control" 
                required 
              />
            </div>
          </div>
        </div>

        <div class="d-flex justify-content-between align-items-center mb-4">
        <span class="text-muted">{{ milestones.length }} milestones added</span>
          <button 
            type="button" 
            class="btn btn-success add-milestone-button" 
            @click="addMilestone"
          >
            + Add Milestone
          </button>
        </div>

        <div class="d-grid">
          <button 
            type="submit" 
            class="btn btn-primary btn-lg create-button"
          >
            Create Project
          </button>
        </div>
      </form>
    </section>
  </div>`,

  data() {
    return {
      projectHeading: '',
      projectDescription: '',
      projectStartDate: '',
      projectEndDate: '',
      milestones: [], // Start with an empty array
      aiResponse: [] // AI-generated milestones to display in the DOM
    };
  },

  methods: {
    addMilestone() {
      this.milestones.push({ task: '', description: '', deadline: '' });
    },

    removeMilestone(index) {
      this.milestones.splice(index, 1);
    },

    async fetchMilestonesFromAI() {
      try {
        const response = await fetch('/generate-milestones', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': localStorage.getItem('auth-token')
          },
          body: JSON.stringify({
            projectHeading: this.projectHeading,
            projectDescription: this.projectDescription
          })
        });
        const data = await response.json();

        if (data.milestones && data.milestones.length) {
          this.aiResponse = data.milestones.map(milestone => ({
            task: milestone.task,
            description: milestone.description || ''
          }));
        } else {
          alert('No milestones generated by AI. Please try again.');
        }
      } catch (error) {
        console.error('Error fetching milestones from AI:', error);
        alert('Failed to fetch milestones from AI. Please check your connection and try again.');
      }
    },

    async createProject() {
      try {
        const projectResponse = await fetch('/project', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': localStorage.getItem('auth-token')
          },
          body: JSON.stringify({
            title: this.projectHeading,
            description: this.projectDescription,
            start_date: this.projectStartDate,
            end_date: this.projectEndDate
          })
        });

        const projectData = await projectResponse.json();
        console.log(projectData);
        if (!projectResponse.ok) {
          throw new Error(projectData.message || 'Failed to create project.');
        }


        const projectId = projectData.id;

        const milestonesResponse = await fetch('/milestone', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': localStorage.getItem('auth-token')
          },
          body: JSON.stringify({
          project_id: projectId,
          milestones: this.milestones
        })
        });

        const milestonesData = await milestonesResponse.json();
        console.log(milestonesData);

        if (!milestonesResponse.ok) {
          throw new Error(milestonesData.message || 'Failed to create milestones.');
        }

        alert('Project and milestones created successfully!');
        this.$router.push(`/project/${projectId}`);
      } catch (error) {
        console.error('Error creating milestones:', error);
        alert('Failed to create milestones. Please try again.');
      }
    }
  }
};

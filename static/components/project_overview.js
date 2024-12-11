export default {
    template: `
<div class="edit-project-page container my-5">
    <h1 class="mb-4 text-center">Project Overview</h1>
    <div class="card p-4 shadow">
        <!-- Progress Bar -->
        <div class="mb-4">
            <label class="fw-bold">Progress:</label>
            <div class="progress">
                <div class="progress-bar" role="progressbar" :style="{ width: progress + '%' }"
                    :aria-valuenow="progress" aria-valuemin="0" aria-valuemax="100">
                    {{ progress }}%
                </div>
            </div>
        </div>

        <!-- Project Fields -->
        <div class="mb-4">
            <label class="fw-bold">Project Name:</label>
            <h2 v-if="!editing">{{ project.name }}</h2>
            <input v-if="editing" type="text" v-model="editedProject.name" class="form-control"
                placeholder="Enter project name" />
        </div>

        <div class="mb-4">
            <label class="fw-bold">Description:</label>
            <p v-if="!editing">{{ project.description }}</p>
            <textarea v-if="editing" v-model="editedProject.description" class="form-control"
                placeholder="Enter project description" rows="3"></textarea>
        </div>

        <!-- Start and End Date on Single Line -->
        <div class="row g-3 mb-4">
            <div class="col-md-6">
                <label class="fw-bold">Start Date:</label>
                <p v-if="!editing">{{ project.startDate }}</p>
                <input v-if="editing" type="date" v-model="editedProject.startDate" :max="maxStartDate"
                    class="form-control" />
            </div>
            <div class="col-md-6">
                <label class="fw-bold">End Date:</label>
                <p v-if="!editing">{{ project.endDate }}</p>
                <input v-if="editing" type="date" v-model="editedProject.endDate" :min="minEndDate"
                    class="form-control" />
            </div>
        </div>

        <!-- Edit/Save/Cancel Buttons -->
        <div class="d-flex justify-content-end">
            <button v-if="!editing" class="btn btn-outline-primary" @click="toggleEdit">
                <i class="fas fa-edit"></i> Edit
            </button>
            <button v-if="editing" class="btn btn-success me-2" @click="saveChanges">
                <i class="fas fa-save"></i> Save
            </button>
            <button v-if="editing" class="btn btn-danger" @click="cancelChanges">
                <i class="fas fa-times"></i> Cancel
            </button>
        </div>
    </div>

    <h2 class="mt-5 text-center">Milestones</h2>
    <ul class="list-group mb-3">
        <li v-for="milestone in editedMilestone" :key="milestone.id"
            class="list-group-item d-flex justify-content-between align-items-center">
            <div>
                <h5 v-if="!milestone.editing">{{ milestone.taskName }}</h5>
                <input v-if="milestone.editing" type="text" v-model="milestone.taskName"
                    class="form-control form-control-sm" />
                <p v-if="!milestone.editing">{{ milestone.description }}</p>
                <textarea v-if="milestone.editing" v-model="milestone.description" class="form-control form-control-sm"
                    rows="2"></textarea>
            </div>
            <span>
                <span v-if="!milestone.editing">
                    Deadline: {{ milestone.deadline }}
                    <button class="btn btn-sm btn-outline-primary ms-2" @click="editMilestone(milestone)">
                        <i class="fas fa-edit"></i> Edit
                    </button>
                </span>
                <span v-if="milestone.editing">
                    <input type="date" v-model="milestone.deadline" class="form-control form-control-sm" />
                    <button class="btn btn-sm btn-success ms-2" @click="saveMilestone(milestone)">
                        <i class="fas fa-save"></i> Save
                    </button>
                    <button class="btn btn-sm btn-danger ms-2" @click="cancelMilestoneEdit(milestone)">
                        <i class="fas fa-times"></i> Cancel
                    </button>
                </span>
            </span>
        </li>
    </ul>
    <div class="d-flex justify-content-center mt-4">
        <router-link :to="'/milestone_tracker/' + id" class="btn btn-primary p-2">
            <i class="fas fa-chart-line"></i> Track Milestones
        </router-link>
    </div>
</div>
    `,
  
    data() {
      return {
        id : this.$route.params.id,
        project: {
          name: "Programmable client-driven synergy",
          description: "This is a synthetic project used for demo purposes.",
          startDate: "2024-01-01",
          endDate: "2024-12-31",
          milestones: [
            { id: 5464, taskName: 'Milestone 1', description: 'Description 1', deadline: '2024-12-31'},
            { id: 5345, taskName: 'Milestone 1', description: 'Description 1', deadline: '2024-12-31'},
            { id: 5464354, taskName: 'Milestone 1', description: 'Description 1', deadline: '2024-12-31'}
            // ... other milestones ...
          ]
        },
        editedProject: {}, // Holds editable values during edit mode
        editedMilestone: {},
        editing: false, // Toggles editing mode
        progress: 0, // Tracks progress percentage
      };
    },
    
    async beforeCreate(){
      try {
        const response = await fetch(`/projects/${this.$route.params.id}`);
        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.message || "Failed to fetch project details.");
        }

        this.project = data;
      } catch (error) {
        console.error("Error fetching project details:", error);
        alert("Failed to load project details.");
      }
    },
    created(){
      this.editedProject = {name: this.project.name,
                            description: this.project.description,
                            startDate: this.project.startDate,
                            endDate: this.project.endDate
                          }; // Clone project for editing
      this.editedMilestone = this.project.milestones.map(milestone => ({ 
                                                                        ...milestone,
                                                                         editing: false }));
      console.log(this.editedMilestone)
      this.calculateProgress();
    },

    watch: {
      // Recalculate progress whenever startDate or endDate changes
      "project.startDate": "calculateProgress",
      "project.endDate": "calculateProgress",
    },
    computed: {
        maxStartDate() {
          return this.editedProject.endDate ? this.editedProject.endDate : '';
        },
        minEndDate() {
          return this.editedProject.startDate ? this.editedProject.startDate : '';
        },
      },
  
    methods: {
  
      toggleEdit() {
        this.editing = true;
      },
  
      saveChanges() {
        this.project.name = this.editedProject.name;
        this.project.description = this.editedProject.description;
        this.project.startDate = this.editedProject.startDate;
        this.project.endDate = this.editedProject.endDate;
        this.editing = false;
        this.calculateProgress(); // Recalculate progress after saving
  
        // Optional: Update project via API
        this.updateProject();
      },
  
      cancelChanges() {
        this.editedProject = {name: this.project.name,
          description: this.project.description,
          startDate: this.project.startDate,
          endDate: this.project.endDate
          }; // Revert to original project data
        this.editing = false;
      },
      editMilestone(milestone) {
        const index = this.editedMilestone.findIndex(item => item.id === milestone.id);
        if (index !== -1) {
            this.$set(this.editedMilestone, index, { ...milestone, editing: true });
        }
        console.log(this.editedMilestone);
    },
    
  
    saveMilestone(milestone) {
      const index = this.editedMilestone.findIndex(item => item.id === milestone.id);
      if (index !== -1) {
          this.$set(this.editedMilestone, index, { ...milestone, editing: false });
      }
      this.updateMilestone(milestone);
  },
  
  cancelMilestoneEdit(milestone) {
    this.editedMilestone = this.project.milestones.map(m => ({
        ...m,
        editing: false
    }));
},


      async updateProject() {
        try {
          const response = await fetch(`/projects/${this.id}`, {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
              'Authentication-Token': localStorage.getItem('auth-token')
            },
            body: JSON.stringify(this.editedProject),
          });
  
          if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || "Failed to update project.");
          }
  
          alert("Project updated successfully!");
        } catch (error) {
          console.error("Error updating project:", error);
          alert("Failed to update project. Please try again.");
        }
      },
      async updateMilestone(milestone) {
        delete milestone.editing;
        try {
          const response = await fetch(`/milestone/${milestone.id}`, {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
              'Authentication-Token': localStorage.getItem('auth-token')
            },
            body: JSON.stringify(milestone),
          });
  
          if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || "Failed to update project.");
          }
  
          alert("Milestone updated successfully!");
        } catch (error) {
          console.error("Error updating milestone:", error);
          alert("Failed to update milestone. Please try again.");
        }
      },
  
      calculateProgress() {
        const startDate = new Date(this.project.startDate);
        const endDate = new Date(this.project.endDate);
        const today = new Date();
  
        if (isNaN(startDate) || isNaN(endDate) || startDate >= endDate) {
          this.progress = 0; // Default to 0% for invalid dates
          return;
        }
  
        const totalDuration = endDate - startDate;
        const elapsedDuration = today - startDate;
        this.progress = Math.min(100, Math.max(0, Math.floor((elapsedDuration / totalDuration) * 100)));
      },
    },
  };
  
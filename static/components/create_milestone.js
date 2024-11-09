// export default {
//     template: `
//      <div class="create-milestone-page">
//       <section class="page-header">
//         <div class="header-content">
//           <h1 class="hero-title">Create Milestone</h1>
//           <p class="hero-subtitle">Define your project milestones and set tasks with ease.</p>
//         </div>
//       </section>

//       <section class="milestone-form">
//         <form @submit.prevent="createMilestone">
//           <div class="form-group">
//             <label for="project-heading" class="form-label">Project Heading</label>
//             <input type="text" id="project-heading" v-model="projectHeading" class="form-control" placeholder="Enter project heading" required />
//           </div>

//           <div class="form-group">
//             <label for="num-milestones" class="form-label">Number of Milestones</label>
//             <select id="num-milestones" v-model.number="numMilestones" class="form-control" @change="generateMilestoneInputs" required>
//               <option v-for="n in 10" :key="n" :value="n">{{ n }}</option>
//             </select>
//           </div>

//           <div v-for="(milestone, i) in numMilestones" :key="i + 1" class="milestone-inputs">
//             <h3>Milestone {{ i + 1 }}</h3>
//             <div class="form-group">
//                 <label :for="'milestone-task-' + (i + 1)" class="form-label">Task</label>
//                 <input type="text" :id="'milestone-task-' + (i + 1)" v-model="milestones[i].task" class="form-control" placeholder="Enter task name" required />
//             </div>
//             <div class="form-group">
//                 <label :for="'milestone-desc-' + (i + 1)" class="form-label">Description</label>
//                 <textarea :id="'milestone-desc-' + (i + 1)" v-model="milestones[i].description" class="form-control" placeholder="Enter task description" required></textarea>
//             </div>
//           </div>

//           <button type="submit" class="create-button">Create Milestone</button>
//         </form>
//       </section>
//     </div>`,

//     data() {
//         return {
//             projectHeading: '',
//             numMilestones: 1,
//             milestones: [
//                 { task: '', description: '' }
//             ]
//         }
//     },

//     methods: {
//         generateMilestoneInputs() {
//             this.milestones = Array.from({ length: this.numMilestones }, () => ({ task: '', description: '' }));
//         },

//         createMilestone() {
//             console.log('Project Heading:', this.projectHeading);
//             console.log('Milestones:', this.milestones);
//             alert('Milestone created successfully!');
//             // Logic for submitting the milestone data can be added here
//         }
//     }
// }




export default {
    template: `
     <div class="create-milestone-page">
      <section class="page-header">
        <div class="header-content">
          <h1 class="hero-title">Create Milestone</h1>
          <p class="hero-subtitle">Define your project milestones and set tasks with ease.</p>
        </div>
      </section>

      <section class="milestone-form">
        <form @submit.prevent="createMilestone">
          <div class="form-group">
            <label for="project-heading" class="form-label">Project Heading</label>
            <input type="text" id="project-heading" v-model="projectHeading" class="form-control" placeholder="Enter project heading" required />
          </div>

          <div class="form-group ai-group">
            <label for="project-description" class="form-label">Project Description</label>
            <input type="text" id="project-description" v-model="projectDescription" class="form-control" placeholder="Enter project description" required />
            <button type="button" class="ai-button" @click="fetchMilestonesFromAI">Generate With AI</button>
          </div>

          <div class="form-group">
            <label for="num-milestones" class="form-label">Number of Milestones</label>
            <select id="num-milestones" v-model.number="numMilestones" class="form-control" @change="generateMilestoneInputs" required>
              <option v-for="n in 10" :key="n" :value="n">{{ n }}</option>
            </select>
          </div>

          <div v-for="i in numMilestones" :key="i" class="milestone-inputs">
            <h3>Milestone {{ i }}</h3>
            <div class="form-group">
              <label :for="'milestone-task-' + i" class="form-label">Task</label>
              <input type="text" :id="'milestone-task-' + i" v-model="milestones[i - 1].task" class="form-control" placeholder="Enter task name" required />
            </div>
            <div class="form-group">
              <label :for="'milestone-desc-' + i" class="form-label">Description</label>
              <textarea :id="'milestone-desc-' + i" v-model="milestones[i - 1].description" class="form-control" placeholder="Enter task description" required></textarea>
            </div>
          </div>

          <button type="submit" class="create-button">Create Milestone</button>
        </form>
      </section>
    </div>`,

    data() {
        return {
            projectHeading: '',
            projectDescription: '',
            numMilestones: 1,
            milestones: [
                { task: '', description: '' }
            ]
        }
    },

    methods: {
        generateMilestoneInputs() {
            this.milestones = Array.from({ length: this.numMilestones }, () => ({ task: '', description: '' }));
        },

        async fetchMilestonesFromAI() {
            try {
                const response = await fetch('https://api.example.com/generate-milestones', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        projectHeading: this.projectHeading,
                        projectDescription: this.projectDescription
                    })
                });
                const data = await response.json();

                // Populate the milestones array with the response
                if (data.milestones && data.milestones.length) {
                    this.numMilestones = data.milestones.length;
                    this.milestones = data.milestones.map(milestone => ({
                        task: milestone.task,
                        description: milestone.description
                    }));
                } else {
                    alert('No milestones generated by AI. Please try again.');
                }
            } catch (error) {
                console.error('Error fetching milestones from AI:', error);
                alert('Failed to fetch milestones from AI. Please check your connection and try again.');
            }
        },

        createMilestone() {
            console.log('Project Heading:', this.projectHeading);
            console.log('Project Description:', this.projectDescription);
            console.log('Milestones:', this.milestones);
            alert('Milestone created successfully!');
            // Logic for submitting the milestone data can be added here
        }
    }
}
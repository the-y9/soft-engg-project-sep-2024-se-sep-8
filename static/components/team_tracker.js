export default {
    template: `
     <div class="milestone-tracker-page">
      <section class="page-header">
        <div class="container">
          <div class="row">
            <div class="col text-center">
              <h1 class="display-4">Team Tracker</h1>
              <p class="lead">Monitor the contributions of each team member for your project.</p>
            </div>
          </div>
        </div>
      </section>

      <section class="container">
        <div v-if="loading" class="text-center">
          <div class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>
        <div v-else>
          <div class="team-section my-4">
            <div class="d-flex justify-content-between align-items-center mb-3">
            <h2 class="h4">Team: {{ team.name }}</h2>
            <button class="btn btn-warning mb-3" @click="notifyTeam">Notify Team</button>
            </div>
            <div v-for="member in team.members" :key="member.id" class="member-card card p-3 mb-3">
              <h3 class="h5">{{ member.name }}</h3>
              <p class="mb-2">Total GitHub Commits: {{ member.totalCommits }}</p>
              <h4 class="h6">Last 5 GitHub Commits:</h4>
              <ul>
                <li v-for="commit in member.lastCommits" :key="commit.id">{{ commit.date }} - {{ commit.message }}</li>
              </ul>
              <button class="btn btn-sm btn-info mt-2" @click="notifyMember(member.id)">Notify Member</button>
            </div>
          </div>
        </div>
      </section>
    </div>`,

    data() {
        return {
            project_id : null,
            team_id : null,
            team: {
                id: 1,
                name: 'Team Alpha',
                members: [
                    {
                        id: 1,
                        name: 'Alice',
                        totalCommits: 120,
                        lastCommits: [
                            { id: 'c1', date: '2024-06-01 10:30', message: 'Fixed bug in user authentication' },
                            { id: 'c2', date: '2024-05-31 14:20', message: 'Added new feature for profile management' },
                            { id: 'c3', date: '2024-05-30 09:10', message: 'Refactored codebase' },
                            { id: 'c4', date: '2024-05-29 17:05', message: 'Updated dependencies' },
                            { id: 'c5', date: '2024-05-28 08:50', message: 'Improved performance of data processing' }
                        ]
                    },
                    {
                        id: 2,
                        name: 'Bob',
                        totalCommits: 95,
                        lastCommits: [
                            { id: 'c6', date: '2024-06-01 12:45', message: 'Implemented search functionality' },
                            { id: 'c7', date: '2024-05-30 10:00', message: 'Enhanced UI for dashboard' },
                            { id: 'c8', date: '2024-05-29 13:30', message: 'Fixed CSS issues' },
                            { id: 'c9', date: '2024-05-28 16:15', message: 'Added unit tests' },
                            { id: 'c10', date: '2024-05-27 11:20', message: 'Created initial project setup' }
                        ]
                    }
                ]
            },
            loading: false
        }
    },

    async created() {
        this.loading = true;
        this.project_id = this.$route.params.projID;
        this.team_id = this.$route.params.teamID;
        await this.fetchTeamDetails(this.project_id, this.team_id);
        this.loading = false;
    },

    methods: {
        async fetchTeamDetails(projectId, teamId) {
            try {
                const response = await fetch(`/projects/${projectId}/teams/${teamId}`);
                const data = await response.json();
                if (!response.ok) {
                    throw new Error(data.message || "Failed to fetch team details.");
                }
                this.team = data.team;
            } catch (error) {
                console.error("Error fetching team details:", error);
                alert("Failed to load team details.");
            }
        },
        notifyTeam() {
            this.$router.push(`/notification?team_id=${this.team_id}&team_name=${this.team.name}`);
        },
        notifyMember(memberId) {
            const member = this.team.members.find(m => m.id === memberId);
            this.$router.push(`/notification?team_name=${this.team.name}&member_id=${memberId}&member_name=${member.name}`);
        }
    }
};

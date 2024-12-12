export default {
template:`
  <div>
    <h1>Team Commit History</h1>
    <div v-if="loading" class="loading-spinner">
      <p>Loading commit history...</p>
    </div>
    <div v-else-if="teamData" class="team-commit-history">
      <h4>Team Name: {{ teamData.name }}</h4>
      <ul>
        <li v-for="member in teamData.members" :key="member.id" class="team-member">
          <p><strong>Name:</strong> {{ member.name }}</p>
          <p><strong>Total Commits:</strong> {{ member.totalCommits }}</p>
          <div v-if="member.lastCommits.length > 0">
            <p><strong>Last Commits:</strong></p>
            <ul>
              <li v-for="commit in member.lastCommits" :key="commit.id">
                <p><strong>Commit Message:</strong> {{ commit.message }}</p>
                <p><strong>Date:</strong> {{ commit.date }}</p>
                <p><strong>Author:</strong> {{ commit.author }}</p>
              </li>
            </ul>
          </div>
          <p v-else>No recent commits available.</p>
        </li>
      </ul>
    </div>
    <div v-else>
      <p>No team commit history available.</p>
    </div>
  </div>
`,


  data() {
    return {
      teamData: null,
      loading: true,
    };
  },
  methods: {
    async fetchCommitHistory() {
      try {
        console.log("fetchCommitHistory triggered");
        const projectId = localStorage.getItem('project_id');
        const teamid = localStorage.getItem('team_id');
        const res = await fetch(`/projects/${projectId}/teams/${teamid}`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('auth-token')}`,
            'Content-Type': 'application/json',
          },
        });

        if (res.ok) {
          const commitHistory = await res.json();
          this.teamData = commitHistory.team;
          console.log("Commit history fetched:", this.teamData);
        } else {
          console.error('Failed to fetch commit history.');
        }
      } catch (error) {
        console.error('Error fetching commit history:', error);
      } finally {
        this.loading = false;
      }
    },
  },
  created() {
    this.fetchCommitHistory();
  },
};


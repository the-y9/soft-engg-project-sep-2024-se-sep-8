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
          <div class="dashboard-card" @click="goToCreateMilestone">
            <img src="static/images/milestone.webp" alt="Create Milestone" class="dashboard-image" />
            <h3 class="dashboard-card-title">Create Milestone</h3>
            <p class="dashboard-card-description">Plan and define your project milestones with ease.</p>
          </div>
          <div class="dashboard-card" @click="goToMilestoneTracker">
            <img src="static/images/track_milestone.webp" alt="Milestone Tracker" class="dashboard-image" />
            <h3 class="dashboard-card-title">Milestone Tracker</h3>
            <p class="dashboard-card-description">Track and monitor the progress of your milestones in real-time.</p>
          </div>
          <div class="dashboard-card" @click="goToDocumentAnalyzer">
            <img src="static/images/doc_analyzer.webp" alt="Document Analyzer" class="dashboard-image" />
            <h3 class="dashboard-card-title">Document Analyzer</h3>
            <p class="dashboard-card-description">Analyze documents and extract key insights quickly.</p>
          </div>
        </div>
        </center>
      </section>
    </div>`,
    
    data() {
        return {
            options: [
                { id: 1, title: "Create Milestone", description: "Plan and define your project milestones with ease.", image: "static/images/milestone.webp" },
                { id: 2, title: "Milestone Tracker", description: "Track and monitor the progress of your milestones in real-time.", image: "static/images/track_milestone.webp" },
                { id: 3, title: "Document Analyzer", description: "Analyze documents and extract key insights quickly.", image: "static/images/doc_analyzer.webp" },
            ]
        }
    },
    methods: {
        goToCreateMilestone() {
            this.$router.push('/create_milestone')
        },
        goToMilestoneTracker() {
            this.$router.push('/milestone-tracker')
        },
        goToDocumentAnalyzer() {
            this.$router.push('/document-analyzer')
        }
    }
}
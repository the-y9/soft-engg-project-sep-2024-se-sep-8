// import librarian_dashboard from "./librarian_dashboard.js"
// import user_dashboard from "./user_dashboard.js"

export default  {
    template: `
     <div class="landing-page">

      <section class="hero">
        <div class="hero-content">
          <h1 class="hero-title">Track Your Project Milestones Effortlessly</h1>
          <p class="hero-subtitle">Stay on top of your project’s progress, deadlines, and key milestones with ease.</p>
          <button class="cta-button" @click="goToRegister">Get Started</button>
        </div>
      </section>

      <section class="features">
        <h2 class="section-title">Why Choose Us?</h2>
        <center>
        <div class="feature-cards">
          <div class="feature-card" v-for="feature in features" :key="feature.id" >
            <img :src="feature.image" alt="Feature Image" class="feature-image" />
            <h3 class="feature-title">{{ feature.title }}</h3>
            <p class="feature-description">{{ feature.description }}</p>
          </div>
        </div>
        </center>
      </section>

      <section class="cta-section">
        <h2 class="cta-title">Ready to Get Started?</h2>
        <p class="cta-subtitle">Sign up today and start managing your project milestones like a pro.</p>
        <button class="cta-button" @click="goToRegister">Sign Up Now</button>
      </section>
    </div>`,
    data(){
        return {
            userRole: localStorage.getItem('role'),
            features: [
                { id: 1, title: "Real-Time Tracking", description: "Monitor project milestones in real time and stay updated with every step.", image: "static/images/2880399.jpg" },
                { id: 2, title: "Team Collaboration", description: "Collaborate with your team and keep everyone aligned on project goals.", image: "static/images/2996609.jpg" },
                { id: 3, title: "Detailed Reporting", description: "Generate reports to get insights on your project’s progress and performance.", image: "static/images/20945194.jpg" },
              ]
        }
    },

    components:{
        // librarian_dashboard,
        // user_dashboard,
    }
}
import home from './components/home.js'
import login from './components/login.js'
import register from './components/register.js'
import Not_found_page from './components/Not_found_page.js'
import instructor_dashboard from './components/instructor_dashboard.js'
<<<<<<< HEAD
import create_milestone from './components/create_milestone.js'
import milestone_tracker from './components/milestone_tracker.js'   
=======
import generate_milestones from './components/generate_milestones.js'
import student_perfomance_prediction from './components/student_perfomance_prediction.js'

>>>>>>> cc87bd2 (added new components)
const routes = [
    { path:'/' , component : home , name:'home'},
    { path:'/login', component: login , name:'login'},
    { path:'/404_page' , component: Not_found_page , name:'404_page'},
    { path:'/register', component: register, name:'register'},
    { path:'/instructor_dashboard', component: instructor_dashboard, name:'instructor_dashboard'},
<<<<<<< HEAD
    { path:'/create_milestone', component: create_milestone, name:'create_milestone'},
    { path:'/milestone_tracker', component: milestone_tracker, name:'milestone_tracker'},
=======
    { path: '/student_performance', component: student_perfomance_prediction, name: 'student_performance'},
    { path: '/generate_milestones', component: generate_milestones, name: 'generate_milestones'}
>>>>>>> cc87bd2 (added new components)
] 

export default new VueRouter({
    routes,
})
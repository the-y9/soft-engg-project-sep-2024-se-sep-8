import home from './components/home.js'
import login from './components/login.js'
import register from './components/register.js'
import Not_found_page from './components/Not_found_page.js'
import instructor_dashboard from './components/instructor_dashboard.js'
import create_milestone from './components/create_milestone.js'
import milestone_tracker from './components/milestone_tracker.js'  
import notification from './components/notification.js'
import student_dashboard from './components/student_dashboard.js'

export default [
    { path:'/' , component : home , name:'Home'},
    { path:'/login', component: login , name:'Login'},
    { path:'/404_page' , component: Not_found_page , name:'404_page'},
    { path:'/register', component: register, name:'Register'},
    { path:'/instructor_dashboard', component: instructor_dashboard, name:'Instructor Dashboard'},
    { path:'/create_milestone', component: create_milestone, name:'Create Milestone'},
    { path:'/milestone_tracker', component: milestone_tracker, name:'Milestone Tracker'},
    { path:'/notification', component: notification, name:'Notification'},
    { path:'/student_dashboard', component: student_dashboard, name:'Student Dashboard'},
]
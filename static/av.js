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
    { path:'/' , component : home , name:'home'},
    { path:'/login', component: login , name:'login'},
    { path:'/404_page' , component: Not_found_page , name:'404_page'},
    { path:'/register', component: register, name:'register'},
    { path:'/instructor_dashboard', component: instructor_dashboard, name:'instructor_dashboard'},
    { path:'/create_milestone', component: create_milestone, name:'create_milestone'},
    { path:'/milestone_tracker', component: milestone_tracker, name:'milestone_tracker'},
    { path:'/notification', component: notification, name:'notification'},
    { path:'/student_dashboard', component: student_dashboard, name:'student_dashboard'},
]
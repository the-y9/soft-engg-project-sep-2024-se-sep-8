import student_perfomance_prediction from './components/student_perfomance_prediction.js'
import projects from './components/projects.js'
import project_overview from './components/project_overview.js'

export default [
    { path: '/student_performance', component: student_perfomance_prediction, name: 'Student Performance'},
    { path: '/project', component: projects, name:'Projects'},
    { path:'/project/:id', component: project_overview, name:'Project Overview'},
]
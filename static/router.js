import avroutes from './av.js'
import ntroutes from './nt.js'

const routes = [
    ...avroutes,
    ...ntroutes
] 

export default new VueRouter({
    routes,
})
import vue from 'vue'
import router from 'vue-router'
import routes from './router'



const originalPush = router.prototype.push
router.prototype.push = function push(location) {
    return originalPush.call(this, location).catch(err => err)
}

vue.use(router)

export default new router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

export default defineNuxtRouteMiddleware((to, from) => {
    if (process.client) {
        const userAuthStore = useUserAuthStore()
        if (userAuthStore.isAuthenticated && userAuthStore.userData){
            if (userAuthStore.userData['role']==='student' && !userAuthStore.studentData.subjects ){
                userAuthStore.getStudentData()
                userAuthStore.getNotifications()
            }
            else if (userAuthStore.userData['role']==='staff'){
                return navigateTo('/staff')
            }
        }
        else {
            return navigateTo('/')
        }
    }
  })
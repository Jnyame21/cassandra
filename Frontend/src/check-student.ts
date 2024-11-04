export default defineNuxtRouteMiddleware((to, from) => {
    if (import.meta.client) {
        const userAuthStore = useUserAuthStore()
        if (userAuthStore.userData?.['role']==='student' && !userAuthStore.studentData?.subjects ){
            userAuthStore.getStudentData()
            userAuthStore.getNotifications()
        }
        else if (userAuthStore.userData?.['role']==='staff'){
            return navigateTo('/staff')
        }
    }
  })
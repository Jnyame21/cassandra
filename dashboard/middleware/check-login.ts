export default defineNuxtRouteMiddleware((to, from) => {
    if (process.client) {
        const userAuthStore = useUserAuthStore()
        if (userAuthStore.isAuthenticated && userAuthStore.userData && userAuthStore.userData['role']==='student'){
            return navigateTo('/student')
        }
        else if (userAuthStore.isAuthenticated && userAuthStore.userData && userAuthStore.userData['role']==='staff' ){
            return navigateTo('/staff')
        }
        else if (userAuthStore.isAuthenticated && userAuthStore.userData && userAuthStore.userData['role']==='head'){
            return navigateTo('/staff')
        }
    }
    
  })
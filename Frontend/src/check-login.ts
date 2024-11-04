export default defineNuxtRouteMiddleware((to, from) => {
    if (import.meta.client) {
        const userAuthStore = useUserAuthStore()
        if (userAuthStore.authTokens && userAuthStore.isAuthenticated && userAuthStore.userData && userAuthStore.userData['role']==='student'){
            return navigateTo('/student')
        }
        else if (userAuthStore.authTokens && userAuthStore.isAuthenticated && userAuthStore.userData && userAuthStore.userData['role']==='staff' ){
            return navigateTo('/staff')
        }
        else if (userAuthStore.authTokens && userAuthStore.isAuthenticated && userAuthStore.userData && userAuthStore.userData['role']==='head'){
            return navigateTo('/staff')
        }
    }
  })

export default defineNuxtRouteMiddleware(async(to, from) => {
    if (import.meta.client) {
        const userAuthStore = useUserAuthStore()
        if (!userAuthStore.authTokens){
            const authTokens = localStorage.getItem("authTokens")
            if (authTokens){
                userAuthStore.authTokens = JSON.parse(authTokens)
                userAuthStore.isAuthenticated = true
                if (!userAuthStore.userData){
                    try{
                        await userAuthStore.getUserData()
                    }
                    catch(error){
                        userAuthStore.logoutUser()
                        return navigateTo('/')
                    }
                }
            }else{
                if (to.path === '/'){
                    return;
                }else{
                    userAuthStore.logoutUser()
                    return navigateTo('/')
                }
            }
        }
    }
  })
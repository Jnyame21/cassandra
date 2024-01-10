
export default defineNuxtRouteMiddleware(async(to, from) => {
    if (process.client) {
        const userAuthStore = useUserAuthStore()
        const authTokens = localStorage.getItem("authTokens")
        if (authTokens && userAuthStore.isAuthenticated===false){
            userAuthStore.authTokens = JSON.parse(authTokens)
            const Router = useRouter()

            if (!userAuthStore.userData || !userAuthStore.authTokens){
                await userAuthStore.getUserData()
                .then(response =>{
                    userAuthStore.isAuthenticated = true
                })
                .catch(e =>{
                    userAuthStore.logoutUser()
                    Router.push('/')
                    return Promise.reject(e)
                })
            }
        }
    }
  })
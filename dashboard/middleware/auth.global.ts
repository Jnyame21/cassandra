import { jwtDecode } from "jwt-decode"

export default defineNuxtRouteMiddleware((to, from) => {
    if (process.client) {
        const userAuthStore = useUserAuthStore()
        const authTokens = localStorage.getItem("authTokens")
        if (authTokens && userAuthStore.isAuthenticated===false){
            userAuthStore.isAuthenticated = true
            if (!userAuthStore.userData || !userAuthStore.authTokens){
                const userInfo: any = jwtDecode(JSON.parse(authTokens).access)
                userAuthStore.userData = userInfo
                userAuthStore.activeAcademicYear = userInfo['academic_year']['name']
                userAuthStore.activeTerm = userInfo['current_sem']
                userAuthStore.authTokens = JSON.parse(authTokens)
            }
        }
    }
    
  })
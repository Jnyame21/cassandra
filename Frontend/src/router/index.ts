import {
  createRouter,
  createWebHistory,
  type NavigationGuardNext,
} from 'vue-router'
import StaffView from '@/views/StaffView.vue'
import StudentView from '@/views/StudentView.vue'
import LoginView from '@/views/LoginView.vue'
import { useUserAuthStore } from '@/stores/userAuthStore'
import { headRoles } from '@/utils/util'
import SuperUserView from '@/views/SuperUserView.vue'

const checkAuth = async () => {
  let isAuthenticated = false
  const userAuthStore = useUserAuthStore()
  if (!userAuthStore.isAuthenticated) {
    if (userAuthStore.authTokens) {
      localStorage.setItem(
        'authTokens',
        JSON.stringify(userAuthStore.authTokens),
      )
      if (!userAuthStore.userData) {
        try {
          await userAuthStore.getUserData()
          userAuthStore.isAuthenticated = true
          isAuthenticated = true
        } catch {
          userAuthStore.logoutUser()
        }
      } else {
        userAuthStore.isAuthenticated = true
        isAuthenticated = true
      }
    }
    const authTokens = localStorage.getItem('authTokens')
    if (authTokens) {
      userAuthStore.authTokens = JSON.parse(authTokens)
      if (!userAuthStore.userData) {
        try {
          await userAuthStore.getUserData()
          userAuthStore.isAuthenticated = true
          isAuthenticated = true
        } catch {
          userAuthStore.logoutUser()
        }
      } else {
        userAuthStore.isAuthenticated = true
        isAuthenticated = true
      }
    }
  } else {
    isAuthenticated = true
  }
  return isAuthenticated
}

const checkSuperuser = async (to: any, from: any, next: NavigationGuardNext) => {
  const userAuthStore = useUserAuthStore()
  const isAuthenticated = await checkAuth()
  if (!isAuthenticated) {
    userAuthStore.logoutUser()
    if (to.path !== '/') {
      return next('/')
    }
  } 
  else if (!userAuthStore.superUserData.schools && userAuthStore.userData?.['role'].toLowerCase() === 'superuser') {
    userAuthStore.getSuperUserData()
  } 
  else if (userAuthStore.userData?.['role'].toLowerCase() === 'student') {
    if (!userAuthStore.studentData.students){
      userAuthStore.getStudentData()
    }
    next('/student')
  } 
  else if (userAuthStore.userData?.['role']?.toLowerCase() === 'staff') {
    if (!userAuthStore.teacherData.staff &&  ['teacher', 'hod'].includes(userAuthStore.userData['staff_role'].toLowerCase())) {
      userAuthStore.getTeacherData()
      userAuthStore.getTeacherStudentsAssessments()
      userAuthStore.getTeacherStudentsExams()
      userAuthStore.getTeacherStudentResults()
      if (userAuthStore.userData?.['staff_role'].toLowerCase() === 'hod') {
        userAuthStore.getHodData()
      }
    } 
    else if (!userAuthStore.adminData.staff && userAuthStore.userData?.['staff_role'].toLowerCase() === 'administrator') {
      userAuthStore.getAdminData()
    }
    else if (!userAuthStore.headData.staff && headRoles.includes(userAuthStore.userData?.['staff_role'].toLowerCase())) {
      userAuthStore.getHeadData()
    }
    next('/staff')
  } 
  else {
    if (to.path !== '/') {
      return next('/')
    }
  }
  next()
}

const checkStudent = async (to: any, from: any, next: NavigationGuardNext) => {
  const userAuthStore = useUserAuthStore()
  const isAuthenticated = await checkAuth()
  if (!isAuthenticated) {
    userAuthStore.logoutUser()
    if (to.path !== '/') {
      return next('/')
    }
  } 
  else if (!userAuthStore.studentData.students && userAuthStore.userData?.['role'].toLowerCase() === 'student') {
    userAuthStore.getStudentData()
  } 
  else if (userAuthStore.userData?.['role']?.toLowerCase() === 'staff') {
    if (!userAuthStore.teacherData.staff && ['teacher', 'hod'].includes(userAuthStore.userData['staff_role'].toLowerCase())) {
      userAuthStore.getTeacherData()
      userAuthStore.getTeacherStudentsAssessments()
      userAuthStore.getTeacherStudentsExams()
      userAuthStore.getTeacherStudentResults()
      if (userAuthStore.userData?.['staff_role'].toLowerCase() === 'hod') {
        userAuthStore.getHodData()
      }
    } 
    else if (!userAuthStore.adminData.staff && userAuthStore.userData?.['staff_role'].toLowerCase() === 'administrator') {
      userAuthStore.getAdminData()
    }
    else if (!userAuthStore.headData.staff && headRoles.includes(userAuthStore.userData?.['staff_role'].toLowerCase())) {
      userAuthStore.getHeadData()
    }
    next('/staff')
  } 
  else if (userAuthStore.userData?.['role'].toLowerCase() === 'superuser') {
    if (!userAuthStore.superUserData.schools){
      userAuthStore.getSuperUserData()
    }
    return next('/superuser')
  } 
  else {
    if (to.path !== '/') {
      return next('/')
    }
  }
  next()
}

const checkStaff = async (to: any, from: any, next: NavigationGuardNext) => {
  const userAuthStore = useUserAuthStore()
  const isAuthenticated = await checkAuth()
  if (!isAuthenticated) {
    userAuthStore.logoutUser()
    if (to.path !== '/') {
      return next('/')
    }
  }
  if (!userAuthStore.teacherData.staff && ['teacher', 'hod'].includes(userAuthStore.userData['staff_role'].toLowerCase())) {
    userAuthStore.getTeacherData()
    userAuthStore.getTeacherStudentsAssessments()
    userAuthStore.getTeacherStudentsExams()
    userAuthStore.getTeacherStudentResults()
    if (userAuthStore.userData?.['staff_role'].toLowerCase() === 'hod') {
      userAuthStore.getHodData()
    }
  } 
  else if (!userAuthStore.adminData.staff && userAuthStore.userData?.['staff_role'].toLowerCase() === 'administrator') {
    userAuthStore.getAdminData()
  } 
  else if (!userAuthStore.headData.staff && headRoles.includes(userAuthStore.userData?.['staff_role'].toLowerCase())) {
    userAuthStore.getHeadData()
  }
  else if (userAuthStore.userData?.['role'] === 'student') {
    if (!userAuthStore.studentData.students) {
      userAuthStore.getStudentData()
    }
    return next('/student')
  } 
  else if (userAuthStore.userData?.['role'].toLowerCase() === 'superuser') {
    if (!userAuthStore.superUserData.schools){
      userAuthStore.getSuperUserData()
    }
    return next('/superuser')
  } 
  else {
    if (to.path !== '/') {
      return next('/')
    }
  }
  next()
}

const checkLogin = async (to: any, from: any, next: NavigationGuardNext) => {
  const userAuthStore = useUserAuthStore()
  const isAuthenticated = await checkAuth()
  if (isAuthenticated && userAuthStore.userData?.['role'].toLowerCase() === 'staff') {
    return next('/staff')
  } 
  else if (isAuthenticated && userAuthStore.userData?.['role'].toLowerCase() === 'student') {
    return next('/student')
  }
  else if (isAuthenticated && userAuthStore.userData?.['role'].toLowerCase() === 'superuser') {
    return next('/superuser')
  } 
  next()
}

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: LoginView,
      beforeEnter: async (to, from, next) => {
        await checkLogin(to, from, next)
      },
    },
    {
      path: '/student',
      name: 'student',
      component: StudentView,
      beforeEnter: async (to, from, next) => {
        await checkStudent(to, from, next)
      },
    },
    {
      path: '/staff',
      name: 'staff',
      component: StaffView,
      beforeEnter: async (to, from, next) => {
        await checkStaff(to, from, next)
      },
    },
    {
      path: '/superuser',
      name: 'superuser',
      component: SuperUserView,
      beforeEnter: async (to, from, next) => {
        await checkSuperuser(to, from, next)
      },
    },
  ],
})

export default router

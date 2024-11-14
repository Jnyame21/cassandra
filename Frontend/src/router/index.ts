import {
  createRouter,
  createWebHistory,
  type NavigationGuardNext,
} from 'vue-router'
import StaffView from '@/views/StaffView.vue'
import StudentView from '@/views/StudentView.vue'
import LoginView from '@/views/LoginView.vue'
import { useUserAuthStore } from '@/stores/userAuthStore'

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

const checkStudent = async (to: any, from: any, next: NavigationGuardNext) => {
  const userAuthStore = useUserAuthStore()
  const isAuthenticated = await checkAuth()
  if (!isAuthenticated) {
    userAuthStore.logoutUser()
    if (to.path !== '/') {
      return next('/')
    }
  } else if (userAuthStore.userData?.['role'] === 'student') {
    if (!userAuthStore.studentData.subjects) {
      userAuthStore.getStudentData()
    }
  } else if (userAuthStore.userData?.['role']?.toLowerCase() === 'staff') {
    if (
      !userAuthStore.staffData.courseWork &&
      ['teacher', 'hod'].includes(
        userAuthStore.userData['staff_role'].toLowerCase(),
      )
    ) {
      userAuthStore.getstaffData()
      userAuthStore.getTeacherStudentsAssessments()
      userAuthStore.getTeacherStudentsExams()
      userAuthStore.getTeacherStudentResults()
      if (userAuthStore.userData?.['staff_role'].toLowerCase() === 'hod') {
        userAuthStore.getHodData()
      }
    } else if (
      userAuthStore.userData?.['staff_role'].toLowerCase() === 'administrator'
    ) {
      userAuthStore.getAdminData()
    }
    next('/staff')
  } else {
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
  if (
    !userAuthStore.staffData.courseWork &&
    ['teacher', 'hod'].includes(
      userAuthStore.userData['staff_role'].toLowerCase(),
    )
  ) {
    userAuthStore.getstaffData()
    userAuthStore.getTeacherStudentsAssessments()
    userAuthStore.getTeacherStudentsExams()
    userAuthStore.getTeacherStudentResults()
    if (userAuthStore.userData?.['staff_role'].toLowerCase() === 'hod') {
      userAuthStore.getHodData()
    }
  } else if (
    userAuthStore.userData?.['staff_role'].toLowerCase() === 'administrator'
  ) {
    userAuthStore.getAdminData()
  } else if (userAuthStore.userData?.['role'] === 'student') {
    if (!userAuthStore.studentData.subjects) {
      userAuthStore.getStudentData()
    }
    return next('/student')
  } else {
    if (to.path !== '/') {
      return next('/')
    }
  }
  next()
}

const checkLogin = async (to: any, from: any, next: NavigationGuardNext) => {
  const userAuthStore = useUserAuthStore()
  const isAuthenticated = await checkAuth()
  if (isAuthenticated && userAuthStore.userData?.['role'] === 'staff') {
    return next('/staff')
  } else if (
    isAuthenticated &&
    userAuthStore.userData?.['role'] === 'student'
  ) {
    return next('/student')
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
  ],
})

export default router

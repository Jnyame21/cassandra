import {
  createRouter,
  createWebHistory,
  useRouter,
  type NavigationGuardNext,
} from 'vue-router'
import StaffView from '@/views/StaffView.vue'
import StudentView from '@/views/StudentView.vue'
import LoginView from '@/views/LoginView.vue'
import { useUserAuthStore } from '@/stores/userAuthStore'
import { headRoles } from '@/utils/util'
import SuperUserView from '@/views/SuperUserView.vue'

const checkAuth = async () => {
  const userAuthStore = useUserAuthStore()
  const router = useRouter()
  if (!userAuthStore.isAuthenticated) {
    try {
      await userAuthStore.UpdateToken()
      userAuthStore.isAuthenticated = true
      await userAuthStore.getUserData()
    } 
    catch (e:any) {
      if (e.response.status === 401){
        userAuthStore.$reset()
        await router.push('/')
        return;
      }
      return Promise.reject(e)
    }
  } 
}

const checkSuperuser = async (to: any, from: any, next: NavigationGuardNext) => {
  const userAuthStore = useUserAuthStore()
  await checkAuth()
  
  if (!userAuthStore.superUserData.schools && userAuthStore.userData?.['role']?.toLowerCase() === 'superuser') {
    userAuthStore.getSuperUserData()
  } 
  else if (userAuthStore.userData?.['role'].toLowerCase() === 'student') {
    if (!userAuthStore.studentData.students){
      userAuthStore.getStudentData()
    }
    next('/student')
  } 
  else if (userAuthStore.userData?.['role']?.toLowerCase() === 'staff') {
    if (!userAuthStore.teacherData.staff && userAuthStore.userData?.['staff_role']?.toLowerCase() === 'teacher') {
      userAuthStore.getTeacherData()
    } 
    else if (!userAuthStore.adminData.staff && userAuthStore.userData?.['staff_role']?.toLowerCase() === 'administrator') {
      userAuthStore.getAdminData()
    }
    else if (!userAuthStore.headData.staff && headRoles.includes(userAuthStore.userData?.['staff_role']?.toLowerCase())) {
      userAuthStore.getHeadData()
    }
    else if (!userAuthStore.otherRolesData.staff && !['teacher', 'administrator'].includes(userAuthStore.userData?.['staff_role']?.toLowerCase()) && !headRoles.includes(userAuthStore.userData?.['staff_role']?.toLowerCase())) {
      userAuthStore.getOtherRolesData()
    }

    next('/staff')
  } 
  
  next()
}

const checkStudent = async (to: any, from: any, next: NavigationGuardNext) => {
  const userAuthStore = useUserAuthStore()
  await checkAuth()
  
  if (!userAuthStore.studentData.students && userAuthStore.userData?.['role']?.toLowerCase() === 'student') {
    userAuthStore.getStudentData()
  } 
  else if (userAuthStore.userData?.['role']?.toLowerCase() === 'staff') {
    if (!userAuthStore.teacherData.staff && userAuthStore.userData?.['staff_role']?.toLowerCase() === 'teacher') {
      userAuthStore.getTeacherData()
    } 
    else if (!userAuthStore.adminData.staff && userAuthStore.userData?.['staff_role']?.toLowerCase() === 'administrator') {
      userAuthStore.getAdminData()
    }
    else if (!userAuthStore.headData.staff && headRoles.includes(userAuthStore.userData?.['staff_role']?.toLowerCase())) {
      userAuthStore.getHeadData()
    }
    else if (!userAuthStore.otherRolesData.staff && !['teacher', 'administrator'].includes(userAuthStore.userData?.['staff_role']?.toLowerCase()) && !headRoles.includes(userAuthStore.userData?.['staff_role']?.toLowerCase())) {
      userAuthStore.getOtherRolesData()
    }

    next('/staff')
  } 
  else if (userAuthStore.userData?.['role'].toLowerCase() === 'superuser') {
    if (!userAuthStore.superUserData.schools){
      userAuthStore.getSuperUserData()
    }
    return next('/superuser')
  } 
  
  next()
}

const checkStaff = async (to: any, from: any, next: NavigationGuardNext) => {
  const userAuthStore = useUserAuthStore()
  await checkAuth()
  
  if (userAuthStore.userData?.['role'] === 'staff'){
    if (!userAuthStore.teacherData.staff && userAuthStore.userData?.['staff_role']?.toLowerCase() === 'teacher') {
      userAuthStore.getTeacherData()
    } 
    else if (!userAuthStore.adminData.staff && userAuthStore.userData?.['staff_role']?.toLowerCase() === 'administrator') {
      userAuthStore.getAdminData()
    } 
    else if (!userAuthStore.headData.staff && headRoles.includes(userAuthStore.userData?.['staff_role']?.toLowerCase())) {
      userAuthStore.getHeadData()
    }
    else if (!userAuthStore.otherRolesData.staff && !['teacher', 'administrator'].includes(userAuthStore.userData?.['staff_role']?.toLowerCase()) && !headRoles.includes(userAuthStore.userData?.['staff_role']?.toLowerCase())) {
      userAuthStore.getOtherRolesData()
    }
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
  
  next()
}

const checkLogin = async (to: any, from: any, next: NavigationGuardNext) => {
  const userAuthStore = useUserAuthStore()
  const isAuthenticated = userAuthStore.isAuthenticated
  if (isAuthenticated && userAuthStore.userData?.['role']?.toLowerCase() === 'staff') {
    return next('/staff')
  } 
  else if (isAuthenticated && userAuthStore.userData?.['role']?.toLowerCase() === 'student') {
    return next('/student')
  }
  else if (isAuthenticated && userAuthStore.userData?.['role']?.toLowerCase() === 'superuser') {
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

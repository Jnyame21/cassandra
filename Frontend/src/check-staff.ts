export default defineNuxtRouteMiddleware((to, from) => {
  if (import.meta.client) {
    const userAuthStore = useUserAuthStore()
    if (
      userAuthStore.userData?.['role'] === 'staff' &&
      userAuthStore.userData['staff_role'] != 'admin' &&
      !userAuthStore.staffData?.courseWork
    ) {
      userAuthStore.getstaffData()
      userAuthStore.getTeacherStudentsAssessments()
      userAuthStore.getTeacherStudentsExams()
      userAuthStore.getTeacherStudentResults()
      // userAuthStore.getNotifications()
    }

    // if (userAuthStore.userData['staff_role']==='hod' && !userAuthStore.staffSubjectAssignment.termOne ){
    //     userAuthStore.getHodData()
    //     userAuthStore.getHodPerformance()
    // }

    // if (userAuthStore.userData['role']==='head' && !userAuthStore.headDepartments ){
    //     userAuthStore.getHeadData()
    //     userAuthStore.getHeadStudentsPerformance()
    //     userAuthStore.getNotifications()
    // }

    // if (userAuthStore.userData['staff_role']==='admin' && !userAuthStore.adminClasses.yearOne ){
    //     userAuthStore.getAdminData()
    //     userAuthStore.getNotifications()
    // }

    if (userAuthStore.userData?.['role'] === 'student') {
      return navigateTo('/student')
    }
  }
})

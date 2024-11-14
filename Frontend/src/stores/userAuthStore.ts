import { defineStore } from 'pinia'
import { jwtDecode } from 'jwt-decode'
import { defaultAxiosInstance } from '@/utils/axiosInstance'
import axiosInstance from '@/utils/axiosInstance'
import { useElementsStore } from '@/stores/elementsStore'
import { AxiosError } from 'axios'

interface states {
  authTokens: any
  userData: any
  studentData: {
    subjects: any
    classData: any
    studentApplications: any
    universities: any
    academicYearsData: any
    currentAcademicYearsResults: any
    currentAttendance: any
    currentAssessments: any
    currentResults: any
  }
  staffData: {
    courseWork: any
    currentCourseWork: any
    studentsattendance: any
    studentsAssessments: any
    studentsExams: any
    studentsResults: any
    departmentData: any
    hodData: {
      subjectAssignmentData: any
    }
  }
  adminData: {
    academicYears: any[] | null
    departments: string[]
    heads: any
    classes: {
      name: string
      students: {
        user: string
        st_id: string
        gender: string
        date_enrolled: string
        index_no: string | null
        img: string
        dob: string
        nationality: string
        guardian: string
        guardian_gender: string
        guardian_nationality: string
        guardian_contact: string
        guardian_email: string
        guardian_address: string
      }[];
      head_teacher: {user: string; staff_id: string; img: string} | null
      students_year: number
      program: string | null
      subjects: string[]
    }[]
    staff: {
      'user': string
      'staff_id': string
      'gender': string
      'contact': string
      'nationality': string
      'department'?: string
      'role': string
      'img': string
      'dob': string
      'subjects': string[]
      'address': string
      'alt_contact': string
      'pob': string
      'email': string
      'date_enrolled': string
      'region': string
      'religion': string
    }[] | null
    linkedClasses: any
    programs: string[]
    subjects: string[]
  }
  message: string
  isAuthenticated: boolean
  staffStudentResultsSubjectAssignment: any
  staffStudentResultsEdit: any
  activeTerm: any
  activeAcademicYear: any
  hodSubjectAssignmentUpload: {
    staff: any
    subjects: any
    classes: any
  }
  staffStudentsResultsFileGenerated: boolean
  hodSubjectAssignment: {
    termOne: any
    termTwo: any
    termThree: any
  }
  staffSubjectAssignment: {
    termOne: any
    termTwo: any
    termThree: any
  }
  headDepartments: any
  headPrograms: any
  notifications: any
  headNotificationsStaff: any
  hodPerformance: any
  headStudentsPerformance: any
  adminClasses: {
    yearOne: any
    yearTwo: any
    yearThree: any
    names: any
    subjects: any
    programs: any
  }
  adminStaff: {
    departmentNames: any
    subjects: any
    departments: any
    academicYears: any
  }
  adminHeads: any
  // Notification
  newNotification: boolean
  notificationStudentsClasses: any
  notificationStudents: any
  notificationStaff: any
}

export const useUserAuthStore = defineStore('userAuthStore', {
  state: (): states => {
    return {
      authTokens: null,
      userData: null,
      studentData: {
        subjects: null,
        classData: null,
        studentApplications: null,
        universities: null,
        academicYearsData: null,
        currentAcademicYearsResults: null,
        currentAttendance: null,
        currentAssessments: null,
        currentResults: null,
      },
      staffData: {
        courseWork: null,
        currentCourseWork: null,
        studentsattendance: null,
        studentsExams: null,
        studentsAssessments: null,
        studentsResults: null,
        departmentData: null,
        hodData: {
          subjectAssignmentData: null
        },
      },
      adminData: {
        academicYears: null,
        departments: [],
        heads: null,
        classes: [],
        staff: null,
        linkedClasses: null,
        programs: [],
        subjects: []
      },
      message: '',
      isAuthenticated: false,
      staffStudentResultsSubjectAssignment: null,
      staffStudentResultsEdit: null,
      activeTerm: null,
      activeAcademicYear: null,
      staffStudentsResultsFileGenerated: false,
      hodSubjectAssignmentUpload: {
        staff: null,
        subjects: null,
        classes: null,
      },
      hodSubjectAssignment: {
        termOne: null,
        termTwo: null,
        termThree: null,
      },
      staffSubjectAssignment: {
        termOne: null,
        termTwo: null,
        termThree: null,
      },
      headDepartments: null,
      headPrograms: null,
      headNotificationsStaff: null,
      hodPerformance: null,
      headStudentsPerformance: null,
      adminClasses: {
        yearOne: null,
        yearTwo: null,
        yearThree: null,
        names: null,
        subjects: null,
        programs: null,
      },
      adminStaff: {
        departmentNames: null,
        subjects: null,
        departments: null,
        academicYears: null,
      },
      adminHeads: null,
      // Notification
      notifications: null,
      newNotification: false,
      notificationStudentsClasses: null,
      notificationStudents: null,
      notificationStaff: null,
    }
  },

  actions: {
    setAuthState(value: boolean) {
      this.isAuthenticated = value
    },

    logoutUser() {
      if (localStorage.getItem('authTokens')) {
        localStorage.removeItem('authTokens')
      }
      if (localStorage.getItem('RozmachAuth')) {
        localStorage.removeItem('RozmachAuth')
      }
      useElementsStore().$reset()
      this.$reset()
    },

    async getStudentData() {
      await axiosInstance
        .get('st/data', {
          params: { year: this.activeAcademicYear, term: this.activeTerm },
        })
        .then(response => {
          this.studentData.subjects = response.data['subjects']
          this.studentData.academicYearsData =
            response.data['academic_years_results']
          this.studentData.classData = response.data['class_data']
        })
        .catch(() => {
          return Promise.reject()
        })
    },

    async refreshData() {
      await axiosInstance
        .post('refresh/data')
        .then(() => {
          return Promise.resolve()
        })
        .catch(() => {
          return Promise.reject()
        })
    },

    async getstaffData() {
      await axiosInstance
        .get('teacher/data', {
          params: { year: this.activeAcademicYear, term: this.activeTerm },
        })
        .then(response => {
          this.staffData.courseWork = response.data['subject_assignments']
          this.staffData.departmentData = response.data['department_data']
        })
        .catch(() => {
          return Promise.reject()
        })
    },
    async getTeacherStudentsAttendance() {
      await axiosInstance
        .get('teacher/students/attendance', {
          params: { year: this.activeAcademicYear, term: this.activeTerm },
        })
        .then(response => {
          this.staffData.studentsattendance =
            response.data['students_attendance']
        })
        .catch(() => {
          return Promise.reject()
        })
    },
    async getTeacherStudentsAssessments() {
      await axiosInstance
        .get('teacher/assessments', {
          params: { year: this.activeAcademicYear, term: this.activeTerm },
        })
        .then(response => {
          this.staffData.studentsAssessments = response.data['assessments']
        })
        .catch(() => {
          return Promise.reject()
        })
    },
    async getTeacherStudentsExams() {
      await axiosInstance
        .get('teacher/exams', {
          params: { year: this.activeAcademicYear, term: this.activeTerm },
        })
        .then(response => {
          this.staffData.studentsExams = response.data['exams_data']
        })
        .catch(() => {
          return Promise.reject()
        })
    },

    async getTeacherSubjectAssignments() {
      await axiosInstance
        .get('teacher/data', {
          params: { year: this.activeAcademicYear, term: this.activeTerm },
        })
        .then(response => {
          this.staffSubjectAssignment.termOne =
            response.data['subject_assignments']['term1']
          this.staffSubjectAssignment.termTwo =
            response.data['subject_assignments']['term2']
          this.staffSubjectAssignment.termThree =
            response.data['subject_assignments']['term3']
        })
        .catch(() => {
          return Promise.reject()
        })
    },

    // async getTeacherStudentsAttendance(){
    //     await axiosInstance.get("teacher/students/attendance", {params: {'year': this.activeAcademicYear, 'term': this.activeTerm}})
    //         .then(response =>{
    //             this.teacherStudentsAttendance = response.data
    //         })
    //         .catch(e =>{
    //             return Promise.reject()
    //         })
    // },

    async getHodData() {
      await axiosInstance
        .get('hod/data', { params: { year: this.activeAcademicYear, term: this.activeTerm } })
        .then(response => {
          this.staffData.hodData.subjectAssignmentData = response.data
        })
        .catch(() => {
          return Promise.reject()
        })
    },

    async getAdminData() {
      await axiosInstance.get('school-admin/data', {params: { year: this.activeAcademicYear, term: this.activeTerm }})
        .then(response => {
          const data = response.data
          this.adminData.academicYears = data['academic_years']
          this.adminData.classes = data['classes']
          this.adminData.linkedClasses = data['linked_classes']
          this.adminData.departments = data['departments']
          this.adminData.staff = data['staff']
          this.adminData.programs = data['programs']
          this.adminData.subjects = data['subjects']
        })
        .catch(() => {
          return Promise.reject()
        })
    },

    async getHeadData() {
      await axiosInstance
        .get('head/data', {
          params: { year: this.activeAcademicYear, term: this.activeTerm },
        })
        .then(response => {
          this.headDepartments = response.data['departments']
          this.headPrograms = response.data['programs']
        })
        .catch(() => {
          return Promise.reject()
        })
    },

    

    async getNotifications() {
      await axiosInstance
        .get('notification')
        .then(response => {
          this.newNotification = response.data['new_notification']
          this.notifications = response.data['notifications']
          this.notificationStudentsClasses = response.data['classes']
          this.notificationStaff = response.data['staff']
        })
        .catch(() => {
          return Promise.reject()
        })
    },

    async getTeacherStudentResults() {
      await axiosInstance
        .get('teacher/students-result', {
          params: { year: this.activeAcademicYear, term: this.activeTerm },
        })
        .then(response => {
          this.staffData.studentsResults = response.data
        })
        .catch(() => {
          return Promise.reject()
        })
    },

    async getHodPerformance() {
      await axiosInstance
        .get('hod/students_performance', {
          params: { year: this.activeAcademicYear },
        })
        .then(response => {
          this.hodPerformance = response.data
        })
        .catch(() => {
          return Promise.reject()
        })
    },

    async getHeadStudentsPerformance() {
      await axiosInstance
        .get('head/students_performance', {
          params: { year: this.activeAcademicYear },
        })
        .then(response => {
          this.headStudentsPerformance = response.data
        })
        .catch(() => {
          return Promise.reject()
        })
    },

    async teacherUploadResults(st_id: string, subject: string, score: number) {
      const data = {
        subject: subject,
        score: score,
        st_id: st_id,
        year: this.activeAcademicYear,
        term: this.activeTerm,
      }
      await axiosInstance
        .post('teacher/results/upload/', data)
        .then(response => {
          this.staffStudentResultsSubjectAssignment = response.data[0]
          this.staffStudentResultsEdit = response.data[1]
        })
        .catch(() => {
          return Promise.reject()
        })
    },

    async getUserData() {
      await axiosInstance
        .get('user/data')
        .then(response => {
          const userInfo = response.data
          this.userData = userInfo
          this.activeAcademicYear = userInfo['academic_year']['name']
          this.activeTerm = userInfo['current_term']
        })
        .catch(e => {
          return Promise.reject(e)
        })
    },

    async userLogin(username: string, password: string) {
      const formData = new FormData()
      formData.append('username', username)
      formData.append('password', password)
      try {
        const response = await defaultAxiosInstance.post('login', formData)
        this.authTokens = response.data
        localStorage.setItem('authTokens', JSON.stringify(response.data))
        await this.getUserData()
        const userInfo: any = jwtDecode(response.data['access'])
        if (userInfo['last_login']) {
          localStorage.setItem(
            'RozmachAuth',
            JSON.stringify({ last_login: true, reset: userInfo['reset'] }),
          )
        } else {
          localStorage.setItem(
            'RozmachAuth',
            JSON.stringify({ last_login: false, reset: userInfo['reset'] }),
          )
        }
        this.isAuthenticated = true
        this.message = 'Login successful'
      } catch (error) {
        if (error instanceof AxiosError) {
          const axiosError = error as AxiosError
          if (axiosError.response) {
            if (axiosError.response.status === 401) {
              this.message = 'Oops! the username or password is wrong.'
            } else {
              this.message = 'Oops! something went wrong. Try again later'
            }
          } else if (
            !axiosError.response &&
            (axiosError.code === 'ECONNABORTED' || !navigator.onLine)
          ) {
            this.message =
              'A network error occurred! Please check you internet connection'
          } else {
            this.message = 'An unexpected error occurred!'
          }
          return Promise.reject()
        }
      }
    },

    async UpdateToken() {
      await defaultAxiosInstance
        .post('api/token/refresh/', { refresh: this.authTokens['refresh'] })
        .then((response: { data: { access: string; refresh: string } }) => {
          this.authTokens = response.data
          // Tokens storage
          localStorage.setItem('authTokens', JSON.stringify(response.data))
        })
        .catch((error: AxiosError) => {
          return Promise.reject(error)
        })
    },

    async startUpServer() {
      defaultAxiosInstance.get('start_up')
    },
  },
})

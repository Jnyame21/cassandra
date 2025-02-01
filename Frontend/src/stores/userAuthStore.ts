import { defineStore } from 'pinia'
import { jwtDecode } from 'jwt-decode'
import { defaultAxiosInstance } from '@/utils/axiosInstance'
import axiosInstance from '@/utils/axiosInstance'
import { useElementsStore } from '@/stores/elementsStore'
import { AxiosError } from 'axios'

export interface states {
  authTokens: any
  userData: any
  message: string
  isAuthenticated: boolean
  activeTerm: number
  activeAcademicYear: string
  activeAcademicYearID: number;
  superUserData: {
    schools: {
      name: string;
      identifier: string;
      code: string;
      logo: string;
      address: string;
      staff_id: boolean;
      region: string;
      city_town: string;
      postal_address: string;
      short_name: string;
      contact: string;
      alt_contact: string;
      email: string;
      date_created: string;
    }[] | null
    levels: {
      name: string;
      id: number;
      identifier: string;
      years_to_complete: number;
      has_departments: boolean;
      has_programs: boolean;
      students_id: boolean;
      students_index_no: boolean;
      schools: string[]
    }[]
    subjects: {
      name: string;
      identifier: string;
      id: number;
      level: string;
      schools: string[];
    }[]
    programs: {
      name: string;
      id: number;
      identifier: string;
      subjects: string[];
      level: string;
      schools: string[];
    }[]
    gradingSystemRanges: {
      id: number;
      label: string;
      upper_limit: number;
      lower_limit: number;
      remark: string;
      identifier: string;
    }[];
    gradingSystems: {
      id: number;
      level: string;
      schools: string[];
      ranges: string[];
    }[];
    departments: {
      [schoolIdentifier: string]: {
        name: string;
        id: number;
        identifier: string;
        subjects: string[];
        hod: string | null;
        level: string;
      }[]
    };
    classes: {
      [schoolIdentifer: string]: {
        name: string;
        id: number;
        identifier: string;
        subjects: string[];
        head_teacher: { user: string; staff_id: string } | null;
        level: string;
        students_year: number;
        program: string | null;
        linked_class: string | null;
      }[]
    };
    academicYears: {
      [schoolIdentifer: string]: {
        name: string;
        id: number;
        start_date: string;
        end_date: string;
        term_1_end_date: string;
        term_2_start_date: string;
        term_2_end_date: string;
        term_3_start_date: string;
        term_3_end_date: string;
        period_division: string;
        no_divisions: number;
        level: string;
        students_graduation_date: string | null
      }[]
    };
    staffRoles: {
      id: number;
      name: string;
      level: string;
      identifier: string;
      schools: string[];
    }[];
    staff: {
      [schoolIdentifier: string]: {
      user: string;
      staff_id: string;
      gender: string;
      contact: string;
      nationality: string;
      departments: string[];
      roles: string[];
      current_role: string;
      img: string;
      dob: string;
      subjects: string[];
      address: string;
      alt_contact: string;
      pob: string;
      email: string;
      date_enrolled: string;
      region: string;
      religion: string;
      }[]
    }
  };
  studentData: {
    headTeacher: {
      user: string
      contact: string
      email: string
      gender: string
      img: string
    } | null
    subjects: {
      name: string
      teacher: string
      teacher_img: string
      teacher_contact: string
      teacher_email: string
      teacher_gender: string
      teacher_department: string
    }[]
    students: {
      user: string
      gender: string
      contact: string
      img: string
    }[] | null;
    attendances: {
      [year_name: string]: {
        [term_name: string]: {
          date: string
          status: string
        }[]
      }
    };
    assessments: {
      [year_name: string]: {
        [term_name: string]: {
          subject: string
          title: string
          score: number
          description: string
          total_score: number
          assessment_date: string
          comment: string
        }[]
      }
    }
    exams: {
      [year_name: string]: {
        [term_name: string]: {
          subject: string
          score: number
          total_score: number
        }[]
      }
    }
    results: {
      [year_name: string]: {
        [term_name: string]: {
          subject: string
          total_assessment_score: number
          exam_score: number
          total_assessment_percentage: number
          exam_percentage: number
          remark: string
          grade: {label: string, remark: string}
          position: string
          result: number
        }[]
      }
    }
    studentApplications: any
    universities: any
  }
  teacherData: {
    courseWork: {
      [class_name: string] : {
        students_class: {
          name: string
          students: {
            user: string
            st_id: string
            gender: string
            img: string
            contact: string
            guardian_contact: string
          }[]
        }
        subjects: string[]
      }
    }
    studentsAttendance: {
      [class_name: string]: {
        attendances: {
          date: string;
          students_present: {
            user: string
            st_id: string
          }[];
          students_absent: {
            user: string
            st_id: string
          }[]
        }[];
        students: {
          name: string
          st_id: string
        }[]
      }
    }
    studentsAssessments: {
      [className: string]: {
        [subject: string]: {
          [assessmentTitle: string]: {
            id: number;
            title: string;
            description: string;
            percentage: number;
            assessment_date: string;
            total_score: number;
            students_with_assessment: {
              [studentId: string]: {
                name: string;
                st_id: string;
                score: number;
                comment: string;
              }
            };
            students_without_assessment: {
              [studentId: string]: {
                name: string;
                st_id: string;
              }
            }
          }
        }
      }
    }
    studentsExams: {
      [class_name: string]: {
        [subject_name: string]: {
          percentage: number
          total_score: number
          students_with_exams: {
            [st_id: string]: {
              name: string
              st_id: string
              score: number
            }
          }
          students_without_exams: {
            [st_id: string]: {
              name: string
              st_id: string
            }
          }
        }
      }
    }
    studentsResults: {
      [class_name: string]: {
        [subject_name: string]: {
          total_assessment_percentage: number
          exam_percentage: number
          student_results: {
            [st_id: string]: {
              result: number;
              total_assessment_score: number;
              exam_score: number;
              student: {
                name: string
                st_id: string
              };
              remark: string;
              grade: string;
              position: string;
            }
          }
        }
      }
    }
    staff: {
      user: string;
      staff_id: string;
      subjects: string[];
      roles: string[];
      alt_contact: string;
      img: string;
      nationality: string;
      contact: string;
      gender: string;
      email: string;
      departments: string[];
      address: string;
    }[] | null
    departmentData: {
      name: string;
      subjects: string[];
      identifier: string;
      id: number;
      hod: { user: string; staff_id: string } | null;
      teachers: {user: string; staff_id: string}[];
    } | null
  }
  hodData: {
    studentClasses: string[]
    subjectAssignments: {
      students_class: string
      teacher: { user: string; staff_id: string }
      subjects: string[]
    }[]
  }
  adminData: {
    academicYears: {
      name: string;
      id: number;
      level: string;
      start_date: string;
      end_date: string;
      term_1_end_date: string;
      term_2_start_date: string;
      term_2_end_date: string;
      term_3_start_date: string | null;
      term_3_end_date: string | null;
      period_division: string;
      no_divisions: number;
      students_graduation_date: string | null;
    }[]
    departments: {
      name: string
      id: number;
      identifier: string
      hod: { user: string; staff_id: string } | null
      subjects: string[]
      teachers: { user: string; staff_id: string }[]
    }[]
    subjectAssignments: {
      id: number
      students_class: string
      teacher: { user: string; staff_id: string }
      subjects: string[]
    }[]
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
        region: string
        religion: string
        pob: string
        email: string
        address: string
        contact: string
        nationality: string
        guardian: string
        guardian_occupation: string
        guardian_gender: string
        guardian_nationality: string
        guardian_contact: string
        guardian_email: string
        guardian_address: string
      }[]
      head_teacher: { user: string; staff_id: string; img: string } | null
      students_year: number
      program: string | null
      subjects: string[]
      linked_class: string
    }[]
    staffRoles: string[]
    staff:{
      user: string;
      staff_id: string;
      gender: string;
      contact: string;
      nationality: string;
      departments: string[];
      roles: string[];
      img: string;
      dob: string;
      subjects: string[];
      address: string;
      alt_contact: string;
      pob: string;
      email: string;
      date_enrolled: string;
      region: string;
      religion: string;
    }[]| null
    programs: string[]
    subjects: string[]
    releasedResults: {
      id: number;
      students_class: string;
      academic_year: string;
      academic_term: number;
      released_by: string;
      date: string;
    }[]
  }
  headData: {
    staff: {
      user: string
      staff_id: string
      subjects: string[]
      role: string
      alt_contact: string
      img: string
      contact: string
      gender: string
      email: string
      department: string;
      address: string
    }[] | null;
    classes: {
      [name: string]: {
        students: {
          user: string
          st_id: string
          gender: string
          date_enrolled: string
          index_no: string | null
          img: string
          dob: string
          region: string
          religion: string
          pob: string
          email: string
          address: string
          contact: string
          nationality: string
          guardian: string
          guardian_occupation: string
          guardian_gender: string
          guardian_nationality: string
          guardian_contact: string
          guardian_email: string
          guardian_address: string
        }[]
        head_teacher: { 
          user: string;
          img: string ;
        } | null
        students_year: number
        program: string | null
        subjects: {
          name: string;
          teacher: string;
          teacher_img: string;
        }[]
      }
    }
    subjects: string[]
    departments: string[]
    programs: string[]
    academic_years: any[]
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
      message: '',
      isAuthenticated: false,
      activeTerm: 0,
      activeAcademicYear: '',
      activeAcademicYearID: 0,
      superUserData: {
        schools: null,
        levels: [],
        subjects: [],
        staffRoles: [],
        programs: [],
        gradingSystemRanges: [],
        gradingSystems: [],
        departments: {},
        classes: {},
        academicYears: {},
        staff: {},
      },
      studentData: {
        subjects: [],
        students: null,
        attendances: {},
        assessments: {},
        exams: {},
        headTeacher: null,
        results: {},
        studentApplications: null,
        universities: null,
      },
      teacherData: {
        courseWork: {},
        studentsAttendance: {},
        studentsExams: {},
        studentsAssessments: {},
        studentsResults: {},
        staff: null,
        departmentData: null,
      },
      hodData: {
        studentClasses: [],
        subjectAssignments: [],
      },
      adminData: {
        academicYears: [],
        departments: [],
        heads: null,
        classes: [],
        staffRoles: [],
        staff: null,
        programs: [],
        subjects: [],
        subjectAssignments: [],
        releasedResults: [],
      },
      headData: {
        staff: null,
        classes: {},
        subjects: [],
        departments: [],
        programs: [],
        academic_years: [],
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
        .get('student/data', {
          params: { year: this.activeAcademicYearID, term: this.activeTerm },
        })
        .then(response => {
          this.studentData.subjects = response.data['subjects']
          this.studentData.attendances = response.data['year_data']['attendance']
          this.studentData.assessments = response.data['year_data']['assessments']
          this.studentData.results = response.data['year_data']['results']
          this.studentData.students = response.data['students']
          this.studentData.exams = response.data['year_data']['exams']
          if (response.data['head_teacher']){
            this.studentData.headTeacher = response.data['head_teacher']
          }
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

    async getSuperUserData() {
      await axiosInstance
        .get('superuser/data')
        .then(response => {
          this.superUserData.schools = response.data['schools']
          this.superUserData.levels = response.data['levels']
          this.superUserData.subjects = response.data['subjects']
          this.superUserData.programs = response.data['programs']
          this.superUserData.departments = response.data['departments']
          this.superUserData.classes = response.data['classes']
          this.superUserData.gradingSystemRanges = response.data['grading_system_ranges']
          this.superUserData.gradingSystems = response.data['grading_systems']
          this.superUserData.academicYears = response.data['academic_years']
          this.superUserData.staff = response.data['staff']
          this.superUserData.staffRoles = response.data['staff_roles']
        })
        .catch(() => {
          return Promise.reject()
        })
    },

    async getTeacherData() {
      await axiosInstance
        .get('teacher/data', {params: { year: this.activeAcademicYearID, term: this.activeTerm },})
        .then(response => {
          this.teacherData.courseWork = response.data['subject_assignments']
          this.teacherData.departmentData = response.data['department_data']
          this.teacherData.staff = response.data['staff']
          this.teacherData.studentsAttendance = response.data['students_attendance']
          this.teacherData.studentsAssessments = response.data['students_assessments']
          this.teacherData.studentsExams = response.data['students_exams']
          this.teacherData.studentsResults = response.data['students_results']
        })
        .catch(() => {
          return Promise.reject()
        })
    },

    async getHodData() {
      await axiosInstance
        .get('hod/data', {
          params: { year: this.activeAcademicYearID, term: this.activeTerm },
        })
        .then(response => {
          this.hodData.subjectAssignments = response.data['subject_assignments']
          this.hodData.studentClasses = response.data['student_classes']
        })
        .catch(() => {
          return Promise.reject()
        })
    },

    async getAdminData() {
      await axiosInstance
        .get('school-admin/data', {
          params: { year: this.activeAcademicYearID, term: this.activeTerm },
        })
        .then(response => {
          const data = response.data
          this.adminData.academicYears = data['academic_years']
          this.adminData.classes = data['classes']
          this.adminData.departments = data['departments']
          this.adminData.staff = data['staff']
          this.adminData.programs = data['programs']
          this.adminData.staffRoles = data['staff_roles']
          this.adminData.subjects = data['subjects']
          this.adminData.subjectAssignments = data['subject_assignments']
          this.adminData.releasedResults = data['released_results']
        })
        .catch(() => {
          return Promise.reject()
        })
    },

    async getHeadData() {
      await axiosInstance
        .get('head/data', {
          params: { year: this.activeAcademicYearID, term: this.activeTerm },
        })
        .then(response => {
          this.headData.staff = response.data['staff']
          this.headData.classes = response.data['classes']
          this.headData.subjects = response.data['subjects']
          this.headData.departments = response.data['departments']
          this.headData.programs = response.data['programs']
          this.headData.academic_years = response.data['academic_years']
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

    async getHodPerformance() {
      await axiosInstance
        .get('hod/students_performance', {
          params: { year: this.activeAcademicYearID },
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
          params: { year: this.activeAcademicYearID },
        })
        .then(response => {
          this.headStudentsPerformance = response.data
        })
        .catch(() => {
          return Promise.reject()
        })
    },

    async getUserData() {
      await axiosInstance.get('user/data')
        .then(response => {
          const userInfo = response.data
          this.userData = userInfo
          if (['staff', 'student'].includes(userInfo['role'].toLowerCase())){
            this.activeAcademicYear = userInfo['academic_year']['name']
            this.activeTerm = userInfo['current_term']
            this.activeAcademicYearID = userInfo['academic_year']['id']
          }
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
          localStorage.setItem('RozmachAuth', JSON.stringify({ last_login: true, reset: userInfo['reset'] }))
        }
        else {
          localStorage.setItem('RozmachAuth', JSON.stringify({ last_login: false, reset: userInfo['reset'] }))
        }
        this.isAuthenticated = true
        this.message = 'Login successful'
      } 
      catch (error) {
        if (error instanceof AxiosError) {
          const axiosError = error as AxiosError
          if (axiosError.response) {
            if (axiosError.response.status === 401 && axiosError.response.data) {
              // if (axiosError.response.data && axiosError.response.data.detail){
              //   this.message = axiosError.response.data.detail as string
              // }
              // else{
              //   this.message = axiosError.response.data as string
              // }
              this.message = axiosError.response.data as string
            } 
            else if (axiosError.response.status === 401 && !axiosError.response.data) {
              this.message = 'Oops! your username or password is wrong'
            }
            else {
              this.message = 'Oops! something went wrong. Try again later'
            }
          } 
          else if (!axiosError.response && (axiosError.code === 'ECONNABORTED' || !navigator.onLine)) {
            this.message = 'A network error occurred! Please check you internet connection'
          } 
          else {
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




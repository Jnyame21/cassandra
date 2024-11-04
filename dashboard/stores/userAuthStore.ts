import {defineStore} from "pinia";
import { jwtDecode } from "jwt-decode";
import { defaultAxiosInstance } from "../utils/axiosInstance";
import axiosInstance from '../utils/axiosInstance'
import { useRouter } from 'vue-router';
import { useElementsStore } from '../stores/elementsStore'
import { AxiosError } from "axios";

interface states {
    authTokens: any;
    userData: any;
    studentData: {
        subjects: any;
        classData: any;
        studentApplications: any;
        universities: any;
        academicYearsData: any;
        currentAcademicYearsResults: any,
        currentAttendance: any;
        currentAssessments: any;
        currentResults: any;
    };
    teacherData: {
        courseWork: any;
        currentCourseWork: any;
        studentsattendance: any;
        studentsAssessments: any;
        studentsExams: any;
        studentsResults: any;
    };
    message: string;
    isAuthenticated: boolean;
    staffStudentResultsSubjectAssignment: any;
    staffStudentResultsEdit: any;
    activeTerm: any;
    activeAcademicYear: any;
    hodSubjectAssignmentUpload: {
        staff: any;
        subjects: any;
        classes: any;
    };
    staffStudentsResultsFileGenerated: boolean;
    hodSubjectAssignment: {
        termOne: any;
        termTwo: any;
        termThree: any;
    };
    staffSubjectAssignment: {
        termOne: any;
        termTwo: any;
        termThree: any;
    };
    headDepartments: any;
    headPrograms: any;
    notifications: any;
    headNotificationsStaff: any;
    hodPerformance: any;
    headStudentsPerformance: any;
    adminClasses: {
        yearOne: any;
        yearTwo: any;
        yearThree: any;
        names: any;
        subjects: any;
        programs: any
    };
    adminStaff: {
        departmentNames: any;
        subjects: any;
        departments: any;
        academicYears: any;
    };
    adminHeads: any;
    teacherStudentsAttendance: any;

    // Notification
    newNotification: Boolean;
    notificationStudentsClasses: any;
    notificationStudents: any;
    notificationStaff: any;
}

export const useUserAuthStore = defineStore('userAuth',{
    state: (): states =>{
        return{
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
            teacherData: {
                courseWork: null,
                currentCourseWork: null,
                studentsattendance: null,
                studentsExams: null,
                studentsAssessments: null,
                studentsResults: null,
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
            teacherStudentsAttendance: null,

            // Notification
            notifications: null,
            newNotification: false,
            notificationStudentsClasses: null,
            notificationStudents: null,
            notificationStaff: null,
        }

    },

    actions: {

        setAuthState(value: boolean){
            this.isAuthenticated = value
        },

        logoutUser(){
            if (localStorage.getItem('authTokens')){
                localStorage.removeItem('authTokens')
            }
            if (localStorage.getItem('RozmachAuth')){
                localStorage.removeItem('RozmachAuth')
            }
            useElementsStore().$reset()
            this.$reset()
        },

        async getStudentData(){
            await axiosInstance.get('st/data', {params: {'year': this.activeAcademicYear, 'term': this.activeTerm}})
                .then(response =>{
                    this.studentData.subjects = response.data['subjects']
                    this.studentData.academicYearsData = response.data['academic_years_results']
                    this.studentData.classData = response.data['class_data']
                })
                .catch(e =>{
                    return Promise.reject()
                })
        },

        async refreshData(){
            await axiosInstance.post("refresh/data")
                .then(response =>{
                    return Promise.resolve()
                })
                .catch(e =>{
                    return Promise.reject()
                })
        },

        async getTeacherData(){
            await axiosInstance.get("teacher/data", {params: {'year': this.activeAcademicYear, 'term': this.activeTerm}})
                .then(response =>{
                    this.teacherData.courseWork = response.data['subject_assignments']
                    this.teacherData.studentsattendance = response.data['students_attendance']
                })
                .catch(e =>{
                    return Promise.reject()
                })
        },
        async getTeacherStudentsAssessments(){
            await axiosInstance.get("teacher/assessments", {params: {'year': this.activeAcademicYear, 'term': this.activeTerm}})
                .then(response =>{
                    this.teacherData.studentsAssessments = response.data['assessments']
                })
                .catch(e =>{
                    return Promise.reject()
                })
        },
        async getTeacherStudentsExams(){
            await axiosInstance.get("teacher/exams", {params: {'year': this.activeAcademicYear, 'term': this.activeTerm}})
                .then(response =>{
                    this.teacherData.studentsExams = response.data['exams_data']
                })
                .catch(e =>{
                    return Promise.reject()
                })
        },

        async getTeacherSubjectAssignments(){
            await axiosInstance.get("teacher/data", {params: {'year': this.activeAcademicYear, 'term': this.activeTerm}})
                .then(response =>{
                    this.staffSubjectAssignment.termOne = response.data['subject_assignments']['term1']
                    this.staffSubjectAssignment.termTwo = response.data['subject_assignments']['term2']
                    this.staffSubjectAssignment.termThree = response.data['subject_assignments']['term3']
                    
                })
                .catch(e =>{
                    return Promise.reject()
                })
        },

        async getTeacherStudentsAttendance(){
            await axiosInstance.get("teacher/students/attendance", {params: {'year': this.activeAcademicYear, 'term': this.activeTerm}})
                .then(response =>{
                    this.teacherStudentsAttendance = response.data
                })
                .catch(e =>{
                    return Promise.reject()
                })
        },

        async getHodData(){
            await axiosInstance.get("hod/data", {params: {'year': this.activeAcademicYear}})
                .then(response =>{
                    this.hodSubjectAssignmentUpload.subjects = response.data.subjects
                    this.hodSubjectAssignmentUpload.staff = response.data.staff
                    this.hodSubjectAssignmentUpload.classes = response.data.classes
                    this.hodSubjectAssignment.termOne = response.data.term_one
                    this.hodSubjectAssignment.termTwo = response.data.term_two
                    this.hodSubjectAssignment.termThree = response.data.term_three
                })
                .catch(e =>{
                    return Promise.reject()
                })
        },

        async getHeadData(){
            await axiosInstance.get("head/data", {params: {'year': this.activeAcademicYear, 'term': this.activeTerm}})
                .then(response =>{
                    this.headDepartments = response.data['departments']
                    this.headPrograms = response.data['programs']
                })
                .catch(e =>{
                    return Promise.reject()
                })
        },

        async getAdminData(){
            await axiosInstance.get("sch-admin/data", {params: {'year': this.activeAcademicYear, 'term': this.activeTerm}})
                .then(response =>{
                    this.adminClasses.yearOne = response.data['classes']['year_one']
                    this.adminClasses.yearTwo = response.data['classes']['year_two']
                    this.adminClasses.yearThree = response.data['classes']['year_three']
                    this.adminHeads = response.data['heads']
                    this.adminClasses.names = response.data['class_names']
                    this.adminClasses.programs = response.data['programs']
                    this.adminStaff.departmentNames = response.data['department_names']
                    this.adminStaff.departments = response.data['departments']
                    this.adminStaff.subjects = response.data['subjects']
                    this.adminStaff.academicYears = response.data['academic_years']
                })
                .catch(e =>{
                    return Promise.reject()
                })
        },

        async getNotifications(){
            await axiosInstance.get("notification")
                .then(response =>{
                    this.newNotification = response.data['new_notification']
                    this.notifications = response.data['notifications']
                    this.notificationStudentsClasses = response.data['classes']
                    this.notificationStaff = response.data['staff']
                })
                .catch(e =>{
                    return Promise.reject()
                })
        },

        async getTeacherStudentResults(){
            await axiosInstance.get("teacher/students-result", {params: {'year': this.activeAcademicYear, 'term': this.activeTerm}})
                .then(response =>{
                    this.teacherData.studentsResults = response.data
                })
                .catch(e =>{
                    return Promise.reject()
                })
        },

        async getHodPerformance(){
            await axiosInstance.get("hod/students_performance", {params: {'year': this.activeAcademicYear}})
                .then(response =>{
                    this.hodPerformance = response.data
                })
                .catch(e =>{
                    return Promise.reject()
                })
        },

        async getHeadStudentsPerformance(){
            await axiosInstance.get("head/students_performance", {params: {'year': this.activeAcademicYear}})
                .then(response =>{
                    this.headStudentsPerformance = response.data
                })
                .catch(e =>{
                    return Promise.reject()
                })
        },

        async teacherUploadResults(st_id: any, subject: any, score: any){
            const data = {'subject': subject, 'score': score, 'st_id': st_id, 'year': this.activeAcademicYear, 'term': this.activeTerm}
            await axiosInstance.post("teacher/results/upload/", data)
                .then(response =>{
                    this.staffStudentResultsSubjectAssignment = response.data[0]
                    this.staffStudentResultsEdit = response.data[1]
                })
                
                .catch(e =>{
                    return Promise.reject()
                })
        },

        async getUserData(){
            await axiosInstance.get('user/data')
                    .then(response =>{
                        const userInfo = response.data
                        this.userData = userInfo
                        this.activeAcademicYear = userInfo['academic_year']['name']
                        this.activeTerm = userInfo['current_term']
                    })
                    .catch(e =>{
                        return Promise.reject(e)
                    })
        },

        async userLogin(username: string, password: string){
            const formData = new FormData()
            formData.append('username', username)
            formData.append('password', password)
            try {
                const response = await defaultAxiosInstance.post('login', formData)
                if (response.status === 200){
                    this.authTokens = response.data
                    localStorage.setItem('authTokens', JSON.stringify(response.data))
                    await this.getUserData()
                    .then(secondResponse =>{
                        const userInfo:any = jwtDecode(response.data['access'])
                        if (userInfo['last_login']){
                            localStorage.setItem('RozmachAuth', JSON.stringify({'last_login': true, 'reset': userInfo['reset']}))
                        }else {
                            localStorage.setItem('RozmachAuth', JSON.stringify({'last_login': false, 'reset': userInfo['reset']}))
                        }
                        this.isAuthenticated = true
                        this.message = "Login successful"
                    })
                    .catch(e =>{
                        return Promise.reject(e)
                    })
                }
                else{
                    this.message = "Oops! the username or password is wrong."
                    return Promise.reject()
                }
            }
            catch (error) {
                if (error instanceof AxiosError && error.response && error.response.status === 401 ){
                    this.message = "Oops! the username or password is wrong."
                    return Promise.reject(error)
                }
                else{
                    this.message = "Oops! something went wrong"
                    return Promise.reject(error)
                }
            }
        },

        async UpdateToken(){
            await defaultAxiosInstance.post("api/token/refresh/", {'refresh': this.authTokens['refresh']})
            .then(response =>{
                this.authTokens = response.data
                // Tokens storage
                localStorage.setItem('authTokens', JSON.stringify(response.data))
            })
            .catch(e =>{
                return Promise.reject(e)
            })
        },

        async startUpServer(){
            defaultAxiosInstance.get('start_up')
            .then(response =>{
                return Promise.resolve()
            })
            .catch(e =>{
                return Promise.reject()
            })
        },
    },
})


import {defineStore} from "pinia";
import { jwtDecode } from "jwt-decode";
import { defaultAxiosInstance } from "../utils/axiosInstance";
import axiosInstance from '../utils/axiosInstance'
import { useRouter } from 'vue-router';

interface states {
    authTokens: any;
    userData: any;
    studentData: {
        subjects: any;
        classData: any;
        results: {
            academicYears: any
            termOne: any;
            termTwo: any;
            termThree: any;
        };
    }
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
    staffNotifications: any;
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
}

export const useUserAuthStore = defineStore('userAuth',{
    state: (): states =>{
        return{
            authTokens: null,
            userData: null,
            studentData: {
                subjects: null,
                classData: null,
                results: {
                    academicYears: null,
                    termOne: null,
                    termTwo: null,
                    termThree: null,
                },
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
            staffNotifications: null,
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
            this.authTokens = null
            this.userData= null,
            this.studentData= {
                subjects: null,
                classData: null,
                results: {
                    academicYears: null,
                    termOne: null,
                    termTwo: null,
                    termThree: null,
                },
            }
            this.message= ''
            this.staffStudentResultsSubjectAssignment= null
            this.staffStudentResultsEdit= null
            this.staffStudentsResultsFileGenerated= false

            this.hodSubjectAssignment= {
                termOne: null, 
                termTwo: null, 
                termThree: null,
            }
            this.hodSubjectAssignmentUpload= {
                staff: null,
                subjects: null,
                classes: null,
            }
            this.staffSubjectAssignment= {
                termOne: null,
                termTwo: null,
                termThree: null,
            }
            this.headPrograms= null
            this.headNotificationsStaff = null
            this.staffNotifications = null
            this.headDepartments = null
            this.hodPerformance = null
            this.headStudentsPerformance = null
            this.isAuthenticated = false
            this.adminClasses = {
                yearOne: null,
                yearTwo: null,
                yearThree: null,
                names: null,
                subjects: null,
                programs: null,
            }
            this.adminStaff = {
                departmentNames: null,
                subjects: null,
                departments: null,
                academicYears: null,
            }
            this.adminHeads = null
            this.teacherStudentsAttendance = null

        },

        async getStudentData(){
            await axiosInstance.get('st/data', {params: {'year': this.activeAcademicYear, 'term': this.activeTerm}})
                .then(response =>{
                    this.studentData.subjects = response.data['subjects']
                    this.studentData.results.termOne = response.data['results']['term_one']
                    this.studentData.results.termTwo = response.data['results']['term_two']
                    this.studentData.results.termThree = response.data['results']['term_three']
                    this.studentData.classData = response.data['class_data']
                    if (response.data['academic_years']){
                        this.studentData.results.academicYears = response.data['academic_years']
                    }
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

        async getTeacherSubjectAssignments(){
            await axiosInstance.get("teacher/subject_assignments/", {params: {'year': this.activeAcademicYear}})
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

        async staffNotification(){
            await axiosInstance.get("staff/notification")
                .then(response =>{
                    if (this.userData && this.userData['role']==='head'){
                        this.headNotificationsStaff = response.data['head_staff_data']
                        this.staffNotifications = response.data['messages']
                    }
                    else{
                        this.staffNotifications = response.data
                    }
                })
                .catch(e =>{
                    return Promise.reject()
                })
        },

        async getTeacherStudentResults(){
            await axiosInstance.get("teacher/results/upload/", {params: {'year': this.activeAcademicYear, 'term': this.activeTerm}})
                .then(response =>{
                    this.staffStudentResultsSubjectAssignment = response.data[0]
                    this.staffStudentResultsEdit = response.data[1]
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
                    await this.getUserData()
                    .then(secondResponse =>{
                        // Tokens storage location
                        localStorage.setItem('authTokens', JSON.stringify(response.data))

                        const userInfo = jwtDecode(response.data['access'])

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
                    this.message = "Oops! your username or password is wrong. Try again"
                    return Promise.reject()
                }
            }
            catch (e) {
                if (e.response && e.response.status === 401 ){
                    this.message = "Oops! your username or password is wrong."
                    return Promise.reject(e)
                }

                else{
                    this.message = "Oops! something went wrong. Check you internet connection"
                    return Promise.reject(e)
                }
            }
        },

        async UpdateToken(){
            if (this.authTokens && this.authTokens['refresh']){
                await defaultAxiosInstance.post("api/token/refresh/", {'refresh': this.authTokens['refresh']})
                .then(response =>{
                    this.authTokens = response.data
                    // Tokens storage
                    localStorage.setItem('authTokens', JSON.stringify(response.data))
                })
                .catch(e =>{
                    const router = useRouter()
                    this.logoutUser()
                    router.push('/')
                })
            }
            else {
                const router = useRouter()
                this.logoutUser()
                router.push('/')
                return Promise.reject()
            }
        },
    },
})


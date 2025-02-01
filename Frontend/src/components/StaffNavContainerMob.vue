<script setup lang="ts">
import { useUserAuthStore } from '@/stores/userAuthStore';
import { useElementsStore } from '@/stores/elementsStore';
import axiosInstance from '@/utils/axiosInstance';
import { headRoles } from '@/utils/util';
import { ref } from 'vue';
import { AxiosError } from 'axios';

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()
const roleSelected = ref('')

const changePage = (page_name: any) => {
    elementsStore.activePage = page_name
}

const showOverlay = () => {
    const logoutOverlay = document.getElementById('logout')
    if (logoutOverlay) {
        elementsStore.overlayPath = '/'
        logoutOverlay.style.display = 'flex'
    }
}

const resetStoreData = (staff_role: string) => {
    if (staff_role === 'teacher') {
        userAuthStore.teacherData = {
            courseWork: {},
            studentsAttendance: {},
            studentsAssessments: {},
            studentsExams: {},
            studentsResults: {},
            departmentData: null,
            staff: null,
        }
    }
    else if (staff_role === 'administrator') {
        userAuthStore.adminData = {
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
        }
    }
}

const changeRole = async () => {
    const formData = new FormData()
    if (roleSelected.value === userAuthStore.userData['current_role']['identifier']) {
        return
    }
    formData.append('newRoleIdentifier', roleSelected.value)
    elementsStore.ShowLoadingOverlay()
    try {
        await axiosInstance.post('staff/change-role', formData)
        await userAuthStore.getUserData()
        if (userAuthStore.userData['staff_role'].toLowerCase() === 'administrator') {
            elementsStore.activePage = 'AdminStaff'
            await userAuthStore.getAdminData()
            resetStoreData('teacher')
        }
        else if (userAuthStore.userData['staff_role'].toLowerCase() === 'teacher') {
            elementsStore.activePage = 'TeacherStaff'
            await userAuthStore.getTeacherData()
            resetStoreData('administrator')
        }
        else if (userAuthStore.userData['staff_role'].toLowerCase() === 'head') {
            elementsStore.activePage = 'HeadOverview'
            await userAuthStore.getHeadData()
        }
        elementsStore.HideLoadingOverlay()
    }
    catch (error) {
        elementsStore.HideLoadingOverlay()
        if (error instanceof AxiosError) {
            if (error.response) {
                if (error.response.status === 400 && error.response.data.message) {
                    elementsStore.ShowOverlay(error.response.data.message, 'red', null, null)
                } else {
                    elementsStore.ShowOverlay('Oops! something went wrong. Try again later', 'red', null, null)
                }
            }
            else if (!error.response && (error.code === 'ECONNABORTED' || !navigator.onLine)) {
                elementsStore.ShowOverlay('A network error occurred! Please check you internet connection', 'red', null, null)
            }
            else {
                elementsStore.ShowOverlay('An unexpected error occurred!', 'red', null, null)
            }
        }
    }
}


</script>


<template>
    <div class="nav-container-drawer" v-show="elementsStore.navDrawer">

        <!-- Admin -->
        <v-list class="nav-list-container" v-if="['administrator'].includes(userAuthStore.userData['staff_role'].toLowerCase())">

            <v-list-item>
                <div class="flex-all">
                    <v-select class="role-select"
                        :items="userAuthStore.userData['roles'].map((item: any) => ({ 'title': `${item.split('|')[1]} ${item.split('|')[0]}`, 'value': item }))"
                        label="CHANGE ROLE" v-model="roleSelected" item-title="title" density="compact"
                        item-value="value" variant="solo-filled" clearable />
                    <v-btn @click="changeRole()" :disabled="!(roleSelected)" :ripple="false" variant="flat"
                        type="submit" color="white" size="x-small" icon="mdi-swap-horizontal" />
                </div>
            </v-list-item>

            <v-list-item style="color: yellow" prepend-icon="mdi-account">
                <v-list-item-title style="color: yellow; font-weight: bold; font-size:.8rem">
                    CURRENT ROLE
                </v-list-item-title>
                <v-list-item-subtitle style="color: yellow; font-weight: bold; font-size:.7rem">
                    {{ userAuthStore.userData['current_role']['level']['name'].toUpperCase() }} {{ userAuthStore.userData['staff_role'].toUpperCase() }}
                </v-list-item-subtitle>
            </v-list-item>

            <v-list-item @click="changePage('AdminStaff')" class="nav-item nav-link"
                prepend-icon="mdi-account-group">
                STAFF
            </v-list-item>

            <v-list-item v-if="userAuthStore.userData['current_role']['level']['has_departments']" @click="changePage('AdminDepartments')" class="nav-item nav-link"
                prepend-icon="mdi-office-building">
                DEPARTMENTS
            </v-list-item>

            <v-list-item class="nav-item nav-link" prepend-icon="mdi-calendar-clock"
                @click="changePage('AdminAcademicYears')">
                ACADEMIC YEARS
            </v-list-item>

            <v-list-group>
                <template v-slot:activator="{ props }">
                    <v-list-item v-bind="props" prepend-icon="mdi-google-classroom" class="nav-item">
                        CLASSES
                    </v-list-item>
                </template>
                <v-list-item class="nav-title nav-link" v-for="(_class, index) in userAuthStore.adminData.classes"
                    :key="`${_class['name']}${index}`"
                    @click="changePage(`AdminStudentsClass,${_class['name']},${index}`)">
                    {{ _class['name'] }}
                </v-list-item>
            </v-list-group>

            <v-list-item @click="changePage('AdminSubjectAssignment')"
                v-if="userAuthStore.userData['current_role']['level']['has_departments']" class="nav-item nav-link"
                prepend-icon="mdi-book-multiple">
                SUBJECT ASSIGNMENTS
            </v-list-item>

            <v-list-item @click="changePage('AdminReleasedResults')" class="nav-item nav-link"
                prepend-icon="mdi-chart-bar">
                RELEASED RESULTS
            </v-list-item>

            <v-list-item @click="changePage('Help')" class="nav-item nav-link" prepend-icon="mdi-help">
                HELP
            </v-list-item>

            <div class="flex-all mt-15">
                <v-btn @click="showOverlay()" color="red" size="small" prepend-icon="mdi-logout">LOGOUT</v-btn>
            </div>
        </v-list>

        <!-- Head -->
        <v-list class="nav-list-container"
            v-if="headRoles.includes(userAuthStore.userData['staff_role'].toLowerCase())">

            <v-list-item class="nav-item nav-link" prepend-icon="mdi-calendar" @click="changePage('HeadOverview')">
                OVERVIEW
            </v-list-item>

            <v-list-item @click="changePage('HeadStaff')" class="nav-item nav-link" prepend-icon="mdi-account-multiple">
                STAFF
            </v-list-item>

            <v-list-group>
                <template v-slot:activator="{ props }">
                    <v-list-item v-bind="props" prepend-icon="mdi-book-outline" class="nav-item">
                        CLASSES
                    </v-list-item>
                </template>
                <v-list-item class="nav-title nav-link"
                    v-for="class_name in Object.keys(userAuthStore.headData.classes || {})" :key="class_name"
                    @click="changePage(`HeadStudents,${class_name}`)">
                    {{ class_name }}
                </v-list-item>
            </v-list-group>

            <v-list-item @click="changePage('Help')" class="nav-item nav-link" prepend-icon="mdi-help">
                HELP
            </v-list-item>

            <div class="flex-all mt-15">
                <v-btn @click="showOverlay()" color="red" size="small" prepend-icon="mdi-logout">LOGOUT</v-btn>
            </div>
        </v-list>

        <!-- Teacher -->
        <v-list class="nav-list-container" v-if="['teacher', 'hod'].includes(userAuthStore.userData['staff_role'].toLowerCase())">
            
            <v-list-item>
                <div class="flex-all">
                    <v-select class="role-select"
                        :items="userAuthStore.userData['roles'].map((item: any) => ({ 'title': `${item.split('|')[1]} ${item.split('|')[0]}`, 'value': item }))"
                        label="CHANGE ROLE" v-model="roleSelected" item-title="title" density="compact"
                        item-value="value" variant="solo-filled" clearable />
                    <v-btn @click="changeRole()" :disabled="!(roleSelected)" :ripple="false" variant="flat"
                        type="submit" color="white" size="x-small" icon="mdi-swap-horizontal" />
                </div>
            </v-list-item>

            <v-list-item style="color: yellow" prepend-icon="mdi-account">
                <v-list-item-title style="color: yellow; font-weight: bold; font-size:.8rem">
                    CURRENT ROLE
                </v-list-item-title>
                <v-list-item-subtitle style="color: yellow; font-weight: bold; font-size:.7rem">
                    {{ userAuthStore.userData['current_role']['level']['name'].toUpperCase() }} {{ userAuthStore.userData['staff_role'].toUpperCase() }}
                </v-list-item-subtitle>
            </v-list-item>
            
            <v-list-item @click="changePage('TeacherStaff')" class="nav-item nav-link"
                prepend-icon="mdi-account-group">
                STAFF
            </v-list-item>

            <v-list-group>
                <template v-slot:activator="{ props }">
                    <v-list-item v-bind="props" prepend-icon="mdi-google-classroom" class="nav-item">
                        MY CLASS(S)
                    </v-list-item>
                </template>
                <v-list-item class="nav-title nav-link"
                    v-for="class_name in Object.keys(userAuthStore.teacherData.courseWork || {})" :key="class_name"
                    @click="changePage(`TeacherCoursework,${class_name}`)">
                    {{ class_name }}
                </v-list-item>
            </v-list-group>

            <v-list-group v-if="Object.keys(userAuthStore.teacherData.studentsAttendance).length > 0">
                <template v-slot:activator="{ props }">
                    <v-list-item v-bind="props" prepend-icon="mdi-clipboard-text-outline" class="nav-item">
                        STUDENT ATTENDANCE
                    </v-list-item>
                </template>
                <v-list-item class="nav-title nav-link"
                    v-for="class_name in Object.keys(userAuthStore.teacherData.studentsAttendance)" :key="class_name"
                    @click="changePage(`TeacherStudentsAttendance,${class_name}`)">
                    {{ class_name }}
                </v-list-item>
            </v-list-group>

            <v-list-group>
                <template v-slot:activator="{ props }">
                    <v-list-item v-bind="props" class="nav-item" prepend-icon="mdi-book-open-outline">
                        STUDENT ASSESSMENTS
                    </v-list-item>
                </template>
                <v-list-group
                    v-for="[class_name, class_data] in Object.entries(userAuthStore.teacherData.studentsAssessments)"
                    :key="class_name">
                    <template v-slot:activator="{ props }">
                        <v-list-item v-bind="props" class="nav-item">
                            {{ class_name }}
                        </v-list-item>
                    </template>
                    <v-list-group v-for="[subject_name, subject_data] in Object.entries(class_data)"
                        :key="subject_name">
                        <template v-slot:activator="{ props }">
                            <v-list-item v-bind="props" class="nav-item">
                                {{ subject_name }}
                            </v-list-item>
                        </template>
                        <h4 class="nav-title nav-link" v-for="assessment_title in Object.keys(subject_data)"
                            :key="assessment_title"
                            @click="changePage(`TeacherStudentsAssessments,${class_name},${subject_name},${assessment_title}`)">
                            {{ assessment_title }}
                        </h4>
                    </v-list-group>
                </v-list-group>
            </v-list-group>

            <v-list-group>
                <template v-slot:activator="{ props }">
                    <v-list-item v-bind="props" class="nav-item" prepend-icon="mdi-file-check-outline">
                        STUDENT EXAMS
                    </v-list-item>
                </template>
                <v-list-group
                    v-for="[class_name, class_exams_data] in Object.entries(userAuthStore.teacherData.studentsExams)"
                    :key="class_name">
                    <template v-slot:activator="{ props }">
                        <v-list-item v-bind="props" class="nav-item">
                            {{ class_name }}
                        </v-list-item>
                    </template>
                    <h4 class="nav-title nav-link" v-for="subject_name in Object.keys(class_exams_data)"
                        :key="subject_name" @click="changePage(`TeacherStudentsExams,${class_name},${subject_name}`)">
                        {{ subject_name }}
                    </h4>
                </v-list-group>
            </v-list-group>

            <v-list-group>
                <template v-slot:activator="{ props }">
                    <v-list-item v-bind="props" class="nav-item" prepend-icon="mdi-trophy-outline">
                        STUDENT RESULTS
                    </v-list-item>
                </template>
                <v-list-group
                    v-for="[class_name, class_student_exams_data] in Object.entries(userAuthStore.teacherData.studentsResults)"
                    :key="class_name">
                    <template v-slot:activator="{ props }">
                        <v-list-item v-bind="props" class="nav-item">
                            {{ class_name }}
                        </v-list-item>
                    </template>
                    <h4 class="nav-title nav-link" v-for="subject_name in Object.keys(class_student_exams_data)"
                        :key="subject_name" @click="changePage(`TeacherStudentsResults,${class_name},${subject_name}`)">
                        {{ subject_name }}
                    </h4>
                </v-list-group>
            </v-list-group>

            <v-list-item v-if="userAuthStore.userData['level'] === 'SHS'" class="nav-item nav-link"
                @click="changePage('StudentTranscript')" prepend-icon="mdi-book-outline">
                TRANSCRIPT
            </v-list-item>
            <v-list-item v-if="userAuthStore.userData['level'] === 'JHS'" class="nav-item nav-link"
                @click="changePage('StudentTranscript')" prepend-icon="mdi-book-outline">
                TERMINAL REPORT
            </v-list-item>
            <v-list-item @click="changePage('Help')" class="nav-item nav-link" prepend-icon="mdi-help">
                HELP
            </v-list-item>
            <div class="flex-all mt-15">
                <v-btn @click="showOverlay()" size="small" color="red" variant="flat"
                    prepend-icon="mdi-logout">LOGOUT</v-btn>
            </div>
        </v-list>
    </div>
</template>


<style scoped>
.role-select {
    height: 40px !important;
}
</style>
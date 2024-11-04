<script setup lang="ts">
import { useUserAuthStore } from '@/stores/userAuthStore';
import { useElementsStore } from '@/stores/elementsStore';

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()


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


</script>


<template>
    <div class="nav-container-drawer" v-show="elementsStore.navDrawer">
        <!-- Admin -->
        <v-list class="nav-list-container" v-if="['admin'].includes(userAuthStore.userData['staff_role'].toLowerCase())">
            <v-list-item class="nav-item nav-link" prepend-icon="mdi-calendar"
                @click="changePage('AdminAcademicYears')">
                ACADEMIC YEAR
            </v-list-item>
            <v-list-group>
                <template v-slot:activator="{ props }">
                    <v-list-item v-bind="props" prepend-icon="mdi-book-outline" class="nav-item">
                        CLASSES
                    </v-list-item>
                </template>
                <v-list-item class="nav-title nav-link" v-for="(_class, index) in userAuthStore.adminData.classes"
                    :key="`${_class['name']}${index}`"
                    @click="changePage(`AdminStudentsClass,${_class['name']},${index}`)">
                    {{ _class['name'] }}
                </v-list-item>
            </v-list-group>
            
            <v-list-item @click="changePage('AdminLinkedClases')" class="nav-item nav-link" prepend-icon="mdi-book">
                LINKED CLASSES
            </v-list-item>

            <v-list-item @click="changePage('AdminStaff')" class="nav-item nav-link" prepend-icon="mdi-account-multiple">
                STAFF
            </v-list-item>

            <v-list-group v-if="userAuthStore.staffData.studentsattendance?.length > 0">
                <template v-slot:activator="{ props }">
                    <v-list-item v-bind="props" prepend-icon="mdi-clipboard-text-outline" class="nav-item">
                        STUDENT ATTENDANCE
                    </v-list-item>
                </template>
                <v-list-item class="nav-title nav-link"
                    v-for="(class_name, index) in userAuthStore.staffData.studentsattendance" :key="index"
                    @click="changePage(`TeacherStudentsAttendance,${class_name['class_name']},${index}`)">
                    {{ class_name['class_name'] }}
                </v-list-item>
            </v-list-group>

            <v-list-group>
                <template v-slot:activator="{ props }">
                    <v-list-item v-bind="props" class="nav-item" prepend-icon="mdi-book-open-outline">
                        STUDENT ASSESSMENTS
                    </v-list-item>
                </template>
                <v-list-group v-for="(_class, index) in userAuthStore.staffData.studentsAssessments"
                    :key="`${_class['class_name']}${index}`">
                    <template v-slot:activator="{ props }">
                        <v-list-item v-bind="props" class="nav-item">
                            {{ _class['class_name'] }}
                        </v-list-item>
                    </template>
                    <v-list-group v-for="(subject, ind) in _class['assignments']"
                        :key="`${_class['class_name']}${subject['subject']}${ind}`">
                        <template v-slot:activator="{ props }">
                            <v-list-item v-bind="props" class="nav-item">
                                {{ subject['subject'] }}
                            </v-list-item>
                        </template>
                        <h4 class="nav-title nav-link" v-for="(assess, i) in subject['assessments']"
                            :key="`${_class['class_name']}${subject['subject']}${assess['title']}${i}`"
                            @click="changePage(`TeacherStudentsAssessments,${_class['class_name']},${subject['subject']},${assess['title']},${i}`)">
                            {{ assess['title'] }}
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
                <v-list-group v-for="(_class, index) in userAuthStore.staffData.studentsExams" :key="index">
                    <template v-slot:activator="{ props }">
                        <v-list-item v-bind="props" class="nav-item">
                            {{ _class['class_name'] }}
                        </v-list-item>
                    </template>
                    <h4 class="nav-title nav-link" v-for="(_subject, ind) in _class['exams']" :key="ind"
                        @click="changePage(`TeacherStudentsExams,${_class['class_name']},${_subject['subject']},${ind}`)">
                        {{ _subject['subject'] }}
                    </h4>
                </v-list-group>
            </v-list-group>

            <v-list-group>
                <template v-slot:activator="{ props }">
                    <v-list-item v-bind="props" class="nav-item" prepend-icon="mdi-trophy-outline">
                        STUDENT RESULTS
                    </v-list-item>
                </template>
                <v-list-group v-for="(_class, index) in userAuthStore.staffData.studentsResults" :key="index">
                    <template v-slot:activator="{ props }">
                        <v-list-item v-bind="props" class="nav-item">
                            {{ _class['class_name'] }}
                        </v-list-item>
                    </template>
                    <h4 class="nav-title nav-link" v-for="(_subject, ind) in _class['results']" :key="ind"
                        @click="changePage(`TeacherStudentsResults,${_class['class_name']},${_subject['subject']},${ind}`)">
                        {{ _subject['subject'] }}
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
                <v-btn @click="showOverlay()" class="logout-btn" prepend-icon="mdi-logout">LOGOUT</v-btn>
            </div>
        </v-list>

        <!-- Teacher/Hod -->
        <v-list class="nav-list-container" v-if="['teacher', 'hod'].includes(userAuthStore.userData['staff_role'].toLowerCase())">
            <v-list-group>
                <template v-slot:activator="{ props }">
                    <v-list-item v-bind="props" prepend-icon="mdi-account-group-outline" class="nav-item">
                        MY CLASS
                    </v-list-item>
                </template>
                <v-list-item class="nav-title nav-link"
                    v-if="!userAuthStore.staffData.courseWork || userAuthStore.staffData.courseWork?.length === 0"
                    @click="changePage('TeacherCoursework,Class,0')">
                    NO CLASS
                </v-list-item>
                <v-list-item class="nav-title nav-link" v-for="(_course, index) in userAuthStore.staffData.courseWork"
                    :key="`${_course['students_class']['name']}${index}`"
                    @click="changePage(`TeacherCoursework,${_course['students_class']['name']},${index}`)">
                    {{ _course['students_class']['name'] }}
                </v-list-item>
            </v-list-group>

            <v-list-item @click="changePage('TeacherDepartment')" class="nav-item nav-link" prepend-icon="mdi-book">
                MY DEPARTMENT
            </v-list-item>

            <v-list-group v-if="userAuthStore.staffData.studentsattendance?.length > 0">
                <template v-slot:activator="{ props }">
                    <v-list-item v-bind="props" prepend-icon="mdi-clipboard-text-outline" class="nav-item">
                        STUDENT ATTENDANCE
                    </v-list-item>
                </template>
                <v-list-item class="nav-title nav-link"
                    v-for="(class_name, index) in userAuthStore.staffData.studentsattendance" :key="index"
                    @click="changePage(`TeacherStudentsAttendance,${class_name['class_name']},${index}`)">
                    {{ class_name['class_name'] }}
                </v-list-item>
            </v-list-group>

            <v-list-group>
                <template v-slot:activator="{ props }">
                    <v-list-item v-bind="props" class="nav-item" prepend-icon="mdi-book-open-outline">
                        STUDENT ASSESSMENTS
                    </v-list-item>
                </template>
                <v-list-group v-for="(_class, index) in userAuthStore.staffData.studentsAssessments"
                    :key="`${_class['class_name']}${index}`">
                    <template v-slot:activator="{ props }">
                        <v-list-item v-bind="props" class="nav-item">
                            {{ _class['class_name'] }}
                        </v-list-item>
                    </template>
                    <v-list-group v-for="(subject, ind) in _class['assignments']"
                        :key="`${_class['class_name']}${subject['subject']}${ind}`">
                        <template v-slot:activator="{ props }">
                            <v-list-item v-bind="props" class="nav-item">
                                {{ subject['subject'] }}
                            </v-list-item>
                        </template>
                        <h4 class="nav-title nav-link" v-for="(assess, i) in subject['assessments']"
                            :key="`${_class['class_name']}${subject['subject']}${assess['title']}${i}`"
                            @click="changePage(`TeacherStudentsAssessments,${_class['class_name']},${subject['subject']},${assess['title']},${i}`)">
                            {{ assess['title'] }}
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
                <v-list-group v-for="(_class, index) in userAuthStore.staffData.studentsExams" :key="index">
                    <template v-slot:activator="{ props }">
                        <v-list-item v-bind="props" class="nav-item">
                            {{ _class['class_name'] }}
                        </v-list-item>
                    </template>
                    <h4 class="nav-title nav-link" v-for="(_subject, ind) in _class['exams']" :key="ind"
                        @click="changePage(`TeacherStudentsExams,${_class['class_name']},${_subject['subject']},${ind}`)">
                        {{ _subject['subject'] }}
                    </h4>
                </v-list-group>
            </v-list-group>

            <v-list-group>
                <template v-slot:activator="{ props }">
                    <v-list-item v-bind="props" class="nav-item" prepend-icon="mdi-trophy-outline">
                        STUDENT RESULTS
                    </v-list-item>
                </template>
                <v-list-group v-for="(_class, index) in userAuthStore.staffData.studentsResults" :key="index">
                    <template v-slot:activator="{ props }">
                        <v-list-item v-bind="props" class="nav-item">
                            {{ _class['class_name'] }}
                        </v-list-item>
                    </template>
                    <h4 class="nav-title nav-link" v-for="(_subject, ind) in _class['results']" :key="ind"
                        @click="changePage(`TeacherStudentsResults,${_class['class_name']},${_subject['subject']},${ind}`)">
                        {{ _subject['subject'] }}
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
                <v-btn @click="showOverlay()" class="logout-btn" prepend-icon="mdi-logout">LOGOUT</v-btn>
            </div>
        </v-list>
    </div>
</template>


<style scoped></style>
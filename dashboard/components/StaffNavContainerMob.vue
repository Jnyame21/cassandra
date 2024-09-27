
<script setup lang="ts">
const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()


const changePage = (page_name:any)=>{
    elementsStore.activePage = page_name
}

const showOverlay = ()=>{
  const logoutOverlay = document.getElementById('logout')
    if (logoutOverlay){
        elementsStore.overlayPath = '/'
        logoutOverlay.style.display = 'flex'
    }
}


</script>


<template>
    <div class="nav-container-drawer" v-show="elementsStore.navDrawer">
        <v-list class="nav-list-container">
            <v-list-item class="nav-item nav-link" @click="changePage('TeacherStudentsAttendance')" prepend-icon="mdi-clipboard-text-outline">
                STUDENTS ATTENDANCE
            </v-list-item>

            <v-list-group>
                <template v-slot:activator="{ props }">
                    <v-list-item v-bind="props" prepend-icon="mdi-account-group-outline" class="nav-item">
                        MY CLASS
                    </v-list-item>
                </template>
                <v-list-item class="nav-title nav-link" v-for="(class_name, index) in userAuthStore.teacherData.courseWork" :key="index" @click="changePage(`TeacherCourseWork,${index}`)">
                    {{ class_name['students_class']['name'] }}
                </v-list-item>
            </v-list-group>

            <v-list-group v-if="userAuthStore.teacherData.studentsWithAssessments">
                <template v-slot:activator="{ props }">
                    <v-list-item v-bind="props" class="nav-item" prepend-icon="mdi-book-open-outline">
                        ASSESSMENTS
                    </v-list-item>
                </template>
                <v-list-group v-for="(_class, index) in userAuthStore.teacherData.studentsWithAssessments" :key="index">
                    <template v-slot:activator="{ props }">
                        <v-list-item v-bind="props" class="nav-item">
                            {{ _class['class_name'] }}
                        </v-list-item>
                    </template>
                    <v-list-group v-for="(subject, ind) in _class['assignments']" :key="ind">
                        <template v-slot:activator="{ props }">
                            <v-list-item v-bind="props" class="nav-item">
                                {{ subject['subject'] }}
                            </v-list-item>
                        </template>
                        <h4 class="nav-title nav-link" v-for="(assess, i) in subject['assessments']" :key="i" @click="changePage(`TeacherStudentsAssessments,${_class['class_name']},${subject['subject']},${assess['title']}`)">
                            {{ assess['title'] }}
                        </h4>
                    </v-list-group>
                </v-list-group>
            </v-list-group>

            <v-list-group>
                <template v-slot:activator="{ props }">
                    <v-list-item v-bind="props" class="nav-item" prepend-icon="mdi-trophy-outline">
                        EXAMS
                    </v-list-item>
                </template>
                <v-list-group v-for="(_class, index) in userAuthStore.teacherData.courseWork" :key="index">
                    <template v-slot:activator="{ props }">
                        <v-list-item v-bind="props" class="nav-item">
                            {{ _class['students_class']['name'] }}
                        </v-list-item>
                    </template>
                    <h4 class="nav-title nav-link" v-for="(subject, ind) in userAuthStore.teacherData.courseWork[index]['subjects']" :key="ind" @click="changePage(`TeacherStudentsExams,${_class['students_class']['name']},${subject['name']}`)">
                        {{ subject['name'] }}
                    </h4>
                </v-list-group>
            </v-list-group>

            
            <v-list-item v-if="userAuthStore.userData['level'] === 'SHS' " class="nav-item nav-link" @click="changePage('StudentTranscript')" prepend-icon="mdi-book-outline">
                TRANSCRIPT
            </v-list-item>
            <v-list-item v-if="userAuthStore.userData['level'] === 'JHS' " class="nav-item nav-link" @click="changePage('StudentTranscript')" prepend-icon="mdi-book-outline">
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


<style scoped>



</style>
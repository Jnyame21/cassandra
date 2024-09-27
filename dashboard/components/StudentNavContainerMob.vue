
<script setup lang="ts">
const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()

const changePage = (page_name:string)=>{
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
    <div id="navContainerDrawer" class="nav-container-drawer" v-show="elementsStore.navDrawer">
        <v-list class="nav-list-container">
            <v-list-item class="nav-title nav-link" @click="changePage('StudentSubjects')" prepend-icon="mdi-book-outline">
                SUBJECTS
            </v-list-item>
            <v-list-item class="nav-title nav-link" @click="changePage('StudentClassStudents')" prepend-icon="mdi-account-group-outline">
                MY CLASS
            </v-list-item>
            <v-list-group v-for="(year, index) in userAuthStore.studentData.academicYearsData" :key="index">
                <template v-slot:activator="{ props }">
                    <v-list-item v-bind="props" class="nav-title" prepend-icon="mdi-book-open-outline">
                        {{ year['name'] }}
                    </v-list-item>
                </template>
                <v-list-group>
                    <template v-slot:activator="{ props }">
                        <v-list-item v-bind="props" class="nav-sub-title">
                            ATTENDANCE
                        </v-list-item>
                    </template>
                    <v-list-item class="nav-item nav-link" v-if="year['period_division'] !== 'SEMESTER' " @click="changePage(`StudentAttendance,${year['name']},${year['period_division']},3`)">
                        {{ year['period_division'] }} 3
                    </v-list-item>
                    <v-list-item class="nav-item nav-link" @click="changePage(`StudentAttendance,${year['name']},${year['period_division']},2`)">
                        {{ year['period_division'] }} 2
                    </v-list-item>
                    <v-list-item class="nav-item nav-link" @click="changePage(`StudentAttendance,${year['name']},${year['period_division']},1`)">
                        {{ year['period_division'] }} 1
                    </v-list-item>
                </v-list-group>
                <v-list-group>
                    <template v-slot:activator="{ props }">
                        <v-list-item v-bind="props" class="nav-sub-title">
                            ASSESSMENTS
                        </v-list-item>
                    </template>
                    <v-list-item class="nav-item nav-link" v-if="year['period_division'] !== 'SEMESTER' " @click="changePage(`StudentAssessments,${year['name']},${year['period_division']},3`)">
                        {{ year['period_division'] }} 3
                    </v-list-item>
                    <v-list-item class="nav-item nav-link" @click="changePage(`StudentAssessments,${year['name']},${year['period_division']},2`)">
                        {{ year['period_division'] }} 2
                    </v-list-item>
                    <v-list-item class="nav-item nav-link" @click="changePage(`StudentAssessments,${year['name']},${year['period_division']},1`)">
                        {{ year['period_division'] }} 1
                    </v-list-item>
                </v-list-group>
                <v-list-group>
                    <template v-slot:activator="{ props }">
                        <v-list-item v-bind="props" class="nav-sub-title">
                            RESULTS
                        </v-list-item>
                    </template>
                    <v-list-item class="nav-item nav-link" v-if="year['period_division'] !== 'SEMESTER' " @click="changePage(`StudentResults,${year['name']},${year['period_division']},3`)">
                        {{ year['period_division'] }} 3
                    </v-list-item>
                    <v-list-item class="nav-item nav-link" @click="changePage(`StudentResults,${year['name']},${year['period_division']},2`)">
                        {{ year['period_division'] }} 2
                    </v-list-item>
                    <v-list-item class="nav-item nav-link" @click="changePage(`StudentResults,${year['name']},${year['period_division']},1`)">
                        {{ year['period_division'] }} 1
                    </v-list-item>
                </v-list-group>
            </v-list-group>
            <v-list-item v-if="userAuthStore.userData['level'] === 'SHS' " class="nav-title nav-link" @click="changePage('StudentTranscript')" prepend-icon="mdi-book-outline">
                TRANSCRIPT
            </v-list-item>
            <v-list-item v-if="userAuthStore.userData['level'] === 'JHS' " class="nav-title nav-link" @click="changePage('StudentTranscript')" prepend-icon="mdi-book-outline">
                TERMINAL REPORT
            </v-list-item>
            <v-list-item @click="changePage('Help')" class="nav-title nav-link" prepend-icon="mdi-help">
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
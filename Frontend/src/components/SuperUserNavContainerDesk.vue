
<script setup lang="ts">
import { useUserAuthStore } from '@/stores/userAuthStore';
import { useElementsStore } from '@/stores/elementsStore';

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
    <div class="nav-container-drawer" v-show="elementsStore.navDrawer">
        <v-list class="nav-list-container">
            <v-list-item class="nav-item nav-link" @click="changePage('SuperUserSchools')" prepend-icon="mdi-account-group-outline">
                CREATE SCHOOL
            </v-list-item>
            <v-list-group>
                <template v-slot:activator="{ props }">
                    <v-list-item v-bind="props" class="nav-item" prepend-icon="mdi-book-open-outline">
                        STAFF
                    </v-list-item>
                </template>
                <v-list-group v-for="[year_name, year_attendance_data] in Object.entries(userAuthStore.studentData.attendances || {})" :key="year_name">
                    <template v-slot:activator="{ props }">
                        <v-list-item v-bind="props" class="nav-item">
                            {{ year_name }}
                        </v-list-item>
                    </template>
                    <v-list-item class="nav-title nav-link" v-for="term_name in Object.keys(year_attendance_data)" :key="term_name" @click="changePage(`StudentAttendance,${year_name},${term_name}`)">
                        {{ term_name }}
                    </v-list-item>
                </v-list-group>
            </v-list-group>

            <v-list-group>
                <template v-slot:activator="{ props }">
                    <v-list-item v-bind="props" class="nav-item" prepend-icon="mdi-book-open-outline">
                        ASSESSMENTS
                    </v-list-item>
                </template>
                <v-list-group v-for="[year_name, year_assessment_data] in Object.entries(userAuthStore.studentData.assessments || {})" :key="year_name">
                    <template v-slot:activator="{ props }">
                        <v-list-item v-bind="props" class="nav-item">
                            {{ year_name }}
                        </v-list-item>
                    </template>
                    <v-list-item class="nav-title nav-link" v-for="term_name in Object.keys(year_assessment_data)" :key="term_name" @click="changePage(`StudentAssessments,${year_name},${term_name}`)">
                        {{ term_name }}
                    </v-list-item>
                </v-list-group>
            </v-list-group>

            <v-list-group>
                <template v-slot:activator="{ props }">
                    <v-list-item v-bind="props" class="nav-item" prepend-icon="mdi-book-open-outline">
                        EXAMS
                    </v-list-item>
                </template>
                <v-list-group v-for="[year_name, year_exam_data] in Object.entries(userAuthStore.studentData.exams || {})" :key="year_name">
                    <template v-slot:activator="{ props }">
                        <v-list-item v-bind="props" class="nav-item">
                            {{ year_name }}
                        </v-list-item>
                    </template>
                    <v-list-item class="nav-title nav-link" v-for="term_name in Object.keys(year_exam_data)" :key="term_name" @click="changePage(`StudentExams,${year_name},${term_name}`)">
                        {{ term_name }}
                    </v-list-item>
                </v-list-group>
            </v-list-group>

            <v-list-group>
                <template v-slot:activator="{ props }">
                    <v-list-item v-bind="props" class="nav-item" prepend-icon="mdi-book-open-outline">
                        RESULTS
                    </v-list-item>
                </template>
                <v-list-group v-for="[year_name, year_result_data] in Object.entries(userAuthStore.studentData.results || {})" :key="year_name">
                    <template v-slot:activator="{ props }">
                        <v-list-item v-bind="props" class="nav-item">
                            {{ year_name }}
                        </v-list-item>
                    </template>
                    <v-list-item class="nav-title nav-link" v-for="term_name in Object.keys(year_result_data)" :key="term_name" @click="changePage(`StudentResults,${year_name},${term_name}`)">
                        {{ term_name }}
                    </v-list-item>
                </v-list-group>
            </v-list-group>
            <div class="flex-all mt-15">
                <v-btn @click="showOverlay()" size="small" color="red" variant="flat" prepend-icon="mdi-logout">LOGOUT</v-btn>
            </div>
        </v-list>
    </div>
</template>


<style scoped>



</style>
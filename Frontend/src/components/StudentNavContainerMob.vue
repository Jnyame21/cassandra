
<script setup lang="ts">
import { useUserAuthStore } from '@/stores/userAuthStore';
import { useElementsStore } from '@/stores/elementsStore';
import axiosInstance from '@/utils/axiosInstance';
import { ref } from 'vue';
import { AxiosError } from 'axios';

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()
const levelSelected = ref('')

const changePage = (page_name:string)=>{
  elementsStore.activePage = page_name
}

const changeLevel = async () => {
  const formData = new FormData()
  if (levelSelected.value === userAuthStore.userData['current_level']['name']) {
    return
  }
  formData.append('levelName', levelSelected.value)
  elementsStore.ShowLoadingOverlay()
  try {
    await axiosInstance.post('student/change-level', formData)
    await userAuthStore.getUserData()
    await userAuthStore.getStudentData()
    elementsStore.HideLoadingOverlay()
  }
  catch (error) {
    elementsStore.HideLoadingOverlay()
    if (error instanceof AxiosError) {
      if (error.response) {
        if (error.response.status === 400 && error.response.data.message) {
          elementsStore.ShowOverlay(error.response.data.message, 'red')
        } 
        else {
          elementsStore.ShowOverlay('Oops! something went wrong. Try again later', 'red')
        }
      }
      else if (!error.response && (error.code === 'ECONNABORTED' || !navigator.onLine)) {
        elementsStore.ShowOverlay('A network error occurred! Please check you internet connection', 'red')
      }
      else {
        elementsStore.ShowOverlay('An unexpected error occurred!', 'red')
      }
    }
  }
}

const showOverlay = ()=>{
  const overalay = document.getElementById('LogoutOverlay')
  if (overalay){
    overalay.style.display = 'flex'
  }
}


</script>


<template>
    <div class="nav-container-drawer" v-show="elementsStore.navDrawer">
        <v-list class="nav-list-container">

            <v-list-item>
                <div class="flex-all">
                    <v-select class="level-select" :items="userAuthStore.userData['levels']" label="CHANGE LEVEL" v-model="levelSelected"
                      item-title="title" density="compact" item-value="value" variant="solo-filled" clearable 
                    />
                    <v-btn @click="changeLevel()" :disabled="!(levelSelected)" :ripple="false" variant="flat" type="submit" color="white" size="x-small" icon="mdi-swap-horizontal" 
                    />
                </div>
            </v-list-item>

            <v-list-item style="color: yellow" prepend-icon="mdi-account">
                <v-list-item-title style="color: yellow; font-weight: bold; font-size:.8rem">
                    CURRENT LEVEL
                </v-list-item-title>
                <v-list-item-subtitle style="color: yellow; font-weight: bold; font-size:.7rem">
                    {{ userAuthStore.userData['current_level']['name'].toUpperCase() }}
                </v-list-item-subtitle>
            </v-list-item>

            <v-list-item class="nav-item nav-link" @click="changePage('StudentClassStudents')" prepend-icon="mdi-google-classroom">
                MY CLASS
            </v-list-item>

            <v-list-group>
                <template v-slot:activator="{ props }">
                    <v-list-item v-bind="props" class="nav-item" prepend-icon="mdi-calendar-check-outline">
                        ATTENDANCE
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
                    <v-list-item v-bind="props" class="nav-item" prepend-icon="mdi-clipboard-text-outline">
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
                    <v-list-item v-bind="props" class="nav-item" prepend-icon="mdi-file-document-outline">
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
                    <v-list-item v-bind="props" class="nav-item" prepend-icon="mdi-chart-line">
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

            <!-- <v-list-item v-if="userAuthStore.userData['level']['name'] === 'SHS' " class="nav-item nav-link" @click="changePage('StudentTranscript')" prepend-icon="mdi-book-outline">
                TRANSCRIPT
            </v-list-item> -->

            <v-list-item @click="changePage('Help')" class="nav-item nav-link" prepend-icon="mdi-headset">
                HELP
            </v-list-item>

            <div class="flex-all mt-15">
                <v-btn @click="showOverlay()" size="small" color="red" variant="flat" prepend-icon="mdi-logout">LOGOUT</v-btn>
            </div>
        </v-list>
    </div>
</template>


<style scoped>

.level-select {
  height: 40px !important;
}

</style>
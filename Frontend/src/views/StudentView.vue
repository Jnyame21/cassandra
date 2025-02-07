<script setup lang="ts">
import { useUserAuthStore } from '@/stores/userAuthStore'
import { useElementsStore } from '@/stores/elementsStore'
import { onBeforeMount, onMounted, ref } from 'vue'
import { AxiosError } from 'axios';
import axiosInstance from '@/utils/axiosInstance';
import { useHead } from '@vueuse/head';
import HelpForm from '@/components/HelpForm.vue'
import TheHeader from '@/components/TheHeader.vue';
import TheFooter from '@/components/TheFooter.vue';
import StudentAttendance from '@/components/StudentAttendance.vue';
import StudentAssessments from '@/components/StudentAssessments.vue';
import StudentResults from '@/components/StudentResults.vue';
import StudentExams from '@/components/StudentExams.vue';
import StudentClassStudents from '@/components/StudentClassStudents.vue';
import StudentNavContainerMob from '@/components/StudentNavContainerMob.vue';
import StudentNavContainerDesk from '@/components/StudentNavContainerDesk.vue';

useHead({
  meta: [
    {name: "robots", content: "no-index"}
  ],
})

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()
const password = ref('')
const repeatPassword = ref('')
const passwordVisible = ref(false)
const repeatPasswordVisible = ref(false)

onBeforeMount(()=>{
  elementsStore.activePage = 'StudentClassStudents'
})

onMounted(()=>{
  if (userAuthStore.resetPassword){
    showOverlay('StudentsWelcomeOverlay')
  }
})

const resetUserPassword = async () => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('password', password.value)

  try {
    await axiosInstance.post('user/reset-password', formData)
    userAuthStore.resetPassword = false
    closeOverlay('StudentsWelcomeOverlay')
    elementsStore.HideLoadingOverlay()
  }
  catch (error) {
    elementsStore.HideLoadingOverlay()
    if (error instanceof AxiosError) {
      if (error.response) {
        if (error.response.status === 400 && error.response.data.message) {
          elementsStore.ShowOverlay(error.response.data.message, 'red')
        } else {
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

const closeOverlay = (element: string)=>{
  const overlay = document.getElementById(element)
  if (overlay){
    overlay.style.display = 'none'
  }
}

const showOverlay = (element: string)=>{
  const overlay = document.getElementById(element)
  if (overlay){
    overlay.style.display = 'flex'
  }
}



</script>


<template>
   
  <!-- Welcome Overlay-->
  <div id="StudentsWelcomeOverlay" class="overlay" v-if="userAuthStore.userData">
    <div class="overlay-card">
      <div class="overlay-card-info-container">
        <p style="text-align: center" class="mb-5">
          <strong>Welcome {{ userAuthStore.userData['first_name'] }} {{ userAuthStore.userData['last_name'] }}! Reset your password to continue</strong>
        </p>
      </div>
      <div class="overlay-card-content-container">
        <v-text-field class="input-field" :append-inner-icon="passwordVisible ? 'mdi-eye-off-outline' : 'mdi-eye-outline'" @click:append-inner="passwordVisible = !passwordVisible"
          :type="passwordVisible ? 'text' : 'password'" clearable density="comfortable" v-model="password" label="NEW PASSWORD" hint="Enter a new password"  prepend-inner-icon="mdi-lock-outline"
        />
        <v-text-field class="input-field" :append-inner-icon="repeatPasswordVisible ? 'mdi-eye-off-outline' : 'mdi-eye-outline'" @click:append-inner="repeatPasswordVisible = !repeatPasswordVisible"
          :type="repeatPasswordVisible ? 'text' : 'password'" clearable density="comfortable" v-model="repeatPassword" label="REPEAT PASSWORD" hint="Repeat the new password"  prepend-inner-icon="mdi-lock-outline"
        />
      </div>
      <div class="overlay-card-action-btn-container">
        <v-btn @click="resetUserPassword"
          :disabled="!(password && repeatPassword && password === repeatPassword)" :ripple="false"
          variant="flat" type="submit" color="black" size="small" append-icon="mdi-checkbox-marked-circle">
          SUBMIT
        </v-btn>
      </div>
    </div>
  </div>

  <TheHeader v-if="userAuthStore.userData"/>
  <main class="main" v-if="userAuthStore.userData">
    <StudentNavContainerMob v-if="!elementsStore.onDesk"/>
    <StudentNavContainerDesk v-if="elementsStore.onDesk"/>
    <div class="pages-container">
      <div class="component-wrapper" :class="{ 'is-active-component': elementsStore.activePage === 'StudentClassStudents' }">
        <StudentClassStudents />
      </div>
      <div class="component-wrapper" v-if="userAuthStore.studentData.results" :class="{ 'is-active-component': elementsStore.activePage.split(',')[0] === 'StudentResults' }">
        <div class="component-wrapper" v-for="[year_name, year_result_data] in Object.entries(userAuthStore.studentData.results )" :key="year_name">
          <StudentResults v-for="term_name in Object.keys(year_result_data)"
          :key="term_name"
          :yearName="year_name"
          :termName="term_name"
          />
        </div>
      </div>
      <div class="component-wrapper" v-if="userAuthStore.studentData.attendances" :class="{ 'is-active-component': elementsStore.activePage.split(',')[0] === 'StudentAttendance' }">
        <div class="component-wrapper" v-for="[year_name, year_attendance_data] in Object.entries(userAuthStore.studentData.attendances)" :key="year_name">
          <StudentAttendance v-for="term_name in Object.keys(year_attendance_data)"
          :key="term_name"
          :yearName="year_name"
          :termName="term_name"
          />
        </div>
      </div>
      <div class="component-wrapper" v-if="userAuthStore.studentData.assessments" :class="{ 'is-active-component': elementsStore.activePage.split(',')[0] === 'StudentAssessments' }">
        <div class="component-wrapper" v-for="[year_name, year_assessment_data] in Object.entries(userAuthStore.studentData.assessments )" :key="year_name">
          <StudentAssessments v-for="term_name in Object.keys(year_assessment_data)"
          :key="term_name"
          :yearName="year_name"
          :termName="term_name"
          />
        </div>
      </div>
      <div class="component-wrapper" v-if="userAuthStore.studentData.exams" :class="{ 'is-active-component': elementsStore.activePage.split(',')[0] === 'StudentExams' }">
        <div class="component-wrapper" v-for="[year_name, year_exam_data] in Object.entries(userAuthStore.studentData.exams )" :key="year_name">
          <StudentExams v-for="term_name in Object.keys(year_exam_data)"
          :key="term_name"
          :yearName="year_name"
          :termName="term_name"
          />
        </div>
      </div>
      <!-- <StudentTranscript v-show="elementsStore.activePage.split(',')[0] === 'StudentTranscript' " /> -->
      <HelpForm v-show="elementsStore.activePage.split(',')[0] === 'Help'" />
    </div>
  </main>
  <TheFooter/>
</template>

<style scoped>

.overlay-card{
  max-width: 500px !important;
}

</style>


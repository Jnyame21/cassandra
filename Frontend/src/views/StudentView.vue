<script setup lang="ts">
import { useUserAuthStore } from '@/stores/userAuthStore'
import { useElementsStore } from '@/stores/elementsStore'
import { onBeforeMount, ref } from 'vue'
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
const rozmachAuth: any = ref(null)

onBeforeMount(()=>{
  elementsStore.activePage = 'StudentClassStudents'
  rozmachAuth.value = localStorage.getItem('RozmachAuth')
  if (rozmachAuth.value){
    rozmachAuth.value = JSON.parse(rozmachAuth.value)
  }
})

const hidOverlay = ()=>{
  const overlay = document.getElementById('welcome')
  if (overlay){
    if (rozmachAuth.value && !rozmachAuth.value.last_login){
      rozmachAuth.value.last_login = true
      localStorage.setItem('RozmachAuth', JSON.stringify(rozmachAuth.value))
    }
    overlay.style.display = 'none'
  }
}


</script>


<template>
    <!-- Welcome Overlay-->
  <div id="welcome" class="overlay welcome-overlay" v-if="rozmachAuth && !rozmachAuth['last_login'] && userAuthStore.userData">
    <v-card class="flex-all-c card">
      <v-card-title id="company-name">{{userAuthStore.userData['school']['name']}}</v-card-title>
      <v-card-text style="font-size: .9rem; font-family: sans-serif; text-align: left; line-height: 1.2">
        <p style="text-align: center">Welcome <strong>{{userAuthStore.userData['first_name']+' '+userAuthStore.userData['last_name']}}!</strong></p>
        <p>We're excited to have you here. This is your special place to find everything you need for a successful school year.
        Explore your subjects, get to know your teachers and classmates, and discover valuable resources to help you thrive in your studies.</p>
        <p>If you face any problem here, go to the help tab and make a submission. We're here for you {{userAuthStore.userData['first_name']}}!</p>
      </v-card-text>
      <v-card-actions class="flex-all">
        <v-btn class="overlay-btn" elevation="4" @click="hidOverlay()">OK</v-btn>
      </v-card-actions>
    </v-card>
  </div>
  <TheHeader v-if="userAuthStore.userData"/>
  <main class="main" v-if="userAuthStore.userData">
    <StudentNavContainerMob v-if="!elementsStore.onDesk"/>
    <StudentNavContainerDesk v-if="elementsStore.onDesk"/>
    <div class="pages-container">
      <div class="component-wrapper" :class="{ 'is-active-component': elementsStore.activePage === 'StudentClassStudents' }">
        <StudentClassStudents v-show="elementsStore.activePage === 'StudentClassStudents'" />
      </div>
      <div class="component-wrapper" v-if="userAuthStore.studentData.results" :class="{ 'is-active-component': elementsStore.activePage.split(',')[0] === 'StudentResults' }">
        <div v-for="[year_name, year_result_data] in Object.entries(userAuthStore.studentData.results )" :key="year_name">
          <StudentResults v-show="elementsStore.activePage.split(',')[0] === 'StudentResults'" v-for="term_name in Object.keys(year_result_data)"
          :key="term_name"
          :yearName="year_name"
          :termName="term_name"
          />
        </div>
      </div>
      <div class="component-wrapper" v-if="userAuthStore.studentData.attendances" :class="{ 'is-active-component': elementsStore.activePage.split(',')[0] === 'StudentAttendance' }">
        <div v-for="[year_name, year_attendance_data] in Object.entries(userAuthStore.studentData.attendances)" :key="year_name">
          <StudentAttendance v-show="elementsStore.activePage.split(',')[0] === 'StudentAttendance'" v-for="term_name in Object.keys(year_attendance_data)"
          :key="term_name"
          :yearName="year_name"
          :termName="term_name"
          />
        </div>
      </div>
      <div class="component-wrapper" v-if="userAuthStore.studentData.assessments" :class="{ 'is-active-component': elementsStore.activePage.split(',')[0] === 'StudentAssessments' }">
        <div v-for="[year_name, year_assessment_data] in Object.entries(userAuthStore.studentData.assessments )" :key="year_name">
          <StudentAssessments v-show="elementsStore.activePage.split(',')[0] === 'StudentAssessments'" v-for="term_name in Object.keys(year_assessment_data)"
          :key="term_name"
          :yearName="year_name"
          :termName="term_name"
          />
        </div>
      </div>
      <div class="component-wrapper" v-if="userAuthStore.studentData.exams" :class="{ 'is-active-component': elementsStore.activePage.split(',')[0] === 'StudentExams' }">
        <div v-for="[year_name, year_exam_data] in Object.entries(userAuthStore.studentData.exams )" :key="year_name">
          <StudentExams v-show="elementsStore.activePage.split(',')[0] === 'StudentExams'" v-for="term_name in Object.keys(year_exam_data)"
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

.welcome-overlay{
  display: flex;
  position: absolute;
  align-items: center;
  justify-content: center;
  height: 100%;
  z-index: 10;
  width: 100%;
  background-color: rgba(0,0,0,0.5);
}
.card{
  width: 80%;
}
.nav-container{
  width: 400px;
  background-color: red;
}
#company-name{
  font-size: .7rem;
  font-family: Verdana, "sans-serif";
  text-align: center;
  font-weight: bold;
  text-transform: uppercase;
  color: #007bff;
}
.overlay-btn{
  background-color: mediumseagreen;
  color: yellow;
}
.overlay-btn:hover{
  background-color: lightseagreen;
  color: white;
}



</style>


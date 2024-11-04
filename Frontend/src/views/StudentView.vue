<script setup lang="ts">

definePageMeta({
  middleware: ['check-student']
})

useHead({
  meta: [
    {name: "robots", content: "no-index"}
  ],
})

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()
const rozmachAuth: any = ref(null)

onBeforeUnmount(()=>{
  document.body.style.overflow = 'auto'
})

onBeforeMount(()=>{
  document.body.style.overflow = 'hidden'
  document.title = "Cassandra"
  elementsStore.activePage = 'StudentSubjects'
  rozmachAuth.value = localStorage.getItem('RozmachAuth')
  if (rozmachAuth.value){
    rozmachAuth.value = JSON.parse(rozmachAuth.value)
  }
})

watch(()=>elementsStore.activePage, (newValue, oldValue)=>{
  if (newValue.split(',')[0] === 'StudentResults'){
    const year_results = userAuthStore.studentData.academicYearsData.find(item => item['name'] === newValue.split(',')[1])
    if (year_results && newValue.split(',')[3] === '1'){
      userAuthStore.studentData.currentResults = year_results['results']['term_one']
    }
    else if (year_results && newValue.split(',')[3] === '2'){
      userAuthStore.studentData.currentResults = year_results['results']['term_two']
    }
    else if (year_results && newValue.split(',')[3] === '3'){
      userAuthStore.studentData.currentResults = year_results['results']['term_three']
    }
  }
  else if (newValue.split(',')[0] === 'StudentAttendance'){
    const year_attendance = userAuthStore.studentData.academicYearsData.find(item => item['name'] === newValue.split(',')[1])
    if (year_attendance && newValue.split(',')[3] === '1'){
      userAuthStore.studentData.currentAttendance = year_attendance['attendance']['term_one']
    }
    else if (year_attendance && newValue.split(',')[3] === '2'){
      userAuthStore.studentData.currentAttendance = year_attendance['attendance']['term_two']
    }
    else if (year_attendance && newValue.split(',')[3] === '3'){
      userAuthStore.studentData.currentAttendance = year_attendance['attendance']['term_three']
    }
  }
  else if (newValue.split(',')[0] === 'StudentAssessments'){
    const year_assessments = userAuthStore.studentData.academicYearsData.find(item => item['name'] === newValue.split(',')[1])
    if (year_assessments && newValue.split(',')[3] === '1'){
      userAuthStore.studentData.currentAssessments = year_assessments['assessments']['term_one']
    }
    else if (year_assessments && newValue.split(',')[3] === '2'){
      userAuthStore.studentData.currentAssessments = year_assessments['assessments']['term_two']
    }
    else if (year_assessments && newValue.split(',')[3] === '3'){
      userAuthStore.studentData.currentAssessments = year_assessments['assessments']['term_three']
    }
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
  <div id="welcome" class="welcome-overlay" v-if="rozmachAuth && !rozmachAuth['last_login'] && userAuthStore.userData">
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
  <TheHeader  v-if="userAuthStore.userData"/>
  <main class="main" v-if="userAuthStore.userData">
    <StudentNavContainerMob v-if="!elementsStore.navDrawer"/>
    <StudentNavContainerDesk v-if="elementsStore.navDrawer"/>
    <div class="pages-container">
      <StudentSubjects v-show="elementsStore.activePage === 'StudentSubjects' " />
      <StudentClassStudents v-show="elementsStore.activePage === 'StudentClassStudents' " />
      <StudentResults v-show="elementsStore.activePage.split(',')[0] === 'StudentResults' " />
      <StudentAttendance v-show="elementsStore.activePage.split(',')[0] === 'StudentAttendance' " />
      <StudentAssessments v-show="elementsStore.activePage.split(',')[0] === 'StudentAssessments' " />
      <StudentTranscript v-show="elementsStore.activePage.split(',')[0] === 'StudentTranscript' " />
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


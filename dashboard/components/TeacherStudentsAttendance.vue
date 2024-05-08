<script setup lang="ts">
import {ref } from "vue";


const sectionPage = ref('section1')
const userAuthStore = useUserAuthStore()


const changeSection = (term: string)=>{
  sectionPage.value = term
}



</script>

<template>
  <div class="subsections-container">
    <TheLoader v-if="!userAuthStore.teacherStudentsAttendance" />
    <NoData v-if="userAuthStore.teacherStudentsAttendance && userAuthStore.teacherStudentsAttendance.length === 0" :message="'You have not uploaded any attendance yet'"/>

    <div v-if="userAuthStore.teacherStudentsAttendance" class="subsection-nav-container">
      <button v-for="(assign, index) in userAuthStore.teacherStudentsAttendance" :key="index" class="nav-btn-1" 
      @click="changeSection(`section${index+1}`)" :class="{'nav-btn-1-active': sectionPage===`section${index+1}`}"
      >
      <p>{{ assign['class_name'] }} FORM {{ assign['students_year'] }}</p>
      <p>{{assign['subject']}}</p>
      </button>
    </div>
  
    <div v-if="userAuthStore.teacherStudentsAttendance" class="subsections">
      <div v-for="(assign, index) in userAuthStore.teacherStudentsAttendance" :key="index" :style="sectionPage===`section${index+1}` ? {'display': 'flex'}: {'display': 'none'}">
        <TeacherStudentsAllSubjecstAttendance :attendance="assign['attendance']" :index="index" :key="assign['attendance']"
        v-if="assign['attendance'] && assign['attendance'].length > 0"
        />
        <NoData v-if="assign['attendance'] && assign['attendance'].length === 0" :message="'No data yet'"/>
      </div>
    </div>
  </div>
</template>

<style scoped>

.subsections{
  height: 85% !important;
}
.subsection-nav-container{
  height: 15% !important;
  justify-content: flex-start !important;
}

.nav-btn-1{
  font-size: .5rem !important;
  min-width: 300px !important;
}

@media screen and (min-width: 576px) {
  .nav-btn-1{
    margin: 0 1.5em !important;
    font-size: .55rem !important;
  }
}

@media screen and (min-width: 767px) {

  .nav-btn-1{
    margin: 0 2em !important;
    font-size: .55rem !important;
  }
}

@media screen and (min-width: 1200px) {
  .subsection-nav-container{
    justify-content: center !important;
  }
}

@media screen and (min-width: 2000px) {
  
  .nav-btn-1{
    margin: 0 3em !important;
  }
}


</style>
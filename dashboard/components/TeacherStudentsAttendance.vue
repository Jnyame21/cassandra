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
      <span>{{ assign['class_name'] }} {{assign['subject']}}</span>
      <span>FORM {{ assign['students_year'] }}</span>
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

.nav-btn-1{
  font-size: .5rem !important;
}

@media screen and (min-width: 576px) {
  .nav-btn-1{
    margin: 0 1.5em !important;
  }
}

@media screen and (min-width: 767px) {
  .nav-btn-1{
    margin: 0 2em !important;
    font-size: .6rem !important;
  }
}

@media screen and (min-width: 991px) {
  .nav-btn-1{
    margin: 0 3em !important;
    font-size: .65rem !important;
  }
}


</style>
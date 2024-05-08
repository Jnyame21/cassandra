<script setup lang="ts">
import {ref, watch } from "vue";


const sectionPage = ref('section1')
const userAuthStore = useUserAuthStore()


const changeSection = (term: string)=>{
  sectionPage.value = term
}

const resultData: any = ref(null)

watch(()=> userAuthStore.staffStudentResultsEdit, (newValue, oldValue)=>{
    if (newValue){
      resultData.value = newValue
    }
}, {deep: true, immediate: true})


</script>

<template>
  <div class="sections-container">
    <TheLoader v-if="!resultData" />

    <div v-if="resultData" class="section-nav-container">
      <button v-for="(resultsAssign, index) in resultData" :key="index" class="nav-btn-1" 
      @click="changeSection(`section${index+1}`)" :class="{'nav-btn-1-active': sectionPage===`section${index+1}`}"
      >
      <p class="subject-name">{{ resultsAssign['class_name'] }} FORM {{ resultsAssign['students_year'] }}</p>
      <p>{{resultsAssign['subject']}}</p>
      </button>
    </div>
  
    <div v-if="resultData" class="sections">
      <div v-for="(resultsAssign, index) in resultData" :key="index" :style="sectionPage===`section${index+1}` ? {'display': 'flex'}: {'display': 'none'}">
        <TeacherAnalyticsStatistics :studentsData="resultsAssign['students']" :key="resultsAssign['students']"
        v-if="resultsAssign['students'] && resultsAssign['students'].length > 0"
        />
        <NoData v-if="resultsAssign['students'] && resultsAssign['students'].length === 0" :message="'You have not uploaded results for students under this subject yet'"/>
      </div>
    </div>
  </div>
</template>

<style scoped>

.sections{
  height: 85% !important;
}
.section-nav-container{
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
    font-size: .6rem !important;
  }
}

@media screen and (min-width: 1200px) {
  .section-nav-container{
    justify-content: center !important;
  }
  
}

@media screen and (min-width: 2000px) {
  
  .nav-btn-1{
    margin: 0 3em !important;
  }
}


</style>
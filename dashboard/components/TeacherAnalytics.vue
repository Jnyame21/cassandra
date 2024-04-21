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
      <span>{{ resultsAssign['class_name'] }} {{resultsAssign['subject']}}</span>
      <span>FORM {{ resultsAssign['students_year'] }}</span>
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
}

.nav-btn-1{
  font-size: .45rem !important;
}

@media screen and (min-width: 576px) {
  .nav-btn-1{
    margin: 0 1.5em !important;
    font-size: .5rem !important;
  }
}

@media screen and (min-width: 767px) {
  .nav-btn-1{
    margin: 0 2em !important;
    font-size: .55rem !important;
  }
}

@media screen and (min-width: 991px) {
  .nav-btn-1{
    margin: 0 3em !important;
    font-size: .6rem !important;
  }
}

@media screen and (min-width: 1200px) {
  .nav-btn-1{
    font-size: .65rem !important;
  }
}

@media screen and (min-width: 2600px) {
  .nav-btn-1{
    font-size: .7rem !important;
  }
}

@media screen and (min-width: 3600px) {
  .nav-btn-1{
    font-size: .75rem !important;
  }
}

</style>
<script setup lang="ts">
import {ref} from "vue";

const sectionPage = ref('section1')
const userAuthStore = useUserAuthStore()


const changeSection = (term: string)=>{
  sectionPage.value = term
}


</script>

<template>
  <div class="sections-container">
    <TheLoader v-if="!userAuthStore.headStudentsPerformance" />

    <div v-if="userAuthStore.headStudentsPerformance" class="section-nav-container">
      <button v-for="(department, index) in userAuthStore.headStudentsPerformance" :key="index" class="nav-btn-1" 
      @click="changeSection(`section${index+1}`)" :class="{'nav-btn-1-active': sectionPage===`section${index+1}`}"
      >
      <v-icon icon="mdi-function-variant" v-if="department['department'] === 'MATHEMATICS' "/>
      <v-icon icon="mdi-book-open-variant" v-if="department['department'] === 'ENGLISH' "/>
      <v-icon icon="mdi-book-open-variant" v-if="department['department'] === 'LANGUAGES' "/>
      <v-icon icon="mdi-history" v-if="department['department'] === 'ARTS' "/>
      <v-icon icon="mdi-flask" v-if="department['department'] === 'SCIENCE' "/>
      <v-icon icon="mdi-finance" v-if="department['department'] === 'BUSINESS' "/>
      <v-icon icon="mdi-finance" v-if="department['department'] === 'ECONOMICS' "/>
      <span>{{department['department']}}</span>
    </button>
    </div>
  
    <div v-if="userAuthStore.headStudentsPerformance"  class="sections">
      <div class="h-100" v-for="(department, index) in userAuthStore.headStudentsPerformance" :key="index" :style="sectionPage===`section${index+1}` ? {'display': 'flex'}: {'display': 'none'}">
        <HeadPerformanceSubjects :department="department" />
      </div>
    </div>
  </div>
</template>

<style scoped>

.section-nav-container{
  justify-content: flex-start !important;
}

@media screen and (min-width: 576px) {
  .nav-btn-1{
    margin: 0em 1em !important;
    font-size: .6rem !important;
  }
}

@media screen and (min-width: 767px) {
  .section-nav-container{
    justify-content: center !important;
  }

  .nav-btn-1{
    margin: 0em 1.5em !important;
    font-size: .6rem !important;
  }
}

@media screen and (min-width: 991px) {
  .nav-btn-1{
    margin: 0em 2em !important;
    font-size: .7rem !important;
  }
}

@media screen and (min-width: 2000px) {
  .nav-btn-1{
    margin: 0em 3em !important;
    font-size: .7rem !important;
  }
}


</style>
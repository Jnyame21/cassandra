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
    <TheLoader v-if="!userAuthStore.hodPerformance" />

    <div v-if="userAuthStore.hodPerformance" class="section-nav-container">
      <button v-for="(subject, index) in userAuthStore.hodPerformance" :key="index" class="nav-btn-1" 
      @click="changeSection(`section${index+1}`)" :class="{'nav-btn-1-active': sectionPage===`section${index+1}`}"
      >
      <v-icon icon="mdi-calculator-variant" v-if="subject['subject']==='CORE MATHEMATICS' "/>
      <v-icon icon="mdi-function-variant" v-if="subject['subject']==='ELECTIVE MATHEMATICS' "/>
      <v-icon icon="mdi-microscope" v-if="subject['subject']==='BIOLOGY' "/>
      <v-icon icon="mdi-flask" v-if="subject['subject']==='CHEMISTRY' "/>
      <v-icon icon="mdi-currency-usd" v-if="subject['subject']==='FINANCIAL ACCOUNTING' "/>
      <v-icon icon="mdi-chart-bar" v-if="subject['subject']==='BUSINESS MANAGEMENT' "/>
      <v-icon icon="mdi-book-open-variant" v-if="subject['subject']==='ENGLISH LANGUAGE' "/>
      <v-icon icon="mdi-account-group" v-if="subject['subject']==='SOCIAL STUDIES' "/>
      <v-icon icon="mdi-scale" v-if="subject['subject']==='INTEGRATED SCIENCE' "/>
      <v-icon icon="mdi-book-cross" v-if="subject['subject']==='CHRISTIAN RELIGIOUS STUDIES (CRS)' "/>
      <v-icon icon="mdi-library" v-if="subject['subject']==='LITERATURE' "/>
      <v-icon icon="mdi-history" v-if="subject['subject']==='HISTORY' "/>
      <v-icon icon="mdi-briefcase-account" v-if="subject['subject']==='GOVERNMENT' "/>
      <v-icon icon="mdi-earth" v-if="subject['subject']==='GEOGRAPHY' "/>
      <v-icon icon="mdi-atom" v-if="subject['subject']==='PHYSICS' "/>
      <v-icon icon="mdi-desktop-tower-monitor" v-if="subject['subject']==='ELECTIVE ICT' "/>
      <v-icon icon="mdi-cash-register" v-if="subject['subject']==='COST ACCOUNTING' "/>
      <v-icon icon="mdi-finance" v-if="subject['subject']==='ECONOMICS' "/>
      <span>{{subject['subject']}}</span>
    </button>
    </div>
  
    <div v-if="userAuthStore.hodPerformance"  class="sections">
      <div class="h-100" v-for="(subject, index) in userAuthStore.hodPerformance" :key="index" :style="sectionPage===`section${index+1}` ? {'display': 'flex'}: {'display': 'none'}">
        <HodPerformanceSubject :data="subject" :key="subject"/>
      </div>
    </div>
  </div>
</template>

<style scoped>



@media screen and (min-width: 576px) {
  .nav-btn-1{
    font-size: .55rem !important;
    margin: 0 2em !important;
  }
}

@media screen and (min-width: 767px) {
  .nav-btn-1{
    font-size: .6rem !important;
    margin: 0 3em !important;
  }
}


</style>
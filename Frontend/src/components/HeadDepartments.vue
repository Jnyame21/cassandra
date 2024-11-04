<script setup lang="ts">
import {ref } from "vue";

const sectionPage = ref('section1')
const userAuthStore = useUserAuthStore()


const changeSection = (term: string)=>{
  sectionPage.value = term
}


</script>

<template>
  <div class="sections-container">
    <TheLoader class="no-data" v-if="!userAuthStore.headDepartments" />
    <NoData :message="'No data yet'" v-if="userAuthStore.headDepartments && userAuthStore.headDepartments.length ===0 "/>

    <div v-if="userAuthStore.headDepartments && userAuthStore.headDepartments.length >0 " class="section-nav-container">
      <button v-for="(department, index) in userAuthStore.headDepartments" :key="index" class="nav-btn-1" 
      @click="changeSection(`section${index+1}`)" :class="{'nav-btn-1-active': sectionPage===`section${index+1}`}"
      ><v-icon icon="mdi-function-variant" v-if="department['department']['name'] === 'MATHEMATICS' "/>
      <v-icon icon="mdi-book-open-variant" v-if="department['department']['name'] === 'ENGLISH' "/>
      <v-icon icon="mdi-book-open-variant" v-if="department['department']['name'] === 'LANGUAGES' "/>
      <v-icon icon="mdi-history" v-if="department['department']['name'] === 'ARTS' "/>
      <v-icon icon="mdi-flask" v-if="department['department']['name'] === 'SCIENCE' "/>
      <v-icon icon="mdi-finance" v-if="department['department']['name'] === 'BUSINESS' "/>
      <span>{{department['department']['name']}}</span>
    </button>
    </div>
  
    <div v-if="userAuthStore.headDepartments && userAuthStore.headDepartments.length >0 "  class="sections">
      <div class="h-100" v-for="(department, index) in userAuthStore.headDepartments" :key="index" :style="sectionPage===`section${index+1}` ? {'display': 'flex'}: {'display': 'none'}">
        <HeadDepartmentPage :department="department"/>
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
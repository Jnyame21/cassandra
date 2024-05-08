<script setup lang="ts">
import {ref} from "vue";


const sectionPage = ref('section1')

const props = defineProps({
    department: null,
})

const changeSection = (term: string)=>{
  sectionPage.value = term
}


</script>

<template>
  <div class="subsections-container">
    <TheLoader v-if="!props.department" />

    <div v-if="props.department" class="subsection-nav-container">
      <button v-for="(subject, index) in props.department['subjects']" :key="index" class="nav-btn-1" 
      @click="changeSection(`section${index+1}`)" :class="{'nav-btn-1-active': sectionPage===`section${index+1}`}"
      >
      <!-- <v-icon icon="mdi-function-variant" v-if="department['department'] === 'MATHEMATICS' "/>
      <v-icon icon="mdi-book-open-variant" v-if="department['department'] === 'ENGLISH' "/>
      <v-icon icon="mdi-book-open-variant" v-if="department['department'] === 'LANGUAGES' "/>
      <v-icon icon="mdi-history" v-if="department['department'] === 'ARTS' "/>
      <v-icon icon="mdi-flask" v-if="department['department'] === 'SCIENCE' "/>
      <v-icon icon="mdi-finance" v-if="department['department'] === 'BUSINESS' "/>
      <v-icon icon="mdi-finance" v-if="department['department'] === 'ECONOMICS' "/> -->
      <span>{{subject['name']}}</span>
    </button>
    </div>
  
    <div v-if="props.department"  class="subsections">
      <div class="h-100" v-for="(subject, index) in props.department['subjects']" :key="index" :style="sectionPage===`section${index+1}` ? {'display': 'flex'}: {'display': 'none'}">
        <HeadPerformanceYear :year="subject" />
      </div>
    </div>
  </div>
</template>

<style scoped>

.subsection-nav-container{
  justify-content: flex-start !important;
}

@media screen and (min-width: 576px) {
  .nav-btn-1{
    margin: 0em 1.5em !important;
    font-size: .6rem !important;
  }
}

@media screen and (min-width: 767px) {
  .subsection-nav-container{
    justify-content: center !important;
  }
  .nav-btn-1{
    margin: 0em 2em !important;
    font-size: .6rem !important;
  }
}

@media screen and (min-width: 991px) {
  .nav-btn-1{
    margin: 0em 2em !important;
    font-size: .7rem !important;
  }
}


</style>
<script setup lang="ts">
import {ref} from "vue";

interface Props{
  data: {
    year_one: {
      term_one: [];
      term_two: [];
      term_three: [];
    };
    year_two: {
      term_one: [];
      term_two: [];
      term_three: [];
    };
    year_three: {
      term_one: [];
      term_two: [];
      term_three: [];
    };
  }
}

const { data } = defineProps<Props>()

const sectionPage = ref('section1')

const changeSection = (term: string)=>{
  sectionPage.value = term
}


</script>

<template>
  <div class="subsections-container">
    
    <v-sheet class="subsection-nav-container" elevation="0">
      <button class="nav-btn-2" @click="changeSection('section1')" :class="{'nav-btn-2-active': sectionPage==='section1'}">Form 1 students</button>
      <button class="nav-btn-2" @click="changeSection('section2')" :class="{'nav-btn-2-active': sectionPage==='section2'}">Form 2 students</button>
      <button class="nav-btn-2" @click="changeSection('section3')" :class="{'nav-btn-2-active': sectionPage==='section3'}">Form 3 students</button>
    </v-sheet>
  
    <div class="subsections">
      <div :style="sectionPage==='section1' ? {'display': 'flex'}: {'display': 'none'}">
        <HodYearPerformance :year="data['year_one']" />
      </div>
      <div :style="sectionPage==='section2' ? {'display': 'flex'}: {'display': 'none'}">
        <HodYearPerformance :year="data['year_two']" />
      </div>
      <div :style="sectionPage==='section3' ? {'display': 'flex'}: {'display': 'none'}">
        <HodYearPerformance :year="data['year_three']" />
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>


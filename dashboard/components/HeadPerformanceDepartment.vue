<script setup lang="ts">
import {ref} from "vue";


const props = defineProps({
    data: null,
})

const sectionPage = ref('section1')

const changeSection = (term: string)=>{
  sectionPage.value = term
}


</script>

<template>
  <div class="subsections-container">
    <v-sheet class="subsection-nav-container" elevation="0">
      <button class="nav-btn-2" @click="changeSection('section1')" :class="{'nav-btn-2-active': sectionPage==='section1'}">form 1 students</button>
      <button class="nav-btn-2" @click="changeSection('section2')" :class="{'nav-btn-2-active': sectionPage==='section2'}">form 2 students</button>
      <button class="nav-btn-2" @click="changeSection('section3')" :class="{'nav-btn-2-active': sectionPage==='section3'}">form 3 students</button>
    </v-sheet>
  
    <div class="subsections">
      <div :style="sectionPage==='section1' ? {'display': 'flex'}: {'display': 'none'}">
        <HeadYearPerformance :year="props.data['year_one']" />
      </div>
      <div :style="sectionPage==='section2' ? {'display': 'flex'}: {'display': 'none'}">
        <HeadYearPerformance :year="props.data['year_two']" />
      </div>
      <div :style="sectionPage==='section3' ? {'display': 'flex'}: {'display': 'none'}">
        <HeadYearPerformance :year="props.data['year_three']" />
      </div>
    </div>
  </div>
</template>

<style scoped>


</style>


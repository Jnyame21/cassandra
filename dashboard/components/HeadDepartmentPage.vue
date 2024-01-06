<script setup lang="ts">
import {ref} from "vue";


const props = defineProps({
  department: null
})

const sectionPage = ref('section1')

const changeSection = (term: string)=>{
  sectionPage.value = term
}


</script>

<template>
  <div class="subsections-container">
    <div class="subsection-nav-container">
      <button class="nav-btn-1 btn-1" @click="changeSection('section1')" :class="{'nav-btn-1-active': sectionPage==='section1'}">
        <v-icon icon="mdi-account"/>
        TEACHERS PROFILE
      </button>
      <button class="nav-btn-1 btn-2" @click="changeSection('section2')" :class="{'nav-btn-1-active': sectionPage==='section2'}">
        <v-icon icon="mdi-book-open-outline"/>
        TEACHERS COURSEWORK
      </button>
    </div>
  
    <div class="subsections">
      <div :style="sectionPage==='section1' ? {'display': 'flex'}: {'display': 'none'}">
        <HeadDepartmentStaffProfile :staff="props.department['department']['teachers']" />
      </div>
      <div class="h-100" :style="sectionPage==='section2' ? {'display': 'flex'}: {'display': 'none'}">
        <HeadDepartmentsCourseAssignment :subjectAssignment="props.department['subject_assignments']" />
      </div>
    </div>
  </div>
</template>

<style scoped>

@media screen and (min-width: 576px) {
  .btn-1{
    margin-right: 2em !important;
  }
  .btn-2{
    margin-left: 2em !important;
  }
}


@media screen and (min-width: 767px) {
  .btn-1{
    margin-right: 3em !important;
  }
  .btn-2{
    margin-left: 3em !important;
  }
}


</style>


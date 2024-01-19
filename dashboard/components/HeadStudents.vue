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
    <TheLoader v-if="!userAuthStore.headPrograms" />
    <NoData :message="'No data yet'"  v-if="userAuthStore.headPrograms && userAuthStore.headPrograms.length === 0" />
    <v-sheet v-if="userAuthStore.headPrograms && userAuthStore.headPrograms.length > 0" class="section-nav-container" elevation="0">
      <button v-for="(program, index) in userAuthStore.headPrograms" :key="index" class="nav-btn-2 btn-1" @click="changeSection(`section${index + 1}`)" :class="{'nav-btn-2-active': sectionPage===`section${index + 1}`}">
        <v-icon icon="mdi-function-variant" v-if="program['name'] === 'AGRICULTURAL SCIENCE' "/>
        <v-icon icon="mdi-book-open-variant" v-if="program['name'] === 'VISUAL ARTS' "/>
        <v-icon icon="mdi-history" v-if="program['name'] === 'GENERAL ARTS' "/>
        <v-icon icon="mdi-flask" v-if="program['name'] === 'GENERAL SCIENCE' "/>
        <v-icon icon="mdi-finance" v-if="program['name'] === 'BUSINESS' "/>
        <v-icon icon="mdi-finance" v-if="program['name'] === 'HOME ECONOMICS' "/>
        {{ program['name'] }}
      </button>
    </v-sheet>
  
    <div class="sections"  v-if="userAuthStore.headPrograms && userAuthStore.headPrograms.length > 0">
      <div class="w-100 h-100" :style="sectionPage===`section${index + 1}` ? {'display': 'flex'}: {'display': 'none'}"
      v-for="(program, index) in userAuthStore.headPrograms" :key="index"
      >
        <HeadStudentsProgram :program="program"/>
      </div>
    </div>
  </div>
</template>

<style scoped>

@media screen and (min-width: 576px) {
  .btn-1{
    margin: 0em 2em !important;
    font-size: .6rem !important;
  }
}

@media screen and (min-width: 767px) {
  .btn-1{
    font-size: .65rem !important;
  }
}

@media screen and (min-width: 991px) {
  .btn-1{
    font-size: .7rem !important;
  }
}


</style>


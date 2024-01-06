<script setup lang="ts">
import {ref} from "vue";



const userAuthStore = useUserAuthStore()
const sectionPage = ref(userAuthStore.activeTerm)

const changeSection = (term: number)=>{
  sectionPage.value = term
}


</script>

<template>
  <div class="subsections-container">
    <div class="subsection-nav-container flex-all">
        <button class="nav-btn-2 btn-1" @click="changeSection(1)" :class="{'nav-btn-2-active': sectionPage===1}">SEMESTER 1</button>
        <button class="nav-btn-2 btn-2" @click="changeSection(2)" :class="{'nav-btn-2-active': sectionPage===2}">SEMESTER 2</button>
        <button v-if="userAuthStore.userData && userAuthStore.userData['academic_year']['sem_3_start_date']" class="nav-btn-2 btn-3" @click="changeSection(3)" :class="{'nav-btn-2-active': sectionPage===3}">SEMESTER 3</button>
    </div>
    
      <div class="subsections">
        <div :style="sectionPage===1 ? {'display': 'flex'}: {'display': 'none'}">
          <HodTermSubjectAssignment :data="'termOne'" :term="1" :term-number="1" />
        </div>
        <div :style="sectionPage===2 ? {'display': 'flex'}: {'display': 'none'}">
          <HodTermSubjectAssignment :data="'termTwo'" :term="2" :term-number="2" />
        </div>
        <div :style="sectionPage===3 ? {'display': 'flex'}: {'display': 'none'}"
        v-if="userAuthStore.userData && userAuthStore.userData['academic_year']['sem_3_start_date']"
        >
          <HodTermSubjectAssignment :data="'termThree'" :term="3" :term-number="3" />
        </div>
      </div>
  </div>
</template>

<style scoped>

@media screen and (min-width: 576px) {
  .nav-btn-2{
    font-size: .65rem !important;
  }
  .btn-1{
    margin-right: 2em !important;
  }
  .btn-2{
    margin-left: 2em !important;
  }
  .btn-3{
    margin-left: 2em !important;
  }
}

@media screen and (min-width: 767px) {
  .nav-btn-2{
    font-size: .7rem !important;
  }
  .btn-1{
    margin-right: 3em !important;
  }
  .btn-2{
    margin-left: 3em !important;
  }
  .btn-3{
    margin-left: 3em !important;
  }
}

</style>




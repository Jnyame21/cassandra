<script setup lang="ts">
import {ref} from "vue";


const sectionPage = ref('section1')
const userAuthStore = useUserAuthStore()

const changeSection = (term: string)=>{
  sectionPage.value = term
}


</script>

<template>
  <div class="subsections-container">
    
    <TheLoader class="no-data" v-if="!userAuthStore.adminStaff.departments || userAuthStore.adminStaff.departments && userAuthStore.adminStaff.departments.length ===0 " />

    <div v-if="userAuthStore.adminStaff.departments && userAuthStore.adminStaff.departments.length >0 " class="subsection-nav-container">
      <button v-for="(department, index) in userAuthStore.adminStaff.departments" :key="index" class="nav-btn-1" 
      @click="changeSection(`section${index+1}`)" :class="{'nav-btn-1-active': sectionPage===`section${index+1}`}"
      ><span>{{department['name']}}</span>
    </button>
    </div>
  
    <div v-if="userAuthStore.adminStaff.departments && userAuthStore.adminStaff.departments.length >0 "  class="sections">
      <div class="h-100" v-for="(department, index) in userAuthStore.adminStaff.departments" :key="index" :style="sectionPage===`section${index+1}` ? {'display': 'flex'}: {'display': 'none'}">
        <AdminDepartmentStaff :staff="department['teachers']" :overlayIndex="index"/>
      </div>
    </div>
  </div>
</template>

<style scoped>

.subsection-nav-container{
  justify-content: flex-start !important;
}

@media screen and (min-width: 767px) {
  .subsection-nav-container{
    justify-content: center !important;
  }
  .nav-btn-1{
    margin: 0em 2em !important;
  }
}
@media screen and (min-width: 991px) {

  .nav-btn-1{
    margin: 0em 3em !important;
  }
}
@media screen and (min-width: 2000px) {

  .nav-btn-1{
    margin: 0em 4em !important;
  }
}


</style>


<script setup lang="ts">
import {ref} from "vue";


const userAuthStore = useUserAuthStore()
const sectionPage = ref('section1')

const changeSection = (term: string)=>{
  sectionPage.value = term
}


</script>

<template>
<div class="overlay">
  <v-sheet class="sheet" elevation="0" style="position: relative">
    <div class="nav-container mb-4 flex-all">
      <button class="nav-btn-1" @click="changeSection('section1')" :class="{'nav-btn-1-active': sectionPage==='section1'}"
      v-if="userAuthStore.userData && userAuthStore.userData['role'] && userAuthStore.userData['staff_role'] !== 'student'"
      >SEND A NOTICE
      </button>
      
      
      <button class="nav-btn-1" @click="changeSection('section2')" :class="{'nav-btn-1-active': sectionPage==='section2'}"
      v-if="userAuthStore.userData && userAuthStore.userData['role']"
      >ALL NOTIFICATIONS
      </button>
    </div>
    
    <div class="sections-container">
      <div :style="sectionPage==='section1' ? {'display': 'flex'}: {'display': 'none'}">
        <SendNotice />
      </div>

      <div :style="sectionPage==='section2' ? {'display': 'flex'}: {'display': 'none'}">
        <AllNotifications />
      </div>
    </div>
  
  </v-sheet>
</div>
  
</template>

<style scoped>

.overlay{
  position: absolute;
  background: rgba(0, 0, 0, .5);
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  z-index: 5;
  align-items: center;
  justify-content: center;
}

.sheet{
  background-color: white;
  width: 90%;
  height: 95%;
  border-radius: .5em;
  overflow-y: hidden;
  max-width: 1200px !important;
}

.sections-container{
  width: 100%;
  height: 100%;
}

.nav-container{
  width: 100%;
  display: flex;
  margin-top: 1em;
  flex-wrap: wrap;
}

.nav-btn{
  margin: 1em 1em;
  margin-top: 0;
}

@media screen and (min-width: 576px) {
  .nav-btn{
    font-size: .8rem;
  }
}

</style>




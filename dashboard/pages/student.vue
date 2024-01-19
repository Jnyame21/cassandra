<script setup lang="ts">

definePageMeta({
    middleware: ['check-student']
})

useHead({
  meta: [
    {name: "robots", content: "no-index"}
  ],
})


const userAuthStore = useUserAuthStore()
const rozmachAuth: any = ref(null)
const activePage = ref('page1')

onBeforeUnmount(()=>{
  document.body.style.overflow = 'auto'
})

onBeforeMount(()=>{
  if (userAuthStore.isAuthenticated){
    document.title = "EduAAP"
  }
  
  document.body.style.overflow = 'hidden'
  rozmachAuth.value = localStorage.getItem('RozmachAuth')
  if (rozmachAuth.value){
    rozmachAuth.value = JSON.parse(rozmachAuth.value)
  }

})


const hidOverlay = ()=>{
  const overlay = document.getElementById('welcome')
  if (overlay){
    if (rozmachAuth.value && !rozmachAuth.value.last_login){
      rozmachAuth.value.last_login = true
      localStorage.setItem('RozmachAuth', JSON.stringify(rozmachAuth.value))
    }
    overlay.style.display = 'none'

  }
}


const changePage = (page: string)=>{

  activePage.value = page

}



</script>

<template>
    <!-- Welcome Overlay-->
  <div id="welcome" class="welcome-overlay" v-if="rozmachAuth && !rozmachAuth['last_login'] && userAuthStore.userData">
    <v-card class="flex-all-c card">
      <v-card-title id="company-name">Rozmach</v-card-title>
      <v-card-text style="font-size: .9rem; font-family: sans-serif; text-align: left; line-height: 1.2">
        <p style="text-align: center">Welcome <strong>{{userAuthStore.userData['first_name']+' '+userAuthStore.userData['last_name']}}!</strong></p>
        <p>We're excited to have you here. This is your special place to find everything you need for a successful school year.
        Explore your subjects, get to know your teachers and classmates, and discover valuable resources to help you thrive in your studies.</p>
        <p>If you face any problem here, go to the help tab and make a submission. We're here for you {{userAuthStore.userData['first_name']}}!</p>
      </v-card-text>
      <v-card-actions class="flex-all">
        <v-btn class="overlay-btn" elevation="4" @click="hidOverlay()">OK</v-btn>
      </v-card-actions>
    </v-card>
  </div>
  <TheHeader />
  <main class="main">
    <div class="pages-container">
      <div class="page-nav-container">
        <button class="nav-btn" @click="changePage('page1')" :class="{'nav-btn-active': activePage==='page1'}"><v-icon icon="mdi-account-group-outline"/>MY CLASS</button>
        <button class="nav-btn" @click="changePage('page2')" :class="{'nav-btn-active': activePage==='page2'}"><v-icon icon="mdi-book-open-outline"/>MY RESULTS</button>
        <button class="nav-btn" @click="changePage('page3')" :class="{'nav-btn-active': activePage==='page3'}"><v-icon icon="mdi-book-account"/>TRANSCRIPT</button>
        <button class="nav-btn" @click="changePage('page4')" :class="{'nav-btn-active': activePage==='page4'}"><v-icon icon="mdi-help"/>HELP</button>
      </div>
  
        <div class="pages" :style="activePage==='page1' ? {'display': 'flex'}: {'display': 'none'}">
          <StudentClass />
        </div>
        <div class="pages" :style="activePage==='page2' ? {'display': 'flex'}: {'display': 'none'}">
          <StudentResults />
        </div>
        <div class="pages" :style="activePage==='page3' ? {'display': 'flex'}: {'display': 'none'}">
          <StudentTranscript />
        </div>
        <div class="pages" :style="activePage==='page4' ? {'display': 'flex'}: {'display': 'none'}">
          <HelpForm />
        </div>
    </div>
  </main>
  <TheFooter/>
</template>

<style scoped>

.welcome-overlay{
  display: flex;
  position: absolute;
  align-items: center;
  justify-content: center;
  height: 100%;
  z-index: 2;
  width: 100%;
  background-color: rgba(0,0,0,0.5);
}

.card{
  width: 80%;
}

#company-name{
  font-size: .7rem;
  font-family: Verdana, "sans-serif";
  text-align: center;
  font-weight: bold;
  text-transform: uppercase;
  color: #007bff;
}

.overlay-btn{
  background-color: mediumseagreen;
  color: yellow;
}

.overlay-btn:hover{
  background-color: lightseagreen;
  color: white;
}



</style>
<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router';

useHead({

  link: [
    {
      rel: 'icon',
      href: '/login_logo.jpg',
    },
  ],

  htmlAttrs: {
    lang: 'en'
  },

})


const elementsStore = useElementsStore()
const router = useRouter()
const userAuthStore = useUserAuthStore()
const loading = ref(false)

let intervalTime = 0
if (process.env.NODE_ENV == 'production'){
  intervalTime = setInterval(()=>{
      userAuthStore.startUpServer()
  }, 60*1000)
}

onBeforeUnmount(()=>{
  clearInterval(intervalTime)
})


const hidOverlay = async ()=>{
  const overlay = document.getElementById('session-alert')

  if (overlay && elementsStore.overlayPath && elementsStore.logout){
      userAuthStore.logoutUser()
      await router.push(`${elementsStore.overlayPath}`)
      overlay.style.display = 'none'
      elementsStore.overlayMessage = ''
      elementsStore.overlayMessageColor = null
      elementsStore.overlayPath = null
      elementsStore.logout = null

  }else if (overlay && elementsStore.overlayPath && !elementsStore.logout){
      await router.push(`${elementsStore.overlayPath}`)
      overlay.style.display = 'none'
      elementsStore.overlayMessage = ''
      elementsStore.overlayPath = null
      elementsStore.overlayMessageColor = null
      elementsStore.logout = null

  }else {
      if (overlay && !elementsStore.overlayPath && !elementsStore.logout){
          overlay.style.display = 'none'
          elementsStore.overlayMessage = ''
          elementsStore.overlayMessageColor = null
          elementsStore.overlayPath = null
          elementsStore.logout = null
      }
    }

  }

const hidLogoutOverlay = ()=>{
  const overlay = document.getElementById('logout')
  overlay? overlay.style.display = 'none' : null
}

const logout = async ()=>{
  const overlay = document.getElementById('logout')
  loading.value = true
  userAuthStore.logoutUser()
  userAuthStore.message = 'Your have been logged out!'
  await router.push(elementsStore.overlayPath)
  loading.value = false
  overlay? overlay.style.display = 'none' : null
  
  setTimeout(()=>{
    elementsStore.overlayPath = null
    userAuthStore.message = ''
  }, 5000)

}


</script>

<template>
  <v-app style="background-color: seagreen">
    <div class="container" style="background-color: white">
    <!-- Logout Overlay -->
      <div id="logout" class="overlay">
        <v-card class="d-flex flex-column align-center">
          <v-card-text style="font-size: .8rem; font-family: sans-serif; text-align: left; line-height: 1.2; font-weight: bold">
            <p v-if="userAuthStore.userData">{{userAuthStore.userData['first_name']}}! are you sure you want to logout?</p>
          </v-card-text>
          <v-card-actions>
            <v-btn class="mr-5" color="red" elevation="4" @click="logout()">YES</v-btn>
            <v-btn :disabled="loading" color="blue" class="ml-5" elevation="4" @click="hidLogoutOverlay">NO</v-btn>
          </v-card-actions>
        </v-card>
      </div>
    
      <!-- Session Overlay -->
      <div id="session-alert" class="overlay">
          <div class="overlay-card d-flex flex-column align-center">
            <h4 id="company-name">Rozmach</h4>
            <p class="overlay-text">{{elementsStore.overlayMessage}}</p>
            <div>
              <v-btn class="overlay-btn" @click="hidOverlay()">OK</v-btn>
            </div>
          </div>
        </div>
      <slot/>
    </div>
    </v-app>
</template>

<style scoped>

div:hover{
  cursor: default;
}
.overlay{
  width: 100%;
  height: 100%;
  position: fixed;
  top: 0;
  left: 0;
  background-color: rgba(0,0,0,0.7);
  display: none;
  align-items: center;
  justify-content: center;
  z-index: 10;
}

.overlay-card{
  background-color: white;
  border-radius: .3em;
  width: max-content;
  padding: .5em .5em;
}


.overlay-text{
  margin-top: 1em;
  margin-bottom: 1em;
  font-size: 9rem;
}



</style>

<script setup lang="ts">
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
let intervalTime:any = 0
if (process.env.NODE_ENV == 'production'){
  intervalTime = setInterval(()=>{
      userAuthStore.startUpServer()
  }, 60*1000)
}

onBeforeUnmount(()=>{
  clearInterval(intervalTime)
})
onBeforeMount(()=>{
  document.title = "Cassandra"
  document.body.style.overflow = 'hidden'
})
const hidOverlay = async ()=>{
  const overlay = document.getElementById('session-alert')
  if (overlay && elementsStore.overlayPath && elementsStore.logout){
      userAuthStore.logoutUser()
      await router.push('/')
      overlay.style.display = 'none'
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

const hideDeletionOverlay = ()=>{
  elementsStore.deleteOverlayMessage = ''
  const overlay = document.getElementById('deleteOverlay')
  overlay ? overlay.style.display = 'none' : null
}

const logout = async ()=>{
  const overlay = document.getElementById('logout')
  userAuthStore.logoutUser()
  userAuthStore.message = 'Your have been logged out!'
  await router.push('/')
  overlay? overlay.style.display = 'none' : null
  setTimeout(()=>{
    elementsStore.overlayPath = null
    userAuthStore.message = ''
  }, 5000)
}

const continueDeletion = ()=>{
  hideDeletionOverlay()
  elementsStore.deleteFunction()
}

</script>

<template>
  <v-app style="background-color: seagreen; overflow: hidden">
    <div class="container" style="background-color: white">
    <!-- Logout Overlay -->
      <div id="logout" class="overlay">
        <v-card class="overlay-card">
          <v-card-text >
            <p class="overlay-text" v-if="userAuthStore.userData">Are you sure you want to logout?</p>
          </v-card-text>
          <v-card-actions>
            <v-btn class="mr-5" size="small" color="red" @click="logout">YES</v-btn>
            <v-btn color="black" size="small" class="ml-5" @click="hidLogoutOverlay">NO</v-btn>
          </v-card-actions>
        </v-card>
      </div>
    
      <!-- Session Overlay -->
      <div id="session-alert" class="overlay">
        <v-card class="overlay-card">
          <v-card-text>
            <p class="overlay-text" :style="`color: ${elementsStore.overlayMessageColor}`">{{elementsStore.overlayMessage}}</p>
          </v-card-text>
          <v-card-actions class="flex-all">
            <v-btn @click="hidOverlay()" color="black" variant="flat">OK</v-btn>
          </v-card-actions>
        </v-card>
      </div>

      <!-- Delete Overlay -->
      <div id="deleteOverlay" class="overlay">
        <v-card class="overlay-card">
          <v-card-text>
            <p class="overlay-text" >{{ elementsStore.deleteOverlayMessage }}</p>
          </v-card-text>
          <v-card-actions>
            <v-btn class="mr-5" color="red" size="small" variant="flat" @click="continueDeletion">YES</v-btn>
            <v-btn class="ml-5" color="black" size="small" variant="flat" @click="hideDeletionOverlay">NO</v-btn>
          </v-card-actions>
        </v-card>
      </div>

      <!-- Loading Overlay -->
      <div id="LoadingOverlay" class="overlay">
        <v-progress-circular :size="50" :width="10" indeterminate color="blue" />
      </div>

      <slot/>
    </div>
    </v-app>
</template>

<style scoped>

div:hover{
  cursor: default;
}
.overlay-card{
  width: fit-content !important;
  height: fit-content !important;
}
.overlay-text{
  margin-top: 1em;
  margin-bottom: 1em;
  font-weight: bold;
  text-align: center;
  font-family: Verdana, Geneva, Tahoma, sans-serif;
  font-size: .8rem;
}
#session-alert{
  z-index: 1000 !important;
}

#LoadingOverlay{
  z-index: 1000 !important;
}


</style>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import { useRouter } from 'vue-router';
import { onBeforeMount, onBeforeUnmount } from 'vue';
import { useUserAuthStore } from '@/stores/userAuthStore';
import { useElementsStore } from '@/stores/elementsStore';
import TheLoader from '@/components/TheLoader.vue';

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
  document.body.style.overflow = 'hidden'
})

if (window.innerWidth >= 767 && window.innerWidth < 2000) {
  elementsStore.btnSize1 = 'small'
} 
else if (window.innerWidth >= 2000) {
  elementsStore.btnSize1 = 'default'
}
if (window.innerWidth > 1000) {
  elementsStore.onDesk = true
}
window.addEventListener('resize', () => {
  if (window.innerWidth <= 1000) {
    elementsStore.onDesk = false
  }
  else if (window.innerWidth > 1000) {
    elementsStore.onDesk = true
  }
  if (window.innerWidth < 767) {
    elementsStore.btnSize1 = 'x-small'
  } 
  else if (window.innerWidth >= 767 && window.innerWidth < 2000) {
    elementsStore.btnSize1 = 'small'
  } 
  else if (window.innerWidth >= 2000) {
    elementsStore.btnSize1 = 'default'
  }
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
  if (overlay) {
    overlay.style.display = 'none';
  }
}

const hideDeletionOverlay = ()=>{
  elementsStore.deleteOverlayMessage = ''
  const overlay = document.getElementById('deleteOverlay')
  if (overlay) {
    overlay.style.display = 'none';
  }
}

const logout = async ()=>{
  const overlay = document.getElementById('logout')
  userAuthStore.logoutUser()
  userAuthStore.message = 'Your have been logged out!'
  await router.push('/')
  if (overlay) {
    overlay.style.display = 'none';
  }
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
  <v-app style="overflow: hidden">
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

      <RouterView/>
      <TheLoader v-if="!userAuthStore.userData"/>
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

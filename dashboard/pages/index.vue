<script setup lang="ts">
import {computed, onBeforeMount, onBeforeUnmount, reactive} from "vue";
import { useRouter } from "vue-router";

definePageMeta({
    middleware: ['check-login']
})

useSeoMeta({
    title: "EduAAP  | LOGIN",
    description: "Login to your Academic Access Point (AAP)"
})

useHead({
  meta: [
    {name: "robots", content: "index, follow"}
  ],
})

onBeforeUnmount(()=>{
  document.body.style.overflow = 'auto'
})

onBeforeMount(() => {
  document.body.style.overflow = 'hidden';

})

const userAuthStore = useUserAuthStore()
const router = useRouter()
const data = reactive({
  form: false,
  username: '',
  password: '',
  loading: false,
  visible: false,
  lockField: false,
})

let checkInput = computed(()=>{
  return !(data.username && data.password)

})

const authenticate = async ()=>{
  data.loading = true
  data.lockField = true
  await userAuthStore.userLogin(data.username, data.password)
  if (userAuthStore.isAuthenticated && userAuthStore.userData['role']==='staff' || userAuthStore.isAuthenticated && userAuthStore.userData['role']==='head' ){
    data.password = ''
    data.loading = false;
    setTimeout(()=>{
      router.push('/staff')
    },2000)
  }

  else if (userAuthStore.isAuthenticated===true && userAuthStore.userData['role']==='student' ){
    data.password = ''
    data.loading = false;
    setTimeout(()=>{
      router.push('/student')
    },2000)
  }

  else {
    data.loading = false
    data.lockField = false
    setTimeout(()=>{
      userAuthStore.message = ''
    },6000)
  }
}


</script>

<template>
  <div class="container flex-c align-center justify-center" style="background-color: seagreen; height: 100dvh">
    <div style="height: 90dvh" class="row-wrapper img-container">
      <section class="flex-all-c">
        <h1 class="portal-name">ACADEMIC ACCESS POINT</h1>
        <img class="sch-logo" src="/login_logo.jpg" alt="school logo">
        <div class="flex-c align-center" style="background-color: transparent">
          <v-form class="flex-c justify-start align-center" @submit.prevent="authenticate">
            <div class="form-message-container">
              <h6 class="form-message" style="color: yellow" v-if="userAuthStore.message && userAuthStore.isAuthenticated">{{userAuthStore.message}}</h6>
              <h6 class="form-message" style="color: #be12121010e71010" v-if="userAuthStore.message && !userAuthStore.isAuthenticated">{{userAuthStore.message}}</h6>
            </div>
            <v-text-field
                :disabled="data.lockField"
                class="form-text-field username"
                v-model="data.username"
                label="USERNAME"
                hint="Enter your username"
                variant="solo"
                density="comfortable"
                type="text"
                clearable
                @focus="checkInput"
                prepend-inner-icon="mdi-account-outline"
            ></v-text-field>
            <v-text-field
                :append-inner-icon="data.visible ? 'mdi-eye-off-outline' : 'mdi-eye-outline'"
                @click:append-inner="data.visible = !data.visible"
                :disabled="data.lockField"
                :type="data.visible ? 'text' : 'password'"
                clearable
                @focus="checkInput"
                density="comfortable"
                variant="solo"
                class="form-text-field password"
                hint="Enter your password"
                v-model="data.password"
                label="PASSWORD"
                prepend-inner-icon="mdi-lock-outline"
            ></v-text-field>
            <p class="forgot-password">forgotten password ?</p>
            <v-btn
              class="submit-btn"
              type="submit"
              prepend-icon="mdi-lock-open-outline"
              :loading="data.loading"
              :disabled="checkInput">LOGIN
            </v-btn>
          </v-form>
        </div>
      </section>
    </div>
    <footer class="footer-container">
      <h6 class="footer-text">© 2024</h6>
    </footer>
  </div>
</template>

<style scoped>


.sch-logo{
  width: 50px;
  height: 50px;
  border-radius: 50%;
}

.portal-name{
  color: yellow;
  cursor: default;
  font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif
}

.aap{
  margin-top: .3em;
  margin-bottom: 1em;
  font-family:Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
  color: yellow;
  font-size: .7rem;
}

.form-message-container{
  margin-bottom: 1em;
}

.form-message{
  font-size: .7rem;
}


.form-text-field{
  width: 250px;
  font-weight: bold;
  margin-top: .5em;
  
}
.submit-btn{
  margin-top: 2em;
  font-weight: bold;
}
.submit-btn:hover{
  background-color: mediumseagreen;
  color: yellow;
}

.forgot-password{
  color: white;
  font-size: 1rem;
}

.forgot-password:hover{
  color: yellow;
  cursor: pointer;
}

.footer-container{
  display: flex;
  flex-direction: row;
  justify-content: center;
  width: 100%;
  position: absolute;
  bottom: 0;
}

.footer-text{
  color: yellow;
  cursor: default;
}

@media screen and (min-width: 576px) {

  .form-message{
      font-size: .8rem;
  }

  .form-text-field{
      width: 300px;        
  }

  .footer-text{
      font-size: .8rem;
  }
}

@media screen and (min-width: 767px) {

  .form-message{
      font-size: .9rem;
  }

  .img-container{
      width: 100%;
      height: 100%;
      border-radius: 1em;
      background-size: cover;
  }

  .form-text-field{
      width: 350px;
  }
  
}


</style>
   
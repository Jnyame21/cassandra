<script setup lang="ts">
import {computed, onBeforeMount, onBeforeUnmount, reactive} from "vue";
import { useRouter } from "vue-router";



const userAuthStore = useUserAuthStore()

definePageMeta({
    middleware: ['check-login']
})

useSeoMeta({
    title: "Cassandra | Login",
    description: "Login to Cassandra, the school management system."
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
  .then(response =>{
    if (userAuthStore.isAuthenticated && userAuthStore.userData['role']==='staff' || userAuthStore.isAuthenticated && userAuthStore.userData['role']==='head' ){
      data.password = ''
      data.loading = false;
      setTimeout(()=>{
        router.push('/staff')
      },2000)
    }

    else if (userAuthStore.isAuthenticated && userAuthStore.userData['role']==='student' ){
      data.password = ''
      data.loading = false;
      setTimeout(()=>{
        router.push('/student')
      },2000)
    }
  })
  .catch(e =>{
    data.loading = false
    data.lockField = false
    setTimeout(()=>{
      userAuthStore.message = ''
    },6000)
  })
}


</script>

<template>
  <div class="container img-container flex-c align-center justify-center" style="height: 100dvh">
    <div style="height: 90dvh" class="row-wrapper">
      <section class="flex-all-c form-container">
        <h1 class="portal-name">CASSANDRA</h1>
        <img class="sch-logo" src="/login_logo.jpg" alt="school logo">
        <div class="flex-c align-center" style="background-color: transparent">
          <v-form class="flex-c justify-start align-center" @submit.prevent="authenticate">
            <div class="form-message-container">
              <h6 class="form-message" style="color: yellow" v-if="userAuthStore.message && userAuthStore.isAuthenticated">{{userAuthStore.message}}</h6>
              <h6 class="form-message" style="color: red" v-if="userAuthStore.message && !userAuthStore.isAuthenticated">{{userAuthStore.message}}</h6>
            </div>
            <v-text-field
                :disabled="data.lockField"
                class="form-text-field username"
                v-model="data.username"
                label="USERNAME"
                hint="Enter your username"
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
                class="form-text-field password"
                hint="Enter your password"
                v-model="data.password"
                label="PASSWORD"
                prepend-inner-icon="mdi-lock-outline"
            ></v-text-field>
            <!-- <p class="forgot-password">forgotten password ?</p> -->
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
    <TheFooter/>
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
  font-family:Georgia, 'Times New Roman', Times, serif
}


.form-message-container{
  margin-bottom: 1em;
  margin-top: 1em;
}

.form-message{
  font-size: .7rem;
  border: 1px solid;
  padding: .1em 1em;
}

.form-container{
  border-radius: 1em;
}
.form-text-field{
  width: 250px;
  font-weight: bold;
  margin-top: .5em;
  color: yellow !important;
  
}

.submit-btn{
  margin-top: 2em;
  font-weight: bold;
}

.forgot-password{
  color: white;
  font-size: 1rem;
}

.forgot-password:hover{
  color: yellow;
  cursor: pointer;
}
.img-container{
  width: 100%;
  height: 100%;
  border-radius: 0 !important;
  background-size: cover;
  background-image: url('/login_logo_main.jpg');
}

.footer-text{
  color: yellow;
  cursor: default;
}

.footer {
  background-color: black;
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

  .form-container{
    margin-right: 10%;
  }

  .form-text-field{
      width: 350px;
  }
}

@media screen and (min-width: 991px){
  .form-container{
    margin-right: 30%;
  }
}



</style>
   
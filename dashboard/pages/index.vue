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

let isFormValid = computed(()=>{
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
  <div class="container flex-c flex-column" style="min-height: 100vh">
    <div class="img-container flex-c align-center justify-center">
      <div class="row-wrapper">
        <section class="flex-all-c form-container">
          <h1 class="portal-name">CASSANDRA</h1>
          <img class="sch-logo" src="/login_logo.jpg" alt="school logo">
          <div class="flex-c align-center" style="background-color: transparent">
            <v-form class="flex-c justify-start align-center" @submit.prevent="authenticate">
              <div class="form-message-container">
                <h6 class="form-message" style="color: yellow; text-transform: uppercase" v-if="userAuthStore.message && userAuthStore.isAuthenticated">{{userAuthStore.message}}</h6>
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
                prepend-inner-icon="mdi-account-outline"
              ></v-text-field>
              <v-text-field
                :append-inner-icon="data.visible ? 'mdi-eye-off-outline' : 'mdi-eye-outline'"
                @click:append-inner="data.visible = !data.visible"
                :disabled="data.lockField"
                :type="data.visible ? 'text' : 'password'"
                clearable
                density="comfortable"
                class="form-text-field password"
                hint="Enter your password"
                v-model="data.password"
                label="PASSWORD"
                prepend-inner-icon="mdi-lock-outline"
              ></v-text-field>
              <v-btn
                class="submit-btn"
                type="submit"
                prepend-icon="mdi-lock-open-outline"
                :loading="data.loading"
                :disabled="isFormValid">LOGIN
              </v-btn>
            </v-form>
          </div>
        </section>
      </div>
    </div>
    <TheFooter class="footer"/>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  min-height: 100dvh;
}

.img-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-size: cover;
  background-image: url('/login_logo_main.jpg');
  background-position: center;
  flex-grow: 1;
}
.row-wrapper {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}
.form-container {
  border-radius: 1em;
  background-color: #333333; 
  padding: 2em;
}
.portal-name {
  color: yellow;
  font-size: 2.5rem; 
  font-weight: 700; 
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5); 
  font-family: 'Roboto', sans-serif; 
  margin-bottom: 1em;
}

.sch-logo {
  width: 50px;
  height: 50px;
  border-radius: 50%;
}

.form-message-container {
  margin-bottom: 1em;
  margin-top: 1em;
}

.form-message {
  font-size: .7rem;
  border: 1px solid;
  padding: .1em 1em;
}

.form-text-field {
  width: 250px;
  font-weight: bold;
  margin-top: .5em;
  color: yellow !important;
}

.submit-btn {
  margin-top: 2em;
  font-weight: bold;
}

.forgot-password {
  color: white;
  font-size: 1rem;
}

.forgot-password:hover {
  color: yellow;
  cursor: pointer;
}

.footer {
  background-color: black;
  color: yellow;
  text-align: center;
  padding: 1em;
}



</style>

   
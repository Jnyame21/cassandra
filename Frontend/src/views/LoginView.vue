<script setup lang="ts">
import { computed, reactive } from "vue";
import { useRouter } from "vue-router";
import { useHead } from '@vueuse/head'
import { useUserAuthStore } from '@/stores/userAuthStore'
const userAuthStore = useUserAuthStore()
import TheFooter from '@/components/TheFooter.vue'

useHead({
  meta: [
    { name: "description", content: "Login to Cassandra, the school management system." },
    { name: "robots", content: "index, follow" }
  ],
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

const isFormValid = computed(() => {
  return !(data.username && data.password)
})

const authenticate = async () => {
  data.loading = true;
  data.lockField = true;
  try {
    await userAuthStore.userLogin(data.username, data.password);
    if (userAuthStore.isAuthenticated && userAuthStore.userData['role'].toLowerCase() === 'staff') {
      data.password = '';
      data.loading = false;
      setTimeout(() => {
        router.push('/staff');
      }, 2000);
    } 
    else if (userAuthStore.isAuthenticated && userAuthStore.userData['role'].toLowerCase() === 'student') {
      data.password = '';
      data.loading = false;
      setTimeout(() => {
        router.push('/student');
      }, 2000);
    }
    else if (userAuthStore.isAuthenticated && userAuthStore.userData['role'].toLowerCase() === 'superuser') {
      data.password = '';
      data.loading = false;
      setTimeout(() => {
        router.push('/superuser');
      }, 2000);
    }
    else{
      userAuthStore.message = "Ooop! Something went wrong. Contact your school administrator"
      data.loading = false;
      data.lockField = false;
      setTimeout(() => {
        userAuthStore.message = '';
      }, 10000);
    }
  } 
  catch {
    data.loading = false;
    data.lockField = false;
    setTimeout(() => {
      userAuthStore.message = '';
    }, 10000);
  }
}


</script>

<template>
  <div class="container flex-c flex-column" style="min-height: 100vh">
    <div class="img-container flex-c align-center justify-center">
      <div class="row-wrapper">
        <section class="flex-all-c form-container">
          <h1 class="portal-name">CASSANDRA</h1>
          <img class="sch-logo" src="/app_logo.jpg" alt="school logo">
          <div class="flex-c align-center" style="background-color: transparent">
            <v-form class="flex-c justify-start align-center" @submit.prevent="authenticate">
              <div class="form-error-message-container">
                <h6 class="form-error-message login-message"
                  v-if="userAuthStore.message && userAuthStore.isAuthenticated">{{ userAuthStore.message }}</h6>
                <h6 class="form-error-message" style="color: red"
                  v-if="userAuthStore.message && !userAuthStore.isAuthenticated">{{ userAuthStore.message }}</h6>
              </div>
              <v-text-field :disabled="data.lockField" class="form-text-field username" v-model="data.username"
                label="USERNAME" hint="Enter your username" density="comfortable" type="text" clearable
                prepend-inner-icon="mdi-account-outline"></v-text-field>
              <v-text-field :append-inner-icon="data.visible ? 'mdi-eye-off-outline' : 'mdi-eye-outline'"
                @click:append-inner="data.visible = !data.visible" :disabled="data.lockField"
                :type="data.visible ? 'text' : 'password'" clearable density="comfortable"
                class="form-text-field password" hint="Enter your password" v-model="data.password" label="PASSWORD"
                prepend-inner-icon="mdi-lock-outline"></v-text-field>
              <v-btn class="submit-btn" type="submit" prepend-icon="mdi-lock-open-outline" :loading="data.loading"
                :disabled="isFormValid">LOGIN
              </v-btn>
            </v-form>
          </div>
        </section>
      </div>
    </div>
    <TheFooter class="footer" />
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
  background-image: url('/login_logo.jpg');
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
  width: 100%;
  max-width: 500px;
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

.form-error-message-container {
  margin-bottom: 1em;
  margin-top: 1em;
  width: 100%;
}

.form-error-message {
  font-size: .7rem;
  border: 1px solid;
  padding: .1em 1em;
  text-align: center;
}
.login-message{
  color: yellow !important;
  text-transform: uppercase !important;
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
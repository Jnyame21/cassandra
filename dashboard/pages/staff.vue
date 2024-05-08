<script setup lang="ts">

definePageMeta({
    middleware: ['check-staff']
})

useHead({
  meta: [
    {name: "robots", content: "no-index"}
  ],
})

const userAuthStore = useUserAuthStore()
const rozmachAuth: any = ref(null)
const activePage = ref('page1')
const formErrorMessage = ref('')
const formSuccessMessage = ref('')
const password = ref('')
const contact = ref('')
const email = ref('')
const altContact = ref('')
const loading = ref(false)
const visible = ref(false)

onBeforeUnmount(()=>{
  document.body.style.overflow = 'auto'
})

onBeforeMount(()=>{
  if (userAuthStore.isAuthenticated && userAuthStore.userData){
    document.title = "Cassandra"
  }
  document.body.style.overflow = 'hidden'
  rozmachAuth.value = localStorage.getItem('RozmachAuth')
  if (rozmachAuth.value){
    rozmachAuth.value = JSON.parse(rozmachAuth.value)
  }

})

const hidOverlay = async()=>{
  loading.value = true
  const formData = new FormData()
  formData.append('password', password.value)
  formData.append('contact', contact.value)
  formData.append('altContact', altContact.value)
  formData.append('email', email.value)

  try{
    const response = await axiosInstance.post('user/data', formData)
    if (response.status === 200){
      if (rozmachAuth.value && rozmachAuth.value.reset){
        rozmachAuth.value.reset = false
        localStorage.setItem('RozmachAuth', JSON.stringify(rozmachAuth.value))
      }
      await userAuthStore.getUserData()
      formSuccessMessage.value = 'success'
      const overlay = document.getElementById('welcome')
      overlay ? overlay.style.display = 'none' : null
    }
    else if (response.status === 201){
      formErrorMessage.value = response.data['ms']
    }
  }
  catch (e){
    formErrorMessage.value = 'Something went wrong. check your internet connection'
    return Promise.reject()
  }
  finally{
    loading.value = false
  }
}

const checkInput = computed(()=>{
  return !(contact.value && password.value)
})

const changePage = (page: string)=>{
  activePage.value = page
}


</script>

<template>
    <!-- Welcome Overlay-->
  <div id="welcome" class="welcome-overlay" v-if="rozmachAuth && rozmachAuth['reset'] && userAuthStore.userData && userAuthStore.userData['role']==='staff' 
  || rozmachAuth && rozmachAuth['reset'] && userAuthStore.userData && userAuthStore.userData['role']==='head' "
  >
    <v-card class="card flex-all-c">
      <v-card-title id="school-name">{{userAuthStore.userData['school']['name']}}</v-card-title>
      <v-card-text style="font-size: .9rem; font-family: sans-serif; text-align: left; line-height: 1.5">
        <p style="text-align: center" class="mb-5"><strong>Welcome {{userAuthStore.userData['first_name']+' '+userAuthStore.userData['last_name']}}! Update your information before you begin</strong></p>
        <h6 class="form-message" style="color: yellow" v-if="formSuccessMessage">{{ formSuccessMessage }}</h6>
        <h6 class="form-message" style="color: red"  v-if="formErrorMessage">{{ formErrorMessage }}</h6>
        <div class="field-container flex-all-c">
          <v-text-field
          :disabled="loading"
          class="form-text-field"
          v-model="contact"
          label="PHONE NUMBER"
          hint="Enter you phone number"
          placeholder="0596021383"
          prepend-inner-icon="mdi-phone"
          type="number"
          variant="outlined"
          density="compact"
          clearable
          />

          <v-text-field
          :disabled="loading"
          class="form-text-field"
          v-model="altContact"
          label="SECOND PHONE (OPTIONAL)"
          type="number"
          placeholder="0556429210"
          hint="Enter you second phone number"
          prepend-inner-icon="mdi-phone"
          density="compact"
          variant="outlined"
          clearable
          />
        </div>
        <div class="field-container flex-all-c">
          <v-text-field
          :disabled="loading"
          class="form-text-field"
          v-model="email"
          label="EMAIL (OPTIONAL)"
          hint="Enter your email address"
          type="email"
          placeholder="nyamejustice2000@gmail.com"
          variant="outlined"
          prepend-inner-icon="mdi-email"
          density="compact"
          clearable
          />

          <v-text-field
          :append-inner-icon="visible ? 'mdi-eye-off-outline' : 'mdi-eye-outline'"
          @click:append-inner="visible = !visible"
          :disabled="loading"
          :type="visible ? 'text' : 'password'"
          clearable
          density="compact"
          class="form-text-field"
          variant="outlined"
          hint="Enter a new password"
          v-model="password"
          label="RESET PASSWORD"
          prepend-inner-icon="mdi-lock-outline"
          />
        </div>
      </v-card-text>
      <v-card-actions class="flex-all">
        <v-btn class="overlay-btn" :disabled="checkInput" :loading="loading" elevation="4" @click="hidOverlay()">DONE</v-btn>
      </v-card-actions>
    </v-card>
  </div>    
  <TheHeader/>
  <main class="main">
    
     <!-- Tabs -->
    <div class="pages-container">

      <div class="page-nav-container">
        <!-- Head -->
        <button class="nav-btn" @click="changePage('page1')" :class="{'nav-btn-active': activePage==='page1'}"
        v-if="userAuthStore.userData && userAuthStore.userData['role'] && userAuthStore.userData['role'] === 'head'">
        <v-icon icon="mdi-eye"/>
          OVERVIEW
        </button>
        
        <button class="nav-btn" @click="changePage('page2')" :class="{'nav-btn-active': activePage==='page2'}"
        v-if="userAuthStore.userData && userAuthStore.userData['role'] && userAuthStore.userData['role'] === 'head'"
        ><v-icon icon="mdi-account"/>
          DEPARTMENTS
        </button>

        <button class="nav-btn" @click="changePage('page3')" :class="{'nav-btn-active': activePage==='page3'}"
        v-if="userAuthStore.userData && userAuthStore.userData['role'] && userAuthStore.userData['role'] === 'head'"
        ><v-icon icon="mdi-account-group-outline"/>
          STUDENTS
        </button>

        <button class="nav-btn" @click="changePage('page4')" :class="{'nav-btn-active': activePage==='page4'}"
        v-if="userAuthStore.userData && userAuthStore.userData['role'] && userAuthStore.userData['role'] === 'head'"
        ><v-icon icon="mdi-chart-bar"/>
          ANALYTICS
        </button>

        <button class="nav-btn" @click="changePage('page5')" :class="{'nav-btn-active': activePage==='page5'}"
        v-if="userAuthStore.userData && userAuthStore.userData['role'] && userAuthStore.userData['role'] === 'head'"
        ><v-icon icon="mdi-alert-octagon-outline"/>
          HELP
        </button>


        <!-- Staff -->
        <button class="nav-btn" @click="changePage('page1')" :class="{'nav-btn-active': activePage==='page1'}"
        v-if="userAuthStore.userData && userAuthStore.userData['staff_role']=== 'teacher' || userAuthStore.userData && userAuthStore.userData['staff_role']=== 'hod'"
        ><v-icon icon="mdi-book-open-outline"/>
          COURSEWORK
        </button>

        <button class="nav-btn" @click="changePage('page2')" :class="{'nav-btn-active': activePage==='page2'}"
        v-if="userAuthStore.userData && userAuthStore.userData['staff_role']=== 'teacher' || userAuthStore.userData && userAuthStore.userData['staff_role']=== 'hod' "
        ><v-icon icon="mdi-account-group-outline"/>
          STUDENTS
        </button>

        <button class="nav-btn" @click="changePage('page3')" :class="{'nav-btn-active': activePage==='page3'}"
        v-if="userAuthStore.userData && userAuthStore.userData['staff_role']=== 'teacher' || userAuthStore.userData && userAuthStore.userData['staff_role']=== 'hod' "
        ><v-icon icon="mdi-chart-bar"/>
          ANALYTICS
        </button>

        <button class="nav-btn" @click="changePage('page4')" :class="{'nav-btn-active': activePage==='page4'}"
        v-if="userAuthStore.userData && userAuthStore.userData['staff_role']=== 'hod'"
        ><v-icon icon="mdi-account-multiple"/>
          TEACHERS
        </button>
        
        <button class="nav-btn" @click="changePage('page5')" :class="{'nav-btn-active': activePage==='page5'}"
        v-if="userAuthStore.userData && userAuthStore.userData['staff_role']=== 'hod' "
        ><v-icon icon="mdi-chart-line"/>
          PERFORMANCE
        </button>


        <!-- Admin -->
        <button class="nav-btn" @click="changePage('page1')" :class="{'nav-btn-active': activePage==='page1'}"
        v-if="userAuthStore.userData && userAuthStore.userData['staff_role']=== 'admin'"
        ><v-icon icon="mdi-calendar"/>
          CALENDAR
        </button>

        <button class="nav-btn" @click="changePage('page2')" :class="{'nav-btn-active': activePage==='page2'}"
        v-if="userAuthStore.userData && userAuthStore.userData['staff_role']=== 'admin'"
        ><v-icon icon="mdi-account-group-outline"/>
          STUDENTS
        </button>

        <button class="nav-btn" @click="changePage('page3')" :class="{'nav-btn-active': activePage==='page3'}"
        v-if="userAuthStore.userData && userAuthStore.userData['staff_role']=== 'admin' "
        ><v-icon icon="mdi-account-multiple"/>
          TEACHERS
        </button>

        <button class="nav-btn" @click="changePage('page4')" :class="{'nav-btn-active': activePage==='page4'}"
        v-if="userAuthStore.userData && userAuthStore.userData['staff_role']=== 'admin' "
        ><v-icon icon="mdi-account"/>
          HEAD
        </button>

        <!-- Admin -->

        <button class="nav-btn" @click="changePage('page6')" :class="{'nav-btn-active': activePage==='page6'}"
        v-if="userAuthStore.userData && userAuthStore.userData['role']=== 'staff' "
        ><v-icon icon="mdi-alert-octagon-outline"/>
          HELP
        </button>
      </div>

      <!-- Pages -->

      <!-- Head -->
      <div class="pages" :style="activePage==='page1' ? {'display': 'flex'}: {'display': 'none'}"
      v-if="userAuthStore.userData && userAuthStore.userData['role'] && userAuthStore.userData['role'] === 'head'"
      ><HeadOverview />
      </div>

      <div class="pages" :style="activePage==='page2' ? {'display': 'flex'}: {'display': 'none'}"
      v-if="userAuthStore.userData && userAuthStore.userData['role'] && userAuthStore.userData['role']=== 'head'"
      ><HeadDepartments />
      </div>

      <div class="pages" :style="activePage==='page3' ? {'display': 'flex'}: {'display': 'none'}"
      v-if="userAuthStore.userData && userAuthStore.userData['role'] && userAuthStore.userData['role']=== 'head'"
      ><HeadStudents />
      </div>

      <div class="pages" :style="activePage==='page4' ? {'display': 'flex'}: {'display': 'none'}"
      v-if="userAuthStore.userData && userAuthStore.userData['role'] && userAuthStore.userData['role']=== 'head'"
      ><HeadPerformanceDepartment />
      </div>

      <div class="pages" :style="activePage==='page5' ? {'display': 'flex'}: {'display': 'none'}"
      v-if="userAuthStore.userData && userAuthStore.userData['role'] && userAuthStore.userData['role']=== 'head' "
      ><HelpForm />
      </div>


        <!-- Staff -->
      <div class="pages" :style="activePage==='page1' ? {'display': 'flex'}: {'display': 'none'}"
      v-if="userAuthStore.userData && userAuthStore.userData['staff_role']=== 'teacher' || userAuthStore.userData && userAuthStore.userData['staff_role']=== 'hod' "
      ><TeacherCourseWork />
      </div>

      <div class="pages" :style="activePage==='page2' ? {'display': 'flex'}: {'display': 'none'}"
      v-if="userAuthStore.userData && userAuthStore.userData['staff_role']=== 'teacher' || userAuthStore.userData && userAuthStore.userData['staff_role']=== 'hod' "
      ><TeacherStudents />
      </div>

      <div class="pages" :style="activePage==='page3' ? {'display': 'flex'}: {'display': 'none'}"
      v-if="userAuthStore.userData && userAuthStore.userData['staff_role']=== 'teacher' || userAuthStore.userData && userAuthStore.userData['staff_role']=== 'hod' "
      ><TeacherAnalytics />
      </div>

      <div class="pages" :style="activePage==='page4' ? {'display': 'flex'}: {'display': 'none'}"
      v-if="userAuthStore.userData && userAuthStore.userData['staff_role']=== 'hod'"
      ><HodTeachers />
      </div>

      <div class="pages" :style="activePage==='page5' ? {'display': 'flex'}: {'display': 'none'}"
      v-if="userAuthStore.userData && userAuthStore.userData['staff_role']=== 'hod' "
      ><HodPerformance />
      </div>

      <!-- Admin -->
      <div class="pages" :style="activePage==='page1' ? {'display': 'flex'}: {'display': 'none'}"
      v-if="userAuthStore.userData && userAuthStore.userData['staff_role']=== 'admin' "
      ><AdminCalendar />
      </div>

      <div class="pages" :style="activePage==='page2' ? {'display': 'flex'}: {'display': 'none'}"
      v-if="userAuthStore.userData && userAuthStore.userData['staff_role']=== 'admin' "
      ><AdminStudents />
      </div>

      <div class="pages" :style="activePage==='page3' ? {'display': 'flex'}: {'display': 'none'}"
      v-if="userAuthStore.userData && userAuthStore.userData['staff_role']=== 'admin' "
      ><AdminStaff />
      </div>

      <div class="pages" :style="activePage==='page4' ? {'display': 'flex'}: {'display': 'none'}"
      v-if="userAuthStore.userData && userAuthStore.userData['staff_role']=== 'admin' "
      ><AdminHead />
      </div>

        <!-- Admin -->

      <div class="pages" :style="activePage==='page6' ? {'display': 'flex'}: {'display': 'none'}"
      v-if="userAuthStore.userData && userAuthStore.userData['role'] && userAuthStore.userData['role']=== 'staff' "
      ><HelpForm />
      </div>
    </div>

  </main>
  <TheFooter />
</template>

<style scoped>

.welcome-overlay{
  display: flex;
  position: absolute;
  align-items: center;
  justify-content: center;
  height: 100%;
  z-index: 10;
  width: 100%;
  background-color: rgba(0,0,0,0.5);
}

.card{
  width: 90%;
  max-width: 800px;
  display: flex;
  align-items: center !important;
  justify-content: center !important;
}

.form-message{
  font-size: .7rem;
  margin-top: 1em;
  margin-bottom: 1em;
  text-align: center;
  border: 1px solid;
  padding: .1em 1em;
}

.form-text-field{
  margin-top: 1em;
  width: 300px !important;
  max-width: 300px !important;
}


#school-name{
  font-size: .7rem;
  font-family: Verdana, "sans-serif";
  text-align: center;
  font-weight: bold;
  text-transform: uppercase;
  color: #007bff;
}
.overlay-btn{
  background-color: lightseagreen;
  color: white;
}
.overlay-btn:hover{
  background-color: mediumseagreen;
  color: yellow;
}


</style>
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
const elementsStore = useElementsStore()
const rozmachAuth: any = ref(null)
const formErrorMessage = ref('')
const formSuccessMessage = ref('')
const password = ref('')
const contact = ref('')
const email = ref('')
const altContact = ref('')
const loading = ref(false)
const visible = ref(false)
const onDesk = ref(false)

onBeforeUnmount(()=>{
  document.body.style.overflow = 'auto'
})

onBeforeMount(()=>{
  document.body.style.overflow = 'hidden'
  document.title = "Cassandra"
  elementsStore.activePage = "TeacherCoursework,Class,0"
  rozmachAuth.value = localStorage.getItem('RozmachAuth')
  if (rozmachAuth.value){
    rozmachAuth.value = JSON.parse(rozmachAuth.value)
  }
})

if (window.innerWidth >=576 && window.innerWidth < 1200){
  elementsStore.btnSize1 = 'small'
}else if (window.innerWidth > 1200){
  elementsStore.btnSize1 = 'default'
}
window.addEventListener('resize', ()=>{
  if (window.innerWidth < 576){
    elementsStore.btnSize1 = 'x-small'
    elementsStore.navDrawer = false
  }else if (window.innerWidth <=1200 && window.innerWidth >= 576){
    elementsStore.btnSize1 = 'small'
    elementsStore.navDrawer = false
  }else if (window.innerWidth > 1300){
    elementsStore.btnSize1 = 'default'
  }
})

watch(()=> userAuthStore.teacherData.courseWork, (newValue, oldValue)=>{
  if (newValue && newValue.length > 0){
    elementsStore.activePage = `TeacherCoursework,${newValue[0]['students_class']['name']},${0}`
  }
}, {'once': true})

const updateStaffData = async()=>{
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

if (window.innerWidth > 1000){
    onDesk.value = true
}else{
    onDesk.value = false
}

window.addEventListener('resize', (event)=>{
  if (window.innerWidth > 1000){
    onDesk.value = true;
  }else{
    onDesk.value = false;
  }
});

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
        <v-btn class="overlay-btn" :disabled="checkInput" @click="updateStaffData" :loading="loading" elevation="4">DONE</v-btn>
      </v-card-actions>
    </v-card>
  </div>    
  <TheHeader v-if="userAuthStore.userData"/>
  <main class="main" v-if="userAuthStore.userData">
    <StaffNavContainerMob v-if="!onDesk"/>
    <StaffNavContainerDesk v-if="onDesk"/>
    <div class="pages-container">
      <div class="component-wrapper" v-if="!userAuthStore.teacherData.courseWork || userAuthStore.teacherData.courseWork?.length ===0 ">
        <TeacherCourseWork :class="{'is-active-component': elementsStore.activePage.split(',')[0] === 'TeacherCoursework'}" />
      </div>
      <div class="component-wrapper" v-if="userAuthStore.teacherData.courseWork?.length >0 " :class="{'is-active-component': elementsStore.activePage.split(',')[0] === 'TeacherCoursework'}" >
        <TeacherCourseWork v-for="(course, index) in userAuthStore.teacherData.courseWork" :key="`${course['students_class']['name']}${index}`" 
        :className="course['students_class']['name']" 
        :classIndex="index" 
        :subjects="course['subjects'].map(item => item['name'])" 
        :students="course['students_class']['students'].map(item => ({'name': `${item['user']['first_name']} ${item['user']['last_name']}`, 'st_id': item['st_id'], 'gender': item['gender'], 'img': item['img']}))" 
        />
      </div>
      
      <div class="component-wrapper" v-if="userAuthStore.teacherData.studentsattendance?.length > 0" :class="{'is-active-component': elementsStore.activePage.split(',')[0] === 'TeacherStudentsAttendance'}" >
        <TeacherStudentsAttendance v-for="(_class, index) in userAuthStore.teacherData.studentsattendance" :key="`${_class['name']}${index}`" 
        :className="_class['class_name']" 
        :classIndex="index" 
        :students="_class['students']" 
        />
      </div>
      
      <div class="component-wrapper" v-if="userAuthStore.teacherData.studentsAssessments?.length >0 " :class="{'is-active-component': elementsStore.activePage.split(',')[0] === 'TeacherStudentsAssessments'}" >
        <div class="component-wrapper" v-for="(_class, index) in userAuthStore.teacherData.studentsAssessments" :key="`${_class['class_name']}${index}`">
          <div class="component-wrapper" v-for="(_course, ind) in _class['assignments']" :key="`${_class['class_name']}${_course['subject']}${ind}`">
            <TeacherStudentsAssessments v-for="(_assessment, i) in _course['assessments']" :key="`${_class['class_name']}${_course['subject']}${_assessment['title']}${i}`" 
            :className="_class['class_name']" :classIndex="index"
            :subjectName="_course['subject']" :subjectIndex="ind"
            :assessment="_assessment" :assessmentIndex="i"
            />
          </div>
        </div>
      </div>
      
      <div class="component-wrapper" v-if="userAuthStore.teacherData.studentsExams?.length >0 " :class="{'is-active-component': elementsStore.activePage.split(',')[0] === 'TeacherStudentsExams'}" >
        <div class="component-wrapper" v-for="(_class, index) in userAuthStore.teacherData.studentsExams" :key="`${_class['class_name']}${index}`">
          <TeacherStudentsExams v-for="(_subject, ind) in _class['exams']" :key="`${_subject['subject']}${ind}`" 
          :className="_class['class_name']" 
          :classIndex="index" 
          :subjectName="_subject['subject']" 
          :subjectIndex="ind"
          :examsData="_subject" 
          />
        </div>
      </div>

      <div class="component-wrapper" v-if="userAuthStore.teacherData.studentsResults?.length >0 " :class="{'is-active-component': elementsStore.activePage.split(',')[0] === 'TeacherStudentsResults'}" >
        <div class="component-wrapper" v-for="(_class, index) in userAuthStore.teacherData.studentsResults" :key="`${_class['class_name']}${index}`">
          <TeacherStudentsResults v-for="(_subject, ind) in _class['results']" :key="`${_subject['subject']}${ind}`" 
          :className="_class['class_name']" 
          :classIndex="index" 
          :subjectName="_subject['subject']" 
          :subjectIndex="ind"
          :resultData="_subject" 
          />
        </div>
      </div>

      <div class="component-wrapper" :class="{'is-active-component': elementsStore.activePage === 'Help'}" >
        <HelpForm v-show="elementsStore.activePage ==='Help' "/>
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
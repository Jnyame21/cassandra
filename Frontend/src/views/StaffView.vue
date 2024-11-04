<script setup lang="ts">
import { useUserAuthStore } from '@/stores/userAuthStore'
import { useElementsStore } from '@/stores/elementsStore'
import { computed, onBeforeMount, ref, watch } from 'vue'
import { useHead } from '@vueuse/head';
import axiosInstance from '@/utils/axiosInstance';
import { AxiosError } from 'axios';
import TeacherCourseWork from '@/components/TeacherCourseWork.vue'
import TeacherStudentsAttendance from '@/components/TeacherStudentsAttendance.vue'
import TeacherStudentsAssessments from '@/components/TeacherStudentsAssessments.vue'
import TeacherStudentsExams from '@/components/TeacherStudentsExams.vue'
import TeacherStudentsResults from '@/components/TeacherStudentsResults.vue'
import HelpForm from '@/components/HelpForm.vue'
import TheHeader from '@/components/TheHeader.vue';
import TheFooter from '@/components/TheFooter.vue';
import StaffNavContainerMob from '@/components/StaffNavContainerMob.vue';
import StaffNavContainerDesk from '@/components/StaffNavContainerDesk.vue';
import TeacherDepartment from '@/components/TeacherDepartment.vue';
import AdminAcademicYears from '@/components/AdminAcademicYears.vue';
import AdminStudentsClass from '@/components/AdminStudentsClass.vue';
import AdminLinkedClasses from '@/components/AdminLinkedClasses.vue';
import AdminStaff from '@/components/AdminStaff.vue';

useHead({
  meta: [
    { name: "robots", content: "no-index" }
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

onBeforeMount(() => {
  rozmachAuth.value = localStorage.getItem('RozmachAuth')
  if (rozmachAuth.value) {
    rozmachAuth.value = JSON.parse(rozmachAuth.value)
  }
})

watch(() => userAuthStore.staffData.courseWork, (newValue) => {
  if (newValue?.length > 0 && ['teacher', 'hod'].includes(userAuthStore.userData?.['staff_role'].toLowerCase())) {
    elementsStore.activePage = `TeacherCoursework,${newValue[0]['students_class']['name']},${0}`
  }
}, { 'once': true })

watch(() => userAuthStore.userData, (newValue) => {
  if (newValue && newValue['staff_role'].toLowerCase() === 'admin') {
    elementsStore.activePage = 'AdminAcademicYears'
  }
  else if (newValue && ['teacher', 'hod'].includes(userAuthStore.userData?.['staff_role'].toLowerCase())){
    elementsStore.activePage = 'TeacherCoursework,Class,0'
  }
}, { 'once': true , 'immediate': true})

const updateStaffData = async () => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('password', password.value)
  formData.append('contact', contact.value)
  formData.append('altContact', altContact.value)
  formData.append('email', email.value)

  try {
    await axiosInstance.post('user/data', formData)
    if (rozmachAuth.value?.reset) {
      rozmachAuth.value.reset = false
      localStorage.setItem('RozmachAuth', JSON.stringify(rozmachAuth.value))
    }
    await userAuthStore.getUserData()
    const overlay = document.getElementById('welcomeOverlay')
    if (overlay) {
      overlay.style.display = 'none'
    }
    elementsStore.HideLoadingOverlay()
    elementsStore.ShowOverlay('success', 'green', null, null)
  }
  catch (error) {
    elementsStore.HideLoadingOverlay()
    if (error instanceof AxiosError) {
      if (error.response) {
        if (error.response.status === 400 && error.response.data.message) {
          elementsStore.ShowOverlay(error.response.data.message, 'red', null, null)
        } else {
          elementsStore.ShowOverlay('Oops! something went wrong. Try again later', 'red', null, null)
        }
      }
      else if (!error.response && (error.code === 'ECONNABORTED' || !navigator.onLine)) {
        elementsStore.ShowOverlay('A network error occurred! Please check you internet connection', 'red', null, null)
      }
      else {
        elementsStore.ShowOverlay('An unexpected error occurred!', 'red', null, null)
      }
    }
  }

}

const checkInput = computed(() => {
  return !(contact.value && password.value)
})

</script>

<template>
  <!-- Welcome Overlay-->
  <div id="welcomeOverlay" class="welcome-overlay"
    v-if="rozmachAuth?.['reset'] && userAuthStore.userData?.['role'] === 'staff'">
    <v-card class="card flex-all-c">
      <v-card-title id="school-name">{{ userAuthStore.userData['school']['name'] }}</v-card-title>
      <v-card-text style="font-size: .9rem; font-family: sans-serif; text-align: left; line-height: 1.5">
        <p style="text-align: center" class="mb-5"><strong>Welcome {{userAuthStore.userData['first_name']}}
        {{userAuthStore.userData['last_name']}}! Update your information before you begin</strong></p>
        <h6 class="form-message" style="color: yellow" v-if="formSuccessMessage">{{ formSuccessMessage }}</h6>
        <h6 class="form-message" style="color: red" v-if="formErrorMessage">{{ formErrorMessage }}</h6>
        <div class="field-container flex-all-c">
          <v-text-field :disabled="loading" class="form-text-field" v-model="contact" label="PHONE NUMBER"
            hint="Enter you phone number" placeholder="0596021383" prepend-inner-icon="mdi-phone" type="number"
            variant="outlined" density="compact" clearable />

          <v-text-field :disabled="loading" class="form-text-field" v-model="altContact" label="SECOND PHONE (OPTIONAL)"
            type="number" placeholder="0556429210" hint="Enter you second phone number" prepend-inner-icon="mdi-phone"
            density="compact" variant="outlined" clearable />
        </div>
        <div class="field-container flex-all-c">
          <v-text-field :disabled="loading" class="form-text-field" v-model="email" label="EMAIL (OPTIONAL)"
            hint="Enter your email address" type="email" placeholder="nyamejustice2000@gmail.com" variant="outlined"
            prepend-inner-icon="mdi-email" density="compact" clearable />

          <v-text-field :append-inner-icon="visible ? 'mdi-eye-off-outline' : 'mdi-eye-outline'"
            @click:append-inner="visible = !visible" :disabled="loading" :type="visible ? 'text' : 'password'" clearable
            density="compact" class="form-text-field" variant="outlined" hint="Enter a new password" v-model="password"
            label="RESET PASSWORD" prepend-inner-icon="mdi-lock-outline" />
        </div>
      </v-card-text>
      <v-card-actions class="flex-all">
        <v-btn class="overlay-btn" :disabled="checkInput" @click="updateStaffData" :loading="loading"
          elevation="4">DONE</v-btn>
      </v-card-actions>
    </v-card>
  </div>
  <TheHeader v-if="userAuthStore.userData" />
  <main class="main" v-if="userAuthStore.userData">
    <StaffNavContainerMob v-if="!elementsStore.onDesk" />
    <StaffNavContainerDesk v-if="elementsStore.onDesk" />
    
    <!-- Admin -->
    <div class="pages-container" v-if="userAuthStore.userData['staff_role'].toLowerCase() === 'admin'">
      <div class="component-wrapper"
        :class="{ 'is-active-component': elementsStore.activePage === 'AdminAcademicYears' }">
        <AdminAcademicYears />
      </div>
      <div class="component-wrapper" v-if="userAuthStore.adminData.classes?.length > 0"
        :class="{ 'is-active-component': elementsStore.activePage.split(',')[0] === 'AdminStudentsClass' }">
        <AdminStudentsClass v-for="(_class, index) in userAuthStore.adminData.classes"
          :key="`${_class['name']}${index}`" :className="_class['name']"
          :classIndex="index" :subjects="_class['subjects'].map((item: any)=>item['name'])"
          :students="_class['students']" 
          :program="_class['program']"
          :students_year="_class['students_year']"
          />
      </div>
      <div class="component-wrapper"
        :class="{ 'is-active-component': elementsStore.activePage === 'AdminLinkedClases' }">
        <AdminLinkedClasses />
      </div>
      <div class="component-wrapper" v-if="userAuthStore.adminData.staff?.length > 0"
        :class="{ 'is-active-component': elementsStore.activePage === 'AdminStaff' }">
        <AdminStaff />
      </div>
      <div class="component-wrapper" :class="{ 'is-active-component': elementsStore.activePage === 'Help' }">
        <HelpForm v-show="elementsStore.activePage === 'Help'" />
      </div>
    </div>

    <!-- Teacher/Hod -->
    <div class="pages-container" v-if="['teacher', 'hod'].includes(userAuthStore.userData['staff_role'].toLowerCase())">
      <div class="component-wrapper"
        v-if="!userAuthStore.staffData.courseWork || userAuthStore.staffData.courseWork?.length === 0">
        <TeacherCourseWork
          :class="{ 'is-active-component': elementsStore.activePage.split(',')[0] === 'TeacherCoursework' }" />
      </div>
      <div class="component-wrapper" 
        :class="{ 'is-active-component': elementsStore.activePage === 'TeacherDepartment' }"
        v-if="userAuthStore.userData['department']">
        <TeacherDepartment/>
      </div>
      <div class="component-wrapper" v-if="userAuthStore.staffData.courseWork?.length > 0"
        :class="{ 'is-active-component': elementsStore.activePage.split(',')[0] === 'TeacherCoursework' }">
        <TeacherCourseWork v-for="(course, index) in userAuthStore.staffData.courseWork"
          :key="`${course['students_class']['name']}${index}`" :className="course['students_class']['name']"
          :classIndex="index" :subjects="course['subjects']"
          :students="course['students_class']['students']" />
      </div>

      <div class="component-wrapper" v-if="userAuthStore.staffData.studentsattendance?.length > 0"
        :class="{ 'is-active-component': elementsStore.activePage.split(',')[0] === 'TeacherStudentsAttendance' }">
        <TeacherStudentsAttendance v-for="(_class, index) in userAuthStore.staffData.studentsattendance"
          :key="`${_class['name']}${index}`" :className="_class['class_name']" :classIndex="index"
          :students="_class['students']" />
      </div>

      <div class="component-wrapper" v-if="userAuthStore.staffData.studentsAssessments?.length > 0"
        :class="{ 'is-active-component': elementsStore.activePage.split(',')[0] === 'TeacherStudentsAssessments' }">
        <div class="component-wrapper" v-for="(_class, index) in userAuthStore.staffData.studentsAssessments"
          :key="`${_class['class_name']}${index}`">
          <div class="component-wrapper" v-for="(_course, ind) in _class['assignments']"
            :key="`${_class['class_name']}${_course['subject']}${ind}`">
            <TeacherStudentsAssessments v-for="(_assessment, i) in _course['assessments']"
              :key="`${_class['class_name']}${_course['subject']}${_assessment['title']}${i}`"
              :className="_class['class_name']" :classIndex="index" :subjectName="_course['subject']"
              :subjectIndex="ind" :assessment="_assessment" :assessmentIndex="i" />
          </div>
        </div>
      </div>

      <div class="component-wrapper" v-if="userAuthStore.staffData.studentsExams?.length > 0"
        :class="{ 'is-active-component': elementsStore.activePage.split(',')[0] === 'TeacherStudentsExams' }">
        <div class="component-wrapper" v-for="(_class, index) in userAuthStore.staffData.studentsExams"
          :key="`${_class['class_name']}${index}`">
          <TeacherStudentsExams v-for="(_subject, ind) in _class['exams']" :key="`${_subject['subject']}${ind}`"
            :className="_class['class_name']" :classIndex="index" :subjectName="_subject['subject']" :subjectIndex="ind"
            :examsData="_subject" />
        </div>
      </div>

      <div class="component-wrapper" v-if="userAuthStore.staffData.studentsResults?.length > 0"
        :class="{ 'is-active-component': elementsStore.activePage.split(',')[0] === 'TeacherStudentsResults' }">
        <div class="component-wrapper" v-for="(_class, index) in userAuthStore.staffData.studentsResults"
          :key="`${_class['class_name']}${index}`">
          <TeacherStudentsResults v-for="(_subject, ind) in _class['results']" :key="`${_subject['subject']}${ind}`"
            :className="_class['class_name']" :classIndex="index" :subjectName="_subject['subject']" :subjectIndex="ind"
            :resultData="_subject" />
        </div>
      </div>

      <div class="component-wrapper" :class="{ 'is-active-component': elementsStore.activePage === 'Help' }">
        <HelpForm v-show="elementsStore.activePage === 'Help'" />
      </div>
    </div>
  </main>
  <TheFooter v-if="userAuthStore.userData" />
</template>

<style scoped>
.welcome-overlay {
  display: flex;
  position: absolute;
  align-items: center;
  justify-content: center;
  height: 100%;
  z-index: 10;
  width: 100%;
  background-color: rgba(0, 0, 0, 0.5);
}

.card {
  width: 90%;
  max-width: 800px;
  display: flex;
  align-items: center !important;
  justify-content: center !important;
}

.form-message {
  font-size: .7rem;
  margin-top: 1em;
  margin-bottom: 1em;
  text-align: center;
  border: 1px solid;
  padding: .1em 1em;
}

.form-text-field {
  margin-top: 1em;
  width: 300px !important;
  max-width: 300px !important;
}


#school-name {
  font-size: .7rem;
  font-family: Verdana, "sans-serif";
  text-align: center;
  font-weight: bold;
  text-transform: uppercase;
  color: #007bff;
}

.overlay-btn {
  background-color: lightseagreen;
  color: white;
}

.overlay-btn:hover {
  background-color: mediumseagreen;
  color: yellow;
}
</style>
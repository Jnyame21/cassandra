<script setup lang="ts">
import { useUserAuthStore } from '@/stores/userAuthStore'
import { useElementsStore } from '@/stores/elementsStore'
import { ref, watch } from 'vue'
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
import TeacherStaff from '@/components/TeacherStaff.vue';
import AdminAcademicYears from '@/components/AdminAcademicYears.vue';
import AdminStudentsClass from '@/components/AdminStudentsClass.vue';
import AdminStaff from '@/components/AdminStaff.vue';
import AdminSubjectAssignment from '@/components/AdminSubjectAssignment.vue';
import { headRoles } from '@/utils/util';
import HeadOverview from '@/components/HeadOverview.vue';
import HeadStaff from '@/components/HeadStaff.vue';
import HeadStudents from '@/components/HeadStudents.vue';
import AdminDepartments from '@/components/AdminDepartments.vue';
import AdminReleasedResults from '@/components/AdminReleasedResults.vue';
import TeacherDepartment from '@/components/TeacherDepartment.vue';

useHead({
  meta: [
    { name: "robots", content: "no-index" }
  ],
})

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()
const password = ref('')
const repeatPassword = ref('')
const passwordVisible = ref(false)
const repeatPasswordVisible = ref(false)

watch(() => userAuthStore.userData, (newValue) => {
  if (newValue && newValue['staff_role'].toLowerCase() === 'administrator') {
    elementsStore.activePage = 'AdminStaff'
  }
  else if (newValue && ['teacher', 'hod'].includes(userAuthStore.userData?.['staff_role'].toLowerCase())) {
    elementsStore.activePage = 'TeacherStaff'
  }
  else if (newValue && headRoles.includes(userAuthStore.userData?.['staff_role'].toLowerCase())) {
    elementsStore.activePage = 'HeadOverview'
  }
}, { 'once': true, 'immediate': true })

const resetUserPassword = async () => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('password', password.value)

  try {
    await axiosInstance.post('user/reset-password', formData)
    userAuthStore.additionalLocalStorageData.password_reset = false
    closeOverlay('StaffWelcomeOverlay')
    elementsStore.HideLoadingOverlay()
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

const closeOverlay = (element: string)=>{
  const overlay = document.getElementById(element)
  if (overlay){
    overlay.style.display = 'none'
  }
}


</script>

<template>

  <!-- Welcome Overlay-->
  <div id="StaffWelcomeOverlay" class="overlay" v-if="userAuthStore.userData?.['role'].toLowerCase() === 'staff' && userAuthStore.additionalLocalStorageData.password_reset">
    <div class="overlay-card">
      <div class="overlay-card-info-container">
        <p style="text-align: center" class="mb-5">
          <strong>Welcome {{ userAuthStore.userData['first_name'] }} {{ userAuthStore.userData['last_name'] }}! Reset your password to continue</strong>
        </p>
      </div>
      <div class="overlay-card-content-container">
        <v-text-field class="input-field" :append-inner-icon="passwordVisible ? 'mdi-eye-off-outline' : 'mdi-eye-outline'" @click:append-inner="passwordVisible = !passwordVisible"
          :type="passwordVisible ? 'text' : 'password'" clearable density="comfortable" v-model="password" label="NEW PASSWORD" hint="Enter a new password"  prepend-inner-icon="mdi-lock-outline"
        />
        <v-text-field class="input-field" :append-inner-icon="repeatPasswordVisible ? 'mdi-eye-off-outline' : 'mdi-eye-outline'" @click:append-inner="repeatPasswordVisible = !repeatPasswordVisible"
          :type="repeatPasswordVisible ? 'text' : 'password'" clearable density="comfortable" v-model="repeatPassword" label="REPEAT PASSWORD" hint="Repeat the new password"  prepend-inner-icon="mdi-lock-outline"
        />
      </div>
    </div>
    <div class="overlay-card-action-btn-container">
      <v-btn @click="resetUserPassword"
        :disabled="!(password && repeatPassword && password === repeatPassword)" :ripple="false"
        variant="flat" type="submit" color="black" size="small" append-icon="mdi-checkbox-marked-circle">
        SUBMIT
      </v-btn>
    </div>
  </div>

  <TheHeader v-if="userAuthStore.userData" />
  <main class="main" v-if="userAuthStore.userData">
    <StaffNavContainerMob v-if="!elementsStore.onDesk" />
    <StaffNavContainerDesk v-if="elementsStore.onDesk" />

    <!-- Admin -->
    <div class="pages-container" v-if="userAuthStore.userData['staff_role'].toLowerCase() === 'administrator'">
      <div class="component-wrapper" :class="{ 'is-active-component': elementsStore.activePage === 'AdminStaff' }">
        <AdminStaff />
      </div>

      <div class="component-wrapper" :class="{ 'is-active-component': elementsStore.activePage === 'AdminDepartments' }">
        <AdminDepartments />
      </div>

      <div class="component-wrapper" :class="{ 'is-active-component': elementsStore.activePage === 'AdminAcademicYears' }">
        <AdminAcademicYears />
      </div>

      <div class="component-wrapper" :class="{ 'is-active-component': elementsStore.activePage.split(',')[0] === 'AdminStudentsClass' }">
        <AdminStudentsClass v-for="(_class, index) in userAuthStore.adminData.classes"
          :key="`${_class['name']}${index}`" :className="_class['name']" :classIndex="index"
          :subjects="_class['subjects']" :program="_class['program']"
          :students_year="_class['students_year']" 
        />
      </div>

      <div class="component-wrapper" v-if="!userAuthStore.userData['current_role']['level']['has_departments']" :class="{ 'is-active-component': elementsStore.activePage === 'AdminSubjectAssignment' }">
        <AdminSubjectAssignment />
      </div>

      <div class="component-wrapper" :class="{ 'is-active-component': elementsStore.activePage === 'AdminReleasedResults' }">
        <AdminReleasedResults />
      </div>

      <div class="component-wrapper" :class="{ 'is-active-component': elementsStore.activePage === 'Help' }">
        <HelpForm v-show="elementsStore.activePage === 'Help'" />
      </div>
    </div>

    <!-- Head -->
    <div class="pages-container" v-if="headRoles.includes(userAuthStore.userData['staff_role'].toLowerCase())">
      <div class="component-wrapper" :class="{ 'is-active-component': elementsStore.activePage === 'HeadOverview' }">
        <HeadOverview />
      </div>

      <div class="component-wrapper" :class="{ 'is-active-component': elementsStore.activePage === 'HeadStaff' }">
        <HeadStaff />
      </div>

      <div class="component-wrapper"
        :class="{ 'is-active-component': elementsStore.activePage.split(',')[0] === 'HeadStudents' }">
        <HeadStudents v-for="class_name in Object.keys(userAuthStore.headData.classes || {})" :key="class_name"
          :className="class_name" />
      </div>

      <div class="component-wrapper" :class="{ 'is-active-component': elementsStore.activePage === 'Help' }">
        <HelpForm v-show="elementsStore.activePage === 'Help'" />
      </div>

    </div>

    <!-- Teacher/Hod -->
    <div class="pages-container" v-if="['teacher', 'hod'].includes(userAuthStore.userData['staff_role'].toLowerCase())">

      <div class="component-wrapper" v-if="Object.keys(userAuthStore.teacherData.courseWork).length > 0" :class="{ 'is-active-component': elementsStore.activePage.split(',')[0] === 'TeacherCoursework' }">
        <TeacherCourseWork v-for="class_name in Object.keys(userAuthStore.teacherData.courseWork)" 
          :key="class_name" 
          :className="class_name"
        />
      </div>

      <div class="component-wrapper" :class="{ 'is-active-component': elementsStore.activePage === 'TeacherStaff' }">
        <TeacherStaff />
      </div>

      <div class="component-wrapper" :class="{ 'is-active-component': elementsStore.activePage === 'TeacherDepartment' }">
        <TeacherDepartment />
      </div>

      <div class="component-wrapper" v-if="Object.keys(userAuthStore.teacherData.studentsAttendance).length > 0"
        :class="{ 'is-active-component': elementsStore.activePage.split(',')[0] === 'TeacherStudentsAttendance' }">
        <TeacherStudentsAttendance v-for="class_name in Object.keys(userAuthStore.teacherData.studentsAttendance)"
          :key="class_name" :className="class_name" />
      </div>

      <div class="component-wrapper" v-if="Object.keys(userAuthStore.teacherData.studentsAssessments || {}).length > 0"
        :class="{ 'is-active-component': elementsStore.activePage.split(',')[0] === 'TeacherStudentsAssessments' }">
        <div class="component-wrapper"
          v-for="[class_name, class_data] in Object.entries(userAuthStore.teacherData.studentsAssessments)"
          :key="class_name">
          <div class="component-wrapper" v-for="[subject_name, subject_data] in Object.entries(class_data)"
            :key="subject_name">
            <TeacherStudentsAssessments v-for="assessment_title in Object.keys(subject_data)" :key="assessment_title"
              :className="class_name" :subjectName="subject_name" :assessmentTitle="assessment_title" />
          </div>
        </div>
      </div>

      <div class="component-wrapper" v-if="Object.keys(userAuthStore.teacherData.studentsExams || {}).length > 0"
        :class="{ 'is-active-component': elementsStore.activePage.split(',')[0] === 'TeacherStudentsExams' }">
        <div class="component-wrapper"
          v-for="[class_name, class_data] in Object.entries(userAuthStore.teacherData.studentsExams)" :key="class_name">
          <TeacherStudentsExams v-for="subject_name in Object.keys(class_data)" :key="subject_name"
            :className="class_name" :subjectName="subject_name" />
        </div>
      </div>

      <div class="component-wrapper" v-if="Object.keys(userAuthStore.teacherData.studentsResults || {}).length > 0"
        :class="{ 'is-active-component': elementsStore.activePage.split(',')[0] === 'TeacherStudentsResults' }">
        <div class="component-wrapper"
          v-for="[class_name, class_data] in Object.entries(userAuthStore.teacherData.studentsResults)"
          :key="class_name">
          <TeacherStudentsResults v-for="subject_name in Object.keys(class_data)" :key="`${class_name},${subject_name}`"
            :className="class_name" :subjectName="subject_name" />
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

.overlay-card{
  max-width: 600px !important;
}
.overlay-card-info-container{
  margin-top: 3em !important;
}


</style>
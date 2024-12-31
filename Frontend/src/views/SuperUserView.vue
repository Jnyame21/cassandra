<script setup lang="ts">
import { useUserAuthStore } from '@/stores/userAuthStore'
import { useElementsStore } from '@/stores/elementsStore'
import { useHead } from '@vueuse/head';
import TheHeader from '@/components/TheHeader.vue';
import TheFooter from '@/components/TheFooter.vue';
import SuperUserNavContainerDesk from '@/components/SuperUserNavContainerDesk.vue';
import SuperUserNavContainerMob from '@/components/SuperUserNavContainerMob.vue';
import { onBeforeMount } from 'vue';
import SuperUserSchools from '@/components/SuperUserSchools.vue';
import SuperUserLevels from '@/components/SuperUserLevels.vue';
import SuperUserPrograms from '@/components/SuperUserPrograms.vue';
import SuperUserDepartments from '@/components/SuperUserDepartments.vue';
import SuperUserClasses from '@/components/SuperUserClasses.vue';
import SuperUserSubjects from '@/components/SuperUserSubjects.vue';
import SuperUserGradingSystems from '@/components/SuperUserGradingSystems.vue';
import SuperUserGradingSystemRanges from '@/components/SuperUserGradingSystemRanges.vue';
import SuperUserAcademicYears from '@/components/SuperUserAcademicYears.vue';
import SuperUserStaff from '@/components/SuperUserStaff.vue';
import SuperUserStaffRoles from '@/components/SuperUserStaffRoles.vue';

useHead({
  meta: [
    { name: "robots", content: "no-index" }
  ],
})

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()

onBeforeMount(() => {
  elementsStore.activePage = 'SuperUserSchools'
})



</script>


<template>
  <TheHeader v-if="userAuthStore.userData" />
  <main class="main" v-if="userAuthStore.userData">
    <SuperUserNavContainerDesk v-if="elementsStore.onDesk" />
    <SuperUserNavContainerMob v-if="!elementsStore.onDesk" />
    <div class="pages-container">
      <div class="component-wrapper"
        :class="{ 'is-active-component': elementsStore.activePage === 'SuperUserSchools' }">
        <SuperUserSchools />
      </div>

      <div class="component-wrapper" :class="{ 'is-active-component': elementsStore.activePage === 'SuperUserLevels' }">
        <SuperUserLevels />
      </div>

      <div class="component-wrapper"
        :class="{ 'is-active-component': elementsStore.activePage === 'SuperUserSubjects' }">
        <SuperUserSubjects />
      </div>

      <div class="component-wrapper"
        :class="{ 'is-active-component': elementsStore.activePage === 'SuperUserPrograms' }">
        <SuperUserPrograms />
      </div>

      <div class="component-wrapper"
        :class="{ 'is-active-component': elementsStore.activePage === 'SuperUserGradingSystemRanges' }">
        <SuperUserGradingSystemRanges />
      </div>

      <div class="component-wrapper"
        :class="{ 'is-active-component': elementsStore.activePage === 'SuperUserGradingSystems' }">
        <SuperUserGradingSystems />
      </div>

      <div class="component-wrapper" v-if="Object.keys(userAuthStore.superUserData.departments).length > 0"
        :class="{ 'is-active-component': elementsStore.activePage.split(',')[0] === 'SuperUserDepartments' }">
        <SuperUserDepartments v-for="school in Object.keys(userAuthStore.superUserData.departments)" :key="school"
          :schoolIdentifier="school" />
      </div>

      <div class="component-wrapper" v-if="Object.keys(userAuthStore.superUserData.classes).length > 0"
        :class="{ 'is-active-component': elementsStore.activePage.split(',')[0] === 'SuperUserClasses' }">
        <SuperUserClasses v-for="school in Object.keys(userAuthStore.superUserData.classes)" :key="school"
          :schoolIdentifier="school" />
      </div>

      <div class="component-wrapper" v-if="Object.keys(userAuthStore.superUserData.academicYears).length > 0"
        :class="{ 'is-active-component': elementsStore.activePage.split(',')[0] === 'SuperUserAcademicYears' }">
        <SuperUserAcademicYears v-for="school in Object.keys(userAuthStore.superUserData.academicYears)" :key="school"
          :schoolIdentifier="school" />
      </div>

      <div class="component-wrapper"
        :class="{ 'is-active-component': elementsStore.activePage === 'SuperUserStaffRoles' }">
        <SuperUserStaffRoles />
      </div>

      <div class="component-wrapper" v-if="Object.keys(userAuthStore.superUserData.staff).length > 0"
        :class="{ 'is-active-component': elementsStore.activePage.split(',')[0] === 'SuperUserStaff' }">
        <SuperUserStaff v-for="school in Object.keys(userAuthStore.superUserData.staff)" :key="school"
          :schoolIdentifier="school" />
      </div>

      <!-- <div class="component-wrapper" v-if="userAuthStore.studentData.results" :class="{ 'is-active-component': elementsStore.activePage.split(',')[0] === 'StudentResults' }">
        <div v-for="[year_name, year_result_data] in Object.entries(userAuthStore.studentData.results )" :key="year_name">
          <StudentResults v-show="elementsStore.activePage.split(',')[0] === 'StudentResults'" v-for="term_name in Object.keys(year_result_data)"
          :key="term_name"
          :yearName="year_name"
          :termName="term_name"
          />
        </div>
      </div> -->
      <!-- <div class="component-wrapper" v-if="userAuthStore.studentData.attendances" :class="{ 'is-active-component': elementsStore.activePage.split(',')[0] === 'StudentAttendance' }">
        <div v-for="[year_name, year_attendance_data] in Object.entries(userAuthStore.studentData.attendances)" :key="year_name">
          <StudentAttendance v-show="elementsStore.activePage.split(',')[0] === 'StudentAttendance'" v-for="term_name in Object.keys(year_attendance_data)"
          :key="term_name"
          :yearName="year_name"
          :termName="term_name"
          />
        </div>
      </div>
      <div class="component-wrapper" v-if="userAuthStore.studentData.assessments" :class="{ 'is-active-component': elementsStore.activePage.split(',')[0] === 'StudentAssessments' }">
        <div v-for="[year_name, year_assessment_data] in Object.entries(userAuthStore.studentData.assessments )" :key="year_name">
          <StudentAssessments v-show="elementsStore.activePage.split(',')[0] === 'StudentAssessments'" v-for="term_name in Object.keys(year_assessment_data)"
          :key="term_name"
          :yearName="year_name"
          :termName="term_name"
          />
        </div>
      </div> -->

    </div>
  </main>
  <TheFooter />
</template>

<style scoped></style>

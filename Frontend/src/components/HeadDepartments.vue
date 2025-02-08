<script setup lang="ts">
import { computed, ref } from 'vue';
import { useUserAuthStore } from '@/stores/userAuthStore';
import { useElementsStore } from '@/stores/elementsStore';

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()
const departmentTeachers = ref<{user: string; staff_id: string}[]>([])
const departmentSubjects = ref<string[]>([])


const departments = computed(() => {
  return userAuthStore.headData.departments
})

const showOverlay = (element: string, department_teacher:{user: string; staff_id: string}[], department_subjects:string[]) => {
  departmentTeachers.value = department_teacher
  departmentSubjects.value = department_subjects
  const overlay = document.getElementById(element)
  if (overlay) {
    overlay.style.display = 'flex'
  }
}

const closeOverlay = (element: string) => {
  const overlay = document.getElementById(element)
  if (overlay) {
    overlay.style.display = 'none'
  }
}



</script>

<template>
  <div class="content-wrapper" v-show="elementsStore.activePage === `HeadDepartments`" :class="{ 'is-active-page': elementsStore.activePage === `HeadDepartments` }">

    <!-- department teacher overlay -->
    <div id="HeadDepartmentTeachersOverlay" class="overlay upload">
      <div class="overlay-card">
        <v-btn @click="closeOverlay('HeadDepartmentTeachersOverlay')" color="red" size="small" variant="flat" class="close-btn">
          X
        </v-btn>
        <div class="overlay-card-info-container"></div>
        <div class="overlay-card-content-container">
          <p class="subject-card" v-for="(teacher, index) in departmentTeachers" :key=index>{{teacher.user}}[ {{ teacher.staff_id }} ]</p>
          <p class="no-data" v-if="departmentTeachers.length === 0">NO DATA</p>
        </div>
      </div>
    </div>

    <!-- department subjects overlay -->
    <div id="HeadDepartmentSubjectsOverlay" class="overlay upload">
      <div class="overlay-card">
        <v-btn @click="closeOverlay('HeadDepartmentSubjectsOverlay')" color="red" size="small" variant="flat" class="close-btn">
          X
        </v-btn>
        <div class="overlay-card-info-container"></div>
        <div class="overlay-card-content-container">
          <p class="subject-card" v-for="(subject, index) in departmentSubjects" :key=index>{{subject.split('|')[0]}} ({{subject.split('|')[1]}})</p>
          <p class="no-data" v-if="departmentSubjects.length === 0">NO DATA</p>
        </div>
      </div>
    </div>
    
    <div class="content-header"></div>
    <v-table fixed-header class="table">
      <thead>
        <tr>
          <th class="table-head">NAME</th>
          <th class="table-head">HOD</th>
          <th class="table-head">TEACHERS</th>
          <th class="table-head">SUBJECTS</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(_department, index) in departments" :key="index">
          <td class="table-data">
            {{ _department.name }}
          </td>
          <td class="table-data">
            <v-chip v-if="_department.hod">{{ _department.hod.user }}[ {{ _department.hod.staff_id }} ] </v-chip>
          </td>
          <td class="table-data">
            <v-btn @click="showOverlay('HeadDepartmentTeachersOverlay', _department.teachers, _department.subjects)" color="blue" :size="elementsStore.btnSize1">
              VIEW TEACHERS
            </v-btn>
          </td>
          <td class="table-data">
            <v-btn @click="showOverlay('HeadDepartmentSubjectsOverlay', _department.teachers, _department.subjects)" color="blue" :size="elementsStore.btnSize1">
              VIEW SUBJECTS
            </v-btn>
          </td>
        </tr>
      </tbody>
    </v-table>
  </div>
</template>

<style scoped>


.overlay-card-info-container {
  margin-top: 3em !important;
}

.overlay-card {
  max-width: 600px !important;
}



</style>
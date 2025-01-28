<script setup lang="ts">
import { AxiosError } from 'axios';
import { computed, ref } from 'vue';
import axiosInstance from '@/utils/axiosInstance';
import { useUserAuthStore } from '@/stores/userAuthStore';
import { useElementsStore } from '@/stores/elementsStore';

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()
const staffDepartmentSelected = ref('')
const departmentHODSelected = ref('')
const departmentTeachers = ref<{user: string; staff_id: string}[]>([])
const departmentSubjects = ref<string[]>([])
const departments = computed(() => {
  return userAuthStore.adminData.departments
})


const setDepartmentHOD = async () => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', 'setDepartmentHOD')
  formData.append('departmentHOD', departmentHODSelected.value)
  formData.append('departmentIdentifier', staffDepartmentSelected.value)

  try {
    const response = await axiosInstance.post('school-admin/staff', formData)
    const departmentItem = userAuthStore.adminData.departments.find(item => item.identifier === staffDepartmentSelected.value)
    if (departmentItem) {
      departmentItem.hod = response.data
    }
    closeOverlay('AdminSetDepartmentHODOverlay')
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

const removeDepartmentHOD = async (department_index:number, department_id:number) => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', 'removeDepartmentHOD')
  formData.append('departmentId', department_id.toString())

  try {
    await axiosInstance.post('school-admin/staff', formData)
    userAuthStore.adminData.departments[department_index].hod = null
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

const showOverlay = (element: string, department_teacher:{user: string; staff_id: string}[], department_subjects:string[]) => {
  departmentTeachers.value = department_teacher
  departmentSubjects.value = department_subjects
  const overlay = document.getElementById(element)
  if (overlay) {
    overlay.style.display = 'flex'
  }
}

const closeOverlay = (element: string) => {
  staffDepartmentSelected.value = ''
  departmentHODSelected.value = ''
  const overlay = document.getElementById(element)
  if (overlay) {
    overlay.style.display = 'none'
  }
}



</script>

<template>
  <div class="content-wrapper" v-show="elementsStore.activePage === `AdminDepartments`" :class="{ 'is-active-page': elementsStore.activePage === `AdminDepartments` }">

    <!-- department teacher overlay -->
    <div id="AdminDepartmentTeachersOverlay" class="overlay upload">
      <div class="overlay-card">
        <v-btn @click="closeOverlay('AdminDepartmentTeachersOverlay')" color="red" size="small" variant="flat" class="close-btn">
          X
        </v-btn>
        <div class="overlay-card-info-container"></div>
        <div class="overlay-card-content-container">
          <p class="subject-card" v-for="(teacher, index) in departmentTeachers" :key=index>{{teacher.user}}[ {{ teacher.staff_id }} ]</p>
        </div>
      </div>
    </div>

    <!-- department subjects overlay -->
    <div id="AdminDepartmentSubjectsOverlay" class="overlay upload">
      <div class="overlay-card">
        <v-btn @click="closeOverlay('AdminDepartmentSubjectsOverlay')" color="red" size="small" variant="flat" class="close-btn">
          X
        </v-btn>
        <div class="overlay-card-info-container"></div>
        <div class="overlay-card-content-container">
          <p class="subject-card" v-for="(subjects, index) in departmentSubjects" :key=index>{{subjects}}</p>
        </div>
      </div>
    </div>

    <!-- set department hod overlay -->
    <div id="AdminSetDepartmentHODOverlay" class="overlay">
      <div class="overlay-card edit-overlay">
        <v-btn @click="closeOverlay('AdminSetDepartmentHODOverlay')" color="red" size="small" variant="flat" class="close-btn">
          X
        </v-btn>
        <div class="overlay-card-info-container mb-10">
        </div>
        <div class="overlay-card-content-container">
          <v-select class="select"
            :items="userAuthStore.adminData.departments" label="DEPARTMENT" v-model="staffDepartmentSelected" @update:model-value="() => departmentHODSelected = ''"
            variant="solo-filled" item-title="name" item-value="identifier" density="comfortable" persistent-hint hint="Select the department" clearable
          />
          <v-select class="select"
            :items="userAuthStore.adminData.staff?.filter(item=> item.departments.includes(staffDepartmentSelected)).map(item => ({ 'title': item.user, 'value': item.staff_id }))" label="STAFF"
            v-model="departmentHODSelected" variant="solo-filled" item-title="title" item-value="value" density="comfortable" persistent-hint hint="Select the staff you want to set as the HOD" clearable >
            <template v-slot:item="{ props, item }">
              <v-list-item v-bind="props" :subtitle="item.raw.value"></v-list-item>
            </template>
          </v-select>
        </div>
        <div class="overlay-card-action-btn-container">
          <v-btn @click="setDepartmentHOD()" :disabled="!(departmentHODSelected && staffDepartmentSelected)" :ripple="false" variant="flat"
            type="submit" color="black" size="small" append-icon="mdi-checkbox-marked-circle">
            SUBMIT
          </v-btn>
        </div>
      </div>
    </div>
    <div class="content-header">
      <v-btn v-if="userAuthStore.userData['current_role']['level']['has_departments']" @click="showOverlay('AdminSetDepartmentHODOverlay', [], [])" color="blue" :size="elementsStore.btnSize1">
        SET DEPARTMENT HOD
      </v-btn>
    </div>
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
            <v-chip v-if="_department.hod">{{ _department.hod.user }}[ {{ _department.hod.staff_id }} ] </v-chip><v-icon v-if="_department.hod" @click="elementsStore.ShowDeletionOverlay(()=>removeDepartmentHOD(index, _department.id), 'Are you sure you want to remove the HOD of the selected department?')" icon="mdi-delete" color="red" size="small" />
          </td>
          <td class="table-data">
            <v-btn @click="showOverlay('AdminDepartmentTeachersOverlay', _department.teachers, _department.subjects)" color="blue" :size="elementsStore.btnSize1">
              VIEW TEACHERS
            </v-btn>
          </td>
          <td class="table-data">
            <v-btn @click="showOverlay('AdminDepartmentSubjectsOverlay', _department.teachers, _department.subjects)" color="blue" :size="elementsStore.btnSize1">
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
<script setup lang="ts">
import axiosInstance from '../utils/axiosInstance';
import { AxiosError } from 'axios';
import { useUserAuthStore } from '@/stores/userAuthStore'
import { useElementsStore } from '@/stores/elementsStore'
import { computed, ref } from 'vue'
const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()
const formErrorMessage = ref('')
const departmentName = ref('')
const departmentLevelIdentifer = ref('')
const departmentSubjectIdentifersSelected = ref<string[]>([])
const departmentIndex: any = ref(null)
const departmentId = ref('')
const addRemoveType = ref('')
const subjectOptions = ref<string[]>([])

interface Props {
  schoolIdentifier: string;
}
const props = defineProps<Props>()
const schoolIdentifier = props.schoolIdentifier

const departments = computed(() => {
  return userAuthStore.superUserData.departments[schoolIdentifier]
})

const createDepartment = async () => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', 'create')
  formData.append('name', departmentName.value);
  formData.append('levelIdentifier', departmentLevelIdentifer.value);
  formData.append('schoolIdentifier', schoolIdentifier);

  try {
    const response = await axiosInstance.post('superuser/departments', formData)
    userAuthStore.superUserData.departments[schoolIdentifier].unshift(response.data)
    departmentName.value = ''
    elementsStore.HideLoadingOverlay()
    elementsStore.ShowOverlay('Operation successful!', 'green', null, null)
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

const addRemoveSubject = async () => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', addRemoveType.value)
  formData.append('departmentId', departmentId.value);
  formData.append('subjectIdentifiers', JSON.stringify(departmentSubjectIdentifersSelected.value));

  try {
    await axiosInstance.post('superuser/departments', formData)
    if (addRemoveType.value === 'addSubject') {
      departmentSubjectIdentifersSelected.value.forEach(item => userAuthStore.superUserData.departments[schoolIdentifier][departmentIndex.value].subjects.push(item))
    }
    else if (addRemoveType.value === 'removeSubject') {
      departmentSubjectIdentifersSelected.value.forEach(item => userAuthStore.superUserData.departments[schoolIdentifier][departmentIndex.value].subjects.splice(userAuthStore.superUserData.departments[schoolIdentifier][departmentIndex.value].subjects.indexOf(item), 1))
    }
    departmentId.value = ''
    departmentSubjectIdentifersSelected.value = []
    departmentIndex.value = null
    closeOverlay(`SuperUserAddRemoveSubjectFromDepartmentOverlay,${schoolIdentifier}`)
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

const deletedepartment = async (index: number, department_id: string) => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', 'delete')
  formData.append('id', department_id);

  try {
    await axiosInstance.post('superuser/departments', formData)
    userAuthStore.superUserData.departments[schoolIdentifier].splice(index, 1)
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


const closeOverlay = (element: string) => {
  const overlay = document.getElementById(element)
  if (overlay) {
    overlay.style.display = 'none'
  }
}

const showOverlay = (element: string, type_option: string = '', department_index: number = 0, department_id: string = '', subjects: string[] = []) => {
  addRemoveType.value = type_option
  departmentIndex.value = department_index
  departmentId.value = department_id
  subjectOptions.value = subjects
  const overlay = document.getElementById(element)
  if (overlay) {
    overlay.style.display = 'flex'
  }
}


</script>

<template>
  <div class="content-wrapper" v-show="elementsStore.activePage === `SuperUserDepartments,${schoolIdentifier}`"
    :class="{ 'is-active-page': elementsStore.activePage === `SuperUserDepartments,${schoolIdentifier}` }">

    <!-- department subjects overlay -->
    <div :id="`SuperUserSubjectsUnderDepartmentOverlay,${schoolIdentifier}`" class="overlay upload">
      <div class="overlay-card">
        <v-btn @click="closeOverlay(`SuperUserSubjectsUnderDepartmentOverlay,${schoolIdentifier}`)" color="red"
          size="small" variant="flat" class="close-btn">
          X
        </v-btn>
        <div class="overlay-card-content-container">
          <p class="subject-card" v-for="(subject, index) in subjectOptions" :key=index>{{ subject }}</p>
        </div>
      </div>
    </div>

    <!-- department creation overlay -->
    <div :id="`SuperUserCreatedepartmentOverlay,${schoolIdentifier}`" class="overlay upload">
      <div class="overlay-card">
        <v-btn @click="closeOverlay(`SuperUserCreatedepartmentOverlay,${schoolIdentifier}`)" color="red" size="small"
          variant="flat" class="close-btn">
          X
        </v-btn>
        <div class="overlay-card-content-container">
          <v-text-field class="input-field" v-model="departmentName" label="NAME" clearable />
          <v-select class="select" :items="userAuthStore.superUserData.levels.map(item => item.identifier)"
            label="LEVEL" v-model="departmentLevelIdentifer" density="comfortable" persistent-hint
            hint="Select the level" variant="solo-filled" clearable />
        </div>
        <div class="overlay-card-action-btn-container">
          <v-btn @click="createDepartment" :disabled="!(departmentName && departmentLevelIdentifer)" :ripple="false"
            variant="flat" type="submit" color="black" size="small" append-icon="mdi-checkbox-marked-circle">
            SUBMIT
          </v-btn>
        </div>
      </div>
    </div>

    <!-- add/remove subject from department overlay -->
    <div :id="`SuperUserAddRemoveSubjectFromDepartmentOverlay,${schoolIdentifier}`" class="overlay upload">
      <div class="overlay-card">
        <v-btn @click="closeOverlay(`SuperUserAddRemoveSubjectFromDepartmentOverlay,${schoolIdentifier}`)" color="red"
          size="small" variant="flat" class="close-btn">
          X
        </v-btn>
        <p class="form-error-message" v-if="formErrorMessage" style="color: red">{{ formErrorMessage }}</p>
        <div class="overlay-card-content-container">
          <v-select class="select" v-if="addRemoveType === 'addSubject'" :items="subjectOptions" label="SUBJECT"
            v-model="departmentSubjectIdentifersSelected" variant="solo-filled" multiple density="comfortable"
            persistent-hint hint="Select the subject you want to add" clearable />
          <v-select class="select" v-if="addRemoveType === 'removeSubject'" :items="subjectOptions" multiple
            label="SUBJECT" v-model="departmentSubjectIdentifersSelected" variant="solo-filled" density="comfortable"
            persistent-hint hint="Select the subject you want to remove" clearable />
        </div>
        <div class="overlay-card-action-btn-container">
          <v-btn @click="addRemoveSubject" :disabled="!(departmentSubjectIdentifersSelected.length > 0)" :ripple="false"
            variant="flat" type="submit" color="black" size="small" append-icon="mdi-checkbox-marked-circle">
            SUBMIT
          </v-btn>
        </div>
      </div>
    </div>
    <div class="content-header">
      <v-btn @click="showOverlay(`SuperUserCreatedepartmentOverlay,${schoolIdentifier}`)" color="blue"
        :size="elementsStore.btnSize1">
        CREATE DEPARTMENT
      </v-btn>
    </div>
    <div class="no-data" v-if="departments.length === 0">
      <p>NO DATA</p>
    </div>
    <v-table fixed-header class="table" v-if="departments.length > 0">
      <thead>
        <tr>
          <th class="table-head">NAME</th>
          <th class="table-head">LEVEL</th>
          <th class="table-head">IDENTIFIER</th>
          <th class="table-head">SUBJECTS</th>
          <th class="table-head">HOD</th>
          <th class="table-head">ACTION</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(department, index) in departments" :key="index">
          <td class="table-data">{{ department.name }}</td>
          <td class="table-data">{{ department.level }}</td>
          <td class="table-data">{{ department.identifier }}</td>
          <td class="table-data">
            <v-btn
              @click="showOverlay(`SuperUserSubjectsUnderDepartmentOverlay,${schoolIdentifier}`, '', 0, '', department.subjects)"
              variant="flat" size="x-small" color="blue">
              VIEW SUBJECTS
            </v-btn>
          </td>
          <td class="table-data">
            <span v-if="department.hod">{{ department.hod.user }}[ {{ department.hod.staff_id }} ]</span>
          </td>
          <td class="table-data flex-all" style="display: flex">
            <v-btn class="ml-2" v-if="userAuthStore.superUserData.schools"
              @click="showOverlay(`SuperUserAddRemoveSubjectFromDepartmentOverlay,${schoolIdentifier}`, 'addSubject', index, department.id.toString(), userAuthStore.superUserData.subjects.map(item => item.identifier).filter(item => !department.subjects.includes(item)))"
              variant="flat" icon="mdi-plus" size="x-small" color="blue" />
            <v-btn class="ma-2" v-if="userAuthStore.superUserData.schools"
              @click="showOverlay(`SuperUserAddRemoveSubjectFromDepartmentOverlay,${schoolIdentifier}`, 'removeSubject', index, department.id.toString(), department.subjects)"
              variant="flat" icon="mdi-minus" size="x-small" color="blue" />
            <v-btn class="ma-2"
              @click="elementsStore.ShowDeletionOverlay(() => deletedepartment(index, department.id.toString()), 'Are you sure you want to delete this department. The process cannot be reversed')"
              variant="flat" icon="mdi-delete" size="x-small" color="red" />
          </td>
        </tr>
      </tbody>
    </v-table>
  </div>
</template>

<style scoped>
.overlay-card {
  max-width: 600px !important;
}

.overlay-card-content-container {
  margin-top: 3em !important;
}
</style>
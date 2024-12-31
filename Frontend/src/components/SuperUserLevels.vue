<script setup lang="ts">
import axiosInstance from '../utils/axiosInstance';
import { AxiosError } from 'axios';
import { useUserAuthStore } from '@/stores/userAuthStore'
import { useElementsStore } from '@/stores/elementsStore'
import { computed, ref } from 'vue'
const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()
const levelName = ref('')
const yearsToComplete = ref('')
const hasDepartments = ref(false)
const hasPrograms = ref(false)
const studentsId = ref(false)
const studentsIndexNo = ref(false)
const levelIdentifier = ref('')
const levelIndex: any = ref(null)
const levelSchoolIdentifier = ref('')
const addRemoveType = ref('')
const schoolOptions = ref<string[]>([])

const levels = computed(() => {
  return userAuthStore.superUserData.levels
})

const createLevel = async () => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', 'create')
  formData.append('name', levelName.value);
  formData.append('yearsToComplete', yearsToComplete.value);
  formData.append('hasDepartments', JSON.stringify(hasDepartments.value));
  formData.append('hasPrograms', JSON.stringify(hasPrograms.value));
  formData.append('studentsId', JSON.stringify(studentsId.value));
  formData.append('studentsIndexNo', JSON.stringify(studentsIndexNo.value));

  try {
    const response = await axiosInstance.post('superuser/levels', formData)
    userAuthStore.superUserData.levels.unshift(response.data)
    elementsStore.HideLoadingOverlay()
    levelName.value = ''
    yearsToComplete.value = ''
    hasDepartments.value = false
    hasPrograms.value = false
    studentsId.value = false
    studentsIndexNo.value = false
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

const addRemoveSchool = async () => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', addRemoveType.value)
  formData.append('levelIdentifier', levelIdentifier.value);
  formData.append('schoolIdentifier', levelSchoolIdentifier.value);

  try {
    await axiosInstance.post('superuser/levels', formData)
    if (addRemoveType.value === 'addSchool') {
      userAuthStore.superUserData.levels[levelIndex.value]?.schools.unshift(levelSchoolIdentifier.value)
    }
    else if (addRemoveType.value === 'removeSchool') {
      userAuthStore.superUserData.levels[levelIndex.value]?.schools.splice(userAuthStore.superUserData.levels[levelIndex.value]?.schools.indexOf(levelSchoolIdentifier.value), 1)
    }
    levelIdentifier.value = ''
    levelSchoolIdentifier.value = ''
    levelIndex.value = null
    closeOverlay('SuperUserAddRemoveSchoolFromLevelOverlay')
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

const deleteLevel = async (index: number, level_identifier: string) => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', 'delete')
  formData.append('identifier', level_identifier);

  try {
    await axiosInstance.post('superuser/levels', formData)
    userAuthStore.superUserData.levels.splice(index, 1)
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

const showOverlay = (element: string, type_options: string = '', level_index: number = 0, level_identifier: string = '', schools: string[] = []) => {
  addRemoveType.value = type_options
  levelIndex.value = level_index
  levelIdentifier.value = level_identifier
  schoolOptions.value = schools
  const overlay = document.getElementById(element)
  if (overlay) {
    overlay.style.display = 'flex'
  }
}


</script>

<template>
  <div class="content-wrapper" v-show="elementsStore.activePage === 'SuperUserLevels'"
    :class="{ 'is-active-page': elementsStore.activePage === 'SuperUserLevels' }">

    <!-- level schools overlay -->
    <div id="SuperUserSchoolsUnderLevelOverlay" class="overlay upload">
      <div class="overlay-card">
        <v-btn @click="closeOverlay('SuperUserSchoolsUnderLevelOverlay')" color="red" size="small" variant="flat"
          class="close-btn">
          X
        </v-btn>
        <div class="overlay-card-content-container">
          <p class="subject-card" v-for="(school, index) in schoolOptions" :key=index>{{ school }}</p>
        </div>
      </div>
    </div>

    <!-- level creation overlay -->
    <div id="SuperUserCreateLevelOverlay" class="overlay upload">
      <div class="overlay-card">
        <v-btn @click="closeOverlay('SuperUserCreateLevelOverlay')" color="red" size="small" variant="flat"
          class="close-btn">
          X
        </v-btn>
        <div class="overlay-card-content-container">
          <v-text-field class="input-field" v-model="levelName" label="NAME" clearable />
          <v-text-field class="input-field" v-model.number="yearsToComplete" type="number" label="YEARS TO COMPLETE"
            clearable />
          <v-checkbox class="select" v-model="hasDepartments" label="HAS DEPARTMENT" color="blue" />
          <v-checkbox class="select" v-model="hasPrograms" label="HAS PROGRAMS" color="blue" />
          <v-checkbox class="select" v-model="studentsId" label="STUDENTS ID" color="blue" />
          <v-checkbox class="select" v-model="studentsIndexNo" label="STUDENTS INDEX NO" color="blue" />
        </div>
        <div class="overlay-card-action-btn-container">
          <v-btn @click="createLevel" :disabled="!(levelName && yearsToComplete)" :ripple="false" variant="flat"
            type="submit" color="black" size="small" append-icon="mdi-checkbox-marked-circle">
            SUBMIT
          </v-btn>
        </div>
      </div>
    </div>

    <!-- add/remove creation overlay -->
    <div id="SuperUserAddRemoveSchoolFromLevelOverlay" class="overlay upload">
      <div class="overlay-card">
        <v-btn @click="closeOverlay('SuperUserAddRemoveSchoolFromLevelOverlay')" color="red" size="small" variant="flat"
          class="close-btn">
          X
        </v-btn>
        <div class="overlay-card-content-container">
          <v-select class="select" v-if="addRemoveType === 'addSchool'" :items="schoolOptions" label="SCHOOL"
            v-model="levelSchoolIdentifier" variant="solo-filled" density="comfortable" persistent-hint
            hint="Select the school you want to add" clearable />
          <v-select class="select" v-if="addRemoveType === 'removeSchool'" :items="schoolOptions" label="SCHOOL"
            v-model="levelSchoolIdentifier" variant="solo-filled" density="comfortable" persistent-hint
            hint="Select the school you want to remove" clearable />
        </div>
        <div class="overlay-card-action-btn-container">
          <v-btn @click="addRemoveSchool" :disabled="!levelSchoolIdentifier" :ripple="false" variant="flat"
            type="submit" color="black" size="small" append-icon="mdi-checkbox-marked-circle">
            SUBMIT
          </v-btn>
        </div>
      </div>
    </div>
    <div class="content-header">
      <v-btn @click="showOverlay('SuperUserCreateLevelOverlay')" color="blue" :size="elementsStore.btnSize1">
        CREATE LEVEL
      </v-btn>
    </div>
    <div class="no-data" v-if="levels.length === 0">
      <p>NO DATA</p>
    </div>
    <v-table fixed-header class="table" v-if="levels.length > 0">
      <thead>
        <tr>
          <th class="table-head">NAME</th>
          <th class="table-head">IDENTIFIER</th>
          <th class="table-head">YEARS TO COMPLETE</th>
          <th class="table-head">SCHOOLS</th>
          <th class="table-head">HAS DEPARTMENT</th>
          <th class="table-head">HAS PROGRAMS</th>
          <th class="table-head">STUDENTS ID</th>
          <th class="table-head">STUDENTS INDEX NO</th>
          <th class="table-head">ACTION</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(level, index) in levels" :key="index">
          <td class="table-data">{{ level.name }}</td>
          <td class="table-data">{{ level.identifier }}</td>
          <td class="table-data">{{ level.years_to_complete }}</td>
          <td class="table-data">
            <v-btn @click="showOverlay('SuperUserSchoolsUnderLevelOverlay', '', 0, '', level.schools)" variant="flat"
              size="x-small" color="blue">
              VIEW SCHOOLS
            </v-btn>
          </td>
          <td class="table-data">
            <v-checkbox-btn color="blue" v-model="level.has_departments" disabled />
          </td>
          <td class="table-data">
            <v-checkbox-btn color="blue" v-model="level.has_programs" disabled />
          </td>
          <td class="table-data">
            <v-checkbox-btn color="blue" v-model="level.students_id" disabled />
          </td>
          <td class="table-data">
            <v-checkbox-btn color="blue" v-model="level.students_index_no" disabled />
          </td>
          <td class="table-data flex-all" style="display: flex">
            <v-btn class="ml-2" v-if="userAuthStore.superUserData.schools"
              @click="showOverlay('SuperUserAddRemoveSchoolFromLevelOverlay', 'addSchool', index, level.identifier, userAuthStore.superUserData.schools.map(item => item.identifier).filter(item => !level.schools.includes(item)))"
              variant="flat" icon="mdi-plus" size="x-small" color="blue" />
            <v-btn class="ma-2"
              @click="showOverlay('SuperUserAddRemoveSchoolFromLevelOverlay', 'removeSchool', index, level.identifier, level.schools)"
              variant="flat" icon="mdi-minus" size="x-small" color="blue" />
            <v-btn class="ma-2"
              @click="elementsStore.ShowDeletionOverlay(() => deleteLevel(index, level.identifier), 'Are you sure you want to delete this level. The process cannot be reversed')"
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
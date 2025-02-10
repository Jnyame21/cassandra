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
    elementsStore.ShowOverlay('Operation successful!', 'green')
  }
  catch (error) {
    elementsStore.HideLoadingOverlay()
    if (error instanceof AxiosError) {
      if (error.response) {
        if (error.response.status === 400 && error.response.data.message) {
          elementsStore.ShowOverlay(error.response.data.message, 'red')
        } else {
          elementsStore.ShowOverlay('Oops! something went wrong. Try again later', 'red')
        }
      }
      else if (!error.response && (error.code === 'ECONNABORTED' || !navigator.onLine)) {
        elementsStore.ShowOverlay('A network error occurred! Please check you internet connection', 'red')
      }
      else {
        elementsStore.ShowOverlay('An unexpected error occurred!', 'red')
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
          elementsStore.ShowOverlay(error.response.data.message, 'red')
        } else {
          elementsStore.ShowOverlay('Oops! something went wrong. Try again later', 'red')
        }
      }
      else if (!error.response && (error.code === 'ECONNABORTED' || !navigator.onLine)) {
        elementsStore.ShowOverlay('A network error occurred! Please check you internet connection', 'red')
      }
      else {
        elementsStore.ShowOverlay('An unexpected error occurred!', 'red')
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

const showOverlay = (element: string) => {
  const overlay = document.getElementById(element)
  if (overlay) {
    overlay.style.display = 'flex'
  }
}


</script>

<template>
  <div class="content-wrapper" v-show="elementsStore.activePage === 'SuperUserLevels'" :class="{ 'is-active-page': elementsStore.activePage === 'SuperUserLevels' }">

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
          <v-btn @click="createLevel()" :disabled="!(levelName && yearsToComplete)" :ripple="false" variant="flat"
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
          <th class="table-head">ID</th>
          <th class="table-head">NAME</th>
          <th class="table-head">IDENTIFIER</th>
          <th class="table-head">YEARS TO COMPLETE</th>
          <th class="table-head">HAS DEPARTMENT</th>
          <th class="table-head">HAS PROGRAMS</th>
          <th class="table-head">STUDENTS ID</th>
          <th class="table-head">STUDENTS INDEX NO</th>
          <th class="table-head">ACTION</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(level, index) in levels" :key="index">
          <td class="table-data">{{ level.id }}</td>
          <td class="table-data">
            <v-chip :size="elementsStore.btnSize1">{{ level.name }}</v-chip>
          </td>
          <td class="table-data">
            <v-chip :size="elementsStore.btnSize1">{{ level.identifier }}</v-chip>
          </td>
          <td class="table-data">
            <v-chip :size="elementsStore.btnSize1">{{ level.years_to_complete }}</v-chip>
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
          <td class="table-data">
            <v-btn class="ma-2" @click="elementsStore.ShowDeletionOverlay(() => deleteLevel(index, level.identifier), 'Are you sure you want to delete this level. The process cannot be reversed')"
              variant="flat" icon="mdi-delete" size="x-small" color="red" 
            />
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
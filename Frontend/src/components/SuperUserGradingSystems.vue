<script setup lang="ts">
import axiosInstance from '../utils/axiosInstance';
import { AxiosError } from 'axios';
import { useUserAuthStore } from '@/stores/userAuthStore'
import { useElementsStore } from '@/stores/elementsStore'
import { computed, ref } from 'vue'
const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()
const gradingSystemLevelIdentifierSelected = ref('')
const gradingSystemIndex: any = ref(null)
const gradingSystemId = ref('')
const gradingSystemSchoolIdentifierSelected = ref('')
const gradingSystemRangesSelected = ref<string[]>([])
const addRemoveOptionSelected = ref('')
const addRemoveType = ref('')
const schoolOptions = ref<string[]>([])
const rangeOptions = ref<string[]>([])

const gradingSystems = computed(() => {
  return userAuthStore.superUserData.gradingSystems
})

const createGradingSystem = async () => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', 'create')
  formData.append('levelIdentifier', gradingSystemLevelIdentifierSelected.value);

  try {
    const response = await axiosInstance.post('superuser/grading_systems', formData)
    userAuthStore.superUserData.gradingSystems.unshift(response.data)
    gradingSystemLevelIdentifierSelected.value = ''
    closeOverlay('SuperUserCreateGradingSystemOverlay')
    elementsStore.HideLoadingOverlay()
  }
  catch (error) {
    elementsStore.HideLoadingOverlay()
    if (error instanceof AxiosError) {
      if (error.response) {
        if (error.response.status === 400 && error.response.data.message) {
          elementsStore.ShowOverlay(error.response.data.message, 'red')
        }
        else {
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

const addRemoveSchoolRange = async () => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', addRemoveType.value)
  if (['addSchool', 'removeSchool'].includes(addRemoveType.value)){
    formData.append('gradingSystemId', gradingSystemId.value);
    formData.append('schoolIdentifier', gradingSystemSchoolIdentifierSelected.value);
  }
  else if (['addRange', 'removeRange'].includes(addRemoveType.value)){
    formData.append('gradingSystemId', gradingSystemId.value);
    formData.append('rangesIdentifiers', JSON.stringify(gradingSystemRangesSelected.value));
  }

  try {
    await axiosInstance.post('superuser/grading_systems', formData)
    if (addRemoveType.value === 'addSchool') {
      userAuthStore.superUserData.gradingSystems[gradingSystemIndex.value]?.schools.unshift(gradingSystemSchoolIdentifierSelected.value)
    }
    else if (addRemoveType.value === 'removeSchool') {
      const selectedSchoolIndex = userAuthStore.superUserData.gradingSystems[gradingSystemIndex.value]?.schools.indexOf(gradingSystemSchoolIdentifierSelected.value)
      userAuthStore.superUserData.gradingSystems[gradingSystemIndex.value]?.schools.splice(selectedSchoolIndex, 1)
    }
    else if (addRemoveType.value === 'addRange') {
      gradingSystemRangesSelected.value.forEach(range => {
        userAuthStore.superUserData.gradingSystems[gradingSystemIndex.value]?.ranges.unshift(range)
      })
    }
    else if (addRemoveType.value === 'removeRange') {
      gradingSystemRangesSelected.value.forEach(range => {
        const selectedRangeIndex = userAuthStore.superUserData.gradingSystems[gradingSystemIndex.value]?.ranges.indexOf(range)
        userAuthStore.superUserData.gradingSystems[gradingSystemIndex.value]?.ranges.splice(selectedRangeIndex, 1)
      })
    }
    gradingSystemSchoolIdentifierSelected.value = ''
    gradingSystemIndex.value = null
    gradingSystemId.value = ''
    addRemoveOptionSelected.value = ''
    gradingSystemRangesSelected.value = []
    addRemoveType.value = ''
    closeOverlay('SuperUserAddRemoveSchoolRangeFromGradingSystemOverlay')
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

const deleteGradingSystem = async (index: number, grading_system_id: string) => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', 'delete')
  formData.append('id', grading_system_id);

  try {
    await axiosInstance.post('superuser/grading_systems', formData)
    userAuthStore.superUserData.gradingSystems.splice(index, 1)
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

const isAddRemoveFormValid = computed(()=>{
  if (addRemoveType.value.split('S')[1] === 'chool'){
    return !(gradingSystemSchoolIdentifierSelected.value)
  }
  else if (addRemoveType.value.split('R')[1] === 'ange'){
    return !(gradingSystemRangesSelected.value.length > 0)
  }
  return true;
})

const closeOverlay = (element: string) => {
  const overlay = document.getElementById(element)
  if (overlay) {
    overlay.style.display = 'none'
  }
}

const showOverlay = (element: string, type_option: string = '', grading_system_index: number = 0, grading_system_id: string = '', schools: string[] = [], ranges: string[] = []) => {
  addRemoveType.value = type_option
  gradingSystemRangesSelected.value = []
  gradingSystemSchoolIdentifierSelected.value = ''
  gradingSystemIndex.value = grading_system_index
  gradingSystemId.value = grading_system_id
  schoolOptions.value = schools
  rangeOptions.value = ranges
  const overlay = document.getElementById(element)
  if (overlay) {
    overlay.style.display = 'flex'
  }
}


</script>

<template>
  <div class="content-wrapper" v-show="elementsStore.activePage === 'SuperUserGradingSystems'" :class="{ 'is-active-page': elementsStore.activePage === 'SuperUserGradingSystems' }">

    <!-- gradingSystem schools overlay -->
    <div id="SuperUserSchoolsUnderGradingSystemOverlay" class="overlay upload">
      <div class="overlay-card">
        <v-btn @click="closeOverlay('SuperUserSchoolsUnderGradingSystemOverlay')" color="red" size="small"
          variant="flat" class="close-btn">
          X
        </v-btn>
        <div class="overlay-card-content-container">
          <p class="subject-card" v-for="(school, index) in schoolOptions" :key=index>{{ school }}</p>
        </div>
      </div>
    </div>

    <!-- gradingSystem ranges overlay -->
    <div id="SuperUserRangesUnderGradingSystemOverlay" class="overlay upload">
      <div class="overlay-card">
        <v-btn @click="closeOverlay('SuperUserRangesUnderGradingSystemOverlay')" color="red" size="small" variant="flat"
          class="close-btn">
          X
        </v-btn>
        <div class="overlay-card-content-container">
          <p class="subject-card" v-for="(range, index) in rangeOptions" :key=index>{{ range }}</p>
        </div>
      </div>
    </div>

    <!-- gradingSystem creation overlay -->
    <div id="SuperUserCreateGradingSystemOverlay" class="overlay upload">
      <div class="overlay-card">
        <v-btn @click="closeOverlay('SuperUserCreateGradingSystemOverlay')" color="red" size="small" variant="flat"
          class="close-btn">
          X
        </v-btn>
        <div class="overlay-card-content-container">
          <v-select class="select" :items="userAuthStore.superUserData.levels.map(item => item.identifier)" label="LEVEL" v-model="gradingSystemLevelIdentifierSelected"
            density="comfortable" persistent-hint hint="Select the level" variant="solo-filled" clearable 
          />
        </div>
        <div class="overlay-card-action-btn-container">
          <v-btn @click="createGradingSystem()" :disabled="!(gradingSystemLevelIdentifierSelected)" :ripple="false"
            variant="flat" type="submit" color="black" size="small" append-icon="mdi-checkbox-marked-circle">
            SUBMIT
          </v-btn>
        </div>
      </div>
    </div>

    <!-- add/remove school/range from gradingSystem overlay -->
    <div id="SuperUserAddRemoveSchoolRangeFromGradingSystemOverlay" class="overlay upload">
      <div class="overlay-card">
        <v-btn @click="closeOverlay('SuperUserAddRemoveSchoolRangeFromGradingSystemOverlay')" color="red" size="small"
          variant="flat" class="close-btn">
          X
        </v-btn>
        <div class="overlay-card-content-container">
          <v-select class="select" v-if="addRemoveType === 'addSchool'" :items="schoolOptions" label="SCHOOL" v-model="gradingSystemSchoolIdentifierSelected" variant="solo-filled"
            density="comfortable" persistent-hint hint="Select the school you want to add" clearable 
          />
          <v-select class="select" v-if="addRemoveType === 'removeSchool'" :items="schoolOptions" label="SCHOOL" v-model="gradingSystemSchoolIdentifierSelected" variant="solo-filled"
            density="comfortable" persistent-hint hint="Select the school you want to remove" clearable 
          />
          <v-select class="select" v-if="addRemoveType === 'addRange'" :items="rangeOptions" label="RANGE" v-model="gradingSystemRangesSelected" variant="solo-filled"
            density="comfortable" persistent-hint hint="Select the range you want to add" multiple clearable 
          />
          <v-select class="select" v-if="addRemoveType === 'removeRange'" :items="rangeOptions" label="RANGE" v-model="gradingSystemRangesSelected" variant="solo-filled"
            density="comfortable" persistent-hint hint="Select the range you want to remove" multiple clearable 
          />
        </div>
        <div class="overlay-card-action-btn-container">
          <v-btn @click="addRemoveSchoolRange()" :disabled="isAddRemoveFormValid" :ripple="false"
            variant="flat" type="submit" color="black" size="small" append-icon="mdi-checkbox-marked-circle">
            SUBMIT
          </v-btn>
        </div>
      </div>
    </div>

    <div class="content-header">
      <v-btn @click="showOverlay('SuperUserCreateGradingSystemOverlay')" color="blue" :size="elementsStore.btnSize1">
        CREATE GRADING SYSTEM
      </v-btn>
    </div>
    <div class="no-data" v-if="gradingSystems.length === 0">
      <p>NO DATA</p>
    </div>
    <v-table fixed-header class="table" v-if="gradingSystems.length > 0">
      <thead>
        <tr>
          <th class="table-head">ID</th>
          <th class="table-head">RANGES</th>
          <th class="table-head">LEVEL</th>
          <th class="table-head">SCHOOLS</th>
          <th class="table-head">ACTION</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(gradingSystem, index) in gradingSystems" :key="index">
          <td class="table-data">{{ gradingSystem.id }}</td>
          <td class="table-data">
            <v-btn @click="showOverlay('SuperUserRangesUnderGradingSystemOverlay', '', 0, '', [], gradingSystem.ranges)" variant="flat" size="x-small" color="blue">
              VIEW RANGES
            </v-btn>
            <v-icon class="ml-2" v-if="userAuthStore.superUserData.schools" icon="mdi-plus" color="blue"
              @click="showOverlay('SuperUserAddRemoveSchoolRangeFromGradingSystemOverlay', 'addRange', index, gradingSystem.id.toString(), [], userAuthStore.superUserData.gradingSystemRanges.map(item => item.identifier).filter(item => !gradingSystem.ranges.includes(item)))"
            />
            <v-icon class="ma-2" icon="mdi-minus" color="blue"
              @click="showOverlay('SuperUserAddRemoveSchoolRangeFromGradingSystemOverlay', 'removeRange', index, gradingSystem.id.toString(), [], gradingSystem.ranges)"
            />
          </td>
          <td class="table-data">
            <v-chip :size="elementsStore.btnSize1">{{ gradingSystem.level }}</v-chip>
          </td>
          <td class="table-data">
            <v-btn @click="showOverlay('SuperUserSchoolsUnderGradingSystemOverlay', '', 0, '', gradingSystem.schools)" variant="flat" size="x-small" color="blue">
              VIEW SCHOOLS
            </v-btn>
            <v-icon class="ml-2" v-if="userAuthStore.superUserData.schools" variant="flat" icon="mdi-plus" color="blue"
              @click="showOverlay('SuperUserAddRemoveSchoolRangeFromGradingSystemOverlay', 'addSchool', index, gradingSystem.id.toString(), userAuthStore.superUserData.schools.map(item => item.identifier).filter(item => !gradingSystem.schools.includes(item)), [])"
            />
            <v-icon class="ma-2" variant="flat" icon="mdi-minus" color="blue"
              @click="showOverlay('SuperUserAddRemoveSchoolRangeFromGradingSystemOverlay', 'removeSchool', index, gradingSystem.id.toString(), gradingSystem.schools, [])"
            />
          </td>
          <td class="table-data flex-all" style="display: flex">
            <v-btn class="ma-2" variant="flat" icon="mdi-delete" size="x-small" color="red"
              @click="elementsStore.ShowDeletionOverlay(() => deleteGradingSystem(index, gradingSystem.id.toString()), 'Are you sure you want to delete this grading system. The process cannot be reversed')"
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
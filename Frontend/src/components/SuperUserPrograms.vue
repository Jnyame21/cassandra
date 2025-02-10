<script setup lang="ts">
import axiosInstance from '../utils/axiosInstance';
import { AxiosError } from 'axios';
import { useUserAuthStore } from '@/stores/userAuthStore'
import { useElementsStore } from '@/stores/elementsStore'
import { computed, ref } from 'vue'
const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()
const formErrorMessage = ref('')
const programName = ref('')
const programLevelIdentifer = ref('')
const programSubjectIdentifer = ref('')
const programIndex:any = ref(null)
const programIdentifier = ref('')
const programSchoolIdentifer = ref('')
const addRemoveType = ref('')
const schoolOptions = ref<string[]>([])
const subjectOptions = ref<string[]>([])

const programs = computed(() => {
  return userAuthStore.superUserData.programs
})

const createProgram = async () => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', 'create')
  formData.append('name', programName.value);
  formData.append('levelIdentifier', programLevelIdentifer.value);

  try {
    const response = await axiosInstance.post('superuser/programs', formData)
    userAuthStore.superUserData.programs.unshift(response.data)
    elementsStore.HideLoadingOverlay()
    programName.value = ''
    programLevelIdentifer.value = ''
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

const addRemoveSchoolOrSubject = async () => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', addRemoveType.value)
  formData.append('programIdentifier', programIdentifier.value);
  if (['addSchool', 'removeSchool'].includes(addRemoveType.value)){
    formData.append('schoolIdentifier', programSchoolIdentifer.value);
  }
  else if (['addSubject', 'removeSubject'].includes(addRemoveType.value)){
    formData.append('subjectIdentifier', programSubjectIdentifer.value);
  }

  try {
    await axiosInstance.post('superuser/programs', formData)
    let objectItem = ''
    let objectPointer:any = []
    if (['addSchool', 'removeSchool'].includes(addRemoveType.value)){
      objectItem = programSchoolIdentifer.value
      objectPointer = userAuthStore.superUserData.programs[programIndex.value]?.schools
    }
    else if (['addSubject', 'removeSubject'].includes(addRemoveType.value)){
      objectItem = programSubjectIdentifer.value
      objectPointer = userAuthStore.superUserData.programs[programIndex.value]?.subjects
    }
    if (addRemoveType.value.split('S')[0] === 'add'){
      objectPointer.unshift(objectItem)
    }
    else if (addRemoveType.value.split('S')[0] === 'remove'){
      const objectIndex = objectPointer.indexOf(objectItem)
      objectPointer.splice(objectIndex, 1)
    }
    programIdentifier.value = ''
    programSchoolIdentifer.value = ''
    programSubjectIdentifer.value = ''
    programIndex.value = null
    closeOverlay('SuperUserAddRemoveSchoolOrSubjectFromProgramOverlay')
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

const deleteProgram = async (index: number, program_identifier: string) => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', 'delete')
  formData.append('identifier', program_identifier);

  try {
    await axiosInstance.post('superuser/programs', formData)
    userAuthStore.superUserData.programs.splice(index, 1)
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

const showOverlay = (element: string, type_option:string='', program_index:number=0, program_identifier:string='', schools:string[]=[], subjects:string[]=[]) => {
  addRemoveType.value = type_option
  programIndex.value = program_index
  programIdentifier.value = program_identifier
  schoolOptions.value = schools
  subjectOptions.value = subjects
  const overlay = document.getElementById(element)
  if (overlay) {
    overlay.style.display = 'flex'
  }
}


</script>

<template>
  <div class="content-wrapper" v-show="elementsStore.activePage === 'SuperUserPrograms'" :class="{ 'is-active-page': elementsStore.activePage === 'SuperUserPrograms' }">

    <!-- program schools overlay -->
    <div id="SuperUserSchoolsUnderProgramOverlay" class="overlay upload">
        <div class="overlay-card">
          <v-btn @click="closeOverlay('SuperUserSchoolsUnderProgramOverlay')" color="red" size="small" variant="flat" class="close-btn">
            X
          </v-btn>
          <div class="overlay-card-content-container">
            <p class="subject-card" v-for="(school, index) in schoolOptions" :key=index>{{school}}</p>
          </div>
        </div>
    </div>

    <!-- program subjects overlay -->
    <div id="SuperUserSubjectsUnderProgramOverlay" class="overlay upload">
      <div class="overlay-card">
        <v-btn @click="closeOverlay('SuperUserSubjectsUnderProgramOverlay')" color="red" size="small" variant="flat" class="close-btn">
          X
        </v-btn>
        <div class="overlay-card-content-container">
          <p class="subject-card" v-for="(subject, index) in subjectOptions" :key=index>{{subject}}</p>
        </div>
      </div>
    </div>

    <!-- program creation overlay -->
    <div id="SuperUserCreateProgramOverlay" class="overlay upload">
      <div class="overlay-card">
        <v-btn @click="closeOverlay('SuperUserCreateProgramOverlay')" color="red" size="small" variant="flat" class="close-btn">
          X
        </v-btn>
        <div class="overlay-card-content-container">
          <v-text-field class="input-field" v-model="programName" label="NAME" clearable
          />
          <v-select class="select" :items="userAuthStore.superUserData.levels.map(item=> item.identifier)" label="LEVEL" v-model="programLevelIdentifer" 
          density="comfortable" persistent-hint hint="Select the level" variant="solo-filled" clearable
          />
        </div>
        <div class="overlay-card-action-btn-container">
          <v-btn @click="createProgram()"
            :disabled="!(programName && programLevelIdentifer)" :ripple="false"
            variant="flat" type="submit" color="black" size="small" append-icon="mdi-checkbox-marked-circle">
            SUBMIT
          </v-btn>
        </div>
      </div>
    </div>

    <!-- add/remove school/subject from program overlay -->
    <div id="SuperUserAddRemoveSchoolOrSubjectFromProgramOverlay" class="overlay upload">
        <div class="overlay-card">
          <v-btn @click="closeOverlay('SuperUserAddRemoveSchoolOrSubjectFromProgramOverlay')" color="red" size="small" variant="flat" class="close-btn">
            X
          </v-btn>
          <p class="form-error-message" v-if="formErrorMessage" style="color: red">{{ formErrorMessage }}</p>
          <div class="overlay-card-content-container">
            <v-select class="select" v-if="addRemoveType === 'addSchool'" :items="schoolOptions" label="SCHOOL" v-model="programSchoolIdentifer" variant="solo-filled"
            density="comfortable" persistent-hint hint="Select the school you want to add" clearable
            />
            <v-select class="select" v-if="addRemoveType === 'removeSchool'" :items="schoolOptions" label="SCHOOL" v-model="programSchoolIdentifer" variant="solo-filled"
            density="comfortable" persistent-hint hint="Select the school you want to remove" clearable
            />
            <v-select class="select" v-if="addRemoveType === 'addSubject'" :items="subjectOptions" label="SUBJECT" v-model="programSubjectIdentifer" variant="solo-filled"
            density="comfortable" persistent-hint hint="Select the subject you want to add" clearable
            />
            <v-select class="select" v-if="addRemoveType === 'removeSubject'" :items="subjectOptions" label="SUBJECT" v-model="programSubjectIdentifer" variant="solo-filled"
            density="comfortable" persistent-hint hint="Select the subject you want to remove" clearable
            />
          </div>
          <div class="overlay-card-action-btn-container">
            <v-btn @click="addRemoveSchoolOrSubject()" variant="flat" type="submit" color="black" size="small" append-icon="mdi-checkbox-marked-circle"
              :disabled="!(addRemoveType.split('S')[1]==='chool' && programSchoolIdentifer || addRemoveType.split('S')[1]==='ubject' && programSubjectIdentifer)" :ripple="false">
              SUBMIT
            </v-btn>
          </div>
        </div>
      </div>

    <div class="content-header">
      <v-btn @click="showOverlay('SuperUserCreateProgramOverlay')" color="blue"
        :size="elementsStore.btnSize1">
        CREATE PROGRAM
      </v-btn>
    </div>
    <div class="no-data" v-if="programs.length === 0">
      <p>NO DATA</p>
    </div>
    <v-table fixed-header class="table" v-if="programs.length > 0">
      <thead>
        <tr>
          <th class="table-head">ID</th>
          <th class="table-head">NAME</th>
          <th class="table-head">IDENTIFIER</th>
          <th class="table-head">SCHOOLS</th>
          <th class="table-head">LEVEL</th>
          <th class="table-head">SUBJECTS</th>
          <th class="table-head">ACTION</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(program, index) in programs" :key="index">
          <td class="table-data">{{ program.id }}</td>
          <td class="table-data">
            <v-chip :size="elementsStore.btnSize1">{{ program.name }}</v-chip>
          </td>
          <td class="table-data">
            <v-chip :size="elementsStore.btnSize1">{{ program.identifier }}</v-chip>
          </td>
          <td class="table-data flex-all">
            <v-btn @click="showOverlay('SuperUserSchoolsUnderProgramOverlay', '', 0, '', program.schools, [])" variant="flat" size="x-small" color="blue">
              VIEW SCHOOLS
            </v-btn>
            <v-icon class="ml-2" v-if="userAuthStore.superUserData.schools" @click="showOverlay('SuperUserAddRemoveSchoolOrSubjectFromProgramOverlay', 'addSchool', index, program.identifier, userAuthStore.superUserData.schools.map(item=> item.identifier).filter(item=> !program.schools.includes(item)), [])" variant="flat" icon="mdi-plus" color="blue" />
            <v-icon class="ma-2" v-if="userAuthStore.superUserData.schools" @click="showOverlay('SuperUserAddRemoveSchoolOrSubjectFromProgramOverlay', 'removeSchool', index, program.identifier, program.schools, [])" variant="flat" icon="mdi-minus" color="blue" />
          </td>
          <td class="table-data">
            <v-chip :size="elementsStore.btnSize1">{{ program.level.split('|')[0] }}</v-chip>
          </td>
          <td class="table-data flex-all">
            <v-btn @click="showOverlay('SuperUserSubjectsUnderProgramOverlay', '', 0, '', [], program.subjects)" variant="flat" size="x-small" color="blue">
              VIEW SUBJECTS
            </v-btn>
            <v-icon class="ml-2" v-if="userAuthStore.superUserData.schools" @click="showOverlay('SuperUserAddRemoveSchoolOrSubjectFromProgramOverlay', 'addSubject', index, program.identifier, [], userAuthStore.superUserData.subjects.map(item=> item.identifier).filter(item=> !program.subjects.includes(item)))" variant="flat" icon="mdi-plus" color="blue" />
            <v-icon class="ma-2" v-if="userAuthStore.superUserData.schools" @click="showOverlay('SuperUserAddRemoveSchoolOrSubjectFromProgramOverlay', 'removeSubject', index, program.identifier, [], program.subjects)" variant="flat" icon="mdi-minus" color="blue" />
          </td>
          <td class="table-data">
            <v-btn class="ma-2" @click="elementsStore.ShowDeletionOverlay(()=>deleteProgram(index, program.identifier), 'Are you sure you want to delete this program. The process cannot be reversed')" variant="flat" icon="mdi-delete" size="x-small" color="red" />
          </td>
        </tr>
      </tbody>
    </v-table>
  </div>
</template>

<style scoped>

.overlay-card{
  max-width: 600px !important;
}

.overlay-card-content-container{
  margin-top: 3em !important;
}


</style>
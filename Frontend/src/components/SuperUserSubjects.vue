<script setup lang="ts">
import axiosInstance from '../utils/axiosInstance';
import { AxiosError } from 'axios';
import { useUserAuthStore } from '@/stores/userAuthStore'
import { useElementsStore } from '@/stores/elementsStore'
import { computed, ref } from 'vue'
const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()
const subjectName = ref('')
const subjectLevel = ref('')
const subjectIndex:any = ref(null)
const subjectIdentifier = ref('')
const subjectSchoolIdentifier = ref('')
const addRemoveType = ref('')
const schoolOptions = ref<string[]>([])

const subjects = computed(() => {
  return userAuthStore.superUserData.subjects
})

const createSubject = async () => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', 'create')
  formData.append('name', subjectName.value);
  formData.append('levelIdentifier', subjectLevel.value);

  try {
    const response = await axiosInstance.post('superuser/subjects', formData)
    userAuthStore.superUserData.subjects.unshift(response.data)
    elementsStore.HideLoadingOverlay()
    subjectName.value = ''
    subjectLevel.value = ''
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
    formData.append('subjectIdentifier', subjectIdentifier.value);
    formData.append('schoolIdentifier', subjectSchoolIdentifier.value);

    try {
      await axiosInstance.post('superuser/subjects', formData)
      if (addRemoveType.value === 'addSchool'){
        userAuthStore.superUserData.subjects[subjectIndex.value]?.schools.unshift(subjectSchoolIdentifier.value)
      }
      else if (addRemoveType.value === 'removeSchool'){
        const selectedSchoolIndex = userAuthStore.superUserData.subjects[subjectIndex.value]?.schools.indexOf(subjectSchoolIdentifier.value)
        userAuthStore.superUserData.subjects[subjectIndex.value]?.schools.splice(selectedSchoolIndex, 1)
      }
      subjectLevel.value = ''
      subjectSchoolIdentifier.value = ''
      subjectIndex.value = null
      subjectIdentifier.value = ''
      closeOverlay('SuperUserAddRemoveSchoolFromSubjectOverlay')
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

const deleteSubject = async (index: number, subject_identifier:string) => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', 'delete')
  formData.append('identifier', subject_identifier);

  try {
    await axiosInstance.post('superuser/subjects', formData)
    userAuthStore.superUserData.subjects.splice(index, 1)
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

const showOverlay = (element: string, type_option:string='', subject_index:number=0, subject_identifier:string='', schools:string[]=[]) => {
  addRemoveType.value = type_option
  subjectIndex.value = subject_index
  subjectIdentifier.value = subject_identifier
  schoolOptions.value = schools
  const overlay = document.getElementById(element)
  if (overlay) {
    overlay.style.display = 'flex'
  }
}


</script>

<template>
  <div class="content-wrapper" v-show="elementsStore.activePage === 'SuperUserSubjects'" :class="{ 'is-active-page': elementsStore.activePage === 'SuperUserSubjects' }">

    <!-- subject schools overlay -->
    <div id="SuperUserSchoolsUnderSubjectOverlay" class="overlay upload">
        <div class="overlay-card">
          <v-btn @click="closeOverlay('SuperUserSchoolsUnderSubjectOverlay')" color="red" size="small" variant="flat" class="close-btn">
            X
          </v-btn>
          <div class="overlay-card-content-container">
            <p class="subject-card" v-for="(school, index) in schoolOptions" :key=index>{{school}}</p>
          </div>
        </div>
    </div>

    <!-- subject creation overlay -->
    <div id="SuperUserCreateSubjectOverlay" class="overlay upload">
      <div class="overlay-card">
        <v-btn @click="closeOverlay('SuperUserCreateSubjectOverlay')" color="red" size="small" variant="flat" class="close-btn">
          X
        </v-btn>
        <div class="overlay-card-content-container">
          <v-text-field class="input-field" v-model="subjectName" label="NAME" clearable
          />
          <v-select class="select" :items="userAuthStore.superUserData.levels.map(item=> item.identifier)" label="LEVEL" v-model="subjectLevel" 
          density="comfortable" persistent-hint hint="Select the level" variant="solo-filled" clearable
          />
        </div>
        <div class="overlay-card-action-btn-container">
          <v-btn @click="createSubject"
            :disabled="!(subjectName && subjectLevel)" :ripple="false"
            variant="flat" type="submit" color="black" size="small" append-icon="mdi-checkbox-marked-circle">
            SUBMIT
          </v-btn>
        </div>
      </div>
    </div>

    <!-- add/remove school from subject overlay -->
    <div id="SuperUserAddRemoveSchoolFromSubjectOverlay" class="overlay upload">
        <div class="overlay-card">
          <v-btn @click="closeOverlay('SuperUserAddRemoveSchoolFromSubjectOverlay')" color="red" size="small" variant="flat" class="close-btn">
            X
          </v-btn>
          <div class="overlay-card-content-container">
            <v-select class="select" v-if="addRemoveType === 'addSchool'" :items="schoolOptions" label="SCHOOL" v-model="subjectSchoolIdentifier" variant="solo-filled"
            density="comfortable" persistent-hint hint="Select the school you want to add" clearable
            />
            <v-select class="select" v-if="addRemoveType === 'removeSchool'" :items="schoolOptions" label="SCHOOL" v-model="subjectSchoolIdentifier" variant="solo-filled"
            density="comfortable" persistent-hint hint="Select the school you want to remove" clearable
            />
          </div>
          <div class="overlay-card-action-btn-container">
            <v-btn @click="addRemoveSchool"
              :disabled="!subjectSchoolIdentifier" :ripple="false"
              variant="flat" type="submit" color="black" size="small" append-icon="mdi-checkbox-marked-circle">
              SUBMIT
            </v-btn>
          </div>
        </div>
    </div>
    <div class="content-header">
      <v-btn @click="showOverlay('SuperUserCreateSubjectOverlay')" color="blue"
        :size="elementsStore.btnSize1">
        CREATE SUBJECT
      </v-btn>
    </div>
    <div class="no-data" v-if="subjects.length === 0">
      <p>NO DATA</p>
    </div>
    <v-table fixed-header class="table" v-if="subjects.length > 0">
      <thead>
        <tr>
          <th class="table-head">NAME</th>
          <th class="table-head">LEVEL</th>
          <th class="table-head">IDENTIFIER</th>
          <th class="table-head">SCHOOLS</th>
          <th class="table-head">ACTION</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(subject, index) in subjects" :key="index">
            <td class="table-data">{{ subject.name }}</td>
            <td class="table-data">{{ subject.level }}</td>
            <td class="table-data">{{ subject.identifier }}</td>
            <td class="table-data">
              <v-btn @click="showOverlay('SuperUserSchoolsUnderSubjectOverlay', '', 0, '', subject.schools)" variant="flat" size="x-small" color="blue">VIEW SCHOOLS</v-btn>
            </td>
            <td class="table-data flex-all" style="display: flex">
              <v-btn class="ml-2" v-if="userAuthStore.superUserData.schools" @click="showOverlay('SuperUserAddRemoveSchoolFromSubjectOverlay', 'addSchool', index, subject.identifier, userAuthStore.superUserData.schools.map(item=> item.identifier).filter(item=> !subject.schools.includes(item)))" variant="flat" icon="mdi-plus" size="x-small" color="blue" />
              <v-btn class="ma-2" @click="showOverlay('SuperUserAddRemoveSchoolFromSubjectOverlay', 'removeSchool', index, subject.identifier, subject.schools)" variant="flat" icon="mdi-minus" size="x-small" color="blue" />
              <v-btn class="ma-2" @click="elementsStore.ShowDeletionOverlay(()=>deleteSubject(index, subject.identifier), 'Are you sure you want to delete this subject. The process cannot be reversed')" variant="flat" icon="mdi-delete" size="x-small" color="red" />
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
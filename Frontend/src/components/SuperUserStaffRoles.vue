<script setup lang="ts">
import axiosInstance from '../utils/axiosInstance';
import { AxiosError } from 'axios';
import { useUserAuthStore } from '@/stores/userAuthStore'
import { useElementsStore } from '@/stores/elementsStore'
import { computed, ref } from 'vue'
const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()
const name = ref('')
const roleIndex = ref<number | null>(null)
const roleId = ref('')
const levelIdentifier = ref('')
const addRemoveType = ref('')
const schoolIdentifiers = ref<string[]>([])
const schoolOptions = ref<string[]>([])

const roles = computed(() => {
  return userAuthStore.superUserData.staffRoles
})

const createRole = async () => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', 'create')
  formData.append('name', name.value);
  formData.append('levelIdentifier', levelIdentifier.value);

  try {
    const response = await axiosInstance.post('superuser/staff_roles', formData)
    userAuthStore.superUserData.staffRoles.unshift(response.data)
    name.value = ''
    levelIdentifier.value = ''
    elementsStore.HideLoadingOverlay()
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

const addRemoveSchool = async () => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', addRemoveType.value)
  formData.append('id', roleId.value);
  formData.append('schoolIdentifiers', JSON.stringify(schoolIdentifiers.value));

  try {
    await axiosInstance.post('superuser/staff_roles', formData)
    if (addRemoveType.value === 'addSchool') {
      schoolIdentifiers.value.forEach(item => {
        userAuthStore.superUserData.staffRoles[roleIndex.value as number].schools.unshift(item)
      })
    }
    else if (addRemoveType.value === 'removeSchool') {
      schoolIdentifiers.value.forEach(item => {
        const selectedLevelIndex = userAuthStore.superUserData.staffRoles[roleIndex.value as number].schools.indexOf(item)
        userAuthStore.superUserData.staffRoles[roleIndex.value as number].schools.splice(selectedLevelIndex, 1)
      })
    }
    schoolIdentifiers.value = []
    roleId.value = ''
    addRemoveType.value = ''
    closeOverlay('SuperUserAddRemoveSchoolFromStaffRoleOverlay')
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

const deleteRole = async (index: number, role_id:string) => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', 'delete')
  formData.append('id', role_id);

  try {
    await axiosInstance.post('superuser/staff_roles', formData)
    userAuthStore.superUserData.staffRoles.splice(index, 1)
    closeOverlay('SuperUserAddRemoveSchoolFromStaffRoleOverlay')
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

const showOverlay = (element: string, type_option:string='', role_index:number=0, role_id:string='', school_options:string[]=[]) => {
  addRemoveType.value = type_option
  roleId.value = role_id
  roleIndex.value = role_index
  schoolOptions.value = school_options
  const overlay = document.getElementById(element)
  if (overlay) {
    overlay.style.display = 'flex'
  }
}


</script>

<template>
  <div class="content-wrapper" v-show="elementsStore.activePage === 'SuperUserStaffRoles'" :class="{ 'is-active-page': elementsStore.activePage === 'SuperUserStaffRoles' }">
    <!-- subject schools overlay -->
    <div id="SuperUserSchoolsUnderStaffRoleOverlay" class="overlay upload">
        <div class="overlay-card">
          <v-btn @click="closeOverlay('SuperUserSchoolsUnderStaffRoleOverlay')" color="red" size="small" variant="flat" class="close-btn">
            X
          </v-btn>
          <div class="overlay-card-content-container">
            <p class="subject-card" v-for="(school, index) in schoolOptions" :key=index>{{school}}</p>
          </div>
        </div>
    </div>

    <!-- role creation overlay -->
    <div id="SuperUserCreateStaffRoleOverlay" class="overlay upload">
      <div class="overlay-card">
        <v-btn @click="closeOverlay('SuperUserCreateStaffRoleOverlay')" color="red" size="small" variant="flat" class="close-btn">
          X
        </v-btn>
        <div class="overlay-card-content-container">
          <v-text-field class="input-field" v-model="name" label="NAME" clearable
          />
          <v-select class="select" :items="userAuthStore.superUserData.levels.map(item=> item.identifier)" label="LEVEL" v-model="levelIdentifier" variant="solo-filled"
            density="comfortable" persistent-hint hint="Select the level for the role" clearable
            />
        </div>
        <div class="overlay-card-action-btn-container">
          <v-btn @click="createRole()"
            :disabled="!(name && levelIdentifier)" :ripple="false"
            variant="flat" type="submit" color="black" size="small" append-icon="mdi-checkbox-marked-circle">
            SUBMIT
          </v-btn>
        </div>
      </div>
    </div>

    <!-- add/remove school from staf role overlay -->
    <div id="SuperUserAddRemoveSchoolFromStaffRoleOverlay" class="overlay upload">
        <div class="overlay-card">
          <v-btn @click="closeOverlay('SuperUserAddRemoveSchoolFromStaffRoleOverlay')" color="red" size="small" variant="flat" class="close-btn">
            X
          </v-btn>
          <div class="overlay-card-content-container">
            <v-select class="select" v-if="addRemoveType === 'addSchool'" :items="schoolOptions" label="SCHOOLS" v-model="schoolIdentifiers" variant="solo-filled"
            density="comfortable" persistent-hint hint="Select the school(s) you want to add" clearable multiple
            />
            <v-select class="select" v-if="addRemoveType === 'removeSchool'" :items="schoolOptions" label="SCHOOLS" v-model="schoolIdentifiers" variant="solo-filled"
            density="comfortable" persistent-hint hint="Select the school(s) you want to remove" clearable multiple
            />
          </div>
          <div class="overlay-card-action-btn-container">
            <v-btn @click="addRemoveSchool()"
              :disabled="!(schoolIdentifiers.length > 0)" :ripple="false"
              variant="flat" type="submit" color="black" size="small" append-icon="mdi-checkbox-marked-circle">
              SUBMIT
            </v-btn>
          </div>
        </div>
    </div>
    <div class="content-header">
      <v-btn @click="showOverlay('SuperUserCreateStaffRoleOverlay')" color="blue"
        :size="elementsStore.btnSize1">
        CREATE ROLE
      </v-btn>
    </div>
    <div class="no-data" v-if="roles.length === 0">
      <p>NO DATA</p>
    </div>
    <v-table fixed-header class="table" v-if="roles.length > 0">
      <thead>
        <tr>
          <th class="table-head">ID</th>
          <th class="table-head">NAME</th>
          <th class="table-head">IDENTIFIER</th>
          <th class="table-head">LEVEL</th>
          <th class="table-head">SCHOOLS</th>
          <th class="table-head">ACTION</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(role, index) in roles" :key="index">
          <td class="table-data">{{ role.id }}</td>
          <td class="table-data">
            <v-chip :text="role.name" :size="elementsStore.btnSize1" />
          </td>
          <td class="table-data">
            <v-chip :text="role.identifier" :size="elementsStore.btnSize1" />
          </td>
          <td class="table-data">
            <v-chip :text="role.level.split('|')[0]" :size="elementsStore.btnSize1" />
          </td>
          <td class="table-data flex-all">
            <v-btn @click="showOverlay('SuperUserSchoolsUnderStaffRoleOverlay', '', 0, '', role.schools)" variant="flat" size="x-small" color="blue">
              VIEW SCHOOLS
            </v-btn>
            <v-icon class="ml-2" v-if="userAuthStore.superUserData.schools" @click="showOverlay('SuperUserAddRemoveSchoolFromStaffRoleOverlay', 'addSchool', index, role.id.toString(), userAuthStore.superUserData.schools.map(item=> item.identifier).filter(item=> !role.schools.includes(item)))" icon="mdi-plus" color="blue" />
            <v-icon class="ma-2" @click="showOverlay('SuperUserAddRemoveSchoolFromStaffRoleOverlay', 'removeSchool', index, role.id.toString(), role.schools)" icon="mdi-minus" color="blue" />
          </td>
          <td class="table-data">
            <v-btn class="ma-2" @click="elementsStore.ShowDeletionOverlay(()=>deleteRole(index, role.id.toString()), 'Are you sure you want to delete this role. The process cannot be reversed')" variant="flat" icon="mdi-delete" size="x-small" color="red" />
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
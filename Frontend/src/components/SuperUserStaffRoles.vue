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
const levelIdentifiers = ref<string[]>([])
const addRemoveType = ref('')
const levelOptions = ref<string[]>([])

const roles = computed(() => {
  return userAuthStore.superUserData.staffRoles
})

const rolesData = userAuthStore.superUserData.staffRoles

const createRole = async () => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', 'create')
  formData.append('name', name.value);

  try {
    const response = await axiosInstance.post('superuser/staff_roles', formData)
    rolesData.unshift(response.data)
    name.value = ''
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

const addRemoveLevel = async () => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', addRemoveType.value)
  formData.append('id', roleId.value);
  formData.append('levelIdentifiers', JSON.stringify(levelIdentifiers.value));

  try {
    await axiosInstance.post('superuser/staff_roles', formData)
    if (addRemoveType.value === 'addRole'){
      levelIdentifiers.value.forEach(item => {
        rolesData[roleIndex.value as number].levels.push(item)
      })
    }
    else if (addRemoveType.value === 'removeRole'){
      levelIdentifiers.value.forEach(item => {
        const selectedLevelIndex = rolesData[roleIndex.value as number].levels.indexOf(item)
        rolesData[roleIndex.value as number].levels.splice(selectedLevelIndex, 1)
      })
    }
    levelIdentifiers.value = []
    roleId.value = ''
    addRemoveType.value = ''
    closeOverlay('SuperUserAddRemoveStaffRoleFromLevelOverlay')
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

const deleteRole = async (index: number, role_id:string) => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', 'delete')
  formData.append('id', role_id);

  try {
    await axiosInstance.post('superuser/staff_roles', formData)
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

const showOverlay = (element: string, type_option:string='', role_index:number=0, role_id:string='', level_options:string[]=[]) => {
  addRemoveType.value = type_option
  roleId.value = role_id
  roleIndex.value = role_index
  levelOptions.value = level_options
  const overlay = document.getElementById(element)
  if (overlay) {
    overlay.style.display = 'flex'
  }
}


</script>

<template>
  <div class="content-wrapper" v-show="elementsStore.activePage === 'SuperUserStaffRoles'" :class="{ 'is-active-page': elementsStore.activePage === 'SuperUserStaffRoles' }">
    <!-- subject schools overlay -->
    <div id="SuperUserLevelsUnderStaffRoleOverlay" class="overlay upload">
        <div class="overlay-card">
          <v-btn @click="closeOverlay('SuperUserLevelsUnderStaffRoleOverlay')" color="red" size="small" variant="flat" class="close-btn">
            X
          </v-btn>
          <div class="overlay-card-content-container">
            <p class="subject-card" v-for="(level, index) in levelOptions" :key=index>{{level}}</p>
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
        </div>
        <div class="overlay-card-action-btn-container">
          <v-btn @click="createRole"
            :disabled="!name" :ripple="false"
            variant="flat" type="submit" color="black" size="small" append-icon="mdi-checkbox-marked-circle">
            SUBMIT
          </v-btn>
        </div>
      </div>
    </div>

    <!-- add/remove staff role from level overlay -->
    <div id="SuperUserAddRemoveStaffRoleFromLevelOverlay" class="overlay upload">
        <div class="overlay-card">
          <v-btn @click="closeOverlay('SuperUserAddRemoveStaffRoleFromLevelOverlay')" color="red" size="small" variant="flat" class="close-btn">
            X
          </v-btn>
          <div class="overlay-card-content-container">
            <v-select class="select" v-if="addRemoveType === 'addRole'" :items="levelOptions" label="ROLE" v-model="levelIdentifiers" variant="solo-filled"
            density="comfortable" persistent-hint hint="Select the level you want to add" clearable multiple
            />
            <v-select class="select" v-if="addRemoveType === 'removeRole'" :items="levelOptions" label="ROLE" v-model="levelIdentifiers" variant="solo-filled"
            density="comfortable" persistent-hint hint="Select the level you want to remove" clearable multiple
            />
          </div>
          <div class="overlay-card-action-btn-container">
            <v-btn @click="addRemoveLevel"
              :disabled="!(levelIdentifiers.length > 0)" :ripple="false"
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
          <th class="table-head">NAME</th>
          <th class="table-head">LEVELS</th>
          <th class="table-head">ACTION</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(role, index) in roles" :key="index">
            <td class="table-data">{{ role.name }}</td>
            <td class="table-data">
              <v-btn @click="showOverlay('SuperUserLevelsUnderStaffRoleOverlay', '', 0, '', role.levels)" variant="flat" size="x-small" color="blue">VIEW LEVELS</v-btn>
            </td>
            <td class="table-data flex-all" style="display: flex">
              <v-btn class="ml-2" v-if="userAuthStore.superUserData.schools" @click="showOverlay('SuperUserAddRemoveStaffRoleFromLevelOverlay', 'addRole', index, role.id.toString(), userAuthStore.superUserData.levels.map(item=> item.identifier).filter(item=> !role.levels.includes(item)))" variant="flat" icon="mdi-plus" size="x-small" color="blue" />
              <v-btn class="ma-2" @click="showOverlay('SuperUserAddRemoveStaffRoleFromLevelOverlay', 'removeRole', index, role.id.toString(), role.levels)" variant="flat" icon="mdi-minus" size="x-small" color="blue" />
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
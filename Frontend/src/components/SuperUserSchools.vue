<script setup lang="ts">
import axiosInstance from '../utils/axiosInstance';
import { AxiosError } from 'axios';
import { useUserAuthStore } from '@/stores/userAuthStore'
import { useElementsStore } from '@/stores/elementsStore'
import { ghanaRegions } from '@/utils/util';
import { computed, ref } from 'vue'
import TheLoader from './TheLoader.vue';
const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()
const formErrorMessage = ref('')
const schoolName = ref('')
const schoolCode = ref('')
const schoolLogo = ref('')
const schoolAddress = ref('')
const schoolRegion = ref('')
const schoolCityTown = ref('')
const schoolPostalAddress = ref('')
const schoolShortName = ref('')
const schoolContact = ref('')
const schoolAltContact = ref('')
const schoolEmail = ref('')
const staffId = ref(false)
const levelOptions = ref<string[]>([])
const schoolIndex = ref(0)
const selectedSchoolId = ref(0)
const schoolLevelsIdSelected = ref([])
const levelIdentifierSelected = ref('')
const addRemoveType = ref('')

const schools = computed(() => {
  return userAuthStore.superUserData.schools
})

const createSchool = async () => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', 'create')
  formData.append('name', schoolName.value);
  formData.append('address', schoolAddress.value);
  formData.append('shortName', schoolShortName.value);
  formData.append('logo', schoolLogo.value);
  formData.append('code', schoolCode.value);
  formData.append('altContact', schoolAltContact.value);
  formData.append('postalAddress', schoolPostalAddress.value);
  formData.append('region', schoolRegion.value);
  formData.append('cityTown', schoolCityTown.value);
  formData.append('contact', schoolContact.value);
  formData.append('email', schoolEmail.value);
  formData.append('levelIds', JSON.stringify(schoolLevelsIdSelected.value));
  formData.append('staffId', JSON.stringify(staffId.value));

  try {
    const response = await axiosInstance.post('superuser/schools', formData)
    userAuthStore.superUserData.schools?.unshift(response.data)
    elementsStore.HideLoadingOverlay()
    schoolName.value = ''
    schoolCode.value = ''
    schoolAddress.value = ''
    schoolAltContact.value = ''
    schoolCityTown.value = ''
    schoolPostalAddress.value = ''
    schoolLevelsIdSelected.value = []
    schoolContact.value = ''
    schoolRegion.value = ''
    schoolShortName.value = ''
    schoolLogo.value = ''
    schoolEmail.value = ''
    staffId.value = false
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

const deleteSchool = async (index: number, school_id: number) => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', 'delete')
  formData.append('schoolId', school_id.toString());

  try {
    await axiosInstance.post('superuser/schools', formData)
    userAuthStore.superUserData.schools?.splice(index, 1)
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

const addRemoveLevel = async () => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', addRemoveType.value)
  formData.append('levelIdentifier', levelIdentifierSelected.value)
  formData.append('schoolId', selectedSchoolId.value.toString())

  try {
    await axiosInstance.post('superuser/schools', formData)
    if (addRemoveType.value === 'addLevel') {
      userAuthStore.superUserData.schools?.[schoolIndex.value]?.levels.unshift(levelIdentifierSelected.value)
    }
    else if (addRemoveType.value === 'removeLevel') {
      const levelIndex = userAuthStore.superUserData.schools?.[schoolIndex.value]?.levels.indexOf(levelIdentifierSelected.value)
      if (levelIndex) {
        userAuthStore.superUserData.schools?.[schoolIndex.value]?.levels.splice(levelIndex, 1)
      }
    }
    schoolIndex.value = 0
    levelIdentifierSelected.value = ''
    addRemoveType.value = ''
    closeOverlay('SuperUserAddRemoveLevelFromSchoolOverlay')
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

const getSchoolLogo = (event: any) => {
  const file = event.target.files[0]
  schoolLogo.value = file
}

const isCreateSchoolFormValid = computed(() => {
  return !(schoolName.value && schoolAddress.value && schoolLevelsIdSelected.value.length > 0 && schoolContact.value && schoolCityTown.value && schoolRegion.value && schoolPostalAddress.value && schoolLogo.value)
})

const closeOverlay = (element: string) => {
  const overlay = document.getElementById(element)
  if (overlay) {
    overlay.style.display = 'none'
  }
}

const showOverlay = (element: string, add_remove_type: string = '', index: number = 0, levels_options: string[] = [], school_id: number = 0) => {
  addRemoveType.value = add_remove_type
  selectedSchoolId.value = school_id
  schoolIndex.value = index
  levelOptions.value = levels_options
  const overlay = document.getElementById(element)
  if (overlay) {
    overlay.style.display = 'flex'
  }
}



</script>

<template>
  <div class="content-wrapper" v-show="elementsStore.activePage === 'SuperUserSchools'"
    :class="{ 'is-active-page': elementsStore.activePage === 'SuperUserSchools' }">

    <!-- school levels overlay -->
    <div id="SuperUserLevelsUnderSchoolOverlay" class="overlay upload">
      <div class="overlay-card">
        <v-btn @click="closeOverlay('SuperUserLevelsUnderSchoolOverlay')" color="red" size="small" variant="flat"
          class="close-btn">
          X
        </v-btn>
        <div class="overlay-card-content-container">
          <p class="subject-card" v-for="(level, index) in levelOptions" :key=index>{{ level }}</p>
        </div>
      </div>
    </div>

    <!-- add/remove level from school overlay -->
    <div id="SuperUserAddRemoveLevelFromSchoolOverlay" class="overlay upload">
      <div class="overlay-card">
        <v-btn @click="closeOverlay('SuperUserAddRemoveLevelFromSchoolOverlay')" color="red" size="small" variant="flat"
          class="close-btn">
          X
        </v-btn>
        <div class="overlay-card-content-container">
          <v-select class="select" v-if="addRemoveType === 'addLevel'" :items="levelOptions" label="LEVEL"
            v-model="levelIdentifierSelected" variant="solo-filled" density="comfortable" persistent-hint
            hint="Select the level you want to add" clearable />
          <v-select class="select" v-if="addRemoveType === 'removeLevel'" :items="levelOptions" label="LEVEL"
            v-model="levelIdentifierSelected" variant="solo-filled" density="comfortable" persistent-hint
            hint="Select the level you want to remove" clearable />
        </div>
        <div class="overlay-card-action-btn-container">
          <v-btn @click="addRemoveLevel()" variant="flat" type="submit" color="black" size="small"
            append-icon="mdi-checkbox-marked-circle" :disabled="!(levelIdentifierSelected)" :ripple="false">
            SUBMIT
          </v-btn>
        </div>
      </div>
    </div>

    <!-- school creation overlay -->
    <div id="SuperUserCreateSchoolOverlay" class="overlay upload">
      <div class="overlay-card">
        <v-btn @click="closeOverlay('SuperUserCreateSchoolOverlay')" color="red" size="small" variant="flat"
          class="close-btn">
          X
        </v-btn>
        <p class="form-error-message" v-if="formErrorMessage" style="color: red">{{ formErrorMessage }}</p>
        <div class="overlay-card-content-container">
          <v-text-field class="input-field" v-model="schoolName" label="NAME" />
          <v-text-field class="input-field" v-model="schoolShortName" label="SHORT NAME" hint="Optional" />
          <v-text-field class="input-field" v-model="schoolCode" label="CODE" maxlength="10" hint="Optional" />
          <v-checkbox class="select" v-model="staffId" label="STAFF ID" hint="Does the school give staff IDs"
            color="blue" />
          <v-file-input class="input-field" @change="getSchoolLogo" label="LOGO" accept="image/*" outlined />
          <v-text-field class="input-field" v-model="schoolAddress" label="ADDRESS" />
          <v-select class="select" :items="ghanaRegions" label="REGION" v-model="schoolRegion" variant="solo-filled"
            density="comfortable" persistent-hint hint="Select the Region the school is located at" />
          <v-select class="select"
            :items="userAuthStore.superUserData.levels.map(item => ({ 'title': item.identifier, 'value': item.id }))"
            label="LEVELS" v-model="schoolLevelsIdSelected" variant="solo-filled" density="comfortable"
            item-title="title" item-value="value" multiple chip persistent-hint
            hint="Select the levels in the school" />
          <v-text-field class="input-field" v-model="schoolCityTown" label="CITY/TOWN" />
          <v-text-field class="input-field" v-model="schoolPostalAddress" label="POSTAL ADDRESS" />
          <v-text-field class="input-field" v-model="schoolContact" label="PHONE NUMBER" />
          <v-text-field class="input-field" v-model="schoolAltContact" label="ALTERNATE PHONE NUMBER" hint="Optional" />
          <v-text-field class="input-field" v-model="schoolEmail" label="EMAIL" hint="Optional" />
        </div>
        <div class="overlay-card-action-btn-container">
          <v-btn @click="createSchool()" :disabled="isCreateSchoolFormValid" :ripple="false" variant="flat"
            type="submit" color="black" size="small" append-icon="mdi-checkbox-marked-circle">
            SUBMIT
          </v-btn>
        </div>
      </div>
    </div>

    <div class="content-header">
      <v-btn @click="showOverlay('SuperUserCreateSchoolOverlay')" color="blue" :size="elementsStore.btnSize1">
        ADD SCHOOL
      </v-btn>
    </div>
    <TheLoader v-if="!schools" :func="userAuthStore.getSuperUserData" />
    <div class="no-data" v-if="schools?.length === 0">
      <p>NO DATA</p>
    </div>
    <v-table fixed-header class="table" v-if="schools && schools.length > 0">
      <thead>
        <tr>
          <th class="table-head">NAME</th>
          <th class="table-head">IDENTIFIER</th>
          <th class="table-head">LEVELS</th>
          <th class="table-head">CODE</th>
          <th class="table-head">STAFF ID</th>
          <th class="table-head">LOGO</th>
          <th class="table-head">ADDRESS</th>
          <th class="table-head">REGION</th>
          <th class="table-head">CITY/TOWN</th>
          <th class="table-head">POSTAL ADDRESS</th>
          <th class="table-head">SHORT NAME</th>
          <th class="table-head">CONTACT</th>
          <th class="table-head">ALTERNATE CONTACT</th>
          <th class="table-head">EMAIL</th>
          <th class="table-head">DATE CREATED</th>
          <th class="table-head">ACTION</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(school, index) in schools" :key="index">
          <td class="table-data">
            <v-chip>{{ school.name }}</v-chip>
          </td>
          <td class="table-data">{{ school.identifier }}</td>
          <td class="table-data flex-all">
            <v-btn @click="showOverlay('SuperUserLevelsUnderSchoolOverlay', '', 0, school.levels)" variant="flat"
              size="x-small" color="blue">
              SEE LEVELS
            </v-btn>
            <v-icon class="ml-2"
              @click="showOverlay('SuperUserAddRemoveLevelFromSchoolOverlay', 'addLevel', index, userAuthStore.superUserData.levels.map(item => item.identifier), school.id)"
              variant="flat" icon="mdi-plus" color="blue" />
            <v-icon class="ma-2" v-if="school.levels.length > 0"
              @click="showOverlay('SuperUserAddRemoveLevelFromSchoolOverlay', 'removeLevel', index, school.levels, school.id)"
              variant="flat" icon="mdi-minus" color="blue" />
          </td>
          <td class="table-data">
            <v-chip v-if="school.code">{{ school.code }}</v-chip>
          </td>
          <td class="table-data">
            <v-checkbox-btn color="blue" v-model="school.staff_id" disabled />
          </td>
          <td class="table-data">
            <img class="profile-img" v-if="school.logo" :src="school.logo" alt="School Logo" width="50" height="50" />
          </td>
          <td class="table-data">{{ school.address }}</td>
          <td class="table-data">
            <v-chip>{{ school.region }}</v-chip>
          </td>
          <td class="table-data">
            <v-chip>{{ school.city_town }}</v-chip>
          </td>
          <td class="table-data">{{ school.postal_address }}</td>
          <td class="table-data">
            <v-chip v-if="school.short_name">{{ school.short_name }}</v-chip>
          </td>
          <td class="table-data">
            <v-chip>{{ school.contact }}</v-chip>
          </td>
          <td class="table-data">
            <v-chip v-if="school.alt_contact">{{ school.alt_contact }}</v-chip>
          </td>
          <td class="table-data">
            <v-chip v-if="school.email">{{ school.email }}</v-chip>
          </td>
          <td class="table-data">
            <v-chip>{{ school.date_created }}</v-chip>
          </td>
          <td class="table-data">
            <v-btn
              @click="elementsStore.ShowDeletionOverlay(() => deleteSchool(index, school.id), 'Are you sure you want to delete this school. The process cannot be reversed')"
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
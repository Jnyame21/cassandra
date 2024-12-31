<script setup lang="ts">
import { AxiosError } from 'axios';
import { computed, ref } from 'vue';
import axiosInstance from '@/utils/axiosInstance';
import { useUserAuthStore } from '@/stores/userAuthStore';
import { useElementsStore } from '@/stores/elementsStore';
import { downloadFile, countriesData, ghanaRegions, roleOptions, religionOptions, titleOptions, genderOptions, uploadTypeOptions } from '@/utils/util';


const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()
const firstName = ref('')
const lastName = ref('')
const staffId = ref('')
const title = ref('')
const gender = ref('')
const dateOfBirth = ref('')
const departments = ref<string[]>([])
const selectedSubjects = ref<string[]>([])
const staffRoles = ref<string[]>([])
const levels = ref<string[]>([])
const contact = ref('')
const address = ref('')
const img: any = ref('')
const nationality = ref('')
const typeSelected = ref('')
const region = ref('')
const religion = ref('')
const formErrorMessage = ref('')
const email = ref('')
const dateEnrolled = ref('')
const pob = ref('')
const staffFile: any = ref('')
const altContact = ref('')
const previousValue: any = ref('')
const newValue: any = ref('')
const editType = ref('')
const editStaffId = ref('')
const editStaffIndex: any = ref('')
const nameTypeSelected = ref('')
const editSubjectsSelected = ref<string[]>([])


interface Props {
  schoolIdentifier: string;
}
const props = defineProps<Props>()
const schoolIdentifier = props.schoolIdentifier

const staff = computed(() => {
  return userAuthStore.superUserData.staff[schoolIdentifier]
})

const staffData = userAuthStore.superUserData.staff[schoolIdentifier]

const maleStaff = computed(() => {
  return staff.value.filter((item: any) => item['gender'].toLowerCase() === 'male').length
})

const femaleStaff = computed(() => {
  return staff.value.filter((item: any) => item['gender'].toLowerCase() === 'female').length
})

const schoolIndex = userAuthStore.superUserData.schools?.findIndex(item => item.identifier === schoolIdentifier)

let timeout: any;
const showErrorMessage = (message: string) => {
  formErrorMessage.value = message
  if (timeout) {
    clearTimeout(timeout)
  }
  timeout = setTimeout(() => {
    formErrorMessage.value = ''
  }, 10 * 1000)
}

const nameTypeOptions = [
  { 'label': 'TITLE', 'value': 'title' },
  { 'label': 'FIRST NAME', 'value': 'first_name' },
  { 'label': 'LAST NAME', 'value': 'last_name' },
]

const addStaff = async () => {
  const formData = new FormData()
  if (typeSelected.value === 'noFile') {
    if (img.value?.size > 1024 * 1024) {
      showErrorMessage("The size of the image must not exceed 1MB")
      return;
    }
    formData.append('type', 'createWithoutFile')
    formData.append('firstName', firstName.value)
    formData.append('lastName', lastName.value)
    formData.append('dateOfBirth', dateOfBirth.value)
    formData.append('gender', gender.value)
    formData.append('title', title.value)
    formData.append('schoolIdentifier', schoolIdentifier)
    formData.append('roles', JSON.stringify(staffRoles.value))
    formData.append('dateEnrolled', dateEnrolled.value)
    formData.append('contact', contact.value)
    formData.append('pob', pob.value)
    formData.append('region', region.value)
    formData.append('religion', religion.value)
    formData.append('altContact', altContact.value)
    formData.append('email', email.value)
    formData.append('address', address.value)
    formData.append('img', img.value)
    formData.append('nationality', nationality.value)
    formData.append('subjects', JSON.stringify(selectedSubjects.value))
    formData.append('departments', JSON.stringify(departments.value))
    if (userAuthStore.userData['school']['staff_id']) {
      formData.append('staff_id', staffId.value)
    }
  }
  else if (typeSelected.value === 'file') {
    formData.append('type', 'createWithFile')
    formData.append('file', staffFile.value)
  }

  elementsStore.ShowLoadingOverlay()
  try {
    const response = await axiosInstance.post('school-admin/staff', formData)
    const data = response.data
    if (typeSelected.value === 'file') {
      data.forEach((item: any) => {
        staffData.unshift(item)
      })
      staffFile.value = ''
    }
    else if (typeSelected.value === 'noFile') {
      staffData.unshift(data)
      firstName.value = ''
      lastName.value = ''
      dateOfBirth.value = ''
      contact.value = ''
      pob.value = ''
      altContact.value = ''
      email.value = ''
      address.value = ''
      staffId.value = ''
      img.value = ''
      selectedSubjects.value = []
    }
    elementsStore.HideLoadingOverlay()
    elementsStore.ShowOverlay('Success', 'green', null, null)
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

const editStaff = async () => {
  const formData = new FormData()
  formData.append('staffId', editStaffId.value)
  formData.append('type', 'edit')
  if (editType.value === 'img' && newValue.value?.size > 1024 * 1024) {
    showErrorMessage("The size of the image must not exceed 1MB")
    return;
  }
  if (editType.value === 'subjects') {
    formData.append('editType', editType.value)
    formData.append('newValue', JSON.stringify(newValue.value))
  }
  else if (editType.value === 'user') {
    formData.append('editType', nameTypeSelected.value)
    formData.append('newValue', newValue.value)
  }
  else {
    formData.append('editType', editType.value)
    formData.append('newValue', newValue.value)
  }

  elementsStore.ShowLoadingOverlay()
  try {
    const response = await axiosInstance.post('school-admin/staff', formData)
    const data = response.data
    if (userAuthStore.adminData.staff) {
      if (editType.value === 'user') {
        staffData[editStaffIndex.value]['user'] = data
      }
      else if (editType.value === 'staff_id') {
        staffData[editStaffIndex.value]['staff_id'] = data
      }
      else if (editType.value === 'dob') {
        staffData[editStaffIndex.value]['dob'] = data
      }
      else if (editType.value === 'pob') {
        staffData[editStaffIndex.value]['pob'] = data
      }
      else if (editType.value === 'subjects') {
        staffData[editStaffIndex.value]['subjects'] = data
      }
      else if (editType.value === 'staff_id') {
        staffData[editStaffIndex.value]['staff_id'] = data
      }
      else if (editType.value === 'date_enrolled') {
        staffData[editStaffIndex.value]['date_enrolled'] = data
      }
      else if (editType.value === 'region') {
        staffData[editStaffIndex.value]['region'] = data
      }
      else if (editType.value === 'religion') {
        staffData[editStaffIndex.value]['religion'] = data
      }
      else if (editType.value === 'nationality') {
        staffData[editStaffIndex.value]['nationality'] = data
      }
      else if (editType.value === 'contact') {
        staffData[editStaffIndex.value]['contact'] = data
      }
      else if (editType.value === 'alt_contact') {
        staffData[editStaffIndex.value]['alt_contact'] = data
      }
      else if (editType.value === 'address') {
        staffData[editStaffIndex.value]['address'] = data
      }
      else if (editType.value === 'email') {
        staffData[editStaffIndex.value]['email'] = data
      }
      else if (editType.value === 'img') {
        staffData[editStaffIndex.value]['img'] = data
      }
    }
    newValue.value = ''
    editType.value = ''
    nameTypeSelected.value = ''
    previousValue.value = ''
    elementsStore.HideLoadingOverlay()
    closeOverlay(`'SuperUserEditStaffOverlay,${schoolIdentifier}'`)
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

const deleteStaff = async (staffToDeleteId: string) => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', 'delete')
  formData.append('staffId', staffToDeleteId)

  try {
    await axiosInstance.post('school-admin/staff', formData)
    const staffToDelete = staffData.find((item: any) => item['staff_id'] === staffToDeleteId)
    if (staffToDelete) {
      const staffToDeletIndex = staffData.indexOf(staffToDelete)
      staffData.splice(staffToDeletIndex, 1)
    }
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

const getStaffFile = async () => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', 'getFile')
  formData.append('schoolIdentifier', schoolIdentifier)

  try {
    const response = await axiosInstance.post('school-admin/staff', formData, { 'responseType': 'blob' })
    downloadFile(response.headers, response.data, "staff-creation.xlsx")
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

const requiredFields = computed(() => {
  return !(firstName.value && lastName.value && contact.value && address.value && nationality.value && title.value && dateOfBirth.value && gender.value && staffRoles.value.length > 0 && region.value && religion.value && pob.value)
})

const isStaffFormValid = computed(() => {
  if (typeSelected.value === 'noFile') {
    if (schoolIndex && userAuthStore.superUserData.schools?.[schoolIndex].staff_id) {
      return !(staffId.value && requiredFields.value)
    }
    else {
      return requiredFields.value
    }
  }
  else if (typeSelected.value === 'file') {
    return !(staffFile.value)
  }
  return true;
})

const imgChange = (event: any) => {
  const file = event.target.files[0]
  img.value = file
}

const editImgChange = (event: any) => {
  const file = event.target.files[0]
  newValue.value = file
}

const showEditOverlay = (edit_type: string, previous_value: string, staff_id: string, staff_index: number) => {
  const overlay = document.getElementById(`SuperUserEditStaffOverlay,${schoolIdentifier}`)
  previousValue.value = previous_value
  editType.value = edit_type
  editStaffId.value = staff_id
  editStaffIndex.value = staff_index
  if (overlay) {
    overlay.style.display = 'flex'
  }
}

const fileChanged = (file: any) => {
  if (!file) {
    staffFile.value = ''
    img.value = ''
    if (editType.value === 'img') {
      newValue.value = ''
    }
  }
}

const staffFileChanged = (event: any) => {
  const file = event.target.files[0]
  staffFile.value = file
}

const showOverlay = (element: string) => {
  const overlay = document.getElementById(element)
  if (overlay) {
    overlay.style.display = 'flex'
  }
}

const closeOverlay = (element: string) => {
  const overlay = document.getElementById(element)
  if (overlay) {
    overlay.style.display = 'none'
  }
}



</script>

<template>
  <div class="content-wrapper" v-show="elementsStore.activePage === `SuperUserStaff,${schoolIdentifier}`"
    :class="{ 'is-active-page': elementsStore.activePage === `SuperUserStaff,${schoolIdentifier}` }">

    <!-- edit staff overlay -->
    <div :id="`SuperUserEditStaffOverlay,${schoolIdentifier}`" class="overlay" v-if="staff">
      <div class="overlay-card edit-overlay">
        <v-btn @click="closeOverlay(`SuperUserEditStaffOverlay,${schoolIdentifier}`)" color="red" size="small"
          variant="flat" class="close-btn">
          X
        </v-btn>
        <p class="form-error-message" v-if="formErrorMessage">{{ formErrorMessage }}</p>
        <div class="overlay-card-info-container mb-10">
          <h4 class="previous-value" v-if="editType !== 'img'"><span style="color: black">PREVIOUS VALUE:</span> {{
            previousValue }}</h4>
          <img class="profile-img2" v-if="editType === 'img'" :src="previousValue" alt="staff profile image">
        </div>
        <div class="overlay-card-content-container">
          <v-select class="select" v-if="editType === 'user'" :items="nameTypeOptions" label="NAME TYPE"
            v-model="nameTypeSelected" item-title="label" density="comfortable" item-value="value" variant="solo-filled"
            persistent-hint clearable hint="Select whether you want to change the first name or last name" />
          <v-text-field class="input-field" v-if="editType === 'user' && nameTypeSelected === 'first_name'"
            v-model="newValue" label="FIRST NAME" clearable variant="solo-filled" density="comfortable"
            placeholder="Eg. Cassandra" persistent-hint hint="Enter the first name of the staff" />
          <v-text-field class="input-field" v-if="editType === 'user' && nameTypeSelected === 'last_name'"
            v-model="newValue" label="LAST NAME (MIDDLE NAME + SURNAME)" clearable variant="solo-filled"
            density="comfortable" placeholder="Eg. Akua Afriyie" persistent-hint
            hint="Enter the last name of the staff" />
          <v-select class="select" v-if="editType === 'user' && nameTypeSelected === 'title'" :items="titleOptions"
            label="TITLE" v-model="newValue" variant="solo-filled" density="comfortable" clearable persistent-hint
            hint="Select the title of the staff" />
          <v-select class="select" v-if="editType === 'gender'" :items="genderOptions" label="GENDER" v-model="newValue"
            item-title="label" item-value="value" variant="solo-filled" density="comfortable" clearable />
          <v-text-field v-if="editType === 'staffId' && userAuthStore.userData['school']['staff_id']"
            class="input-field" v-model="newValue" label="STAFF ID" variant="solo-filled" density="comfortable"
            clearable persistent-hint hint="Enter the staff ID of the staff" />
          <v-text-field class="input-field" v-if="editType === 'dob'" v-model="newValue" label="DATE OF BIRTH"
            type="date" variant="solo-filled" density="comfortable" clearable persistent-hint
            hint="Select the date of birth of the staff" />
          <v-text-field class="input-field" v-if="editType === 'date_enrolled'" v-model="newValue"
            label="DATE EMPLOYED(OPTIONAL)" type="date" variant="solo-filled" density="comfortable" clearable
            persistent-hint hint="Select date the staff was employed" />
          <v-select class="select" v-if="editType === 'religion'" :items="religionOptions" label="RELIGION"
            v-model="newValue" item-title="label" item-value="value" variant="solo-filled" density="comfortable"
            persistent-hint hint="Select religion the staff belongs to" clearable />
          <v-select class="select" v-if="editType === 'nationality'"
            :items="countriesData.sort((a: any, b: any) => a.nationality.localeCompare(b.nationality))"
            label="NATIONALITY" v-model="newValue" item-title="nationality" item-value="nationality"
            variant="solo-filled" density="comfortable" persistent-hint hint="Select the nationality of the staff"
            clearable />
          <v-text-field class="input-field" v-if="editType === 'region'" v-model="newValue" label="REGION/STATE"
            variant="solo-filled" density="comfortable" placeholder="Eg. Asanti" clearable persistent-hint
            hint="Enter the region/state the staff is from" />
          <v-text-field class="input-field" v-if="editType === 'pob'" v-model="newValue"
            label="PLACE OF BIRTH(HOME CITY/TOWN)" variant="solo-filled" density="comfortable"
            placeholder="Eg. Ayeduase" clearable persistent-hint hint="Enter the city/town the staff was born" />
          <v-text-field class="input-field" v-if="editType === 'contact'" v-model="newValue" label="PHONE NUMBER"
            variant="solo-filled" density="comfortable" placeholder="Eg. +233596021383" clearable />
          <v-text-field class="input-field" v-if="editType === 'alt_contact'" v-model="newValue"
            label="ALTERNATE PHONE NUMBER(OPTIONAL)" variant="solo-filled" density="comfortable"
            placeholder="Eg. +233596021383" clearable />
          <v-text-field class="input-field" v-if="editType === 'address'" v-model="newValue" label="RESIDENTIAL ADDRESS"
            type="address" variant="solo-filled" density="comfortable" placeholder="Eg. Ak-509-1066, Kotei, Kumasi"
            clearable />
          <v-text-field class="input-field" v-if="editType === 'email'" v-model="newValue" label="EMAIL(OPTIONAL)"
            type="email" variant="solo-filled" density="comfortable" placeholder="Eg. nyamejustice2000@gmail.com"
            clearable />
          <v-file-input @change="editImgChange" @update:model-value="fileChanged" v-if="editType === 'img'" clearable
            show-size class="select" label="STAFF IMAGE" density="comfortable" variant="solo-filled" chips
            accept="image/*" prepend-icon="mdi-image" persistent-hint hint="Upload a picture of the staff">
          </v-file-input>
          <v-select class="select" v-if="editType === 'role'" :items="roleOptions" label="ROLE" v-model="newValue"
            item-title="label" item-value="value" variant="solo-filled" density="comfortable" persistent-hint
            hint="Select the role of the staff" clearable />
          <v-select class="select" v-if="editType === 'subjects'" :items="userAuthStore.superUserData.subjects"
            label="SUJECTS" v-model="editSubjectsSelected" variant="solo-filled" density="comfortable" persistent-hint
            hint="Select the subjects the staff teaches" multiple chips clearable 
          />
        </div>
        <div class="overlay-card-action-btn-container">
          <v-btn @click="editStaff()" :disabled="!newValue" :ripple="false" variant="flat" type="submit" color="black"
            size="small" append-icon="mdi-checkbox-marked-circle">
            SUBMIT
          </v-btn>
        </div>
      </div>
    </div>

    <!-- add staff overlay -->
    <div :id="`SuperUserAddStaffOverlay,${schoolIdentifier}`" class="overlay" v-if="staff">
      <div class="overlay-card">
        <v-btn @click="closeOverlay(`SuperUserAddStaffOverlay,${schoolIdentifier}`)" color="red" size="small"
          variant="flat" class="close-btn">X</v-btn>
        <p class="form-error-message" v-if="formErrorMessage">{{ formErrorMessage }}</p>
        <div class="overlay-card-info-container">
          <v-select class="select" :items="uploadTypeOptions" label="UPLOAD TYPE" v-model="typeSelected" item-title="label"
            density="comfortable" item-value="value" variant="solo-filled" persistent-hint clearable
            hint="Select whether you want to use an excel file or input the data here" 
          />
        </div>
        <div class="overlay-card-content-container" v-if="typeSelected === 'noFile' && schoolIndex">
          <v-text-field class="input-field" v-model="firstName" label="FIRST NAME" clearable variant="solo-filled"
            density="comfortable" placeholder="Eg. Cassandra" persistent-hint
            hint="Enter the first name of the staff" 
          />
          <v-text-field class="input-field" v-model="lastName" label="LAST NAME (MIDDLE NAME + SURNAME)" clearable
            variant="solo-filled" density="comfortable" placeholder="Eg. Akua Afriyie" persistent-hint
            hint="Enter the last name of the staff" 
          />
          <v-select class="select" :items="genderOptions" label="GENDER" v-model="gender" item-title="label"
            item-value="value" variant="solo-filled" density="comfortable" clearable 
          />
          <v-select class="select" :items="titleOptions" label="TITLE" v-model="title" variant="solo-filled"
            density="comfortable" clearable persistent-hint hint="Select the title of the staff" 
          />
          <v-text-field v-if="userAuthStore.superUserData.schools[schoolIndex].staff_id" class="input-field" v-model="staffId"
            label="STAFF ID" variant="solo-filled" density="comfortable" clearable persistent-hint
            hint="Enter the staff ID of the staff" 
          />
          <v-text-field class="input-field" v-model="dateOfBirth" label="DATE OF BIRTH" type="date"
            variant="solo-filled" density="comfortable" clearable persistent-hint
            hint="Select the date of birth of the staff" 
          />
          <v-text-field class="input-field" v-model="dateEnrolled" label="DATE EMPLOYED(OPTIONAL)" type="date"
            variant="solo-filled" density="comfortable" clearable persistent-hint
            hint="Select date the staff was employed" 
          />
          <v-select class="select" :items="religionOptions" label="RELIGION" v-model="religion" item-title="label"
            item-value="value" variant="solo-filled" density="comfortable" persistent-hint
            hint="Select religion the staff belongs to" clearable 
          />
          <v-select class="select"
            :items="countriesData.sort((a: any, b: any) => a.nationality.localeCompare(b.nationality))"
            label="NATIONALITY" v-model="nationality" clearable item-title="nationality" item-value="nationality"
            variant="solo-filled" density="comfortable" persistent-hint hint="Select the nationality of the staff" 
          />
          <v-text-field class="input-field" v-if="nationality && nationality?.toLowerCase() !== 'ghanaian'"
            v-model="region" label="REGION/STATE" variant="solo-filled" density="comfortable" placeholder="Eg. Asanti"
            clearable persistent-hint hint="Enter the region/state the staff is from" 
          />
          <v-select class="select" v-if="nationality?.toLowerCase() === 'ghanaian'" :items="ghanaRegions" label="REGION"
            v-model="region" variant="solo-filled" density="comfortable" persistent-hint
            hint="Select the region the staff is from" clearable 
          />
          <v-text-field class="input-field" v-model="pob" label="PLACE OF BIRTH(HOME CITY/TOWN)" variant="solo-filled"
            density="comfortable" placeholder="Eg. Ayeduase" clearable persistent-hint
            hint="Enter the city/town the staff was born" 
          />
          <v-text-field class="input-field" v-model="contact" label="PHONE NUMBER" variant="solo-filled"
            density="comfortable" placeholder="Eg. +233596021383" clearable 
          />
          <v-text-field class="input-field" v-model="altContact" label="ALTERNATE PHONE NUMBER(OPTIONAL)"
            variant="solo-filled" density="comfortable" placeholder="Eg. +233596021383" clearable 
          />
          <v-text-field class="input-field" v-model="address" label="RESIDENTIAL ADDRESS" type="address"
            variant="solo-filled" density="comfortable" placeholder="Eg. Ak-509-1066, Kotei, Kumasi" clearable 
          />
          <v-text-field class="input-field" v-model="email" label="EMAIL(OPTIONAL)" type="email" variant="solo-filled"
            density="comfortable" placeholder="Eg. nyamejustice2000@gmail.com" clearable 
          />
          <v-file-input @change="imgChange" @update:model-value="fileChanged" clearable show-size class="select"
            label="STAFF IMAGE" density="comfortable" variant="solo-filled" chips accept="image/*"
            prepend-icon="mdi-image" persistent-hint hint="Upload a picture of the staff">
          </v-file-input>
          <v-select class="select" :items="userAuthStore.superUserData.levels.filter(item=> item.schools.includes(schoolIdentifier)).map(item=> item.identifier)" label="LEVELS" v-model="levels"
            variant="solo-filled" density="comfortable" persistent-hint multiple
            hint="Select levels for the staff" clearable 
          />
          <div v-for="level in userAuthStore.superUserData.levels.filter(item=> levels.includes(item.identifier))" :key="level.identifier">
            <v-select class="select" :items="userAuthStore.superUserData.staffRoles.filter(item=> item.levels.includes(level.identifier))" :label="`STAFF ${level.name} ROLE`" v-model="staffRoles"
              variant="solo-filled" density="comfortable" persistent-hint
              :hint="`Select the role for the staff under the level '${level.name}'`" clearable 
            />
          </div>
          <div v-for="level in userAuthStore.superUserData.levels.filter(item=> levels.includes(item.identifier))" :key="level.identifier">
            <div v-for="role in userAuthStore.superUserData.staffRoles.filter(item=> staffRoles.includes(item.name))" :key="role.name">
              <v-select class="select" v-if="role.levels.includes(level.identifier) && level.has_departments && ['teacher', 'hod'].includes(role.name.toLowerCase())" 
                :items="userAuthStore.superUserData.departments[schoolIdentifier].filter(item=> level.identifier===item.level)" 
                label="DEPARTMENT" v-model="departments" variant="solo-filled" density="comfortable" persistent-hint :hint="`Select the department the staff is in for the level '${level.name}'`" clearable 
              />
            </div>
          </div>
          <v-select class="select" :items="userAuthStore.superUserData.subjects.filter(item=> item.schools.includes(schoolIdentifier)).map(item=> item.identifier)" label="SUJECTS" v-model="selectedSubjects"
            variant="solo-filled" density="comfortable" persistent-hint hint="Select the subjects the staff teaches if any" multiple chips clearable
          />
        </div>

        <!-- file -->
        <div class="overlay-card-content-container" v-if="typeSelected === 'file' && schoolIndex">
          <v-btn class="mb-10" @click="getStaffFile()" v-if="typeSelected === 'file'" :ripple="false" color="blue"
            size="small">
            GET FILE
          </v-btn>
          <v-file-input @change="staffFileChanged" v-if="typeSelected === 'file'" clearable show-size class="select"
            label="UPLOAD FILE" density="comfortable" variant="solo-filled" @update:model-value="fileChanged"
            accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            prepend-icon="mdi-microsoft-excel">
          </v-file-input>
        </div>
        <div class="overlay-card-action-btn-container">
          <v-btn @click="addStaff()" :disabled="isStaffFormValid" :ripple="false" variant="flat" type="submit"
            color="black" size="small" append-icon="mdi-checkbox-marked-circle">
            SUBMIT
          </v-btn>
        </div>
      </div>
    </div>

    <div class="content-header" v-if="staff">
      <div class="content-header-text">
        TOTAL NUMBER OF STAFF:
        <span class="content-header-text-value">
          {{ staff.length }}
        </span>
      </div>
      <div class="content-header-text">
        MALE STAFF:
        <span class="content-header-text-value">
          {{ maleStaff }} <span v-if="staff.length > 0">[{{ ((maleStaff / staff.length) * 100).toFixed(1) }}%]</span>
        </span>
      </div>
      <div class="content-header-text">
        FEMALE STAFF:
        <span class="content-header-text-value">
          {{ femaleStaff }} <span v-if="staff.length > 0">[{{ ((femaleStaff / staff.length) * 100).toFixed(1)
            }}%]</span>
        </span>
      </div>
    </div>
    <div class="content-header btn-container" v-if="staff">
      <v-btn @click="showOverlay(`SuperUserAddStaffOverlay,${schoolIdentifier}`)" color="blue"
        :size="elementsStore.btnSize1">
        ADD STAFF
      </v-btn>
    </div>
    <div class="no-data" v-if="staff.length === 0">
      <p>NO DATA</p>
    </div>
    <v-table fixed-header class="table" v-if="staff.length > 0">
      <thead>
        <tr>
          <th class="table-head">NAME</th>
          <th class="table-head">GENDER</th>
          <th class="table-head">ROLES</th>
          <th class="table-head">LEVEL</th>
          <th class="table-head">DEPARTMENTS</th>
          <th class="table-head">SUBJECTS</th>
          <th class="table-head">DATE OF BIRTH</th>
          <th class="table-head">DATE EMPLOYED</th>
          <th class="table-head">RELIGION</th>
          <th class="table-head">PLACE OF BIRTH</th>
          <th class="table-head">REGION/STATE</th>
          <th class="table-head">NATIONALITY</th>
          <th class="table-head">CONTACT</th>
          <th class="table-head">ALT CONTACT</th>
          <th class="table-head">RESIDENTIAL ADDRESS</th>
          <th class="table-head">EMAIL</th>
          <th class="table-head">IMAGE</th>
          <th class="table-head">ACTION</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(_staff, index) in staff" :key="index">
          <td class="table-data">
            {{ _staff['user'] }}<v-icon icon="mdi-pencil"
              @click="showEditOverlay('user', _staff['user'], _staff['staff_id'], index)" color="black" />
            <v-list-item-subtitle>
              {{ _staff['staff_id'] }}<v-icon v-if="userAuthStore.userData['school']['staff_id']" icon="mdi-pencil"
                size="medium" @click="showEditOverlay('staffId', _staff['staff_id'], _staff['staff_id'], index)"
                color="black" />
            </v-list-item-subtitle>
          </td>
          <td class="table-data">
            {{ _staff['gender'].toUpperCase() }}<v-icon icon="mdi-pencil"
              @click="showEditOverlay('gender', _staff['gender'], _staff['staff_id'], index)" color="black" />
          </td>
          <td class="table-data">
            <v-chip v-for="(role, ind) in _staff['roles']" variant="outlined" :key="ind" :text="(role)"
              :size="elementsStore.btnSize1" />
          </td>
          <td class="table-data">
            <v-chip v-for="(_level, ind) in _staff['levels']" variant="outlined" :key="ind" :text="(_level)"
              :size="elementsStore.btnSize1" />
          </td>
          <td class="table-data">
            <v-chip v-for="(department, ind) in _staff['departments']" variant="outlined" :key="ind"
              :text="(department)" :size="elementsStore.btnSize1" />
          </td>
          <td class="table-data">
            <v-chip v-for="(_subj, ind) in _staff['subjects']" variant="outlined" :key="ind" :text="(_subj)"
              :size="elementsStore.btnSize1" />
          </td>
          <td class="table-data">
            {{ _staff['dob'] }}<v-icon icon="mdi-pencil"
              @click="showEditOverlay('dob', `${_staff['dob']}`, _staff['staff_id'], index)" color="black" />
          </td>
          <td class="table-data">
            {{ _staff['date_enrolled'] }}<v-icon icon="mdi-pencil"
              @click="showEditOverlay('date_enrolled', `${_staff['date_enrolled']}`, _staff['staff_id'], index)"
              color="black" />
          </td>
          <td class="table-data">
            {{ _staff['religion'] }}<v-icon icon="mdi-pencil"
              @click="showEditOverlay('religion', `${_staff['religion']}`, _staff['staff_id'], index)" color="black" />
          </td>
          <td class="table-data">
            {{ _staff['pob'] }}<v-icon icon="mdi-pencil"
              @click="showEditOverlay('pob', `${_staff['pob']}`, _staff['staff_id'], index)" color="black" />
          </td>
          <td class="table-data">
            {{ _staff['region'] }}<v-icon icon="mdi-pencil"
              @click="showEditOverlay('region', `${_staff['region']}`, _staff['staff_id'], index)" color="black" />
          </td>
          <td class="table-data">
            {{ _staff['nationality'] }}<v-icon icon="mdi-pencil"
              @click="showEditOverlay('nationality', `${_staff['nationality']}`, _staff['staff_id'], index)"
              color="black" />
          </td>
          <td class="table-data">
            {{ _staff['contact'] }}<v-icon icon="mdi-pencil"
              @click="showEditOverlay('contact', `${_staff['contact']}`, _staff['staff_id'], index)" color="black" />
          </td>
          <td class="table-data">
            {{ _staff['alt_contact'] }}<v-icon icon="mdi-pencil"
              @click="showEditOverlay('alt_contact', `${_staff['alt_contact']}`, _staff['staff_id'], index)"
              color="black" />
          </td>
          <td class="table-data">
            {{ _staff['address'] }}<v-icon icon="mdi-pencil"
              @click="showEditOverlay('address', `${_staff['address']}`, _staff['staff_id'], index)" color="black" />
          </td>
          <td class="table-data">
            {{ _staff['email'] }}<v-icon icon="mdi-pencil"
              @click="showEditOverlay('email', `${_staff['email']}`, _staff['staff_id'], index)" color="black" />
          </td>
          <td class="table-data">
            <img class="profile-img" :src="_staff['img']">
            <v-icon icon="mdi-pencil" @click="showEditOverlay('img', `${_staff['img']}`, _staff['staff_id'], index)"
              color="black" />
          </td>
          <td class="table-data">
            <v-btn color="red" size="x-small" variant="flat"
              @click="elementsStore.ShowDeletionOverlay(() => deleteStaff(_staff['staff_id']), 'Are you sure you want to delete this staff?')">
              DELETE
            </v-btn>
          </td>
        </tr>
      </tbody>
    </v-table>
  </div>
</template>

<style scoped>
.content-header {
  min-height: 20% !important;
}

.btn-container {
  min-height: 10% !important;
}

.overlay-card-info-container {
  margin-top: 3em !important;
}

.overlay-card {
  max-width: 600px !important;
}

.previous-value {
  font-size: .7rem !important;
  font-family: Verdana, Geneva, Tahoma, sans-serif;
  color: green;
}

@media screen and (min-width: 400px) {
  .content-header {
    min-height: 15% !important;
  }

  .btn-container {
    min-height: 10% !important;
  }

  .previous-value {
    font-size: .75rem !important;
  }
}

@media screen and (min-width: 576px) {
  .previous-value {
    font-size: .8rem !important;
  }
}



@media screen and (min-width: 700px) {
  .content-header {
    min-height: 10% !important;
  }

  .previous-value {
    font-size: .75rem !important;
  }
}

@media screen and (min-width: 767px) {
  .previous-value {
    font-size: .85rem !important;
  }
}
</style>
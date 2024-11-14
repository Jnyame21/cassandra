<script setup lang="ts">
import { AxiosError } from 'axios';
import { computed, ref } from 'vue';
import axiosInstance from '@/utils/axiosInstance';
import { useUserAuthStore } from '@/stores/userAuthStore';
import { useElementsStore } from '@/stores/elementsStore';
import { downloadFile } from '@/utils/util';
import TheLoader from './TheLoader.vue';

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()
const firstName = ref('')
const lastName = ref('')
const staffId = ref('')
const gender = ref('')
const dateOfBirth = ref('')
const department = ref('')
const selectedSubjects = ref([])
const staffRole = ref('')
const contact = ref('')
const address = ref('')
const img = ref('')
const nationality = ref('')
const departmentSelected = ref('')
const departmentHod = ref('')
const typeSelected = ref('')
const region = ref('')
const religion = ref('')
const nationalitySelected = ref('')
const formErrorMessage = ref('')
const email = ref('')
const dateEnrolled = ref('')
const pob = ref('')
const staffFile:any = ref(null)
const altContact = ref('')


const staff = computed(() => {
  return userAuthStore.adminData.staff
})

const maleStaff = computed(() => {
  if (userAuthStore.adminData.staff) {
    return userAuthStore.adminData.staff.filter((item: any) => item['gender'].toLowerCase() === 'male').length
  }
  return 0;
})

const femaleStaff = computed(() => {
  if (userAuthStore.adminData.staff) {
    return userAuthStore.adminData.staff.filter((item: any) => item['gender'].toLowerCase() === 'female').length
  }
  return 0;
})

const genderOptions = [
  { 'label': 'MALE', 'value': 'male' },
  { 'label': 'FEMALE', 'value': 'female' },
]

const typeOptions = [
  { 'label': 'USE AN EXCEL FILE', 'value': 'file' },
  { 'label': 'INPUT DATA HERE', 'value': 'noFile' },
]

const roleOptions = [
  { 'label': 'TEACHER', 'value': 'teacher' },
  { 'label': 'HEADMASTER/HEADMISTRESS', 'value': 'head' },
  { 'label': 'ASSISTANT HEADMASTER/HEADMISTRESS', 'value': 'assistant_head' },
  { 'label': 'HEAD OF ACADEMICS', 'value': 'head_of_academic' },
  { 'label': 'ASSISTANT HEAD OF ACADEMICS', 'value': 'assistant_head_of_academics' },
  { 'label': 'ADMINISTRATOR', 'value': 'administrator' },
]

const nationalityOptions = [
  { 'label': 'GHANAIAN', 'value': 'Ghanaian' },
  { 'label': 'OTHER', 'value': 'other' },
]

const regionOptions = [
  { 'label': 'GREATER ACCRA', 'value': 'Greater Accra' },
  { 'label': 'ASHANTI', 'value': 'Ashanti' },
  { 'label': 'WESTERN', 'value': 'Western' },
  { 'label': 'WESTERN NORTH', 'value': 'Western North' },
  { 'label': 'CENTRAL', 'value': 'Central' },
  { 'label': 'EASTERN', 'value': 'Eastern' },
  { 'label': 'VOLTA', 'value': 'Volta' },
  { 'label': 'OTI', 'value': 'Oti' },
  { 'label': 'NORTHERN', 'value': 'Northern' },
  { 'label': 'NORTH EAST', 'value': 'North East' },
  { 'label': 'SAVANNAH', 'value': 'Savannah' },
  { 'label': 'UPPER EAST', 'value': 'Upper East' },
  { 'label': 'UPPER WEST', 'value': 'Upper West' },
  { 'label': 'BONO', 'value': 'Bono' },
  { 'label': 'BONO EAST', 'value': 'Bono East' },
  { 'label': 'AHAFO', 'value': 'Ahafo' }
]

const religionOptions = [
  { 'label': 'CHRISTIANITY', 'value': 'Christianity' },
  { 'label': 'ISLAM', 'value': 'Islam' },
  { 'label': 'TRADITIONAL AFRICAN RELIGION', 'value': 'Traditional African Religion' },
  { 'label': 'HINDUISM', 'value': 'Hinduism' },
  { 'label': 'BUDDHISM', 'value': 'Buddhism' },
  { 'label': 'NONE', 'value': 'None' },
  { 'label': 'OTHER', 'value': 'Other' }
];

const addStaff = async () => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  if (typeSelected.value === 'noFile'){
    formData.append('type', 'createWithoutFile')
    formData.append('firstName', firstName.value)
    formData.append('lastName', lastName.value)
    formData.append('dateOfBirth', dateOfBirth.value)
    formData.append('gender', gender.value)
    formData.append('role', staffRole.value)
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
    if (userAuthStore.userData['school']['staff_id']) {
      formData.append('staff_id', staffId.value)
    }
    if (userAuthStore.userData['school']['has_departments']) {
      formData.append('department', department.value)
    }
  }
  else if (typeSelected.value === 'file'){
    formData.append('type', 'createWithFile')
    formData.append('file', staffFile.value)
  }

  try {
    const response = await axiosInstance.post('school-admin/staff', formData)
    const data = response.data
    data.forEach((item:any)=>{
      userAuthStore.adminData.staff?.unshift(item)
    })
    staffFile.value = null
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

const setDepartmentHOD = async () => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', 'setDepartmentHOD')
  formData.append('department', departmentSelected.value)
  formData.append('staffId', departmentHod.value)

  try {
    const response = await axiosInstance.post('school-admin/staff', formData)
    const data = response.data
    const staffHod = userAuthStore.adminData.staff?.find((item: any) => item['staff_id'] === departmentHod.value)
    if (staffHod && userAuthStore.adminData.staff) {
      const staffHodIndex = userAuthStore.adminData.staff.indexOf(staffHod)
      userAuthStore.adminData.staff[staffHodIndex]['role'] = 'hod'
    }
    const previousHod = userAuthStore.adminData.staff?.find((item: any) => item['staff_id'] === data['previous_hod_id'])
    if (previousHod && userAuthStore.adminData.staff) {
      const previousHodIndex = userAuthStore.adminData.staff.indexOf(previousHod)
      userAuthStore.adminData.staff[previousHodIndex]['role'] = 'teacher'
    }
    departmentSelected.value = ''
    departmentHod.value = ''
    elementsStore.HideLoadingOverlay()
    closeOverlay('AdminSetDepartmentHODOverlay')
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
    const staffToDelet = userAuthStore.adminData.staff?.find((item: any) => item['staff_id'] === staffToDeleteId)
    if (staffToDelet && userAuthStore.adminData.staff) {
      const staffToDeletIndex = userAuthStore.adminData.staff.indexOf(staffToDelet)
      userAuthStore.adminData.staff.splice(staffToDeletIndex, 1)
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

const imgChange = (event: any) => {
  const file = event.target.files[0]
  img.value = file
}

const staffFileChanged = (event: any) => {
  const file = event.target.files[0]
  staffFile.value = file
}

const requiredFields = computed(() => {
  return !(firstName.value && lastName.value && contact.value && address.value && nationality.value && dateOfBirth.value && gender.value && staffRole.value && selectedSubjects.value.length > 0 && region.value && religion.value && pob.value)
})

const isStaffFormValid = computed(() => {
  if (typeSelected.value === 'noFile'){
    if (userAuthStore.userData['school']['has_departments']) {
      if (userAuthStore.userData['school']['staff_id']) {
        return !(department.value && staffId.value && !requiredFields.value)
      }
      else {
        return !(department.value && !requiredFields.value)
      }
    }
    else {
      if (userAuthStore.userData['school']['staff_id']) {
        return !(staffId.value && !requiredFields.value)
      }
      else {
        return !requiredFields.value
      }
    }
  }
  else if (typeSelected.value === 'file'){
    return !(staffFile.value)
  }
  return true;
})

const nationalityChanged = (value: string) => {
  if (value === 'Ghanaian') {
    nationality.value = value
  }
  else {
    nationality.value = ''
  }
  region.value = ''
}

const showOverlay = (element: string) => {
  const overlay = document.getElementById(element)
  if (overlay) {
    overlay.style.display = 'flex'
  }
}

const clearSelectedStaff = () => {
  departmentHod.value = ''
}
const closeOverlay = (element: string) => {
  const overlay = document.getElementById(element)
  if (overlay) {
    overlay.style.display = 'none'
  }
}


</script>

<template>
  <div class="content-wrapper" v-show="elementsStore.activePage === 'AdminStaff'"
    :class="{ 'is-active-page': elementsStore.activePage === 'AdminStaff' }">
    <!-- add staff overlay -->
    <div id="AdminAddStaffOverlay" class="overlay" v-if="staff">
      <div class="overlay-card">
        <v-btn @click="closeOverlay('AdminAddStaffOverlay')" color="red" size="small" variant="flat"
          class="close-btn">X</v-btn>
        <p class="form-message" v-if="formErrorMessage">{{ formErrorMessage }}</p>
        <form class="overlay-card-content-container">
          <v-select class="select" :items="typeOptions" label="UPLOAD TYPE" v-model="typeSelected" item-title="label"
            item-value="value" variant="solo-filled" density="comfortable" persistent-hint
            hint="Select whether you want to use an excel file or input the data here" />
          <v-text-field class="input-field" v-if="typeSelected === 'noFile'" v-model="firstName" label="FIRST NAME"
            clearable variant="solo-filled" density="comfortable" placeholder="Eg. Cassandra" persistent-hint
            hint="Enter the first name of the staff" />
          <v-text-field class="input-field" v-if="typeSelected === 'noFile'" v-model="lastName"
            label="LAST NAME (MIDDLE NAME + SURNAME)" clearable variant="solo-filled" density="comfortable"
            placeholder="Eg. Akua Afriyie" persistent-hint hint="Enter the last name of the staff" />
          <v-select class="select" v-if="typeSelected === 'noFile'" :items="genderOptions" label="GENDER"
            v-model="gender" item-title="label" item-value="value" variant="solo-filled" density="comfortable"
            clearable />
          <v-text-field v-if="typeSelected === 'noFile' && userAuthStore.userData['school']['staff_id']"
            class="input-field" v-model="staffId" label="STAFF ID" variant="solo-filled" density="comfortable" clearable
            persistent-hint hint="Enter the staff ID of the staff" />
          <v-text-field class="input-field" v-if="typeSelected === 'noFile'" v-model="dateOfBirth" label="DATE OF BIRTH"
            type="date" variant="solo-filled" density="comfortable" clearable />
          <v-text-field class="input-field" v-if="typeSelected === 'noFile'" v-model="dateEnrolled"
            label="DATE EMPLOYED" type="date" variant="solo-filled" density="comfortable" clearable />
          <v-select class="select" v-if="typeSelected === 'noFile'" @update:model-value="nationalityChanged"
            :items="nationalityOptions" label="NATIONALITY" v-model="nationalitySelected" item-title="label"
            item-value="value" variant="solo-filled" density="comfortable" persistent-hint
            hint="Select the nationality of the staff" />
          <v-text-field class="input-field" v-if="typeSelected === 'noFile' && nationalitySelected === 'other'"
            v-model="nationality" label="SPECIFY THE NATIONALITY" variant="solo-filled" density="comfortable"
            placeholder="Eg. Nigerian" clearable persistent-hint hint="Enter the nationality of the staff" />
          <v-select class="select" v-if="typeSelected === 'noFile' && nationalitySelected === 'Ghanaian'"
            :items="regionOptions" label="REGION" v-model="region" item-title="label" item-value="value"
            variant="solo-filled" density="comfortable" persistent-hint hint="Select the region the staff is from" />
          <v-text-field class="input-field" v-if="typeSelected === 'noFile' && nationalitySelected === 'other'"
            v-model="region" label="REGION/STATE" variant="solo-filled" density="comfortable" placeholder="Eg. Asanti"
            clearable persistent-hint hint="Enter the region/state the staff is from" />
          <v-text-field class="input-field" v-if="typeSelected === 'noFile'" v-model="pob"
            label="PLACE OF BIRTH(HOME CITY/TOWN)" variant="solo-filled" density="comfortable"
            placeholder="Eg. Ayeduase" clearable persistent-hint hint="Enter the city/town the staff was born" />
          <v-text-field class="input-field" v-if="typeSelected === 'noFile'" v-model="contact" label="PHONE NUMBER"
            variant="solo-filled" density="comfortable" placeholder="Eg. 0596021383" clearable />
          <v-text-field class="input-field" v-if="typeSelected === 'noFile'" v-model="altContact"
            label="ALTERNATE PHONE NUMBER(OPTIONAL)" variant="solo-filled" density="comfortable"
            placeholder="Eg. 0596021383" clearable />
          <v-select class="select" v-if="typeSelected === 'noFile'" :items="religionOptions" label="RELIGION"
            v-model="religion" item-title="label" item-value="value" variant="solo-filled" density="comfortable"
            persistent-hint hint="Select religion the staff belongs to" />
          <v-text-field class="input-field" v-if="typeSelected === 'noFile'" v-model="address"
            label="RESIDENTIAL ADDRESS" type="address" variant="solo-filled" density="comfortable"
            placeholder="Eg. Ak-509-1066, Kotei, Kumasi" clearable />
          <v-text-field class="input-field" v-if="typeSelected === 'noFile'" v-model="email" label="EMAIL(OPTIONAL)"
            type="email" variant="solo-filled" density="comfortable" placeholder="Eg. nyamejustice2000@gmail.com"
            clearable />
          <v-file-input @change="imgChange" v-if="typeSelected === 'noFile'" clearable show-size class="select"
            label="STAFF IMAGE" density="comfortable" variant="solo-filled" accept="image/*" prepend-icon="mdi-image"
            persistent-hint hint="Upload a picture of the staff">
          </v-file-input>
          <v-select class="select" v-if="typeSelected === 'noFile'" :items="roleOptions" label="ROLE"
            v-model="staffRole" item-title="label" item-value="value" variant="solo-filled" density="comfortable"
            persistent-hint hint="Select the role of the staff" />
          <v-select class="select"
            v-if="typeSelected === 'noFile' && ['teacher', 'hod'].includes(staffRole) && userAuthStore.userData['school']['has_departments']"
            :items="userAuthStore.adminData.departments" label="DEPARTMENT" v-model="department" variant="solo-filled"
            density="comfortable" persistent-hint hint="Select the department the staff belongs to" clearable />
          <v-select class="select" v-if="typeSelected === 'noFile' && ['teacher', 'hod'].includes(staffRole)"
            :items="userAuthStore.adminData.subjects" label="SUJECTS" v-model="selectedSubjects" variant="solo-filled"
            density="comfortable" persistent-hint hint="Select the subjects the staff teaches" multiple chips
            clearable />

          <!-- file -->
          <v-btn class="mb-10" @click="getStaffFile()" v-if="typeSelected === 'file'" :ripple="false" color="blue"
            size="small">GET FILE</v-btn>
          <v-file-input @change="staffFileChanged" v-if="typeSelected === 'file'" clearable show-size class="select"
            label="UPLOAD FILE" density="comfortable" variant="solo-filled"
            accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            prepend-icon="mdi-microsoft-excel">
          </v-file-input>
        </form>
        <div class="overlay-card-action-btn-container">
          <v-btn @click="addStaff()" :disabled="isStaffFormValid" :ripple="false" variant="flat" type="submit"
            color="black" size="small" append-icon="mdi-checkbox-marked-circle">
            SUBMIT
          </v-btn>
        </div>
      </div>
    </div>

    <!-- Set Department HOD overlay -->
    <div id="AdminSetDepartmentHODOverlay" class="overlay"
      v-if="staff && userAuthStore.userData['school']['has_departments']">
      <div class="overlay-card">
        <v-btn @click="closeOverlay('AdminSetDepartmentHODOverlay')" color="red" size="small" variant="flat"
          class="close-btn">X</v-btn>
        <div class="overlay-card-content-container">
          <v-select class="select" :items="userAuthStore.adminData.departments" label="DEPARTMENT"
            v-model="departmentSelected" @update:model-value="clearSelectedStaff" variant="solo-filled"
            density="comfortable" persistent-hint hint="Select the department for which the staff is the HOD"
            clearable />
          <v-select class="select" v-if="departmentSelected"
            :items="userAuthStore.adminData.staff.filter((item: any) => item['department'] === departmentSelected)"
            label="STAFF" v-model="departmentHod" item-title="user" item-value="staff_id" variant="solo-filled"
            density="comfortable" persistent-hint hint="Select the staff" clearable>
            <template v-slot:item="{ props, item }">
              <v-list-item v-bind="props" :subtitle="(item as any).raw.staff_id"></v-list-item>
            </template>
          </v-select>
        </div>
        <div class="overlay-card-action-btn-container">
          <v-btn @click="setDepartmentHOD()" :disabled="!(departmentHod && departmentSelected)" :ripple="false"
            variant="flat" type="submit" color="black" size="small" append-icon="mdi-checkbox-marked-circle">
            SUBMIT
          </v-btn>
        </div>
      </div>
    </div>

    <TheLoader :func="userAuthStore.getAdminData" v-if="!staff" />
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
          {{ maleStaff }} [{{ ((maleStaff / staff.length) * 100).toFixed(1) }}%]
        </span>
      </div>
      <div class="content-header-text">
        FEMALE STAFF:
        <span class="content-header-text-value">
          {{ femaleStaff }} [{{ ((femaleStaff / staff.length) * 100).toFixed(1) }}%]
        </span>
      </div>
    </div>
    <div class="content-header btn-container" v-if="staff">
      <v-btn @click="showOverlay('AdminAddStaffOverlay')" color="blue" :size="elementsStore.btnSize1">
        ADD STAFF
      </v-btn>
      <v-btn v-if="userAuthStore.userData['school']['has_departments']"
        @click="showOverlay('AdminSetDepartmentHODOverlay')" class="ml-5" color="blue" :size="elementsStore.btnSize1">
        SET DEPARTMENT HOD
      </v-btn>
    </div>
    <v-table fixed-header class="table" v-if="staff">
      <thead>
        <tr>
          <th class="table-head">NAME</th>
          <th class="table-head">GENDER</th>
          <th class="table-head">ROLE</th>
          <th class="table-head">DEPARTMENT</th>
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
            {{ _staff['user'] }}
            <v-list-item-subtitle>{{ _staff['staff_id'] }}</v-list-item-subtitle>
          </td>
          <td class="table-data">{{ _staff['gender'].toUpperCase() }}</td>
          <td class="table-data">{{ _staff['role'].toUpperCase() }}</td>
          <td class="table-data">{{ _staff['department'] }}</td>
          <td class="table-data">
            <span v-for="(_subj, ind) in _staff['subjects']" :key="ind">{{ _subj }}</span>
          </td>
          <td class="table-data">{{ _staff['dob'] }}</td>
          <td class="table-data">{{ _staff['date_enrolled'] }}</td>
          <td class="table-data">{{ _staff['religion'] }}</td>
          <td class="table-data">{{ _staff['pob'] }}</td>
          <td class="table-data">{{ _staff['region'] }}</td>
          <td class="table-data">{{ _staff['nationality'] }}</td>
          <td class="table-data">{{ _staff['contact'] }}</td>
          <td class="table-data">{{ _staff['alt_contact'] }}</td>
          <td class="table-data">{{ _staff['address'] }}</td>
          <td class="table-data">{{ _staff['email'] }}</td>
          <td class="table-data"><img class="profile-img" :src="_staff['img']"></td>
          <td class="table-data">
            <v-btn color="red" size="x-small" v-if="['teacher', 'hod'].includes(_staff['role'].toLowerCase())" variant="flat"
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

.overlay-card-content-container {
  margin-top: 3em !important;
}

.overlay-card {
  max-width: 600px !important;
}

@media screen and (min-width: 400px) {
  .content-header {
    min-height: 15% !important;
  }

  .btn-container {
    min-height: 10% !important;
  }
}

@media screen and (min-width: 700px) {
  .content-header {
    min-height: 10% !important;
  }
}

@media screen and (min-width: 1200px) {}
</style>
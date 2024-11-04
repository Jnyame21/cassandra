<script setup lang="ts">
import { AxiosError } from 'axios';
import { computed, ref } from 'vue';
import axiosInstance from '@/utils/axiosInstance';
import { useUserAuthStore } from '@/stores/userAuthStore';
import { useElementsStore } from '@/stores/elementsStore';

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
// const typeSelected = ref('')
// const file:any = ref(null)


// const showOverlay = (element: string) => {
//   const overlay = document.getElementById(element)
//   if (overlay) {
//     overlay.style.display = 'flex'
//   }
// }

// const closeOverlay = (element: string) => {
//   formErrorMessage.value = ''
//   subjectSelected.value = null
//   toClass.value = null
//   const overlay = document.getElementById(element)
//   if (overlay) {
//     overlay.style.display = 'none'
//   }
// }
const staff = computed(()=>{
  return userAuthStore.adminData.staff
})

const maleStaff = computed(()=>{
  return userAuthStore.adminData.staff.filter((item:any)=> item['gender'].toLowerCase() === 'male').length
})

const femaleStaff = computed(()=>{
  return userAuthStore.adminData.staff.filter((item:any)=> item['gender'].toLowerCase() === 'female').length
})

const genderOptions = [
  {'label': 'MALE', 'value': 'male'},
  {'label': 'FEMALE', 'value': 'female'},
]

// const typeOptions = [
//   {'label': 'USER AN EXCEL FILE', 'value': 'file'},
//   {'label': 'INPUT DATA HERE', 'value': 'noFile'},
// ]

const roleOptions = [
  {'label': 'TEACHER', 'value': 'teacher'},
  {'label': 'HOD', 'value': 'hod'},
  {'label': 'HEADMASTER/HEADMISTRESS', 'value': 'head'},
  {'label': 'ASSISTANT HEADMASTER/HEADMISTRESS', 'value': 'assistant_head'},
  {'label': 'HEAD OF ACADEMICS', 'value': 'head_of_academic'},
  {'label': 'ASSISTANT HEAD OF ACADEMICS', 'value': 'assistant_head_of_academics'},
  {'label': 'ADMINISTRATOR', 'value': 'admin'},
]

const addStaff = async () => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', 'create')
  formData.append('firstName', firstName.value)
  formData.append('lastName', lastName.value)
  formData.append('dateOfBirth', dateOfBirth.value)
  formData.append('gender', gender.value)
  formData.append('role', staffRole.value)
  formData.append('contact', contact.value)
  formData.append('address', address.value)
  formData.append('img', img.value)
  formData.append('nationality', nationality.value)
  formData.append('subjects', JSON.stringify(selectedSubjects.value))
  if (userAuthStore.userData['school']['staff_id']){
    formData.append('staff_id', staffId.value)
  }
  if (userAuthStore.userData['school']['has_departments']){
    formData.append('department', department.value)
  }

  try {
    const response = await axiosInstance.post('school-admin/staff', formData)
    userAuthStore.adminData.staff.unshift(response.data)
    firstName.value = ''
    lastName.value = ''
    selectedSubjects.value = []
    dateOfBirth.value = ''
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

// const assignClassHeadTeacher = async () => {
//   elementsStore.ShowLoadingOverlay()
//   const formData = new FormData()
//   formData.append('type', 'assignClassHeadTeacher')
//   formData.append('studentsClass', className);
//   formData.append('teacherId', selectedHeadTeacher.value);

//   try {
//     const response = await axiosInstance.post('school-admin/data', formData)
//     userAuthStore.adminData.classes[classIndex]['head_teacher'] = response.data
//     closeOverlay(`AdminAssignClassHeadTeacherOverlay${className}${classIndex}`)
//     elementsStore.HideLoadingOverlay()
//   }
//   catch (error) {
//     elementsStore.HideLoadingOverlay()
//     if (error instanceof AxiosError) {
//       if (error.response) {
//         if (error.response.status === 400 && error.response.data.message) {
//           elementsStore.ShowOverlay(error.response.data.message, 'red', null, null)
//         } else {
//           elementsStore.ShowOverlay('Oops! something went wrong. Try again later', 'red', null, null)
//         }
//       }
//       else if (!error.response && (error.code === 'ECONNABORTED' || !navigator.onLine)) {
//         elementsStore.ShowOverlay('A network error occurred! Please check you internet connection', 'red', null, null)
//       }
//       else {
//         elementsStore.ShowOverlay('An unexpected error occurred!', 'red', null, null)
//       }
//     }
//   }
// }

const isStaffFormValid = computed(()=>{
  if (userAuthStore.userData['school']['has_departments']){
    if (userAuthStore.userData['school']['staff_id']){
      return !(firstName.value && lastName.value && contact.value && address.value && nationality.value && staffId.value && dateOfBirth.value && gender.value && staffRole.value && department.value && selectedSubjects.value.length > 0)
    }
    else{
      return !(firstName.value && lastName.value && contact.value && address.value && nationality.value && dateOfBirth.value && gender.value && staffRole.value && department.value && selectedSubjects.value.length > 0)
    }
  }
  else{
    if (userAuthStore.userData['school']['staff_id']){
      return !(firstName.value && lastName.value && contact.value && address.value && nationality.value && staffId.value && dateOfBirth.value && gender.value && staffRole.value && selectedSubjects.value.length > 0)
    }
    else{
      return !(firstName.value && lastName.value && contact.value && address.value && nationality.value && dateOfBirth.value && gender.value && staffRole.value)
    }
  }
})

const showOverlay = (element:string)=>{
  const overlay = document.getElementById(element)
  if (overlay){
    overlay.style.display = 'flex'
  }
}

const closeOverlay = (element:string)=>{
  const overlay = document.getElementById(element)
  if (overlay){
    overlay.style.display = 'none'
  }
}


</script>

<template>
  <div class="content-wrapper" v-show="elementsStore.activePage === 'AdminStaff'" :class="{ 'is-active-page': elementsStore.activePage === 'AdminStaff' }">
    <!-- link class overlay -->
    <div id="AdminAddStaffOverlay" class="overlay">
      <div class="overlay-card">
        <v-btn @click="closeOverlay('AdminAddStaffOverlay')" color="red" size="small" variant="flat" class="close-btn">X</v-btn>
        <div class="overlay-card-content-container">
          <!-- <v-select class="select" :items="typeOptions" label="UPLOAD TYPE" v-model="typeSelected" 
          item-title="label" item-value="value" variant="solo-filled" density="comfortable" persistent-hint hint="Select whether you want to use an excel file or input the data here" 
          /> -->
          <v-text-field class="input-field" v-model="firstName" label="FIRST NAME"
            variant="solo-filled" density="comfortable" persistent-hint hint="Enter the first name of the staff" 
          />
          <v-text-field class="input-field" v-model="lastName" label="LAST NAME"
            variant="solo-filled" density="comfortable" persistent-hint hint="Enter the last name of the staff" 
          />
          <v-select class="select" :items="genderOptions" label="GENDER" v-model="gender" 
          item-title="label" item-value="value" variant="solo-filled" density="comfortable" 
          />
          <v-text-field v-if="userAuthStore.userData['school']['staff_id']" class="input-field" v-model="staffId" label="STAFF ID"
            variant="solo-filled" density="comfortable" persistent-hint hint="Enter the staff ID of the staff" 
          />
          <v-text-field class="input-field" v-model="dateOfBirth" label="DATE OF BIRTH" type="date"
            variant="solo-filled" density="comfortable" persistent-hint hint="Enter the date of birth of the staff" 
          />
          <v-text-field class="input-field" v-model="contact" label="PHONE NUMBER" type="contact"
            variant="solo-filled" density="comfortable" persistent-hint hint="Enter phone number of the staff" 
          />
          <v-text-field class="input-field" v-model="contact" label="ADDRESS" type="address"
            variant="solo-filled" density="comfortable" persistent-hint hint="Enter add of the staff" 
          />
          <v-text-field class="input-field" v-model="nationality" label="NATIONALITY" type="contact"
            variant="solo-filled" density="comfortable" persistent-hint hint="Enter phone number of the staff" 
          />
          <v-select class="select" :items="roleOptions" label="ROLE" v-model="staffRole" 
          item-title="label" item-value="value" variant="solo-filled" density="comfortable" persistent-hint hint="Select the role of the staff" 
          />
          <v-select class="select" v-if="['teacher', 'hod'].includes(staffRole) && userAuthStore.userData['school']['has_departments']" :items="userAuthStore.adminData.departments" label="DEPARTMENT" v-model="department" 
          variant="solo-filled" density="comfortable" persistent-hint hint="Select the department the staff belongs to" 
          />
          <v-select class="select" v-if="['teacher', 'hod'].includes(staffRole)" :items="userAuthStore.adminData.subjects" label="SUJECTS" v-model="selectedSubjects" 
          variant="solo-filled" density="comfortable" persistent-hint hint="Select the subjects the staff teaches" multiple chips
          />
        </div>
        <div class="overlay-card-action-btn-container">
          <v-btn @click="addStaff()" :disabled="isStaffFormValid" :ripple="false" variant="flat"
            type="submit" color="black" size="small" append-icon="mdi-checkbox-marked-circle">
            SUBMIT
          </v-btn>
        </div>
      </div>
    </div>
    <div class="content-header">
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
    <div class="content-header btn-container">
      <v-btn @click="showOverlay('AdminAddStaffOverlay')" class="ml-5" color="blue"
        :size="elementsStore.btnSize1">
        ADD STAFF
      </v-btn>
    </div>
    <v-table fixed-header class="table">
      <thead>
        <tr>
          <th class="table-head">NAME</th>
          <th class="table-head">GENDER</th>
          <th class="table-head">ROLE</th>
          <th class="table-head">DEPARTMENT</th>
          <th class="table-head">SUBJECTS</th>
          <th class="table-head">DATE OF BIRTH</th>
          <th class="table-head">NATIONALITY</th>
          <th class="table-head">CONTACT</th>
          <th class="table-head">IMAGE</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(_staff, index) in staff" :key="index">
          <td class="table-data">
            {{ _staff['user'] }}
            <v-list-item-subtitle>{{ _staff['staff_id'] }}</v-list-item-subtitle>
          </td>
          <td class="table-data">{{ _staff['gender'] }}</td>
          <td class="table-data">{{ _staff['role'] }}</td>
          <td class="table-data">{{ _staff['department'] }}</td>
          <td class="table-data">
            <span v-for="(_subj, ind) in _staff['subjects']" :key="ind">{{ _subj }}</span>
          </td>
          <td class="table-data">{{ _staff['dob'] }}</td>
          <td class="table-data">{{ _staff['nationality'] }}</td>
          <td class="table-data">{{ _staff['contact'] }}</td>
          <td class="table-data"><img class="profile-img" :src="_staff['img']"></td>
        </tr>
      </tbody>
    </v-table>
  </div>
</template>

<style scoped>

.content-header{
  min-height: 20% !important;
}
.btn-container{
  min-height: 10% !important;
}
.overlay-card-content-container{
  margin-top: 3em !important;
}

@media screen and (min-width: 500px) {
  
}

@media screen and (min-width: 576px) {
  
}

@media screen and (min-width: 767px) {
  
}

@media screen and (min-width: 1200px) {
  
}



</style>
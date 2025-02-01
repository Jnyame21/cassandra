<script setup lang="ts">
import { AxiosError } from 'axios';
import { ref, computed } from 'vue';
import axiosInstance from '@/utils/axiosInstance';
import { useUserAuthStore } from '@/stores/userAuthStore';
import { useElementsStore } from '@/stores/elementsStore';
import { downloadFile, countriesData, ghanaRegions, genderOptions, religionOptions, uploadTypeOptions } from '@/utils/util';


const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()
const formErrorMessage = ref('')
const firstName = ref('')
const lastName = ref('')
const dob = ref('')
const contact = ref('')
const address = ref('')
const studentId = ref('')
const guardianContact = ref('')
const guardianAddress = ref('')
const guardianEmail = ref('')
const guardianNationality = ref('')
const guardianOccupation = ref('')
const img: any = ref('')
const gender = ref('')
const nationality = ref('')
const typeSelected = ref('')
const guardianFullname = ref('')
const guardianGender = ref('')
const studentsExcelFile: any = ref('')
const dateEnrolled = ref('')
const email = ref('')
const religion = ref('')
const region = ref('')
const pob = ref('')
const editType = ref('')
const nameTypeSelected = ref('')
const newValue: any = ref('')
const previousValue = ref('')
const editStudentIndex = ref(0)
const editStudentId = ref('')

interface Props {
  className: string;
  classIndex: number;
  subjects: string[];
  students_year: number;
  program: string | null;
}

const props = defineProps<Props>()
const className = props.className
const classIndex = props.classIndex || 0
const subjects = props.subjects
const students_year = props.students_year
const program = props.program || null
const selectedHeadTeacher = ref('')

const students = computed(() => {
  return userAuthStore.adminData.classes[classIndex].students || []
})

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

const showOverlay = (element: string) => {
  const overlay = document.getElementById(element)
  if (overlay) {
    overlay.style.display = 'flex'
  }
}

const nameTypeOptions = [
  { 'label': 'FIRST NAME', 'value': 'firstName' },
  { 'label': 'LAST NAME', 'value': 'lastName' },
]

const maleStudents = computed(() => {
  return students.value.filter(item => item.gender.toLowerCase() === 'male').length
})

const femaleStudents = computed(() => {
  return students.value.filter(item => item.gender.toLowerCase() === 'female').length
})

const removeClassHeadTeacher = async () => {
  const formData = new FormData()
  formData.append('type', 'removeClassHeadTeacher')
  formData.append('studentsClassName', className);
  elementsStore.ShowLoadingOverlay()
  try {
    await axiosInstance.post('school-admin/students', formData)
    userAuthStore.adminData.classes[classIndex].head_teacher = null
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

const assignClassHeadTeacher = async () => {
  const formData = new FormData()
  formData.append('type', 'assignClassHeadTeacher')
  formData.append('studentsClass', className);
  formData.append('teacherId', selectedHeadTeacher.value);
  elementsStore.ShowLoadingOverlay()
  try {
    const response = await axiosInstance.post('school-admin/students', formData)
    userAuthStore.adminData.classes[classIndex]['head_teacher'] = response.data
    selectedHeadTeacher.value = ''
    closeOverlay(`AdminAssignClassHeadTeacherOverlay${className}${classIndex}`)
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

const getStudentFile = async () => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', 'getFile')
  formData.append('studentsClassName', className)

  try {
    const response = await axiosInstance.post('school-admin/students', formData, { 'responseType': 'blob' })
    downloadFile(response.headers, response.data, "students-creation-file.xlsx")
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

const addStudent = async () => {
  const formData = new FormData()
  formData.append('studentsClassName', className);
  if (typeSelected.value === 'file') {
    formData.append('type', 'createWithFile')
    formData.append('file', studentsExcelFile.value);
  }
  else if (typeSelected.value === 'noFile') {
    formData.append('type', 'createWithoutFile')
    formData.append('studentClassName', className)
    formData.append('year', userAuthStore.activeAcademicYear)
    formData.append('term', userAuthStore.activeTerm.toString());
    formData.append('firstName', firstName.value);
    formData.append('lastName', lastName.value);
    formData.append('gender', gender.value);
    formData.append('dob', dob.value);
    formData.append('studentId', studentId.value);
    formData.append('img', img.value);
    if (img.value && img.value?.size > 1024 * 1024) {
      showErrorMessage("The size of the image must not exceed 1MB")
      return;
    }

    formData.append('nationality', nationality.value);
    formData.append('contact', contact.value);
    formData.append('religion', religion.value);
    formData.append('dateEnrolled', dateEnrolled.value);
    formData.append('region', region.value);
    formData.append('pob', pob.value);
    formData.append('email', email.value)
    formData.append('address', address.value);
    formData.append('guardianFullname', guardianFullname.value);
    formData.append('guardianGender', guardianGender.value);
    formData.append('guardianOccupation', guardianOccupation.value);
    formData.append('guardianAddress', guardianAddress.value);
    formData.append('guardianEmail', guardianEmail.value);
    formData.append('guardianNationality', guardianNationality.value);
    formData.append('guardianContact', guardianContact.value);
  }
  else {
    return;
  }
  elementsStore.ShowLoadingOverlay()
  try {
    const response = await axiosInstance.post('school-admin/students', formData)
    const data = response.data
    if (typeSelected.value === 'noFile') {
      userAuthStore.adminData.classes[classIndex]['students'].unshift(data)
    }
    else if (typeSelected.value === 'file') {
      data.forEach((_student: any) => {
        userAuthStore.adminData.classes[classIndex].students.unshift(_student)
      })
    }
    firstName.value = ''
    lastName.value = ''
    dob.value = ''
    pob.value = ''
    studentId.value = ''
    img.value = ''
    contact.value = ''
    address.value = ''
    email.value = ''
    guardianFullname.value = ''
    guardianOccupation.value = ''
    guardianEmail.value = ''
    guardianContact.value = ''
    guardianAddress.value = ''
    elementsStore.HideLoadingOverlay()
    elementsStore.ShowOverlay('Operation successful', 'green', null, null)
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

const editStudent = async () => {
  const formData = new FormData()
  formData.append('studentId', editStudentId.value)
  formData.append('type', 'edit')
  formData.append('studentClassName', className)
  if (editType.value === 'img' && newValue.value?.size > 1024 * 1024) {
    showErrorMessage("The size of the image must not exceed 1MB")
    return;
  }
  if (editType.value === 'user') {
    formData.append('editType', nameTypeSelected.value)
    formData.append('newValue', newValue.value)
  }
  else {
    formData.append('editType', editType.value)
    formData.append('newValue', newValue.value)
  }

  elementsStore.ShowLoadingOverlay()
  try {
    const response = await axiosInstance.post('school-admin/students', formData)
    const data = response.data
    if (userAuthStore.adminData.staff) {
      if (editType.value === 'user') {
        userAuthStore.adminData.classes[classIndex]['students'][editStudentIndex.value]['user'] = data
      }
      else if (editType.value === 'st_id') {
        userAuthStore.adminData.staff[editStudentIndex.value]['staff_id'] = data
      }
      else if (editType.value === 'gender') {
        userAuthStore.adminData.classes[classIndex]['students'][editStudentIndex.value]['gender'] = data
      }
      else if (editType.value === 'dob') {
        userAuthStore.adminData.classes[classIndex]['students'][editStudentIndex.value]['dob'] = data
      }
      else if (editType.value === 'pob') {
        userAuthStore.adminData.classes[classIndex]['students'][editStudentIndex.value]['pob'] = data
      }
      else if (editType.value === 'st_id') {
        userAuthStore.adminData.classes[classIndex]['students'][editStudentIndex.value]['st_id'] = data
      }
      else if (editType.value === 'date_enrolled') {
        userAuthStore.adminData.classes[classIndex]['students'][editStudentIndex.value]['date_enrolled'] = data
      }
      else if (editType.value === 'region') {
        userAuthStore.adminData.classes[classIndex]['students'][editStudentIndex.value]['region'] = data
      }
      else if (editType.value === 'religion') {
        userAuthStore.adminData.classes[classIndex]['students'][editStudentIndex.value]['religion'] = data
      }
      else if (editType.value === 'nationality') {
        userAuthStore.adminData.classes[classIndex]['students'][editStudentIndex.value]['nationality'] = data
      }
      else if (editType.value === 'contact') {
        userAuthStore.adminData.classes[classIndex]['students'][editStudentIndex.value]['contact'] = data
      }
      else if (editType.value === 'address') {
        userAuthStore.adminData.classes[classIndex]['students'][editStudentIndex.value]['address'] = data
      }
      else if (editType.value === 'email') {
        userAuthStore.adminData.classes[classIndex]['students'][editStudentIndex.value]['email'] = data
      }
      else if (editType.value === 'img') {
        userAuthStore.adminData.classes[classIndex]['students'][editStudentIndex.value]['img'] = data
      }
      else if (editType.value === 'guardian') {
        userAuthStore.adminData.classes[classIndex]['students'][editStudentIndex.value]['guardian'] = data
      }
      else if (editType.value === 'guardianGender') {
        userAuthStore.adminData.classes[classIndex]['students'][editStudentIndex.value]['guardian_gender'] = data
      }
      else if (editType.value === 'guardianOccupation') {
        userAuthStore.adminData.classes[classIndex]['students'][editStudentIndex.value]['guardian_occupation'] = data
      }
      else if (editType.value === 'guardianAddress') {
        userAuthStore.adminData.classes[classIndex]['students'][editStudentIndex.value]['guardian_address'] = data
      }
      else if (editType.value === 'guardianEmail') {
        userAuthStore.adminData.classes[classIndex]['students'][editStudentIndex.value]['guardian_email'] = data
      }
      else if (editType.value === 'guardianNationality') {
        userAuthStore.adminData.classes[classIndex]['students'][editStudentIndex.value]['guardian_nationality'] = data
      }
      else if (editType.value === 'guardianContact') {
        userAuthStore.adminData.classes[classIndex]['students'][editStudentIndex.value]['guardian_contact'] = data
      }
    }
    newValue.value = ''
    editType.value = ''
    nameTypeSelected.value = ''
    previousValue.value = ''
    elementsStore.HideLoadingOverlay()
    closeOverlay(`AdminEditStudentOverlay${className}${classIndex}`)
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

const deleteStudent = async (studentToDeleteId: string) => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', 'delete')
  formData.append('studentId', studentToDeleteId)

  try {
    await axiosInstance.post('school-admin/students', formData)
    const studentToDelete = userAuthStore.adminData.classes[classIndex]['students'].find((item: any) => item['st_id'] === studentToDeleteId)
    if (studentToDelete) {
      const studentToDeletIndex = userAuthStore.adminData.classes[classIndex]['students'].indexOf(studentToDelete)
      userAuthStore.adminData.classes[classIndex]['students'].splice(studentToDeletIndex, 1)
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

const studentImage = (event: any) => {
  const file = event.target.files[0]
  img.value = file
}

const editImg = (event: any) => {
  const file = event.target.files[0]
  newValue.value = file
}

const studentsFile = (event: any) => {
  const file = event.target.files[0]
  studentsExcelFile.value = file
}

const fileChanged = (file: any) => {
  if (!file) {
    studentsExcelFile.value = ''
    img.value = ''
    if (editType.value === 'img') {
      newValue.value = ''
    }
  }
}

const requiredFields = computed(() => {
  return !(firstName.value && lastName.value && dob.value && contact.value && address.value && guardianContact.value && guardianAddress.value && guardianNationality.value && guardianOccupation.value && guardianFullname.value && gender.value && nationality.value && guardianGender.value && religion.value && region.value && pob.value && dateEnrolled.value)
})

const isStudentFormValid = computed(() => {
  if (typeSelected.value === 'noFile') {
    if (userAuthStore.userData['current_role']['level']['students_id']) {
      return !(studentId.value && !requiredFields.value)
    }
    else if (!userAuthStore.userData['current_role']['level']['students_id']) {
      return !requiredFields.value
    }
  }
  else if (typeSelected.value === 'file') {
    return !(studentsExcelFile.value)
  }
  return true;
})

const showEditOverlay = (edit_type: string, previous_value: string, st_id: string, student_index: number) => {
  const overlay = document.getElementById(`AdminEditStudentOverlay${className}${classIndex}`)
  previousValue.value = previous_value
  editType.value = edit_type
  editStudentId.value = st_id
  editStudentIndex.value = student_index
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
  <div class="content-wrapper" v-show="elementsStore.activePage === `AdminStudentsClass,${className},${classIndex}`"
    :class="{ 'is-active-page': elementsStore.activePage === `AdminStudentsClass,${className},${classIndex}` }">

    <!-- class subjects overlay -->
    <div :id="`AdminStudentClassSubjectsOverlay${className}${classIndex}`" class="overlay class-subjects">
      <div class="overlay-card">
        <v-btn @click="closeOverlay(`AdminStudentClassSubjectsOverlay${className}${classIndex}`)" color="red"
          size="small" variant="flat" class="close-btn">X</v-btn>
        <div class="overlay-card-info-container">
          <h3 class="mb-5" style="color: green; font-size: .9rem; font-family: monospace">
            SUBJECTS[{{ subjects.length }}]</h3>
          <p class="subject-card" v-for="(_subject, index) in subjects" :key="index">
            {{ _subject }}
          </p>
        </div>
      </div>
    </div>

    <!-- edit student overlay -->
    <div :id="`AdminEditStudentOverlay${className}${classIndex}`" class="overlay" v-if="students">
      <div class="overlay-card edit-overlay">
        <v-btn @click="closeOverlay(`AdminEditStudentOverlay${className}${classIndex}`)" color="red" size="small"
          variant="flat" class="close-btn">
          X
        </v-btn>
        <p class="form-error-message" v-if="formErrorMessage">{{ formErrorMessage }}</p>
        <div class="overlay-card-info-container mb-10">
          <h4 class="previous-value" v-if="editType !== 'img'"><span style="color: black">PREVIOUS VALUE:</span> {{
            previousValue }}</h4>
          <img class="profile-img2" v-if="editType === 'img'" :src="previousValue" alt="student profile image">
        </div>
        <div class="overlay-card-content-container">
          <v-select class="select" v-if="editType === 'user'" :items="nameTypeOptions" label="NAME TYPE"
            v-model="nameTypeSelected" item-title="label" density="comfortable" item-value="value" variant="solo-filled"
            persistent-hint clearable hint="Select whether you want to change the first name or last name" />
          <v-text-field class="input-field" v-if="editType === 'user' && nameTypeSelected === 'firstName'"
            v-model="newValue" label="FIRST NAME" clearable variant="solo-filled" density="comfortable"
            placeholder="Eg. Cassandra" persistent-hint hint="Enter the first name of the student" />
          <v-text-field class="input-field" v-if="editType === 'user' && nameTypeSelected === 'lastName'"
            v-model="newValue" label="LAST NAME (MIDDLE NAME + SURNAME)" clearable variant="solo-filled"
            density="comfortable" placeholder="Eg. Akua Afriyie" persistent-hint
            hint="Enter the last name of the student" />
          <v-select class="select" v-if="editType === 'gender'" :items="genderOptions" label="GENDER" v-model="newValue"
            item-title="label" item-value="value" variant="solo-filled" density="comfortable" clearable />
          <v-text-field
            v-if="editType === 'studentId' && userAuthStore.userData['current_role']['level']['students_id']"
            class="input-field" v-model="newValue" label="STUDENT ID" variant="solo-filled" density="comfortable"
            clearable persistent-hint hint="Enter the student ID of the student" />
          <v-text-field class="input-field" v-if="editType === 'dob'" v-model="newValue" label="DATE OF BIRTH"
            type="date" variant="solo-filled" density="comfortable" clearable persistent-hint
            hint="Select the date of birth of the student" />
          <v-text-field class="input-field" v-if="editType === 'dateEnrolled'" v-model="newValue" label="DATE ENROLLED"
            type="date" variant="solo-filled" density="comfortable" clearable persistent-hint
            hint="Select date the student was employed" />
          <v-select class="select" v-if="editType === 'religion'" :items="religionOptions" label="RELIGION"
            v-model="newValue" item-title="label" item-value="value" variant="solo-filled" density="comfortable"
            persistent-hint hint="Select religion the student belongs to" clearable />
          <v-select class="select" v-if="editType === 'nationality'"
            :items="countriesData.sort((a: any, b: any) => a.nationality.localeCompare(b.nationality))"
            label="NATIONALITY" v-model="newValue" item-title="nationality" item-value="nationality"
            variant="solo-filled" density="comfortable" persistent-hint hint="Select the nationality of the student"
            clearable />
          <v-text-field class="input-field" v-if="editType === 'region'" v-model="newValue" label="REGION/STATE"
            variant="solo-filled" density="comfortable" placeholder="Eg. Asanti" clearable persistent-hint
            hint="Enter the region/state the student is from" />
          <v-text-field class="input-field" v-if="editType === 'pob'" v-model="newValue"
            label="PLACE OF BIRTH(HOME CITY/TOWN)" variant="solo-filled" density="comfortable"
            placeholder="Eg. Ayeduase" clearable persistent-hint hint="Enter the city/town the student was born" />
          <v-text-field class="input-field" v-if="editType === 'contact'" v-model="newValue" label="PHONE NUMBER"
            variant="solo-filled" density="comfortable" placeholder="Eg. +233596021383" clearable />
          <v-text-field class="input-field" v-if="editType === 'address'" v-model="newValue" label="RESIDENTIAL ADDRESS"
            type="address" variant="solo-filled" density="comfortable" placeholder="Eg. Ak-509-1066, Kotei, Kumasi"
            clearable />
          <v-text-field class="input-field" v-if="editType === 'email'" v-model="newValue" label="EMAIL(OPTIONAL)"
            type="email" variant="solo-filled" density="comfortable" placeholder="Eg. nyamejustice2000@gmail.com"
            clearable />
          <v-file-input @change="editImg" @update:model-value="fileChanged" v-if="editType === 'img'" clearable
            show-size class="select" label="STUDENT IMAGE" density="comfortable" variant="solo-filled" chips
            accept="image/*" prepend-icon="mdi-image" persistent-hint hint="Upload a picture of the student">
          </v-file-input>
          <v-text-field class="input-field" v-if="editType === 'guardian'" v-model="newValue" label="GUARDIAN FULLNAME"
            type="text" variant="solo-filled" density="comfortable" placeholder="Eg. Justice Nyame" clearable />
          <v-select class="select" v-if="editType === 'guardianGender'" :items="genderOptions" label="GUARDIAN GENDER"
            v-model="newValue" item-title="label" item-value="value" variant="solo-filled" density="comfortable"
            clearable />
          <v-text-field class="input-field" v-if="editType === 'guardianContact'" v-model="newValue"
            label="GUARDIAN PHONE NUMBER" type="text" variant="solo-filled" density="comfortable"
            placeholder="Eg. +233596021383" clearable />
          <v-text-field class="input-field" v-if="editType === 'guardianOccupation'" v-model="newValue"
            label="GUARDIAN OCCUPATION" type="text" variant="solo-filled" density="comfortable"
            placeholder="Eg. Accountant" clearable />
          <v-select class="select" v-if="editType === 'guardianNationality'"
            :items="countriesData.sort((a: any, b: any) => a.nationality.localeCompare(b.nationality))"
            label="GUARDIAN NATIONALITY" v-model="newValue" item-title="nationality" item-value="nationality"
            variant="solo-filled" density="comfortable" persistent-hint
            hint="Select the nationality of the student's guardian" />
          <v-text-field class="input-field" v-if="editType === 'guardianAddress'" v-model="newValue"
            label="GUARDIAN RESIDENTIAL ADDRESS" type="text" variant="solo-filled" density="comfortable"
            placeholder="Eg. Ak-509-1066, Kotei, Kumasi" clearable />
          <v-text-field class="input-field" v-if="editType === 'guardianEmail'" v-model="newValue"
            label="GUARDIAN EMAIL(OPTIONAL)" type="email" variant="solo-filled" density="comfortable"
            placeholder="Eg. nyamejustice2000@gmail.com" clearable />
        </div>
        <div class="overlay-card-action-btn-container">
          <v-btn @click="editStudent()" :disabled="!newValue" :ripple="false" variant="flat" color="black" size="small"
            append-icon="mdi-checkbox-marked-circle">
            SUBMIT
          </v-btn>
        </div>
      </div>
    </div>

    <!-- add student overlay -->
    <div :id="`AdminAddStudentOverlay${className}${classIndex}`" class="overlay">
      <div class="overlay-card">
        <v-btn @click="closeOverlay(`AdminAddStudentOverlay${className}${classIndex}`)" color="red" size="small"
          variant="flat" class="close-btn">X</v-btn>
        <p class="form-error-message" v-if="formErrorMessage">{{ formErrorMessage }}</p>
        <div class="overlay-card-content-container">
          <v-select class="select" :items="uploadTypeOptions" label="UPLOAD TYPE" v-model="typeSelected"
            item-title="label" item-value="value" variant="solo-filled" density="comfortable" persistent-hint clearable
            hint="Select whether you want to use an excel file or input the data here" />
          <v-text-field class="input-field" v-if="typeSelected === 'noFile'" v-model="firstName" label="FIRST NAME"
            clearable variant="solo-filled" density="comfortable" placeholder="Eg. Cassandra" persistent-hint
            hint="Enter the first name of the student" />
          <v-text-field class="input-field" v-if="typeSelected === 'noFile'" v-model="lastName"
            label="LAST NAME (MIDDLE NAME + SURNAME)" clearable variant="solo-filled" density="comfortable"
            placeholder="Eg. Akua Afriyie" persistent-hint hint="Enter the last name of the student" />
          <v-select class="select" v-if="typeSelected === 'noFile'" :items="genderOptions" label="GENDER"
            v-model="gender" item-title="label" item-value="value" variant="solo-filled" density="comfortable"
            clearable />
          <v-text-field
            v-if="typeSelected === 'noFile' && userAuthStore.userData['current_role']['level']['students_id']"
            class="input-field" v-model="studentId" label="STUDENT ID" variant="solo-filled" density="comfortable"
            clearable persistent-hint hint="Enter the student ID of the student" />
          <v-text-field class="input-field" v-if="typeSelected === 'noFile'" v-model="dob" label="DATE OF BIRTH"
            type="date" variant="solo-filled" density="comfortable" clearable />
          <v-text-field class="input-field" v-if="typeSelected === 'noFile'" v-model="dateEnrolled"
            label="DATE ENROLLED" type="date" variant="solo-filled" density="comfortable" clearable />
          <v-select class="select" v-if="typeSelected === 'noFile'" label="NATIONALITY" v-model="nationality"
            :items="countriesData.sort((a: any, b: any) => a.nationality.localeCompare(b.nationality))"
            item-title="nationality" item-value="nationality" variant="solo-filled" density="comfortable"
            persistent-hint hint="Select the student's nationality" clearable />
          <v-text-field class="input-field"
            v-if="typeSelected === 'noFile' && nationality && nationality.toLowerCase() !== 'ghanaian'" v-model="region"
            label="REGION/STATE" variant="solo-filled" density="comfortable" placeholder="Eg. Asanti" clearable
            persistent-hint hint="Enter the region/state the student is from" />
          <v-select class="select" v-if="typeSelected === 'noFile' && nationality?.toLowerCase() === 'ghanaian'"
            label="REGION" v-model="region" :items="ghanaRegions" variant="solo-filled" density="comfortable"
            persistent-hint hint="Select the region the student is from" clearable />
          <v-text-field class="input-field" v-if="typeSelected === 'noFile'" v-model="pob"
            label="PLACE OF BIRTH(HOME CITY/TOWN)" variant="solo-filled" density="comfortable"
            placeholder="Eg. Ayeduase" clearable persistent-hint hint="Enter the city/town the student was born" />
          <v-select class="select" v-if="typeSelected === 'noFile'" :items="religionOptions" label="RELIGION"
            v-model="religion" item-title="label" item-value="value" variant="solo-filled" density="comfortable"
            persistent-hint hint="Select the student's religion" clearable />
          <v-text-field class="input-field" v-if="typeSelected === 'noFile'" v-model="contact" label="PHONE NUMBER"
            variant="solo-filled" density="comfortable" placeholder="Eg. +233596021383" clearable />
          <v-text-field class="input-field" v-if="typeSelected === 'noFile'" v-model="address"
            label="RESIDENTIAL ADDRESS" type="address" variant="solo-filled" density="comfortable"
            placeholder="Eg. Ak-509-1066, Kotei, Kumasi" clearable />
          <v-text-field class="input-field" v-if="typeSelected === 'noFile'" v-model="email" label="EMAIL(OPTIONAL)"
            type="email" variant="solo-filled" density="comfortable" placeholder="Eg. nyamejustice2000@gmail.com"
            clearable />
          <v-file-input @change="studentImage" @update:model-value="fileChanged" v-if="typeSelected === 'noFile'"
            clearable show-size class="select" label="IMAGE" density="comfortable" variant="solo-filled"
            accept="image/*" prepend-icon="mdi-image" persistent-hint hint="Upload a picture of the student">
          </v-file-input>
          <v-text-field class="input-field" v-if="typeSelected === 'noFile'" v-model="guardianFullname"
            label="GUARDIAN FULLNAME" variant="solo-filled" density="comfortable" placeholder="Eg. Justice Nyame"
            clearable />
          <v-select class="select" v-if="typeSelected === 'noFile'" :items="genderOptions" label="GUARDIAN GENDER"
            v-model="guardianGender" item-title="label" item-value="value" variant="solo-filled" density="comfortable"
            clearable />
          <v-select class="select" v-if="typeSelected === 'noFile'" :items="countriesData" label="GUARDIAN NATIONALITY"
            v-model="guardianNationality" item-title="nationality" item-value="nationality" variant="solo-filled"
            density="comfortable" persistent-hint hint="Select the nationality of the guardian" clearable />
          <v-text-field class="input-field" v-if="typeSelected === 'noFile'" v-model="guardianOccupation"
            label="GUARDIAN OCCUPATION" variant="solo-filled" density="comfortable" placeholder="Eg. Accountant"
            clearable />
          <v-text-field class="input-field" v-if="typeSelected === 'noFile'" v-model="guardianContact"
            label="GUARDIAN PHONE NUMBER" variant="solo-filled" density="comfortable" placeholder="Eg. +233596021383"
            clearable />
          <v-text-field class="input-field" v-if="typeSelected === 'noFile'" v-model="guardianAddress"
            label="GUARDIAN ADDRESS" variant="solo-filled" density="comfortable"
            placeholder="Eg. Ak-509-1066, Kotei, Kumasi" clearable />
          <v-text-field class="input-field" v-if="typeSelected === 'noFile'" v-model="guardianEmail"
            label="GUARDIAN EMAIL(OPTIONAL)" variant="solo-filled" density="comfortable"
            placeholder="Eg. nyamejustice2000@gmail.com" clearable type="email" />

          <!-- file -->
          <v-btn class="mb-10" @click="getStudentFile()" v-if="typeSelected === 'file'" :ripple="false" variant="flat"
            color="blue" size="small">GET FILE</v-btn>
          <v-file-input @change="studentsFile" v-if="typeSelected === 'file'" clearable show-size class="select"
            label="UPLOAD FILE" density="comfortable" variant="solo-filled" @update:model-value="fileChanged"
            accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            prepend-icon="mdi-microsoft-excel">
          </v-file-input>
        </div>
        <div class="overlay-card-action-btn-container">
          <v-btn @click="addStudent()" :disabled="isStudentFormValid" :ripple="false" variant="flat" type="submit"
            color="black" size="small" append-icon="mdi-checkbox-marked-circle">
            SUBMIT
          </v-btn>
        </div>
      </div>
    </div>

    <!-- assign class head teacher overlay -->
    <div :id="`AdminAssignClassHeadTeacherOverlay${className}${classIndex}`" class="overlay" v-if="userAuthStore.adminData.staff">
      <div class="overlay-card">
        <v-btn @click="closeOverlay(`AdminAssignClassHeadTeacherOverlay${className}${classIndex}`)" color="red"
          size="small" variant="flat" class="close-btn">X</v-btn>
        <div class="overlay-card-content-container">
          <v-select class="select"
            :items="userAuthStore.adminData.staff.filter(item => item.roles.map(subItem=> subItem.toLowerCase()).includes(`teacher | ${userAuthStore.userData['current_role']['level']['identifier'].toLowerCase()}`)).map(item=> ({'title': item.user, 'value': item.staff_id}))"
            label="HEAD TEACHER" v-model="selectedHeadTeacher" item-title="title" item-value="value"
            variant="solo-filled" density="comfortable" persistent-hint clearable
            hint="Select the teacher you want to assign to this class as the head teacher">
            <template v-slot:item="{ props, item }">
              <v-list-item v-bind="props" :subtitle="(item as any).raw.value"></v-list-item>
            </template>
          </v-select>
        </div>
        <div class="overlay-card-action-btn-container">
          <v-btn @click="assignClassHeadTeacher()" :disabled="!selectedHeadTeacher" :ripple="false" variant="flat"
            type="submit" color="black" size="small" append-icon="mdi-checkbox-marked-circle">
            SUBMIT
          </v-btn>
        </div>
      </div>
    </div>

    <div class="content-header">
      <h4 class="content-header-title">{{ className }}</h4>
    </div>
    <div class="content-header info">
      <div class="content-header-text">
        TOTAL NUMBER OF STUDENTS:
        <span class="content-header-text-value">
          {{ students.length }}
        </span>
      </div>
      <div class="content-header-text">
        MALE STUDENTS:
        <span class="content-header-text-value">
          {{ maleStudents }} <span v-if="students.length > 0">[{{ ((maleStudents / students.length) * 100).toFixed(1)
            }}%]</span>
        </span>
      </div>
      <div class="content-header-text">
        FEMALE STUDENTS:
        <span class="content-header-text-value">
          {{ femaleStudents }} <span v-if="students.length > 0">[{{ ((femaleStudents / students.length) *
            100).toFixed(1)
            }}%]</span>
        </span>
      </div>
      <h4 class="content-header-text">
        STUDENTS YEAR:
        <span class="content-header-text-value">{{ students_year }}</span>
      </h4>
      <h4 class="content-header-text">
        PROGRAM:
        <span class="content-header-text-value" v-if="program">{{ program }}</span>
      </h4>
    </div>
    <div class="content-header btn-container">
      <h4 class="content-header-text flex-all pointer"
        v-if="userAuthStore.adminData.classes[classIndex]['head_teacher']">
        HEAD TEACHER:
        <span class="content-header-text-value ml-1"
          @click="showOverlay(`AdminAssignClassHeadTeacherOverlay${className}${classIndex}`)">
          {{ userAuthStore.adminData.classes[classIndex]?.head_teacher?.user }}
        </span>
        <img class="profile-img ml-1"
          @click="showOverlay(`AdminAssignClassHeadTeacherOverlay${className}${classIndex}`)"
          :src="userAuthStore.adminData.classes[classIndex]?.head_teacher?.img">
        <v-icon v-if="userAuthStore.adminData.classes[classIndex]?.head_teacher"
          @click="elementsStore.ShowDeletionOverlay(removeClassHeadTeacher, 'Are you sure you want to remove the class head teacher')"
          icon="mdi-delete" color="red" />
      </h4>
      <v-btn v-if="!userAuthStore.adminData.classes[classIndex]['head_teacher']"
        @click="showOverlay(`AdminAssignClassHeadTeacherOverlay${className}${classIndex}`)" color="blue"
        :size="elementsStore.btnSize1">
        ASSIGN HEAD TEACHER
      </v-btn>
      <v-btn @click="showOverlay(`AdminStudentClassSubjectsOverlay${className}${classIndex}`)" class="ml-5" color="blue"
        :size="elementsStore.btnSize1">
        SUBJECT(S)
      </v-btn>
      <v-btn @click="showOverlay(`AdminAddStudentOverlay${className}${classIndex}`)" class="ml-5" color="blue"
        :size="elementsStore.btnSize1">
        ADD STUDENT(S)
      </v-btn>
    </div>
    <div class="no-data" v-if="students.length === 0">
      <p>There are no student in this class</p>
    </div>
    <v-table fixed-header class="table" v-if="students.length > 0">
      <thead>
        <tr>
          <th class="table-head">NAME</th>
          <th class="table-head" v-if="userAuthStore.userData['current_role']['level']['index_no']">INDEX NO</th>
          <th class="table-head">GENDER</th>
          <th class="table-head">DATE OF BIRTH</th>
          <th class="table-head">DATE ENROLLED</th>
          <th class="table-head">RELIGION</th>
          <th class="table-head">CONTACT</th>
          <th class="table-head">PLACE OF BIRTH</th>
          <th class="table-head">REGION/STATE</th>
          <th class="table-head">NATIONALITY</th>
          <th class="table-head">RESIDENTIAL ADDRESS</th>
          <th class="table-head">IMAGE</th>
          <th class="table-head">GUARDIAN</th>
          <th class="table-head">GUARDIAN GENDER</th>
          <th class="table-head">GUARDIAN OCCUPATION</th>
          <th class="table-head">GUARDIAN CONTACT</th>
          <th class="table-head">GUARDIAN NATIONALITY</th>
          <th class="table-head">GUARDIAN RESIDENTIAL ADDRESS</th>
          <th class="table-head">GUARDIAN EMAIL</th>
          <th class="table-head">ACTION</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(st, index) in students" :key="index">
          <td class="table-data">
            {{ st['user'] }}<v-icon @click="showEditOverlay('user', st['user'], st['st_id'], index)"
              icon="mdi-pencil" />
            <v-list-item-subtitle>
              {{ st['st_id'] }}<v-icon v-if="userAuthStore.userData['current_role']['level']['students_id']"
                @click="showEditOverlay('studentId', st['st_id'], st['st_id'], index)" icon="mdi-pencil" />
            </v-list-item-subtitle>
          </td>
          <td class="table-data" v-if="userAuthStore.userData['school']['index_no']">{{ st['index_no'] }}</td>
          <td class="table-data">
            {{ st['gender'] }}<v-icon @click="showEditOverlay('gender', st['gender'], st['st_id'], index)"
              icon="mdi-pencil" />
          </td>
          <td class="table-data">
            {{ st['dob'] }}<v-icon @click="showEditOverlay('dob', st['dob'], st['st_id'], index)" icon="mdi-pencil" />
          </td>
          <td class="table-data">
            {{ st['date_enrolled'] }}<v-icon
              @click="showEditOverlay('dateEnrolled', st['date_enrolled'], st['st_id'], index)" icon="mdi-pencil" />
          </td>
          <td class="table-data">
            {{ st['religion'] }}<v-icon @click="showEditOverlay('religion', st['religion'], st['st_id'], index)"
              icon="mdi-pencil" />
          </td>
          <td class="table-data">
            {{ st['contact'] }}<v-icon @click="showEditOverlay('contact', st['contact'], st['st_id'], index)"
              icon="mdi-pencil" />
          </td>
          <td class="table-data">
            {{ st['pob'] }}<v-icon @click="showEditOverlay('pob', st['pob'], st['st_id'], index)" icon="mdi-pencil" />
          </td>
          <td class="table-data">
            {{ st['region'] }}<v-icon @click="showEditOverlay('region', st['region'], st['st_id'], index)"
              icon="mdi-pencil" />
          </td>
          <td class="table-data">
            {{ st['nationality'] }}<v-icon
              @click="showEditOverlay('nationality', st['nationality'], st['st_id'], index)" icon="mdi-pencil" />
          </td>
          <td class="table-data">
            {{ st['address'] }}<v-icon @click="showEditOverlay('address', st['address'], st['st_id'], index)"
              icon="mdi-pencil" />
          </td>
          <td class="table-data">
            <img class="profile-img" :src="st['img']"><v-icon
              @click="showEditOverlay('img', st['img'], st['st_id'], index)" icon="mdi-pencil" />
          </td>
          <td class="table-data">
            {{ st['guardian'] }}<v-icon @click="showEditOverlay('guardian', st['guardian'], st['st_id'], index)"
              icon="mdi-pencil" />
          </td>
          <td class="table-data">
            {{ st['guardian_gender'] }}<v-icon
              @click="showEditOverlay('guardianGender', st['guardian_gender'], st['st_id'], index)" icon="mdi-pencil" />
          </td>
          <td class="table-data">
            {{ st['guardian_occupation'] }}<v-icon
              @click="showEditOverlay('guardianOccupation', st['guardian_occupation'], st['st_id'], index)"
              icon="mdi-pencil" />
          </td>
          <td class="table-data">
            {{ st['guardian_contact'] }}<v-icon
              @click="showEditOverlay('guardianContact', st['guardian_contact'], st['st_id'], index)"
              icon="mdi-pencil" />
          </td>
          <td class="table-data">
            {{ st['guardian_nationality'] }}<v-icon
              @click="showEditOverlay('guardianNationality', st['guardian_nationality'], st['st_id'], index)"
              icon="mdi-pencil" />
          </td>
          <td class="table-data">
            {{ st['guardian_address'] }}<v-icon
              @click="showEditOverlay('guardianAddress', st['guardian_address'], st['st_id'], index)"
              icon="mdi-pencil" />
          </td>
          <td class="table-data">
            {{ st['guardian_email'] }}<v-icon
              @click="showEditOverlay('guardianEmail', st['guardian_email'], st['st_id'], index)" icon="mdi-pencil" />
          </td>
          <td class="table-data">
            <v-btn color="red" size="x-small" variant="flat" icon="mdi-delete"
              @click="elementsStore.ShowDeletionOverlay(() => deleteStudent(st['st_id']), 'Are you sure you want to delete this student?')">
            </v-btn>
          </td>
        </tr>
      </tbody>
    </v-table>
  </div>
</template>

<style scoped>
.content-header {
  min-height: 10% !important;
}

.btn-container {
  min-height: 20% !important;
}

.info {
  min-height: 25% !important;
}

.table {
  min-height: 40% !important;
}

.overlay-card {
  height: max-content !important;
  max-width: 600px !important;
}

.class-subjects .overlay-card {
  max-width: 500px !important;
}

.class-subjects .overlay-card-info-container {
  margin-top: 4em;
  height: 100% !important;
}

.overlay-card-content-container {
  margin-top: 3em !important;
}

.edit-overlay .overlay-card-content-container {
  margin-top: 0 !important;
}

.edit-overlay .overlay-card-info-container {
  margin-top: 3em !important;
}

.previous-value {
  font-size: .7rem !important;
  font-family: Verdana, Geneva, Tahoma, sans-serif;
  color: green;
}

@media screen and (min-width: 500px) {
  .info {
    min-height: 20% !important;
  }
}

@media screen and (min-width: 767px) {
  .info {
    min-height: 15% !important;
  }
}

@media screen and (min-width: 1200px) {
  .btn-container {
    min-height: 15% !important;
  }

  .title {
    min-height: 10% !important;
  }
}
</style>
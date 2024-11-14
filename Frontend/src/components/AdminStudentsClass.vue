<script setup lang="ts">
import { AxiosError } from 'axios';
import { ref, computed } from 'vue';
import axiosInstance from '@/utils/axiosInstance';
import { useUserAuthStore } from '@/stores/userAuthStore';
import { useElementsStore } from '@/stores/elementsStore';

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()
const femaleStudents = ref(0)
const maleStudents = ref(0)
const toClass:any = ref(null)
const formErrorMessage = ref('')
const firstName = ref('')
const lastName = ref('')
const dateOfBirth = ref('')
const contact = ref('')
const address = ref('')
const studentId = ref('')
const guardian_contact = ref('')
const guardian_address = ref('')
const guardian_email = ref('')
const guardian_nationality = ref('')
const guardian_occupation = ref('')
const img = ref('')
const gender = ref('')
const nationality = ref('')
const typeSelected = ref('')
const guardian_fullname = ref('')
const guardian_gender = ref('')
const studentsExcelFile = ref('')
const dateEnrolled = ref('')
const nationalitySelected = ref('')
const guardianNationalitySelected = ref('')
const email = ref('')
const religion = ref('')
const region = ref('')
const pob = ref('')


interface Props {
  className: string;
  classIndex: number;
  students: any[];
  subjects: string[];
  students_year: number;
  program: string | null;
}

const props = defineProps<Props>()
const className = props.className
const classIndex = props.classIndex || 0
const students = props.students
const subjects = props.subjects
const students_year = props.students_year
const program = props.program || null
const selectedHeadTeacher = ref('')

const showOverlay = (element: string) => {
  const overlay = document.getElementById(element)
  if (overlay) {
    overlay.style.display = 'flex'
  }
}

const genderOptions = [
  {'label': 'MALE', 'value': 'male'},
  {'label': 'FEMALE', 'value': 'female'},
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

const typeOptions = [
  {'label': 'USE AN EXCEL FILE', 'value': 'file'},
  {'label': 'INPUT DATA HERE', 'value': 'noFile'},
]

const nationalityOptions = [
  {'label': 'GHANAIAN', 'value': 'Ghanaian'},
  {'label': 'OTHER', 'value': 'other'},
]

students.forEach((item: any) => {
  if (item['gender'].toLowerCase() === 'male') {
    maleStudents.value += 1
  }
  else if (item['gender'].toLowerCase() === 'female') {
    femaleStudents.value += 1
  }
})

const linkClass = async () => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', 'create')
  formData.append('fromClass', className);
  formData.append('toClass', toClass.value);

  try {
    const response = await axiosInstance.post('school-admin/linked-class', formData)
    userAuthStore.adminData.linkedClasses.unshift(response.data)
    toClass.value = ''
    closeOverlay(`AdminAddLinkedClassOverlay${className}${classIndex}`)
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

const assignClassHeadTeacher = async () => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', 'assignClassHeadTeacher')
  formData.append('studentsClass', className);
  formData.append('teacherId', selectedHeadTeacher.value);

  try {
    const response = await axiosInstance.post('school-admin/data', formData)
    if (userAuthStore.adminData.classes){}
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

const addStudent = async () => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('className', className);
  if (typeSelected.value === 'file'){
    formData.append('type', 'createWithFile')
    formData.append('file', studentsExcelFile.value);
  }
  else if (typeSelected.value === 'noFile'){
    formData.append('type', 'createWithoutFile')
    formData.append('firstName', firstName.value);
    formData.append('lastName', lastName.value);
    formData.append('gender', gender.value);
    formData.append('dob', dateOfBirth.value);
    formData.append('studentId', studentId.value);
    formData.append('img', img.value);
    formData.append('nationality', nationality.value);
    formData.append('contact', contact.value);
    formData.append('religion', religion.value);
    formData.append('dateEnrolled', dateEnrolled.value);
    formData.append('region', region.value);
    formData.append('pob', pob.value);
    formData.append('email', email.value)
    formData.append('address', address.value);
    formData.append('guardianFullname', guardian_fullname.value);
    formData.append('guardianGender', guardian_gender.value);
    formData.append('guardianOccupation', guardian_occupation.value);
    formData.append('guardianAddress', guardian_address.value);
    formData.append('guardianEmail', guardian_email.value);  
    formData.append('guardianNationality', guardian_nationality.value);
    formData.append('guardianContact', guardian_contact.value);
  }
  else{
    return;
  }
  
  try {
    const response = await axiosInstance.post('school-admin/students', formData)
    const data = response.data
    userAuthStore.adminData.classes[classIndex]['head_teacher'] = response.data
    if (typeSelected.value === 'noFile'){
      userAuthStore.adminData.classes[classIndex]['students'].unshift(response.data)
    }
    else if (typeSelected.value === 'file'){
      data.forEach((_student:any)=>{
        userAuthStore.adminData.classes[classIndex]['students'].unshift(_student)
      })
    }
    elementsStore.HideLoadingOverlay()
    elementsStore.ShowOverlay('Student added successfully', 'green', null, null)
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

const studentImage = (event:any)=>{
  const file = event.target.files[0]
  img.value = file
}

const nationalityChanged = (value:string)=>{
  if (value === 'Ghanaian'){
    nationality.value = value
  }
  else{
    nationality.value = ''
  }
  region.value = ''
}

const guardianNationalityChanged = (value:string)=>{
  if (value === 'Ghanaian'){
    guardian_nationality.value = value
  }
  else{
    guardian_nationality.value = ''
  } 
}

const studentsFile = (event:any)=>{
  const file = event.target.files[0]
  studentsExcelFile.value = file
}

const isStudentFormValid = computed(()=>{
  if (typeSelected.value === 'noFile'){
    if (userAuthStore.userData['school']['students_id']){
      return !(firstName.value && lastName.value && dateOfBirth.value && contact.value && address.value && studentId.value && guardian_contact.value && guardian_address.value && guardian_nationality.value && guardian_occupation.value && guardian_fullname.value && gender.value && nationality.value && guardian_gender.value && religion.value && region.value && pob.value && dateEnrolled.value) 
    }
    else if (!userAuthStore.userData['school']['students_id']){
      return !(firstName.value && lastName.value && dateOfBirth.value && contact.value && address.value && guardian_contact.value && guardian_address.value && guardian_nationality.value && guardian_occupation.value && guardian_fullname.value && gender.value && nationality.value && guardian_gender.value && religion.value && region.value && pob.value && dateEnrolled.value) 
    }
  }
  else if (typeSelected.value === 'file'){
    return  !(studentsFile)
  }
  return true;
})

const closeOverlay = (element: string) => {
  const overlay = document.getElementById(element)
  if (overlay) {
    overlay.style.display = 'none'
  }
}


</script>

<template>
  <div class="content-wrapper" v-show="elementsStore.activePage === `AdminStudentsClass,${className},${classIndex}`"
    :class="{ 'is-active-page': elementsStore.activePage === `AdminStudentsClass,${className},${classIndex}` }"
    >

    <!-- class subjects overlay -->
    <div :id="`AdminStudentClassSubjectsOverlay${className}${classIndex}`" class="overlay class-subjects">
      <div class="overlay-card">
        <v-btn @click="closeOverlay(`AdminStudentClassSubjectsOverlay${className}${classIndex}`)" color="red" size="small"
          variant="flat" class="close-btn">X</v-btn>
        <div class="overlay-card-info-container">
          <h3 class="mb-5" style="color: green; font-size: .9rem; font-family: monospace">
            SUBJECTS[{{ subjects.length }}]</h3>
          <p class="subject-card" v-for="(_subject, index) in subjects" :key="index">
            {{ _subject }}
          </p>
        </div>
      </div>
    </div>
    
    <!-- add student overlay -->
    <div :id="`AdminAddStudentOverlay${className}${classIndex}`" class="overlay">
      <div class="overlay-card">
        <v-btn @click="closeOverlay(`AdminAddStudentOverlay${className}${classIndex}`)" color="red" size="small" variant="flat" class="close-btn">X</v-btn>
        <p class="form-message" v-if="formErrorMessage">{{ formErrorMessage }}</p>
        <form class="overlay-card-content-container">
          <v-select class="select" :items="typeOptions" label="UPLOAD TYPE" v-model="typeSelected" 
          item-title="label" item-value="value" variant="solo-filled" density="comfortable" persistent-hint hint="Select whether you want to use an excel file or input the data here" 
          />
          <v-text-field class="input-field" v-if="typeSelected === 'noFile'" v-model="firstName" label="FIRST NAME" clearable
            variant="solo-filled" density="comfortable" placeholder="Eg. Cassandra" persistent-hint hint="Enter the first name of the staff" 
          />
          <v-text-field class="input-field" v-if="typeSelected === 'noFile'" v-model="lastName" label="LAST NAME (MIDDLE NAME + SURNAME)" clearable
            variant="solo-filled" density="comfortable" placeholder="Eg. Akua Afriyie" persistent-hint hint="Enter the last name of the staff" 
          />
          <v-select class="select" v-if="typeSelected === 'noFile'" :items="genderOptions" label="GENDER" v-model="gender" 
          item-title="label" item-value="value" variant="solo-filled" density="comfortable" clearable
          />
          <v-text-field v-if="typeSelected === 'noFile' && userAuthStore.userData['school']['students_id']" class="input-field" v-model="studentId" label="STUDENT ID"
            variant="solo-filled" density="comfortable" clearable persistent-hint hint="Enter the student ID of the student" 
          />
          <v-text-field class="input-field" v-if="typeSelected === 'noFile'" v-model="dateOfBirth" label="DATE OF BIRTH" type="date"
            variant="solo-filled" density="comfortable" clearable
          />
          <v-text-field class="input-field" v-if="typeSelected === 'noFile'" v-model="dateEnrolled" label="DATE ENROLLED" type="date"
            variant="solo-filled" density="comfortable" clearable
          />
          <v-select class="select" v-if="typeSelected === 'noFile'" @update:model-value="nationalityChanged" :items="nationalityOptions" label="NATIONALITY" v-model="nationalitySelected" 
          item-title="label" item-value="value" variant="solo-filled" density="comfortable" persistent-hint hint="Select the student's nationality" 
          />
          <v-text-field class="input-field" v-if="typeSelected === 'noFile' && nationalitySelected === 'other' " v-model="nationality" label="SPECIFY THE NATIONALITY"
            variant="solo-filled" density="comfortable" placeholder="Eg. Nigerian" clearable persistent-hint hint="Enter the nationality of the student" 
          />
          <v-select class="select" v-if="typeSelected === 'noFile' && nationalitySelected === 'Ghanaian'" :items="regionOptions" label="REGION" v-model="region" 
          item-title="label" item-value="value" variant="solo-filled" density="comfortable" persistent-hint hint="Select the region the student is from" 
          />
          <v-text-field class="input-field" v-if="typeSelected === 'noFile' && nationalitySelected === 'other'" v-model="region" label="REGION/STATE"
            variant="solo-filled" density="comfortable" placeholder="Eg. Asanti" clearable persistent-hint hint="Enter the region/state the student is from" 
          />
          <v-text-field class="input-field" v-if="typeSelected === 'noFile'" v-model="pob" label="PLACE OF BIRTH(HOME CITY/TOWN)"
            variant="solo-filled" density="comfortable" placeholder="Eg. Ayeduase" clearable persistent-hint hint="Enter the city/town the student was born" 
          />
          <v-select class="select" v-if="typeSelected === 'noFile'" :items="religionOptions" label="RELIGION" v-model="religion" 
          item-title="label" item-value="value" variant="solo-filled" density="comfortable" persistent-hint hint="Select the student's religion" 
          />
          <v-text-field class="input-field" v-if="typeSelected === 'noFile'" v-model="contact" label="PHONE NUMBER"
            variant="solo-filled" density="comfortable" placeholder="Eg. 0596021383" clearable
          />
          <v-text-field class="input-field" v-if="typeSelected === 'noFile'" v-model="address" label="RESIDENTIAL ADDRESS" type="address"
            variant="solo-filled" density="comfortable" placeholder="Eg. Ak-509-1066, Kotei, Kumasi" clearable
          />
          <v-text-field class="input-field" v-if="typeSelected === 'noFile'" v-model="address" label="EMAIL(OPTIONAL)" type="email"
            variant="solo-filled" density="comfortable" placeholder="Eg. nyamejustice2000@gmail.com" clearable
          />
          <v-file-input @change="studentImage" v-if="typeSelected === 'noFile'" clearable show-size class="select" label="STUDENT PICTURE" density="comfortable"
            variant="solo-filled" accept="image/*" prepend-icon="mdi-image" persistent-hint hint="Upload a picture of the student" >
          </v-file-input>
          <v-text-field class="input-field" v-if="typeSelected === 'noFile'" v-model="guardian_fullname" label="GUARDIAN FULLNAME"
            variant="solo-filled" density="comfortable" placeholder="Eg. Justice Nyame" clearable
          />
          <v-select class="select" v-if="typeSelected === 'noFile'" :items="genderOptions" label="GUARDIAN GENDER" v-model="guardian_gender" 
          item-title="label" item-value="value" variant="solo-filled" density="comfortable" clearable
          />
          <v-select class="select" v-if="typeSelected === 'noFile'" @update:model-value="guardianNationalityChanged" :items="nationalityOptions" label="GUARDIAN NATIONALITY" v-model="guardianNationalitySelected" 
          item-title="label" item-value="value" variant="solo-filled" density="comfortable" persistent-hint hint="Select the nationality of the guardian" 
          />
          <v-text-field class="input-field" v-if="typeSelected === 'noFile' && guardianNationalitySelected === 'other'" v-model="guardian_nationality" label="SPECIFY GUARDIAN NATIONALITY"
            variant="solo-filled" density="comfortable" placeholder="Eg. Nigerian" clearable
          />
          <v-text-field class="input-field" v-if="typeSelected === 'noFile'" v-model="guardian_occupation" label="GUARDIAN OCCUPATION"
            variant="solo-filled" density="comfortable" placeholder="Eg. Accountant" clearable
          />
          <v-text-field class="input-field" v-if="typeSelected === 'noFile'" v-model="guardian_contact" label="GUARDIAN PHONE NUMBER"
            variant="solo-filled" density="comfortable" placeholder="Eg. 0596021383" clearable
          />
          <v-text-field class="input-field" v-if="typeSelected === 'noFile'" v-model="guardian_address" label="GUARDIAN ADDRESS"
            variant="solo-filled" density="comfortable" placeholder="Eg. Ak-509-1066, Kotei, Kumasi" clearable
          />
          <v-text-field class="input-field" v-if="typeSelected === 'noFile'" v-model="guardian_email" label="GUARDIAN EMAIL(OPTIONAL)"
            variant="solo-filled" density="comfortable" placeholder="Eg. nyamejustice2000@gmail.com" clearable type="email"
          />
          
          <!-- file -->
          <v-btn class="mb-10" @click="getStudentsFile()" v-if="typeSelected === 'file'" :ripple="false" variant="flat" color="blue" size="small">GET FILE</v-btn>
          <v-file-input @change="studentsFile" v-if="typeSelected === 'file'" clearable show-size class="select" label="UPLOAD FILE" density="comfortable"
            variant="solo-filled" accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" prepend-icon="mdi-microsoft-excel">
          </v-file-input>
        </form>
        <div class="overlay-card-action-btn-container">
          <v-btn @click="addStudent()" :disabled="isStudentFormValid" :ripple="false" variant="flat"
            type="submit" color="black" size="small" append-icon="mdi-checkbox-marked-circle">
            SUBMIT
          </v-btn>
        </div>
      </div>
    </div>

     <!-- assign class head teacher overlay -->
    <div :id="`AdminAssignClassHeadTeacherOverlay${className}${classIndex}`" class="overlay">
      <div class="overlay-card">
        <v-btn @click="closeOverlay(`AdminAssignClassHeadTeacherOverlay${className}${classIndex}`)" color="red" size="small" variant="flat" class="close-btn">X</v-btn>
        <div class="overlay-card-content-container">
          <v-select class="select" :items="userAuthStore.adminData.staff.filter((_staff: any)=> _staff['role'].toLowerCase() === 'teacher' || _staff['role'].toLowerCase() === 'hod').map((_staff: any) => ({'name': _staff['user'], 'staff_id': _staff['staff_id']}))" label="HEAD TEACHER" v-model="selectedHeadTeacher" 
          item-title="name" item-value="staff_id" variant="solo-filled" density="comfortable" persistent-hint hint="Select the teacher you want to assign to this class as the head teacher">
          <template v-slot:item="{ props, item }">
            <v-list-item v-bind="props" :subtitle="(item as any).raw.staff_id"></v-list-item>
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

    <!-- link class overlay -->
    <div :id="`AdminAddLinkedClassOverlay${className}${classIndex}`" class="overlay" v-if="students_year !== Number(userAuthStore.userData['school']['level']['years_to_complete'])">
      <div class="overlay-card">
        <v-btn @click="closeOverlay(`AdminAddLinkedClassOverlay${className}${classIndex}`)" color="red" size="small" variant="flat" class="close-btn">X</v-btn>
        <div class="overlay-card-content-container" style="min-height: 100px" v-if="userAuthStore.adminData.linkedClasses?.find((_class:any)=> _class['from_class'] === className)">
          <h4>LINKED TO:<span class="subject-card">{{ userAuthStore.adminData.linkedClasses?.find((_class:any)=> _class['from_class'] === className)['to_class'] }}</span></h4>
        </div>
        <div class="overlay-card-content-container" v-if="!userAuthStore.adminData.linkedClasses?.find((_class:any)=> _class['from_class'] === className)">
          <v-select class="select" :items="userAuthStore.adminData.classes.filter((_class: any)=> _class['name'] !== className && _class['program'] === program && _class['students_year'] === students_year+1).map((_class: any) => _class['name'])" label="LINK TO CLASS" v-model="toClass" 
          variant="solo-filled" density="comfortable" persistent-hint hint="Select the class students from this class will be promoted to" 
          />
        </div>
        <div class="overlay-card-action-btn-container" v-if="!userAuthStore.adminData.linkedClasses?.find((_class:any)=> _class['from_class'] === className)">
          <v-btn @click="linkClass()" :disabled="!toClass" :ripple="false" variant="flat"
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
          {{ maleStudents }} [{{ ((maleStudents / students.length) * 100).toFixed(1) }}%]
        </span>
      </div>
      <div class="content-header-text">
        FEMALE STUDENTS:
        <span class="content-header-text-value">
          {{ femaleStudents }} [{{ ((femaleStudents / students.length) * 100).toFixed(1) }}%]
        </span>
      </div>
      <h4 class="content-header-text">
        STUDENTS YEAR:
        <span class="content-header-text-value">{{students_year}}</span>
      </h4>
      <h4 class="content-header-text">
        PROGRAM:
        <span class="content-header-text-value" v-if="program">{{program}}</span>
      </h4>
    </div>
    <div class="content-header btn-container">
      <h4 class="content-header-text flex-all pointer" v-if="userAuthStore.adminData.classes[classIndex]['head_teacher']" @click="showOverlay(`AdminAssignClassHeadTeacherOverlay${className}${classIndex}`)">
          HEAD TEACHER:
          <span class="content-header-text-value ml-1">
            {{ userAuthStore.adminData.classes[classIndex]?.head_teacher?.user }}
          </span>
          <img class="profile-img ml-1" :src="userAuthStore.adminData.classes[classIndex]?.head_teacher?.img">
      </h4>
      <v-btn v-if="!userAuthStore.adminData.classes[classIndex]['head_teacher']" @click="showOverlay(`AdminAssignClassHeadTeacherOverlay${className}${classIndex}`)" color="blue"
        :size="elementsStore.btnSize1">
        ASSIGN HEAD TEACHER
      </v-btn>
      <v-btn @click="showOverlay(`AdminStudentClassSubjectsOverlay${className}${classIndex}`)" class="ml-5" color="blue"
        :size="elementsStore.btnSize1">
        SUBJECT(S)
      </v-btn>
      <v-btn @click="showOverlay(`AdminStudentClassSubjectsOverlay${className}${classIndex}`)" class="ml-5" color="blue"
        :size="elementsStore.btnSize1">
        ASSIGN SUBJECT
      </v-btn>
      <v-btn @click="showOverlay(`AdminAddStudentOverlay${className}${classIndex}`)" class="ml-5" color="blue"
        :size="elementsStore.btnSize1">
        ADD STUDENT(S)
      </v-btn>
      <v-btn @click="showOverlay(`AdminAddLinkedClassOverlay${className}${classIndex}`)" class="ml-5" color="blue"
        :size="elementsStore.btnSize1" v-if="students_year !== Number(userAuthStore.userData['school']['level']['years_to_complete'])">
        LINK CLASS
      </v-btn>
    </div>
    <v-table fixed-header class="table">
      <thead>
        <tr>
          <th class="table-head">NAME</th>
          <th class="table-head" v-if="userAuthStore.userData['school']['index_no']">INDEX NO</th>
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
          <th class="table-head">GUARDIAN ADDRESS</th>
          <th class="table-head">GUARDIAN EMAIL</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(st, index) in students" :key="index">
          <td class="table-data">
            {{ st['user'] }}
            <v-list-item-subtitle>{{ st['st_id'] }}</v-list-item-subtitle>
          </td>
          <td class="table-data" v-if="userAuthStore.userData['school']['index_no']">{{ st['index_no'] }}</td>
          <td class="table-data">{{ st['gender'].toUpperCase() }}</td>
          <td class="table-data">{{ st['dob'] }}</td>
          <td class="table-data">{{ st['date_enrolled'] }}</td>
          <td class="table-data">{{ st['religion'] }}</td>
          <td class="table-data">{{ st['contact'] }}</td>
          <td class="table-data">{{ st['pob'] }}</td>
          <td class="table-data">{{ st['region'] }}</td>
          <td class="table-data">{{ st['nationality'] }}</td>
          <td class="table-data">{{ st['address'] }}</td>
          <td class="table-data"><img class="profile-img" :src="st['img']"></td>
          <td class="table-data">{{ st['guardian'] }}</td>
          <td class="table-data">{{ st['guardian_gender'].toUpperCase() }}</td>
          <td class="table-data">{{ st['guardian_occupation'] }}</td>
          <td class="table-data">{{ st['guardian_contact'] }}</td>
          <td class="table-data">{{ st['guardian_nationality'] }}</td>
          <td class="table-data">{{ st['guardian_address'] }}</td>
          <td class="table-data">{{ st['guardian_email'] }}</td>
        </tr>
      </tbody>
    </v-table>
  </div>
</template>

<style scoped>

.content-header{
  min-height: 10% !important;
}
.btn-container{
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
.class-subjects .overlay-card{
  max-width: 500px !important;
}
.class-subjects .overlay-card-info-container{
  margin-top: 4em;
  height: 100% !important;
}
.overlay-card-content-container {
  margin-top: 3em !important;
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
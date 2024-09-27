<script setup lang="ts">

const userAuthStore = useUserAuthStore()
const formErrorMessage = ref('')
const formSuccessMessage = ref('')
const date = ref('')
const loading = ref(false)
const selectedStudents:any = ref(null)
const students:any = ref([])
const className:any = ref(null)
const subjects:any = ref([])


const clearMessage = ()=>{
  setTimeout(()=>{
    formErrorMessage.value = ''
    formSuccessMessage.value = ''
  }, 10000)
}

const showOverlay = (overlay:string)=>{
  if (overlay === 'attendance'){
    const overlay = document.getElementById('studentAttendanceOverlay')
    overlay ? overlay.style.display = 'flex' : null
  }
  else if (overlay === 'results'){
    const overlay = document.getElementById(`teacherStudentsResultsOverlay${className.value}`)
    overlay ? overlay.style.display = 'flex' : null
  }
  else{
    const overlay = document.getElementById('teacherSubjectsOverlay')
    overlay ? overlay.style.display = 'flex' : null
  }
}

const uploadAttendance = async()=>{
  formErrorMessage.value = ''
  formSuccessMessage.value = ''
  loading.value = true
  const formData = new FormData
  formData.append('className', userAuthStore.teacherData.currentCourseWork['students_class']['name'])
  formData.append('absentStudents', selectedStudents.value)
  formData.append('year', userAuthStore.activeAcademicYear)
  formData.append('term', userAuthStore.activeTerm)
  formData.append('type', 'create')
  formData.append('date', date.value)

  try{
    const response = await axiosInstance.post('teacher/students/attendance', formData)
    if (response.status === 200){
      userAuthStore.teacherData.studentsattendance.unshift(response.data)
      formSuccessMessage.value = 'Upload successful'
      selectedStudents.value = null
    }
    else if (response.status === 201){
      formErrorMessage.value = response.data.ms
    }
  }
  catch(e){
    formErrorMessage.value = 'Oops! something went wrong'
    return Promise.reject(e)
  }
  finally{
    loading.value = false
    clearMessage()
  }
}

const checkInput = computed(()=>{
  return !(date.value)
})

const closeOverlay = ()=>{
  formErrorMessage.value = ''
  formSuccessMessage.value = ''
  selectedStudents.value = null
  date.value = ''

  const overlay = document.getElementById('studentAttendanceOverlay')
  overlay ? overlay.style.display = 'none' : null

  const overlayTwo = document.getElementById('teacherSubjectsOverlay')
  overlayTwo ? overlayTwo.style.display = 'none' : null
}

watch(()=> userAuthStore.teacherData.currentCourseWork, (newValue, oldValue)=>{
  if (newValue){
    const students_data:any = ref([])
    newValue['students_class']['students'].forEach(item =>{
      students_data.value.push({'name': `${item['user']['first_name']} ${item['user']['last_name']}`, 'st_id': item['st_id']})
    })
    students.value = students_data.value
    className.value = newValue['students_class']['name']
    subjects.value = newValue['subjects']
  }
})



</script>

<template>
  <div class="content-wrapper">
    <TeacherStudentsResultsUpload v-if="className && students && subjects" :students="students" :className="className" :subjects="subjects" />
    <div id="teacherSubjectsOverlay" class="overlay" v-if="userAuthStore.teacherData.currentCourseWork">
      <div class="info-container">
        <v-btn @click="closeOverlay()" color="red" size="small" class="close-btn">X</v-btn>
        <div class="flex-all-c mt-15 mb-5">
          <h3 style="color: green; font-size: .9rem; font-family: monospace">SUBJECT(S) ASSIGNED TO THIS CLASS [{{ userAuthStore.teacherData.currentCourseWork['subjects'].length }}]</h3>
          <p class="teacher-subject" v-for="(subject, index) in userAuthStore.teacherData.currentCourseWork['subjects']" :key="index">
            {{ subject['name'] }}
          </p>
        </div>
      </div>
    </div>

    <div id="studentAttendanceOverlay" class="overlay" v-if="userAuthStore.teacherData.currentCourseWork">
      <div class="card" style="position: relative">
          <v-btn @click="closeOverlay()" :disabled="loading" color="red" size="small" class="close-btn flex-all">X</v-btn>
          <h2 class="info mt-5"><strong>CLASS: </strong>{{userAuthStore.teacherData.currentCourseWork['students_class']['name']}}</h2>
          <h2 v-if="formSuccessMessage" class="form-message" style="color: green">{{formSuccessMessage}}</h2>
          <h2 v-if="formErrorMessage" class="form-message" style="color: red">{{formErrorMessage}}</h2>
          
          <v-text-field
          label="DATE"
          class="input-field"
          v-model="date"
          hint="select the date for the class attendance"
          persistent-hint
          clearable
          variant="outlined"
          type="date"
          density="compact"
          />

          <v-select :disabled="loading" v-if="userAuthStore.teacherData.currentCourseWork" clearable multiple chips v-model="selectedStudents" class="select" label="STUDENTS" 
          :items="userAuthStore.teacherData.currentCourseWork['students_class']['students']" item-title="user.last_name" item-value="st_id" persistent-hint hint="Select the students who did not attend class for the specified date">
            <template v-slot:item="{ props, item }">
                <v-list-item v-bind="props" :subtitle="item.raw.user.first_name"></v-list-item>
            </template>
          </v-select>
          
          <v-btn :loading="loading" :disabled="checkInput" @click="uploadAttendance" size="small" color="green"  class="mt-5" type="submit">UPLOAD</v-btn>
        </div>
    </div>
    <TheLoader v-if="!userAuthStore.teacherData.courseWork" />
    <div class="no-data" v-if="userAuthStore.teacherData.courseWork && !userAuthStore.teacherData.currentCourseWork">
      <p>YOU HAVE NOT BEEN ASSIGNED TO A CLASS YET</p>
    </div>
    <div class="info-wrapper" v-if="userAuthStore.teacherData.currentCourseWork">
      <div class="flex-all">
        TOTAL NUMBER OF STUDENTS:
        <h4 class="ml-2">
          {{ userAuthStore.teacherData.currentCourseWork['students_class']['students'].length }}
        </h4>
      </div>
      <div class="flex-all">
        <v-btn @click="showOverlay('subjects')" class="ma-1" color="blue" size="small">SUBJECT(S)</v-btn>
        <v-btn @click="showOverlay('attendance')" class="ma-1" v-if="userAuthStore.teacherData.currentCourseWork['students_class']['head_teacher']['user']['username'] === userAuthStore.userData['username'] " color="blue" size="small">UPLOAD ATTENDANCE</v-btn>
      </div>
      <div class="flex-all-c">
        <v-btn @click="showOverlay('results')" class="ma-1" color="blue" size="small">UPLOAD ASSESSMENT/EXAMS</v-btn>
      </div>
    </div>
    <v-table fixed-header class="table" v-if="userAuthStore.teacherData.currentCourseWork">
      <thead>
      <tr>
        <th class="table-head">NAME</th>
        <th class="table-head">GENDER</th>
        <th class="table-head">IMAGE</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="(st, i) in userAuthStore.teacherData.currentCourseWork['students_class']['students']" :key="i">
        <td class="table-data">{{st['user']['first_name']}} {{st['user']['last_name']}}</td>
        <td class="table-data">{{st['gender']}}</td>
        <td class="table-data"><img class="profile-img" :src="st['img']"></td>
      </tr>
      </tbody>
    </v-table>
  </div>
</template>

<style scoped>

.info-wrapper{
  height: 20% !important;
  flex-wrap: wrap !important;
}
.table{
  height: 80% !important;
}
.overlay{
  position: absolute !important;
  background: rgba(0, 0, 0, .5) !important;
  top: 0 !important;
  left: 0 !important;
  height: 100% !important;
  width: 100% !important;
  z-index: 10 !important;
  align-items: center !important;
  justify-content: center !important;
  display: none;
}
.info-container{
  position: relative;
  width: 95%;
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: white;
  border-radius: .3em;
  max-width: 500px;
}
.teacher-subject{
  color: white;
  margin: .3em;
  font-family:Verdana, Geneva, Tahoma, sans-serif;
  padding: .5em;
  background-color: #333333;
  font-weight: bold;
  border-radius: .2em;
  font-size: .8rem;
}
.card{
  background-color: white;
  padding: .5em 1em;
  border-radius: .3em;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 95%;
  height: 80%;
  max-width: 800px;
  max-height: 700px;
}

.info{
  font-size: 1rem;
  text-align: center;
  font-family: Verdana, Geneva, Tahoma, sans-serif;
}

.info strong{
  font-size: 1rem;
  color: seagreen
}
.form-message{
  font-size: .8rem;
  margin-top: 1em;
  text-align: center;
  border: 1px solid;
  text-transform: uppercase;
  padding: .1em 1em;
}

.select{
  font-weight: bold;
  margin-top: 2em;
  color: black;
  min-width: 300px  !important;
  width: 80% !important;
  margin-bottom: 1em;
  max-height: 100px !important;
  overflow-y: auto !important;
}

.input-field{
  color: black;
  font-weight: bold;
  margin-top: 2em;
  width: 220px !important;
  max-height: 100px !important;
  font-size: .7rem;
  font-family:monospace;
}



</style>
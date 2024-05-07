<script setup lang="ts">

const userAuthStore = useUserAuthStore()
const formErrorMessage = ref('')
const formSuccessMessage = ref('')
const studentsYear = ref(0)
const date = ref('')
const subject = ref('')
const className = ref('')
const loading = ref(false)
const selectedStudents = ref(null)
const students = ref(null)

interface Props {
  term: string;
  termNumber: number;
}

const clearMessage = ()=>{
  setTimeout(()=>{
    formErrorMessage.value = ''
    formSuccessMessage.value = ''
  }, 10000)
}

const { term, termNumber } = defineProps<Props>()

const showOverlay = (clasName: any, selectSt: any, classYear: any, subj: any)=>{
  className.value = clasName
  students.value = selectSt
  studentsYear.value = classYear
  subject.value = subj
  const overlay = document.getElementById(`attendace${termNumber}`)
  overlay ? overlay.style.display = 'flex' : null
}

const uploadAttendance = async()=>{
  loading.value = true
  const formData = new FormData
  formData.append('className', className.value)
  formData.append('absentStudents', selectedStudents.value)
  formData.append('year', userAuthStore.activeAcademicYear)
  formData.append('term', userAuthStore.activeTerm)
  formData.append('type', 'create')
  formData.append('date', date.value)
  formData.append('subject', subject.value)

  try{
    const response = await axiosInstance.post('teacher/students/attendance', formData)
    if (response.status === 200){
      const data = response.data
      const subjectAttendance = userAuthStore.teacherStudentsAttendance.find(c => c['subject'] === data['subject']['name'] && c['class_name'] === data['students_class']['name'])
      if (subjectAttendance){
        const subjectAttendanceIndex = userAuthStore.teacherStudentsAttendance.indexOf(subjectAttendance)
        userAuthStore.teacherStudentsAttendance[subjectAttendanceIndex]['attendance'].unshift(data)
      }
      else{
        await userAuthStore.getTeacherStudentsAttendance()
      }
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
  className.value = ''
  students.value = null
  studentsYear.value = 0
  formErrorMessage.value = ''
  formSuccessMessage.value = ''
  selectedStudents.value = null
  date.value = ''
  subject.value = ''

  const overlay = document.getElementById(`attendace${termNumber}`)
  overlay ? overlay.style.display = 'none' : null
}



</script>

<template>

  <div :id="`attendace${termNumber}`" class="overlay">
    <div class="card" style="position: relative">
        <v-btn @click="closeOverlay" :disabled="loading" color="red" size="small" class="close-btn flex-all">X</v-btn>
        <h2 class="info mt-5"><strong>CLASS:</strong> {{className}} FORM {{studentsYear}}</h2>
        <h2 class="info"><strong>SUBJECT:</strong> {{subject}}</h2>
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

        <v-select :disabled="loading" v-if="students" clearable multiple chips v-model="selectedStudents" class="select" label="STUDENTS" 
        :items="students" item-title="user.last_name" item-value="st_id" persistent-hint hint="Select the students who did not attend class for the specified date">
          <template v-slot:item="{ props, item }">
              <v-list-item v-bind="props" :subtitle="item.raw.st_id"></v-list-item>
          </template>
        </v-select>
        
        <v-btn :loading="loading" :disabled="checkInput" @click="uploadAttendance" size="small" color="green"  class="mt-5" type="submit">UPLOAD</v-btn>
      </div>
</div>

    <div style="width: 100%; position: relatve; height: 100%">
      <TheLoader v-if="!userAuthStore.staffSubjectAssignment[term]" />
      <h4 class="no-data flex-all" v-if="userAuthStore.staffSubjectAssignment[term] && userAuthStore.staffSubjectAssignment[term].length === 0">
        <p v-if="userAuthStore.userData['school']['semesters']">No coursework for semester {{ termNumber }} yet</p>
        <p v-if="userAuthStore.userData && !userAuthStore.userData['school']['semesters']">No coursework for trimester {{ termNumber }} yet</p>
      </h4>
      <v-table fixed-header class="table-1" v-if="userAuthStore.staffSubjectAssignment[term] && userAuthStore.staffSubjectAssignment[term].length > 0">
        <thead>
        <tr>
          <th class="table-head">SUBJECT</th>
          <th class="table-head">CLASS</th>
          <th class="table-head">FORM</th>
          <th class="table-head" v-if="termNumber === userAuthStore.activeTerm">ATTENDANCE</th>
          <th class="table-head">STUDENTS</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(assign, i) in userAuthStore.staffSubjectAssignment[term]" :key="i">
          <td class="table-data">{{assign['subject']['name']}}</td>
          <td class="table-data">{{assign['students_class']['name']}}</td>
          <td class="table-data">{{assign['students_class']['students_year']}}</td>
          <td class="table-data" v-if="termNumber === userAuthStore.activeTerm" @click="showOverlay(assign['students_class']['name'], assign['students_class']['students'], assign['students_class']['students_year'], assign['subject']['name'])"><v-btn size="small" color="blue" >UPLOAD</v-btn></td>
          <td style=" padding: 0">
            <v-list class="pa-0">
              <v-list-group>
                <template v-slot:activator="{ props }">
                  <v-list-item class="title" v-bind="props">
                    <v-icon icon="mdi-account-circle" />{{assign['students_class']['students'].length}} STUDENTS
                  </v-list-item>
                </template>
                  <v-virtual-scroll class="v-scroll" height="22vh" :items="assign['students_class']['students']">
                    <template v-slot:default="{ item }" >
                      <v-list-item style="position: relative">
                        <div class="student-info-container">
                          <img class="profile-img" :src="item['img']">
                          <div class="flex-all-c">
                            <p class="user-name">{{item['user']['first_name']+' '+item['user']['last_name']}}</p>
                            <p class="user-name">{{item['st_id']}}</p>
                          </div>
                        </div>
                        
                      </v-list-item>
                    </template>
                  </v-virtual-scroll>
              </v-list-group>
            </v-list>
          </td>
        </tr>
        </tbody>
      </v-table>
    </div>
</template>

<style scoped>

@import url('../assets/css/tables.css');


.overlay{
  position: absolute;
  background: rgba(0, 0, 0, .5);
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  z-index: 5;
  align-items: center;
  justify-content: center;
  display: none;
}

.card{
  background-color: white;
  padding: .5em 1em;
  border-radius: .3em;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 90%;
  height: 80%;
  max-width: 800px;
  max-height: 700px;
}

.info{
  font-size: .7rem;
  text-align: center;
  font-family: Verdana, Geneva, Tahoma, sans-serif;
}

.info strong{
  font-size: .8rem;
  color: seagreen
}
.form-message{
  font-size: .8rem;
  margin-top: 1em;
  text-align: center;
  border: 1px solid;
  padding: .1em 1em;
}

.select{
  font-weight: bold;
  margin-top: 2em;
  color: black;
  width: 250px !important;
  margin-bottom: 1em;
  max-height: 100px !important;
  overflow-y: auto !important;
}

.input-field{
  color: black;
  font-weight: bold;
  margin-top: 2em;
  width: 250px !important;
  max-height: 100px !important;
  font-size: .7rem;
  font-family:monospace;
}



</style>
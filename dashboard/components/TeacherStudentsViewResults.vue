
<script setup lang="ts">
import axiosInstance from '../utils/axiosInstance';

import { ref } from 'vue';

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()
const formSuccessMessage = ref('')
const formErrorMessage = ref('')
const loading = ref(false)
const studentName = ref('')
const studentId = ref('')
const subjectName = ref('')
const studentClass = ref('')
const studentYear: any = ref(null)
const score:any = ref(null)


const editResult = async()=>{
    loading.value = true
    formErrorMessage.value = ''
    formSuccessMessage.value = ''
    score.value = Number(score.value)

    if (typeof score.value === 'number' && score.value <= 100 && score.value >0){
        const formData = new FormData()
        formData.append('student_year', studentYear.value);
        formData.append('student_class', studentClass.value);
        formData.append('student_name', studentName.value)
        formData.append('subject', subjectName.value);
        formData.append('st_id', studentId.value); 
        formData.append('score', 'edit');
        formData.append('mark', score.value);
        formData.append('year', userAuthStore.activeAcademicYear);
        formData.append('term', userAuthStore.activeTerm.toString());

      try{
          const response = await axiosInstance.post('teacher/results/upload/', formData)
          if (response.status === 200){
            userAuthStore.userData['staff_role']==='hod'? userAuthStore.getHodPerformance() : null
              formSuccessMessage.value = `Result for ${studentName.value} [${studentId.value}] updated successfully`
              userAuthStore.staffStudentResultsSubjectAssignment = response.data[0]
              userAuthStore.staffStudentResultsEdit = response.data[1]
              score.value = null
          }
          else if (response.status === 202){
              formErrorMessage.value = response.data.message
          }
          else{
              formErrorMessage.value = 'Oops! something went wrong. try again'
          }
      }
      catch{
          formErrorMessage.value = 'Oops! something went wrong. try again'
      }
      finally{
          loading.value = false
      }
    }

    else if (typeof score.value === 'number' && score.value >100){
      formErrorMessage.value = 'The exams score must not exceed 100'
      loading.value = false
    }
    else if (typeof score.value === 'number' && score.value <0){
      formErrorMessage.value = 'The exams score can not be negative'
      loading.value = false
    }
    else{
      formErrorMessage.value = 'The exams score must be a number'
      loading.value = false
    }
}

const closeOverlay = ()=>{
    const overlay = document.getElementById('editForm')
    if (overlay){
        score.value = null
        formErrorMessage.value = ''
        formSuccessMessage.value = ''
        loading.value = false
        overlay.style.display = 'none'
    }
}

const showForm = (subject: string, className: string, stName: string, stId: string, Year: any)=>{
    subjectName.value = subject
    studentClass.value = className
    studentYear.value = Year
    studentId.value = stId
    studentName.value = stName
    const formOverlay = document.getElementById('editForm')
    formOverlay ? formOverlay.style.display = 'flex' : null

}

</script>

<template>
    
    <div id="editForm" class="overlay">
        <form style="position: relative">
            <button @click.prevent="closeOverlay" class="close-btn flex-all">X</button>
            <h2 class="info"><strong>CLASS:</strong> {{studentClass}} FORM {{studentYear}}</h2>
            <h2 class="info"><strong>SUBJECT:</strong> {{subjectName}}</h2>
            <h2 class="info"><strong>STUDENT:</strong> {{studentName}} [{{studentId}}]</h2>
            <h2 v-if="formSuccessMessage" class="form-message" style="color: green">{{formSuccessMessage}}</h2>
            <h2 v-if="formErrorMessage" class="form-message" style="color: red">{{formErrorMessage}}</h2>
            
            <v-text-field :disabled="loading" v-model="score" type="number" class="input-field" persistent-hint hint="Enter the student(s) exams score" label="EXAMS SCORE" variant="outlined"/>
            <v-btn :loading="loading" :disabled="!score" @click.prevent="editResult" type="submit" class="submit-btn">SUBMIT</v-btn>
        </form>
    </div>

    <div style="width: 100%; position: relative; height: 100%">
      
      <TheLoader class="no-data flex-all" v-if="!userAuthStore.staffStudentResultsEdit" />
      
        <v-table fixed-header class="table-1" v-if="userAuthStore.staffStudentResultsEdit">
        <thead>
        <tr>
          <th class="table-head">SUBJECT</th>
          <th class="table-head">CLASS</th>
          <th class="table-head">FORM</th>
          <th class="table-head">STUDENTS</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(result, i) in userAuthStore.staffStudentResultsEdit" :key="i">
          <td class="table-data">{{result['subject']}}</td>
          <td class="table-data">{{result['class_name']}}</td>
          <td class="table-data">{{result['students_year']}}</td>
          <td style=" padding: 0">
            <v-list class="pa-0">
              <v-list-group>
                <template v-slot:activator="{ props }">
                  <v-list-item class="title" v-bind="props">
                    <v-icon icon="mdi-account-circle" />{{result['students'].length}} STUDENTS
                  </v-list-item>
                </template>
                  <v-virtual-scroll class="v-scroll" height="22vh" :items="result['students']">
                    <template v-slot:default="{ item }" >
                      <v-list-item style="position: relative">
                        <div class="student-info-container">
                          <img class="student-img" :src="elementsStore.getBaseUrl + item['student']['img']">
                          <div class="flex-all-c">
                            <p class="user-name">{{item['student']['user']['first_name']+' '+item['student']['user']['last_name']}}</p>
                            <p class="user-name">{{item['student']['st_id']}}</p>
                          </div>
                          <div class="score-container flex-all-c">
                            <p class="title">SCORE</p>
                            <p class="score">{{item['score']}}</p>
                          </div>
                          <div class="flex-all pa-2">
                            <button @click="showForm(result['subject'], result['class_name'], `${item['student']['user']['first_name']} ${item['student']['user']['last_name']}`, item['student']['st_id'], result['students_year'])" class="edit-btn page-btn">Edit</button>
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

.edit-btn{
    font-size: .7rem;
    padding: .1em .5em
}

.score-container{
  padding: .1em
}
.score-container .title{
  font-size: .6rem;
}
.score-container .score{
  font-size: .7rem;
  color: lightseagreen;
  font-family: Verdana, Geneva, Tahoma, sans-serif;
  font-weight: bold;
}
.overlay{
    position: absolute;
    background: rgba(0, 0, 0, .5);
    top: 0;
    left: 0;
    height: 100%;
    width: 100%;
    display: flex;
    z-index: 3;
    align-items: center;
    justify-content: center;
    display: none;
}

#editForm form{
    background-color: white;
    padding: .5em 1em;
    border-radius: .3em;
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 90%;
    max-width: 500px;
}

.close-btn{
    position: absolute;
    right: 0;
    top: 0;
    background-color: red;
    width: 25px;
    border-radius: .3em;
    color: white;
}

.close-btn:hover{
    background-color: black;
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
}
.input-field{
    margin-top: 1em;
}
.submit-btn{
    background-color: lightseagreen;
    color: white;
    font-weight: bold;
    margin-top: 1em;
    margin-bottom: 1em;
}

.submit-btn:hover{
    background-color: mediumseagreen;
    color: yellow;
}


</style>
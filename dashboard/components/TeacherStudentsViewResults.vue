
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
const previousScore: any = ref(null)
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
              previousScore.value = null
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

const showForm = (subject: string, className: string, stName: string, stId: string, prevScore: number, Year: any)=>{
    subjectName.value = subject
    studentClass.value = className
    studentYear.value = Year
    studentId.value = stId
    studentName.value = stName
    previousScore.value = prevScore
    const formOverlay = document.getElementById('editForm')
    formOverlay ? formOverlay.style.display = 'flex' : null

}

</script>

<template>
    
    <div id="editForm" class="overlay">
        <form style="position: relative">
            <v-btn @click.prevent="closeOverlay" class="close-btn" size="small" color="red">X</v-btn>
            <h2 class="info"><strong>CLASS:</strong> {{studentClass}} FORM {{studentYear}}</h2>
            <h2 class="info"><strong>SUBJECT:</strong> {{subjectName}}</h2>
            <h2 class="info"><strong>STUDENT:</strong> {{studentName}} [{{studentId}}]</h2>
            <h2 class="info" v-if="previousScore"><strong>PREVIOUS SCORE:</strong> {{previousScore}}</h2>
            <h2 v-if="formSuccessMessage" class="form-message" style="color: green">{{formSuccessMessage}}</h2>
            <h2 v-if="formErrorMessage" class="form-message" style="color: red">{{formErrorMessage}}</h2>
            
            <v-text-field :disabled="loading" v-model="score" type="number" class="input-field" persistent-hint hint="Enter the student's new score" label="NEW SCORE" variant="outlined"/>
            <v-btn :loading="loading" :disabled="!score" @click.prevent="editResult" type="submit" color="green" class="mt-5 mb-5">SUBMIT</v-btn>
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
                      <v-list-item class="list-container">
                        <template v-slot:prepend>
                          <p class="score">{{item['score']}}</p>
                        </template>
                        <v-list-item-title>
                          <p class="user-name">{{item['student']['user']['first_name']+' '+item['student']['user']['last_name']}}</p>
                        </v-list-item-title>
                        <v-list-item-subtitle>
                          <p class="user-name">{{item['student']['st_id']}}</p>
                        </v-list-item-subtitle>
                        <template v-slot:append>
                          <v-btn @click="showForm(result['subject'], result['class_name'], `${item['student']['user']['first_name']} ${item['student']['user']['last_name']}`, item['student']['st_id'], item['score'], result['students_year'])" color="green" size="x-small" icon="mdi-pencil"/>
                        </template>
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


.list-container{
  padding: 0! important;
}
.score{
  background-color: green;
  padding: .5em;
  border-radius: .5em;
  color: white;
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

.info{
    font-size: .7rem;
    text-align: center;
    margin: .5em 0;
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

.input-field{
    margin-top: 1em;
}

.submit-btn{
    font-weight: bold;
    margin-top: 1em;
    margin-bottom: 1em;
}



</style>
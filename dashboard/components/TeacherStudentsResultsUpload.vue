<script setup lang="ts">
import axiosInstance from '../utils/axiosInstance';
import { ref, computed, watch } from 'vue';

const userAuthStore = useUserAuthStore()
const subjectName = ref('')
const studentsClass = ref('')
const studentsYear: any = ref(null)
const formErrorMessage = ref('')
const formSuccessMessage = ref('')
const selectedStudents: any = ref([])
const singleValue = ref('')
const multipleValue = ref([])
const score: any = ref(null)
const multiple = ref(false)
const loading = ref(false)
const fileToUpload: any = ref(null)
const getFileLoading = ref(false)
const show = ref(true)


const clearMessage = ()=>{
    setTimeout(()=>{
        formSuccessMessage.value = ''
        formErrorMessage.value = ''
    }, 15000)
}

// Generate an excel file
const generateFile = async()=>{
    getFileLoading.value = true
    formErrorMessage.value = ''
    formSuccessMessage.value = ''
    const data = {
        'students_year': studentsYear.value, 
        'students_class': studentsClass.value, 
        'subject': subjectName.value, 
        'st_id': selectedStudents.value, 
        'score': 'generate', 
        'year': userAuthStore.activeAcademicYear, 
        'term': userAuthStore.activeTerm
    }
    
    try{
        const response = await axiosInstance.post('teacher/results/upload/', data)
        if (response.status === 200){
            formSuccessMessage.value = response.data.message
            userAuthStore.staffStudentsResultsFileGenerated = true
            const link = document.createElement('a');
            link.href = response.data.file_path;
            link.download = response.data.filename
            link.click()
        }
        else {
            formErrorMessage.value = 'Oops! an error occurred while generating the file. Try again later'
        }

    }
    catch{
        formErrorMessage.value = 'Something went wrong. Try again later'
    }
    finally{
        getFileLoading.value = false
        clearMessage()
    }
}

const fileChange = (event: any)=>{
    const file = event.target.files[0]
    fileToUpload.value = file || null
}

// Upload student results using the generated excel file
const uploadFile = async()=>{
    loading.value = true
    formErrorMessage.value = ''
    formSuccessMessage.value = ''
    
    const formData = new FormData();
    formData.append('students_year', studentsYear.value);
    formData.append('students_class', studentsClass.value);
    formData.append('subject', subjectName.value);
    formData.append('st_id', fileToUpload.value); 
    formData.append('score', 'upload');
    formData.append('year', userAuthStore.activeAcademicYear);
    formData.append('term', userAuthStore.activeTerm.toString());

    try{
        const response = await axiosInstance.post('teacher/results/upload/', formData)
        if (response.status === 200){
            userAuthStore.userData['staff_role']==='hod'? userAuthStore.getHodPerformance() : null
            userAuthStore.staffStudentResultsSubjectAssignment = response.data.data[0]
            userAuthStore.staffStudentResultsEdit = response.data.data[1]
            formSuccessMessage.value = response.data.message
        }
        else if (response.status === 201){
            formErrorMessage.value = response.data.message
        }
        else if (response.status === 202){
            formErrorMessage.value = response.data.message
        }
    }

    catch{
        formErrorMessage.value = "Something went wrong!"
    }

    finally{
        loading.value = false
        clearMessage()
    }
}

// Upload by select and input data
const inputUpload = async()=>{
    loading.value = true
    formErrorMessage.value = ''
    formSuccessMessage.value = ''
    score.value = Number(score.value)

    if (typeof score.value === 'number' && score.value <=100 && score.value >0){
        if (multiple.value){
            singleValue.value = ''
            await userAuthStore.teacherUploadResults(multipleValue.value, subjectName.value, score.value)
            .then(response =>{
                userAuthStore.getTeacherStudentResults()
                userAuthStore.userData['staff_role']==='hod'? userAuthStore.getHodPerformance() : null
                formSuccessMessage.value = `Result for students with IDs [${multipleValue.value}] uploaded and saved successfully`
                multipleValue.value = []
                multiple.value = false
                score.value = null
                loading.value = false
            })
            .catch(e =>{
                formErrorMessage.value = 'Oops! something went wrong while generating the file. Try again'
                loading.value = false
            })
        }
        else if (!multiple.value) {
            multipleValue.value = []
            await userAuthStore.teacherUploadResults(singleValue.value, subjectName.value, score.value)
            .then(response =>{
                userAuthStore.getTeacherStudentResults()
                userAuthStore.userData['staff_role']==='hod'? userAuthStore.getHodPerformance() : null
                const st = singleValue.value
                formSuccessMessage.value = `Result for student with ID ${st} uploaded and saved successfully`
                singleValue.value = ''
                score.value = null
                loading.value = false
            })
            .catch(e =>{
                formErrorMessage.value = 'Oops! something went wrong. try again'
                loading.value = false
            })
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
    clearMessage()
}

const checkInput = computed(()=>{

    return !(multipleValue.value && score.value) && !(singleValue.value && score.value);
    
})

const closeOverlay = (element: string)=>{
    const overlay = document.getElementById(element)
    if (overlay){
        selectedStudents.value = []
        multipleValue.value = []
        score.value = null
        formErrorMessage.value = ''
        formSuccessMessage.value = ''
        singleValue.value = ''
        loading.value = false
        show.value = true
        multiple.value = false
        fileToUpload.value = null
        userAuthStore.staffStudentsResultsFileGenerated = false
        overlay.style.display = 'none'

    }
}

const showForm = (subject: string, className: string, students: [], index: number, Year: any, element: string)=>{
    subjectName.value = subject
    studentsClass.value = className
    studentsYear.value = Year
    selectedStudents.value = students
    
    if (students.length > 0){
        watch(()=> userAuthStore.staffStudentResultsSubjectAssignment, (newValue)=>{
        if (newValue){
            const newsubjectAssignment = newValue[index]
            if (newsubjectAssignment && newsubjectAssignment['students']){

                selectedStudents.value = newsubjectAssignment['students']
                }
            }
        })
    }
    else{
        formErrorMessage.value = `You have already uploaded results for students in this class`
        show.value = false
    }

    const formOverlay = document.getElementById(element)
    formOverlay ? formOverlay.style.display = 'flex' : null

}


</script>

<template>
    <div id="singleForm" class="overlay">
        <form style="position: relative">
            <button @click.prevent="closeOverlay('singleForm')" class="close-btn flex-all">X</button>
            <h2 class="info mt-3"><strong>CLASS:</strong> {{studentsClass}} FORM {{studentsYear}}</h2>
            <h2 class="info"><strong>SUBJECT:</strong> {{subjectName}}</h2>
            <h2 v-if="formSuccessMessage" class="form-message" style="color: green">{{formSuccessMessage}}</h2>
            <h2 v-if="formErrorMessage" class="form-message" style="color: red">{{formErrorMessage}}</h2>
            <v-select :disabled="loading" v-if="!multiple && show" v-model="singleValue" class="select" label="STUDENT" variant="outlined" 
            :items="selectedStudents" item-title="name" item-value="st_id" persistent-hint hint="Select the student you want to upload result for">
            <template v-slot:item="{ props, item }">
                <v-list-item v-bind="props" :subtitle="item.raw.st_id"></v-list-item>
            </template>
            </v-select>
            <v-select :disabled="loading" v-if="multiple && show" multiple clearable v-model="multipleValue" chips class="select" label="STUDENT" variant="outlined" 
            :items="selectedStudents" item-title="name" item-value="st_id" persistent-hint hint="Select the student you want to upload result for">
            <template v-slot:item="{ props, item }">
                <v-list-item v-bind="props" :subtitle="item.raw.st_id"></v-list-item>
            </template>
            </v-select>
            
            <div class="flex-all-c" v-if="show">
                
                <p class="checkbox">Check this box if you want to upload results for multiple students with same score</p>
                <v-checkbox :disabled="loading" v-model="multiple" />
            </div>
            <v-text-field v-if="show" :disabled="loading" type="number" v-model="score" class="input-field" persistent-hint hint="Enter the student(s) exams score" label="EXAMS SCORE" variant="outlined"/>
            <v-btn v-if="show" :loading="loading" :disabled="checkInput" @click.prevent="inputUpload" type="submit" class="submit-btn">SUBMIT</v-btn>
        </form>
    </div>

    <!-- File upload form -->
    <div id="fileForm" class="overlay">
        <form style="position: relative">
            <button @click.prevent="closeOverlay('fileForm')" class="close-btn flex-all">X</button>
            <h2 class="info mt-3"><strong>CLASS:</strong> {{studentsClass}} FORM {{studentsYear}}</h2>
            <h2 class="info"><strong>SUBJECT:</strong> {{subjectName}}</h2>
            <h2 v-if="formSuccessMessage" class="form-message" style="color: green">{{formSuccessMessage}}</h2>
            <h2 v-if="userAuthStore.staffStudentsResultsFileGenerated && !getFileLoading && !loading" class="form-message" style="color: green">Note: you can now edit only the students score, save and upload the same file</h2>
            <h2 v-if="formErrorMessage" class="form-message" style="color: red">{{formErrorMessage}}</h2>
            <div class="flex-all-c mt-5">
                <v-btn v-if="show" :loading="getFileLoading" :disabled="loading" @click.prevent="generateFile" type="submit" class="submit-btn">GET FILE</v-btn>
                <p v-if="!userAuthStore.staffStudentsResultsFileGenerated && show" class="checkbox">Click to get an excel file that contains the students names and IDs</p>
            </div>

            <hr class="line" v-if="show">

            <v-file-input v-if="show" :disabled="loading || getFileLoading" @change="fileChange"  show-size class="file-field" label="Choose an excel file" density="compact"
            variant="outlined" accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet">
            </v-file-input>
            <v-btn v-if="show" :loading="loading" :disabled="!fileToUpload || getFileLoading" @click.prevent="uploadFile" type="submit" class="submit-btn">UPLOAD</v-btn>
        </form>
    </div>


    <div style="width: 100%">
      <TheLoader v-if="!userAuthStore.staffStudentResultsSubjectAssignment" />

      <v-table fixed-header class="table-1" v-if="userAuthStore.staffStudentResultsSubjectAssignment">
        <thead >
        <tr>
          <th class="table-head">SUBJECT</th>
          <th class="table-head">CLASS</th>
          <th class="table-head">FORM</th>
          <th class="table-head">UPLOAD</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(resultsAssign, index) in userAuthStore.staffStudentResultsSubjectAssignment" :key="index">
          <td class="table-data">{{resultsAssign['subject']}}</td>
          <td class="table-data">{{resultsAssign['class_name']}}</td>
          <td class="table-data">{{resultsAssign['students_year']}}</td>
          <td style="padding: 0" class="upload-btn-container">
            <button @click="showForm(resultsAssign['subject'], resultsAssign['class_name'], resultsAssign['students'], index, resultsAssign['students_year'], 'singleForm')" class="upload-btn">SELECT</button>
            <button @click="showForm(resultsAssign['subject'], resultsAssign['class_name'], resultsAssign['students'], index, resultsAssign['students_year'], 'fileForm')" class="upload-btn last-btn">FILE</button>
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

#singleForm form, #fileForm form{
    background-color: white;
    padding: .5em 1em;
    border-radius: .3em;
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 90%;
    max-width: 600px;
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
    border: 1px solid;
    padding: .1em 1em;
}

.select{
    font-weight: bold;
    margin-top: 2em;
    color: black;
    min-width: 200px;
    margin-bottom: 1em;
    max-height: 100px !important;
    overflow-y: auto;
}

.checkbox{
    font-size: .7rem;
    color: black;
    font-family:monospace;
    text-align: center;
}

.input-field{
    color: black;
    font-weight: bold;
    margin-top: 1em;
    width: 150px;
    font-size: .7rem;
    font-family:monospace
}

.file-field{
    min-width: 250px;
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

.upload-btn-container{
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    padding: 0;
}

.upload-btn{
    font-size: .6rem;
    background-color: lightseagreen;
    height: fit-content;
    border-radius: .3em;
    padding: .1em .6em;
    text-transform: uppercase;
    font-weight: bold;
}

.upload-btn:hover{
    background-color: mediumseagreen;
    color: white;
}

.line{
    margin: 1rem;
    width: 100%;
}

@media screen and (min-width: 576px) {
    .upload-btn{
        font-size: .7rem;
    }

    .upload-btn-container{
        justify-content: space-around;
      }
}

@media screen and (min-width: 767px) {
    .upload-btn{
        font-size: .75rem;
    }
}


</style>
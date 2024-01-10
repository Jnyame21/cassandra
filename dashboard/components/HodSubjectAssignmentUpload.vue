<script setup lang="ts">
import axiosInstance from '../utils/axiosInstance';
import { ref, computed } from 'vue';

const userAuthStore = useUserAuthStore()
const subjectName = ref('')
const studentsClass = ref('')
const selectedStaff = ref('')
const formErrorMessage = ref('')
const formSuccessMessage = ref('')
const loading = ref(false)


const clearMessage = ()=>{
    setTimeout(()=>{
        formSuccessMessage.value = ''
        formErrorMessage.value = ''
    }, 10000)
}

const uploadsubjectAssignment = async()=>{
    loading.value = true
    formErrorMessage.value = ''
    formSuccessMessage.value = ''

    const formData = new FormData
    formData.append('subject', subjectName.value)
    formData.append('class_name', studentsClass.value)
    formData.append('staff_id', selectedStaff.value)
    formData.append('year', userAuthStore.activeAcademicYear)
    formData.append('type', 'create')
    formData.append('term', userAuthStore.activeTerm.toString())

    try {
        const response = await axiosInstance.post("hod/data", formData)
        if (response.status === 200){
            userAuthStore.hodSubjectAssignment.termOne = response.data.data.term_one
            userAuthStore.hodSubjectAssignment.termTwo = response.data.data.term_two
            userAuthStore.hodSubjectAssignment.termThree = response.data.data.term_three
            userAuthStore.getTeacherSubjectAssignments()
            userAuthStore.getTeacherStudentResults()
            formSuccessMessage.value = response.data.ms
            subjectName.value = ''
            studentsClass.value = ''
            selectedStaff.value = ''
        }
        else if (response.status === 201){
            formErrorMessage.value = response.data.ms
        }
        else {
            formErrorMessage.value = "Oops! an error occurred during the upload. Try again later"
        }
    }
    catch {
        formErrorMessage.value = "Oops! something went wrong"
    }
    finally{
        loading.value = false
        clearMessage()
    }
}

const checkInput = computed(()=>{
    return !(subjectName.value && studentsClass.value && selectedStaff.value)
})


</script>

<template>
    <div class="flex-all w-100">
        <form class="form" v-if="userAuthStore.hodSubjectAssignmentUpload.staff">
            <p class="mt-10 info" v-if="userAuthStore.userData['school']['semesters']">NB: All subject assignment will be for the current semester</p>
            <p class="mt-10 info" v-if="userAuthStore.userData && !userAuthStore.userData['school']['semesters']">NB: All subject assignment will be for the current trimester</p>
            <h2 v-if="formSuccessMessage" class="form-message" style="color: green">{{formSuccessMessage}}</h2>
            <h2 v-if="formErrorMessage" class="form-message" style="color: red">{{formErrorMessage}}</h2>
            <div class="flex-all justify-center mt-5 w-100">
                <div class="select-wrap">
                    <v-select :disabled="loading" v-model="subjectName" clearable label="SUBJECT" style="width: 100%; color: black; font-weight: bold" density="compact" variant="outlined" 
                    :items="userAuthStore.hodSubjectAssignmentUpload.subjects" persistent-hint hint="Select the subject">
                    </v-select>
                </div>
                <div class="select-wrap ml-5">
                    <v-select :disabled="loading" v-model="studentsClass" clearable label="CLASS" style="width: 100%; color: black; font-weight: bold" density="compact" variant="outlined" 
                    :items="userAuthStore.hodSubjectAssignmentUpload.classes" persistent-hint hint="Select the students class">
                    </v-select>
                </div>
            </div>
            <v-select :disabled="loading" v-model="selectedStaff" class="select" clearable label="TEACHER" density="compact" variant="outlined" 
            :items="userAuthStore.hodSubjectAssignmentUpload.staff" item-title="name" item-value="stf_id" persistent-hint hint="Select the teacher who will be teaching the subject">
            <template v-slot:item="{ props, item }">
                <v-list-item v-bind="props" :subtitle="item.raw.stf_id"></v-list-item>
            </template>
            </v-select>
    
            <v-btn :loading="loading" :disabled="checkInput" @click.prevent="uploadsubjectAssignment" type="submit" class="submit-btn">SUBMIT</v-btn>
        </form>
    </div>

</template>

<style scoped>

.form{
    width: 90%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin-bottom: 8em;
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

.select-wrap{
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    width: 200px
}

.select{
    font-weight: bold;
    margin-top: 1.5em;
    color: black;
    width: 250px;
}

.submit-btn{
    background-color: lightseagreen;
    color: white;
    font-weight: bold;
    margin-top: 3em;
}

.submit-btn:hover{
    background-color: mediumseagreen;
    color: yellow;
}

@media screen and (min-width: 776px) {
    .select-wrap{
      width: 250px
    }
}

@media screen and (min-width: 992px) {
  .select-wrap, .select{
    width: 300px
  }
}

</style>


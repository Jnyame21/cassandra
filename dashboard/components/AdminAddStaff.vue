<script setup lang="ts">
import axiosInstance from '../utils/axiosInstance';
import { ref, computed } from 'vue';

const userAuthStore = useUserAuthStore()
const formErrorMessage = ref('')
const formSuccessMessage = ref('')
const departmentName:any = ref(null)
const firstName:any = ref(null)
const subjects: any = ref(null)
const lastName:any = ref(null)
const staffId:any = ref(null)
const gender:any = ref(null)
const getFileLoading = ref(false)
const dob:any = ref(null)
const selectGender:any = ref(['MALE', 'FEMALE'])
const loading:any = ref(false)
const fileToUpload: any = ref(null)


const clearMessage = ()=>{
    setTimeout(()=>{
        formSuccessMessage.value = ''
        formErrorMessage.value = ''
    }, 5000)
}

// Generate an excel file
const generateFile = async()=>{
    getFileLoading.value = true
    formErrorMessage.value = ''
    formSuccessMessage.value = ''
    const formData = new FormData()
    formData.append('departmentName', departmentName.value)
    formData.append('type', 'get-staff-file')
    
    try{
        const response = await axiosInstance.post('sch-admin/staff', formData)
        if (response.status === 200){
            formSuccessMessage.value = 'File generated successfully. Wait for it to be downloaded'
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

// File upload
const uploadFile = async()=>{
    loading.value = true
    formErrorMessage.value = ''
    formSuccessMessage.value = ''
    
    const formData = new FormData();
    formData.append('departmentName', departmentName.value);
    formData.append('file', fileToUpload.value)
    formData.append('type', 'upload-staff-file')

    try{
        const response = await axiosInstance.post('sch-admin/staff', formData)
        if (response.status === 200){
            const data = response.data['data']
            const department = userAuthStore.adminStaff.departments.find(department_item => department_item['name']===data['name'])
            if (department){
                const department_index = userAuthStore.adminStaff.departments.indexOf(department)
                userAuthStore.adminStaff.departments[department_index] = data
            }
            formSuccessMessage.value = response.data.ms
        }
        else if (response.status === 201){
            formErrorMessage.value = response.data.ms
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

// Input upload
const inputUpload = async()=>{
    loading.value = true
    formErrorMessage.value = ''
    formSuccessMessage.value = ''

    const formData = new FormData()
    formData.append('departmentName', departmentName.value)
    formData.append('firstName', firstName.value)
    formData.append('lastName', lastName.value)
    formData.append('staffId', staffId.value)
    formData.append('gender', gender.value)
    formData.append('subjects', subjects.value)
    formData.append('dob', dob.value)
    formData.append('type', 'input-staff')

    try {
        const response = await axiosInstance.post('sch-admin/staff', formData)
        if (response.status === 200){
            const data = response.data
            const department = userAuthStore.adminStaff.departments.find(item =>item['name']===data['department_name'])
            if (department){
                const department_index = userAuthStore.adminStaff.departments.indexOf(department)
                userAuthStore.adminStaff.departments[department_index]['teachers'].unshift(data['staff'])
            }
            firstName.value = null
            lastName.value = null
            staffId.value = null
            subjects.value = null
            dob.value = null
            formSuccessMessage.value = response.data['ms']
        }
        else if (response.status === 201){
            formErrorMessage.value = response.data['ms']
        }
    }
    catch{
        formErrorMessage.value = 'Oops something went wrong, check you internet connection'
    }
    finally{
        loading.value = false
    }

    
    clearMessage()
}

const checkInput = computed(()=>{
    return  !(
    departmentName.value &&
    subjects.value &&
    firstName.value &&
    lastName.value &&
    staffId.value &&
    gender.value &&
    dob.value
    )
})


const closeOverlay = (element: string)=>{
    const overlay = document.getElementById(element)
    if (overlay){
        formErrorMessage.value = ''
        formSuccessMessage.value = ''
        departmentName.value = null
        subjects.value = ''
        loading.value = false
        fileToUpload.value = null
        overlay.style.display = 'none'

    }
}

const showForm = (element: any)=>{
    const formOverlay = document.getElementById(element)
    formOverlay ? formOverlay.style.display = 'flex' : null
}


</script>

<template>
    <div id="staffInputForm" class="overlay">
        <div class="form" style="position: relative">
            <button @click="closeOverlay('staffInputForm')" class="close-btn flex-all">X</button>
            <h2 v-if="formSuccessMessage" class="form-message" style="color: green">{{formSuccessMessage}}</h2>
            <h2 v-if="formErrorMessage" class="form-message" style="color: red">{{formErrorMessage}}</h2>
            
            <div class="input-container">
            <div class="wrap one">
            <div class="wrap-1 department">
                <v-select v-if="userAuthStore.adminStaff.departmentNames" :disabled="loading" v-model="departmentName" class="select" label="DEPARTMENT" density="compact" variant="outlined" 
                :items="userAuthStore.adminStaff.departmentNames" persistent-hint hint="Select the department the teacher belongs to">
                </v-select>
                <v-select v-if="userAuthStore.adminStaff.subjects" multiple :disabled="loading" chips v-model="subjects" class="select" label="SUBJECTS(S)" density="compact" variant="outlined" 
                :items="userAuthStore.adminStaff.subjects" persistent-hint hint="Select the subject(s) the teacher teaches">
                </v-select>
            </div>
            </div>
            <div class="wrap">
                <v-text-field :disabled="loading" v-model="firstName" clearable class="input-field" label="FIRST NAME" variant="underlined"/>
                <v-text-field :disabled="loading" v-model="lastName" clearable class="input-field" label="LAST NAME" variant="underlined"/>
            </div>
            <div class="wrap-1">
                <v-select :disabled="loading" v-model="gender" class="select" label="GENDER" density="compact" variant="outlined" 
                :items="selectGender">
                </v-select>
            </div>
            <div class="ml-16">
                <v-text-field :disabled="loading" v-model="staffId" type="number" clearable class="input-field" label="STAFF ID" variant="underlined"/>
            </div>
            <div>
            <v-text-field :disabled="loading" v-model="dob" type="date" class="input-field" label="DATE OF BIRTH" variant="underlined"/>
        </div>
            
        </div>
            <v-btn :loading="loading" :disabled="checkInput" @click="inputUpload" class="submit-btn">SUBMIT</v-btn>
        </div>
    </div>

    <!-- File upload form -->
    <div id="staffFileForm" class="overlay">
        <div class="form" style="position: relative">
            <button @click="closeOverlay('staffFileForm')" class="close-btn flex-all">X</button>
            <h2 v-if="formSuccessMessage" class="form-message" style="color: green">{{formSuccessMessage}}</h2>
            <h2 v-if="formErrorMessage" class="form-message" style="color: red">{{formErrorMessage}}</h2>

            <v-select  v-if="userAuthStore.adminStaff.departmentNames" :disabled="loading" v-model="departmentName" class="select file" label="DEPARTMENT" variant="outlined" density="compact"
            :items="userAuthStore.adminStaff.departmentNames" persistent-hint hint="select the department the teacher belongs to">
            </v-select>

            <div class="flex-all-c mt-16">
                <v-btn :loading="getFileLoading" :disabled="loading || !departmentName" @click="generateFile" class="submit-btn">GET FILE</v-btn>
                <p class="hint mt-0">Click to get an excel file based on the selected department</p>
            </div>

            <hr class="line">

            <v-file-input :disabled="loading" @change="fileChange"  clearable  show-size class="file-field" label="upload an excel file" density="compact"
            variant="outlined" accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet">
            </v-file-input>
            <v-btn :loading="loading" :disabled="!fileToUpload || !departmentName" @click="uploadFile" class="submit-btn">UPLOAD</v-btn>
        </div>
    </div>


    <div class="w-100 h-100">
        <div class="flex-all w-100 h-100">
            <v-btn size="small" class="btn mr-5" @click="showForm('staffInputForm')">INPUT DATA</v-btn>
            <v-btn size="small" class="btn ml-5" @click="showForm('staffFileForm')">USE FILE</v-btn>
        </div>
    </div>
</template>

<style scoped>

@import url('../assets/css/tables.css');

.input-container{
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: center !important;
    width: 100%;
    height: 90%;
    overflow: auto;
}

.wrap{
    display: flex;
    width: 100%;
    flex-direction: column;
    align-items: center;
    justify-content: space-evenly;
}

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

.hint{
    font-size: .7rem;
}

.btn{
    background-color: lightseagreen;
    color: white;
    font-size: .5rem;
    font-weight: bold;
    margin-bottom: 6em;
}
.btn:hover{
    background-color: mediumseagreen;
}
#staffInputForm .form, #staffFileForm .form{
    background-color: white;
    border-radius: .3em;
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 90%;
    width: 90%;
    max-width: 900px;
}

#staffFileForm .form{
    height: 400px !important;
    max-width: 500px;
}
#staffFileForm .select{
    height: 0px;
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

.info{
    font-size: .8rem;
    color: red;
}
.form-message{
    font-size: .8rem;
    margin: 1em 3em;
    text-align: center;
}

.select{
    font-weight: bold;
    margin-top: 2em;
    color: black;
    width: 200px !important;
}

.input-field{
    color: black;
    font-weight: bold;
    margin-top: 1em;
    font-size: .7rem;
    width: 300px;
    font-family:monospace;
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
    .hint{
        font-size: .8rem;
    }
}

@media screen and (min-width: 767px) {

    .input-field{
        margin-left: 5em;
        margin-right: 5em;
    }
    .wrap{
        flex-direction: row;
    }
    .select{
        margin-right: 5em;
        margin-left: 5em;
    }
    .btn{
        font-size: .6rem;
    }
    .wrap-1{
        width: 50%;
    }
}


</style>
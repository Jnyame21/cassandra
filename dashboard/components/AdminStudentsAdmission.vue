<script setup lang="ts">
import axiosInstance from '../utils/axiosInstance';
import { ref, computed } from 'vue';

const userAuthStore = useUserAuthStore()
const formErrorMessage = ref('')
const formSuccessMessage = ref('')
const className:any = ref(null)
const firstName:any = ref(null)
const lastName:any = ref(null)
const gender:any = ref(null)
const getFileLoading = ref(false)
const studentId:any = ref(null)
const dob:any = ref(null)
const selectGender:any = ref(['MALE', 'FEMALE'])
const loading:any = ref(false)
const fileToUpload: any = ref(null)


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
    const formData = new FormData()
    formData.append('className', className.value)
    formData.append('type', 'get-students-file')
    
    try{
        const response = await axiosInstance.post('sch-admin/students', formData)
        if (response.status === 200){
            formSuccessMessage.value = 'File generated successfully. wait for it to be downloaded'
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
    formData.append('className', className.value);
    formData.append('file', fileToUpload.value)
    formData.append('year', userAuthStore.activeAcademicYear)
    formData.append('type', 'upload-students-file')

    try{
        const response = await axiosInstance.post('sch-admin/students', formData)
        if (response.status === 200){
            const year = response.data['year']
            const data = response.data['data']
            const clas = userAuthStore.adminClasses[year].find(clas_item => clas_item['name']===data['name'])
            if (clas){
                const clas_index = userAuthStore.adminClasses[year].indexOf(clas)
                userAuthStore.adminClasses[year][clas_index] = data
            }
            else {
                userAuthStore.adminClasses[year].push(data)
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
    formData.append('className', className.value.trim())
    formData.append('firstName', firstName.value.trim())
    formData.append('year', userAuthStore.activeAcademicYear)
    formData.append('lastName', lastName.value.trim())
    formData.append('gender', gender.value)
    formData.append('dob', dob.value)
    formData.append('type', 'input-student')
    formData.append('studentId', studentId.value)

    try {
        const response = await axiosInstance.post('sch-admin/students', formData)
        if (response.status === 200){
            const year = response.data['year']
            const clas = userAuthStore.adminClasses[year].find(item =>item['name']===response.data['class_name'])
            if (clas){
                const clas_index = userAuthStore.adminClasses[year].indexOf(clas)
                userAuthStore.adminClasses[year][clas_index]['students'].push(response.data['student'])
            }
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
    className.value &&
    firstName.value &&
    lastName.value &&
    gender.value &&
    dob.value
    )
})


const closeOverlay = (element: string)=>{
    const overlay = document.getElementById(element)
    if (overlay){
        formErrorMessage.value = ''
        formSuccessMessage.value = ''
        className.value = ''
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
    <div id="inputForm" class="overlay">
        <div class="form" style="position: relative">
            <v-btn @click="closeOverlay('inputForm')" :disabled="loading || getFileLoading" color="red" size="small" class="close-btn flex-all">X</v-btn>
            <h2 v-if="formSuccessMessage" class="form-message" style="color: green">{{formSuccessMessage}}</h2>
            <h2 v-if="formErrorMessage" class="form-message" style="color: red">{{formErrorMessage}}</h2>
            
            <div class="input-container">
                <v-select v-if="userAuthStore.adminClasses.names" :disabled="loading" v-model="className" class="select" label="CLASS" density="compact" variant="outlined" 
                :items="userAuthStore.adminClasses.names" persistent-hint hint="Select the students's class">
                </v-select>
                <v-text-field :disabled="loading" v-model="firstName" clearable class="input-field" label="FIRST NAME" variant="underlined"/>
                <v-text-field :disabled="loading" v-model="lastName" clearable class="input-field" label="LAST NAME" variant="underlined"/>
                <v-text-field :disabled="loading" v-model="studentId" clearable class="input-field" label="STUDENT ID" variant="underlined"/>
                <v-select :disabled="loading" v-model="gender" class="select" label="GENDER" density="compact" variant="outlined" 
                :items="selectGender">
                </v-select>
                <v-text-field :disabled="loading" v-model="dob" type="date" class="input-field" label="DATE OF BIRTH" variant="underlined"/>
            <div>
        </div>
        </div>
            <v-btn :loading="loading" :disabled="checkInput" @click="inputUpload" class="submit-btn">SUBMIT</v-btn>
        </div>
    </div>

    <!-- File upload form -->
    <div id="fileForm" class="overlay">
        <div class="form" style="position: relative">
            <v-btn @click="closeOverlay('fileForm')" :disabled="loading || getFileLoading" color="red" size="small" class="close-btn flex-all">X</v-btn>
            <h2 v-if="formSuccessMessage" class="form-message" style="color: green">{{formSuccessMessage}}</h2>
            <h2 v-if="formErrorMessage" class="form-message" style="color: red">{{formErrorMessage}}</h2>

            <v-select  v-if="userAuthStore.adminClasses.names" :disabled="loading" v-model="className" class="select file" label="CLASS" variant="outlined" density="compact"
            :items="userAuthStore.adminClasses.names" persistent-hint hint="select the students class">
            </v-select>

            <div class="flex-all-c mt-16">
                <v-btn :loading="getFileLoading" :disabled="loading || !className" @click="generateFile" class="submit-btn">GET FILE</v-btn>
                <p class="hint mt-0">Click to get an excel file based on the selected class</p>
            </div>

            <hr class="line">

            <v-file-input :disabled="loading" @change="fileChange" clearable show-size class="file-field" label="upload an excel file" density="compact"
            variant="outlined" accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet">
            </v-file-input>
            <v-btn :loading="loading" :disabled="!fileToUpload || !className" @click="uploadFile" class="submit-btn">UPLOAD</v-btn>
        </div>
    </div>


    <div class="w-100 h-100">
        <div class="flex-all w-100 h-100">
            <v-btn size="small" class="btn mr-5" @click="showForm('inputForm')">INPUT DATA</v-btn>
            <v-btn size="small" class="btn ml-5" @click="showForm('fileForm')">USE FILE</v-btn>
        </div>
    </div>
</template>

<style scoped>

@import url('../assets/css/tables.css');

.input-container{
    display: flex;
    align-items: center;
    flex-direction: column;
    justify-content: flex-start;
    width: 100%;
    height: 90%;
    overflow: auto;
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
#inputForm .form, #fileForm .form{
    background-color: white;
    border-radius: .3em;
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 90%;
    width: 90%;
    max-width: 900px;
}

#inputForm .form{
    max-width: 500px;
}

#fileForm .form{
    height: 400px !important;
    max-width: 500px;
}
#fileForm .select{
    height: 0px;
}


.close-btn{
    position: absolute;
    right: 0;
    top: 0;
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
    border: 1px solid;
    padding: .1em 1em;
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
    width: 300px !important;
    max-width: 300px !important;
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



</style>
<script setup lang="ts">
import axiosInstance from '../utils/axiosInstance';
import { ref, computed, watch } from 'vue';
import { AxiosError } from 'axios';

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()
const studentsYear: any = ref(null)
const formErrorMessage = ref('')
const selectedStudents: any = ref([])
const score: any = ref(null)
const fileToUpload: any = ref(null)
const typeSelected:any = ref(null)
const uploadTypeSelected:any = ref(null)
const assessmentTitle:any = ref(null)
const subjectSelected:any = ref(null)
const assessmentTitleSelected:any = ref(null)
const currentAssessment:any = ref(null)
const currentExams:any = ref(null)
const assessmentPercentage:any = ref(null)
const assessmentTotalScore:any = ref(null)
const assessmentDescription:any = ref(null)
const assessmentComment:any = ref(null)
const assessmentDate:any = ref(null)
const timeOutId:any = ref(null)


interface props {
    subjects: string[],
    className: string,
    students: any[];
}
const { subjects, className, students } = defineProps<props>()

const clearMessage = ()=>{
    if (timeOutId.value){
        clearTimeout(timeOutId.value)
    }
    timeOutId.value = setTimeout(()=>{
        formErrorMessage.value = ''
    }, 15000)
}

const typeOptions = [
    {'option': 'ASSESSMENT', 'value': 'assessment'},
    {'option': 'EXAMS', 'value': 'exam'},
]

const uploadOptions = [
    {'option': 'INPUT DATA HERE', 'value': 'noFile'},
    {'option': 'USE AN EXCEL FILE', 'value': 'file'},
]

watch(()=>userAuthStore.teacherData.studentsWithoutAssessments, (newValue, oldValue)=>{
    if (newValue){
        const assessment = newValue.find(item => item['class_name'] === className)
        assessment ? currentAssessment.value = assessment['assignments'] : null
    }
}, {immediate: true})

watch(()=>userAuthStore.teacherData.studentsWithoutExams, (newValue, oldValue)=>{
    if (newValue){
        const exams = newValue.find(item => item['class_name'] === className)
        exams ? currentExams.value = exams['exams'] : null
    }
}, {immediate: true})

// Generate an excel file
const generateFile = async(generateStudents:any)=>{
    elementsStore.ShowLoadingOverlay()
    formErrorMessage.value = ''
    const formData = new FormData()
    formData.append('studentsYear', studentsYear.value)
    formData.append('studentsClassName', className)
    formData.append('subject', subjectSelected.value)
    formData.append('selectedStudents', JSON.stringify(generateStudents))
    formData.append('type', 'getFile')
    formData.append('year', userAuthStore.activeAcademicYear)
    formData.append('term', userAuthStore.activeTerm)
    
    try{
        if (typeSelected.value == 'exam'){
            const response = await axiosInstance.post('teacher/exams', formData)
            const link = document.createElement('a');
            link.href = response.data.file_path;
            link.download = response.data.filename
            elementsStore.HideLoadingOverlay()
            link.click()
        }
        else if (typeSelected.value == 'assessment'){
            assessmentTitleSelected.value === 'New' ? formData.append('new', 'yes') : formData.append('new', 'no')
            assessmentTitleSelected.value === 'New' ? formData.append('title', assessmentTitle.value) : formData.append('title', assessmentTitleSelected.value)
            const response = await axiosInstance.post('teacher/assessments', formData)
            const link = document.createElement('a');
            link.href = response.data.file_path;
            link.download = response.data.filename
            elementsStore.HideLoadingOverlay()
            link.click()
        }
    }
    catch (error){
        elementsStore.HideLoadingOverlay()
        if (error instanceof AxiosError){
            if(error.response){
                if (error.response.status === 400 && error.response.data.message){
                    elementsStore.ShowOverlay(error.response.data.message, 'red', null, null)
                }
                else{
                    elementsStore.ShowOverlay('Oops! something went wrong. Try again later', 'red', null, null)
                }
            }
            else if (!error.response && (error.code === 'ECONNABORTED' || !navigator.onLine)){
                elementsStore.ShowOverlay('A network error occurred! Please check you internet connection', 'red', null, null)
            }
            else{
                elementsStore.ShowOverlay('An unexpected error occurred!', 'red', null, null)
            }
        }
    }
}

const fileChange = (event: any)=>{
    const file = event.target.files[0]
    fileToUpload.value = file || null
}

const handleSelectionChange = (selectionType:string)=>{
    typeSelected.value === 'assessment' && uploadTypeSelected.value === 'noFile' && selectionType === 'subject' ? assessmentTitleSelected.value = null : null 
    typeSelected.value === 'exam' && uploadTypeSelected.value === 'noFile' ? selectedStudents.value = [] : null 
    typeSelected.value === 'assessment' && uploadTypeSelected.value === 'noFile' ? selectedStudents.value = [] : null 
}

const upload = async()=>{
    formErrorMessage.value = ''

    const formData = new FormData()
    formData.append('year', userAuthStore.activeAcademicYear)
    formData.append('term', userAuthStore.activeTerm)
    formData.append('studentsClassName', className)
    formData.append('subject', subjectSelected.value)
    if (uploadTypeSelected.value === 'file'){
            formData.append('file', fileToUpload.value)
            formData.append('type', 'uploadWithFile')
        }else if (uploadTypeSelected.value === 'noFile'){
            formData.append('selectedStudents', selectedStudents.value)
            formData.append('type', 'uploadWithoutFile')
            formData.append('score', score.value)
        }
    if (typeSelected.value === 'exam'){
        if (score.value > 100){
            formErrorMessage.value = 'The exams score cannot be greater than 100'
            clearMessage()
            return;
        }else if (score.value <0){
            formErrorMessage.value = 'The exams score cannot be negative'
            clearMessage()
            return;
        }

        elementsStore.ShowLoadingOverlay()
        try{
            const response = await axiosInstance.post('teacher/exams', formData)
            await userAuthStore.getTeacherStudentsExams()
            selectedStudents.value = null
            score.value = null
            fileToUpload.value = null
            elementsStore.HideLoadingOverlay()
            elementsStore.ShowOverlay(response.data.message, 'green', null, null)
        }
        catch (error){
            elementsStore.HideLoadingOverlay()
            if (error instanceof AxiosError){
                if(error.response){
                    if (error.response.status === 400 && error.response.data.message){
                        elementsStore.ShowOverlay(error.response.data.message, 'red', null, null)
                    }
                    else{
                        elementsStore.ShowOverlay('Oops! something went wrong. Try again later', 'red', null, null)
                    }
                }
                else if (!error.response && (error.code === 'ECONNABORTED' || !navigator.onLine)){
                    elementsStore.ShowOverlay('A network error occurred! Please check you internet connection', 'red', null, null)
                }
                else if (error.code === 'ERR_NETWORK' && navigator.onLine) {
                    elementsStore.ShowOverlay('The excel file was modified. Please re-select the file before uploading.', 'red', null, null)
                    fileToUpload.value = null 
                }
                else{
                    elementsStore.ShowOverlay('An unexpected error occurred!', 'red', null, null)
                }
            }
        }
    }
    else if (typeSelected.value === 'assessment'){
        if (assessmentComment.value.length > 100){
            formErrorMessage.value = "The title of the assessment must not exceed 100 characters"
            clearMessage()
            return;
        }
        formData.append('comment', assessmentComment.value)
        if (uploadTypeSelected.value === 'noFile'){
            if (score.value < 0){
                formErrorMessage.value = 'The assessment score cannot be negative'
                clearMessage()
                return;
            }else{
                if (assessmentTitleSelected.value === 'New'){
                    if (score.value > assessmentTotalScore.value){
                        formErrorMessage.value = 'The student(s) score cannot be greater than the total assessment score'
                        clearMessage()
                        return;
                    }
                }else {
                    const assessment = userAuthStore.teacherData.studentsWithAssessments.find(item => item['class_name'] === className)
                    if (assessment){
                        const assessmentSubject = assessment['assignments'].find(item => item['subject'] === subjectSelected.value)
                        if (assessmentSubject){
                            const _assessmentTitle = assessmentSubject['assessments'].find(item => item['title'] === assessmentTitleSelected.value)
                            if (_assessmentTitle && score.value > Number(_assessmentTitle['total_score'])){
                                formErrorMessage.value = 'The student(s) score cannot be greater than the total assessment score'
                                clearMessage()
                                return;
                            }
                        }
                    }
                }
            }
        }
        if (assessmentTitleSelected.value === 'New'){
            if (assessmentTitle.value.length > 100 || assessmentDescription.value.length > 150){
                if (assessmentTitle.value.length > 100){
                    formErrorMessage.value = "The title of the assessment must not exceed 100 characters"
                }else if (assessmentDescription.value.length > 150){
                    formErrorMessage.value = "The description of the assessment must not exceed 150 characters"
                }
                clearMessage()
                return;
            }
            formData.append('title', assessmentTitle.value)
            formData.append('new', 'yes')
            formData.append('description', assessmentDescription.value)
            formData.append('totalScore', assessmentTotalScore.value)
            formData.append('percentage', assessmentPercentage.value)
            formData.append('date', assessmentDate.value)
        }else{
            formData.append('new', 'no')
            formData.append('title', assessmentTitleSelected.value)
        }

        elementsStore.ShowLoadingOverlay()
        try{
            const response = await axiosInstance.post('teacher/assessments', formData)
            await userAuthStore.getTeacherStudentsAssessments()
            selectedStudents.value = null
            assessmentTitleSelected.value === 'New' ? assessmentTitleSelected.value = assessmentTitle.value : null
            score.value = null
            assessmentComment.value = ''
            fileToUpload.value = null
            elementsStore.HideLoadingOverlay()
            elementsStore.ShowOverlay(response.data.message, 'green', null, null)
        }
        catch(error){
            elementsStore.HideLoadingOverlay()
            if (error instanceof AxiosError){
                if(error.response){
                    if (error.response.status === 400 && error.response.data.message){
                        elementsStore.ShowOverlay(error.response.data.message, 'red', null, null)
                    }
                    else{
                        elementsStore.ShowOverlay('Oops! something went wrong. Try again later', 'red', null, null)
                    }
                }
                else if (!error.response && (error.code === 'ECONNABORTED' || !navigator.onLine)){
                    elementsStore.ShowOverlay('A network error occurred! Please check you internet connection', 'red', null, null)
                }
                else if (error.code === 'ERR_NETWORK' && navigator.onLine) {
                    elementsStore.ShowOverlay('The excel file was modified. Please re-select the file before uploading.', 'red', null, null)
                    fileToUpload.value = null 
                }
                else{
                    elementsStore.ShowOverlay('An unexpected error occurred!', 'red', null, null)
                }
            }
        }
    }
}

const isFormValid = computed(()=>{
    if (typeSelected.value === 'exam' && uploadTypeSelected.value === 'noFile'){
        return !(subjectSelected.value && selectedStudents.value?.length >0 && score.value);
    }
    else if (typeSelected.value === 'exam' && uploadTypeSelected.value === 'file'){
        return !(subjectSelected.value && fileToUpload.value);
    }
    else if (typeSelected.value === 'assessment' && uploadTypeSelected.value === 'noFile'){
        if (assessmentTitleSelected.value && assessmentTitleSelected.value !== 'New'){
            return !(subjectSelected.value && selectedStudents.value?.length >0 && score.value);
        }else if (typeSelected.value === 'assessment' && assessmentTitleSelected.value === 'New'){
            return !(subjectSelected.value && assessmentTitle.value && assessmentPercentage.value && assessmentTotalScore.value && assessmentDate.value &&  selectedStudents.value?.length >0 && score.value);
        }else{
            return true;
        }
    }
    else if (typeSelected.value === 'assessment' && uploadTypeSelected.value === 'file'){
        if (assessmentTitleSelected.value && assessmentTitleSelected.value !== 'New'){
            return !(subjectSelected.value && fileToUpload.value);
        }else if (assessmentTitleSelected.value && assessmentTitleSelected.value === 'New'){
            return !(subjectSelected.value && assessmentTitle.value && assessmentPercentage.value && assessmentDate.value && assessmentTotalScore.value && fileToUpload.value);
        }else{
        return true;
        }
    }else{
        return true;
    }
})

const closeOverlay = ()=>{
    selectedStudents.value = []
    score.value = null
    assessmentComment.value = ''
    assessmentTitleSelected.value = null
    subjectSelected.value = null
    formErrorMessage.value = ''
    assessmentDate.value = null
    fileToUpload.value = null
    const overlay = document.getElementById(`teacherStudentsResultsOverlay${className}`)
    overlay ? overlay.style.display = 'none' : null
}


</script>

<template>
    <div :id="`teacherStudentsResultsOverlay${className}`" class="overlay">
        <form class="form">
            <div class="h-5">
                <v-btn @click.prevent="closeOverlay()" color="red" variant="flat" size="small" class="close-btn flex-all">X</v-btn>
            </div>
            <div class="top-container">
                <h2 class="info mb-2"><strong>CLASS:</strong> {{className}}</h2>
                <h2 v-if="formErrorMessage" class="form-message" style="color: red">{{formErrorMessage}}</h2>
            </div>
            <div class="input-container">
                <v-select v-model="typeSelected" class="select" label="TYPE" @update:modelValue="handleSelectionChange('assessmentTitle')"
                :items="typeOptions" item-title="option" item-value="value" density="comfortable" persistent-hint hint="Select whether you want to upload students Assessments or Exams">
                </v-select>
                <v-select v-model="uploadTypeSelected" class="select" label="DATA" 
                :items="uploadOptions" item-title="option" item-value="value" density="comfortable" persistent-hint hint="Select whether you want to input the data here or use an excel file">
                </v-select>
                <v-select v-model="subjectSelected" class="select" label="SUBJECT" @update:modelValue="handleSelectionChange('subject')"
                :items="subjects" item-title="name" item-value="name" density="comfortable" persistent-hint hint="Select the subject">
                </v-select>
                
                <!-- assessment -->
                <div v-if="typeSelected === 'assessment' && uploadTypeSelected && subjectSelected">
                    <div v-for="(assess_subject, index) in currentAssessment" :key="index">
                        <v-select v-if="subjectSelected === assess_subject['subject'] " @update:modelValue="handleSelectionChange('assessmentTitle')" clearable v-model="assessmentTitleSelected" class="select" label="ASSESSMENT" 
                            :items="assess_subject['assessments']" item-title="title" item-value="title" density="comfortable" persistent-hint hint="Select the type of assessment">
                        </v-select>
                        <div v-for="(assess_title, ind) in assess_subject['assessments']" :key="ind">
                            <v-text-field v-if="subjectSelected === assess_subject['subject'] && assess_title['title'] === assessmentTitleSelected && assessmentTitleSelected === 'New' " v-model="assessmentTitle" class="input-field" density="comfortable" persistent-hint hint="Enter the title of the assessment" label="TITLE"/>
                            <v-text-field v-if="subjectSelected === assess_subject['subject'] && assess_title['title'] === assessmentTitleSelected && assessmentTitleSelected === 'New' " v-model="assessmentDate" class="input-field" type="date" density="comfortable" persistent-hint hint="Enter a date for the assessment" label="DATE"/>
                            <v-text-field v-if="subjectSelected === assess_subject['subject'] && assess_title['title'] === assessmentTitleSelected && assessmentTitleSelected === 'New' " type="number" v-model="assessmentTotalScore" class="input-field" density="comfortable" persistent-hint hint="Enter the total score of the assessment" label="TOTAL SCORE"/>
                            <v-text-field v-if="subjectSelected === assess_subject['subject'] && assess_title['title'] === assessmentTitleSelected && assessmentTitleSelected === 'New' " type="number" v-model="assessmentPercentage" class="input-field" density="comfortable" persistent-hint hint="Enter the percentage the assessment will constitute in the overall results" label="PERCENTAGE"/>
                            <v-text-field v-if="subjectSelected === assess_subject['subject'] && assess_title['title'] === assessmentTitleSelected && assessmentTitleSelected === 'New' " v-model="assessmentDescription" class="input-field" density="comfortable" persistent-hint hint="Enter a description for the assessment if any" label="DESCRIPTION(OPTIONAL)"/>

                            <v-select v-if="uploadTypeSelected ==='noFile' && subjectSelected === assess_subject['subject'] && assess_title['title'] === assessmentTitleSelected && assessmentTitleSelected !== 'New' " multiple clearable v-model="selectedStudents" chips class="select" label="STUDENT(S)" 
                            :items="assess_title['students']" item-title="name" item-value="st_id" density="comfortable" persistent-hint hint="Select the student(s) you want to upload assessment for">
                                <template v-slot:item="{ props, item }">
                                    <v-list-item v-bind="props" :subtitle="item.raw.st_id"></v-list-item>
                                </template>
                            </v-select>
                            <v-select v-if="uploadTypeSelected ==='noFile' && subjectSelected === assess_subject['subject'] && assess_title['title'] === assessmentTitleSelected && assessmentTitleSelected === 'New' " multiple clearable v-model="selectedStudents" chips class="select" label="STUDENT(S)" 
                            :items="students" item-title="name" item-value="st_id" density="comfortable" persistent-hint hint="Select the student(s) you want to upload assessment for">
                                <template v-slot:item="{ props, item }">
                                    <v-list-item v-bind="props" :subtitle="item.raw.st_id"></v-list-item>
                                </template>
                            </v-select>

                            <v-text-field v-if="uploadTypeSelected ==='noFile' && subjectSelected === assess_subject['subject'] && assess_title['title'] === assessmentTitleSelected" type="number" v-model="score" class="input-field" density="comfortable" persistent-hint hint="Enter the student(s) score" label="STUDENT(S) SCORE"/>
                            <v-text-field v-if="uploadTypeSelected ==='noFile' && subjectSelected === assess_subject['subject'] && assess_title['title'] === assessmentTitleSelected" v-model="assessmentComment" class="input-field" density="comfortable" persistent-hint hint="Comment on the student(s) score if any" label="COMMENT"/>
                            
                            <!-- by file -->
                            <div class="flex-all-c mt-5" v-if="uploadTypeSelected ==='file' && subjectSelected === assess_subject['subject'] && assess_title['title'] === assessmentTitleSelected && assessmentTitleSelected !== 'New'">
                                <v-btn @click.prevent="generateFile(assess_title['students'])" color="blue" variant="flat" class="submit-btn" size="small">GET FILE</v-btn>
                                <p>Click to get an excel file that contains the students data</p>
                            </div>
                            <div class="flex-all-c mt-5" v-if="uploadTypeSelected ==='file' && subjectSelected === assess_subject['subject'] && assess_title['title'] === assessmentTitleSelected && assessmentTitleSelected === 'New' && assessmentTitle ">
                                <v-btn @click.prevent="generateFile(students)" color="blue" variant="flat" class="submit-btn" size="small">GET FILE</v-btn>
                                <p>Click to get an excel file that contains the students names data</p>
                            </div>
                            <hr class="line" v-if="uploadTypeSelected ==='file' && subjectSelected === assess_subject['subject'] && assess_title['title'] === assessmentTitleSelected ">
                            <v-file-input v-if="uploadTypeSelected ==='file' && subjectSelected === assess_subject['subject'] && assess_title['title'] === assessmentTitleSelected " @change="fileChange"  if-size class="file-field" label="Choose an excel file" density="comfortable"
                            accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet">
                            </v-file-input>
                        </div>
                    </div>
                </div>
            
                <!-- exam -->
                <div v-if="typeSelected === 'exam' && uploadTypeSelected && subjectSelected">
                    <div v-for="(exam_subject, index) in currentExams" :key="index">
                        <v-select v-if="uploadTypeSelected ==='noFile' && subjectSelected === exam_subject['subject']" multiple clearable v-model="selectedStudents" chips class="select" label="STUDENT(S)" 
                        :items="exam_subject['students']" item-title="name" item-value="st_id" persistent-hint hint="Select the student(s) you want to upload exams for">
                            <template v-slot:item="{ props, item }">
                                <v-list-item v-bind="props" :subtitle="item.raw.st_id"></v-list-item>
                            </template>
                        </v-select>
                        <v-text-field v-if="uploadTypeSelected ==='noFile' && subjectSelected === exam_subject['subject']" type="number" v-model="score" class="input-field" persistent-hint hint="Enter the student(s) Exam score" label="EXAM SCORE"/>
                        
                        <!-- by file -->
                        <div class="flex-all-c mt-5" v-if="uploadTypeSelected ==='file' && subjectSelected === exam_subject['subject']">
                            <v-btn @click.prevent="generateFile(exam_subject['students'])" color="blue" variant="flat" class="submit-btn" size="small">GET FILE</v-btn>
                            <p>Click to get an excel file that contains the students data</p>
                        </div>
            
                        <hr class="line" v-if="uploadTypeSelected ==='file' && subjectSelected === exam_subject['subject']">
            
                        <v-file-input v-if="uploadTypeSelected ==='file' && subjectSelected === exam_subject['subject']" @change="fileChange"  show-size class="file-field" label="Choose an excel file" density="comfortable"
                        accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet">
                        </v-file-input>
                    </div>
                </div>
            </div>

            <div class="btn-container flex-all">
                <v-btn :disabled="isFormValid" @click.prevent="upload" :ripple="false" variant="flat" type="submit" color="green" size="small">SUBMIT</v-btn>
            </div>
        </form>
    </div>
</template>

<style scoped>

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
    display: flex;
}
.form{
    position: relative;
    background-color: white;
    padding: 0 1em;
    border-radius: .3em;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 90% !important;
    width: 95%;
    max-width: 800px;
}
.top-container{
    width: 100%;
    height: max-content;
    margin-bottom: .5em;
}
.input-container{
    overflow-y: auto;
    overflow-x: hidden;
    width: 100%;
    min-height: 50% !important;
    max-height: 80% !important;
}
.btn-container{
    min-height: 10% !important;
    max-height: 10% !important;
}
.close-btn{
    position: absolute;
    right: 0;
    top: 0;
}
.info{
    color: seagreen;
    font-size: .9rem;
    text-align: center;
    font-family: Verdana, Geneva, Tahoma, sans-serif;
}
.info strong{
    font-size: .8rem;
    color: black;
}
.select{
    font-weight: bold;
    color: black;
    min-width: 100px !important;
    max-width: 500px !important;
    margin: 0 auto;
    margin-bottom: 2em;
    text-align: center;
    overflow-y: auto;
}
.input-field{
    color: black;
    font-weight: bold;
    margin: 0 auto;
    margin-bottom: 2em;
    min-width: 100px !important;
    max-width: 500px !important;
    text-align: center;
    font-size: .7rem;
    font-family: Verdana, Geneva, Tahoma, sans-serif
}
.file-field{
    max-width: 250px;
    margin: 0 auto;
}
.upload-btn-container{
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    padding: 0;
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
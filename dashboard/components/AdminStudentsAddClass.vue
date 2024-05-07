<script setup lang="ts">
import axiosInstance from '../utils/axiosInstance';
import { ref, computed } from 'vue';

const userAuthStore = useUserAuthStore()
const completionDate = ref('')
const subjects = ref(null)
const program = ref('')
const studentsYear = ref(null)
const enrollmentDate = ref('')
const className = ref('')
const formErrorMessage = ref('')
const formSuccessMessage = ref('')
const loading = ref(false)


const clearMessage = ()=>{
    setTimeout(()=>{
        formSuccessMessage.value = ''
        formErrorMessage.value = ''
    }, 10000)
}

const createClass = async()=>{
    loading.value = true
    formErrorMessage.value = ''
    formSuccessMessage.value = ''

    if (studentsYear.value <0 || studentsYear.value > 3){
        formErrorMessage.value = 'The students year must be 1, 2 or 3'
        clearMessage()
        loading.value = false
        return;
    }

    const formData = new FormData
    formData.append('subjects', subjects.value)
    formData.append('program', program.value)
    formData.append('completionDate', completionDate.value)
    formData.append('year', userAuthStore.activeAcademicYear)
    formData.append('type', 'create-class')
    formData.append('className', className.value.trim())
    formData.append('enrollmentDate', enrollmentDate.value)
    formData.append('studentsYear', studentsYear.value)
    formData.append('term', userAuthStore.activeTerm.toString())

    try {
        const response = await axiosInstance.post("sch-admin/students", formData)
        if (response.status === 200){
            userAuthStore.adminClasses.names.unshift(response.data['class_name'])
            userAuthStore.adminClasses.yearOne.unshift(response.data['new_class'])
            formSuccessMessage.value = response.data.ms
            className.value = ''
        }
        else if (response.status === 201){
            formErrorMessage.value = response.data.ms
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
    return !(className.value && subjects.value && program.value && completionDate.value && enrollmentDate.value && studentsYear.value)
})



</script>

<template>
    <div class="flex-all w-100" style="overflow: hidden;">
        <TheLoader v-if="!userAuthStore.adminClasses.programs" />
        <form class="form" v-if="userAuthStore.adminClasses.programs">
            <p class="info">Use uppercase for class names. It will be converted to uppercase though</p>
            <h2 v-if="formSuccessMessage" class="form-message" style="color: green">{{formSuccessMessage}}</h2>
            <h2 v-if="formErrorMessage" class="form-message" style="color: red">{{formErrorMessage}}</h2>
            <div class="field-container">
            <v-text-field label="CLASS NAME" class="input-field class-name" v-model="className" density="compact" variant="outlined"
            persistent-hint hint="Enter the name of the class" placeholder="eg. SCIENCE or SCIENCE-1 or SCIENCE-1-A"
            />
            <v-text-field label="STUDENTS YEAR/FORM" clearable class="input-field mt-7 mb-5" type="number" v-model="studentsYear" density="compact" variant="outlined"
            persistent-hint hint="Enter the year/form of the students" placeholder="eg. 1"
            />
            <div class="select-container mt-5 w-100">
                <div class="select-wrap">
                    <v-select :disabled="loading" v-model="program" class="select" clearable label="PROGRAM" style="width: 100%; color: black; font-weight: bold" density="compact" variant="outlined" 
                    :items="userAuthStore.adminClasses.programs" persistent-hint hint="Select the program that students in this class are enrolled in">
                    </v-select>
                </div>
                <div class="select-wrap">
                    <v-select :disabled="loading" v-model="subjects" multiple clearable label="SUBJECTS" style="width: 100%; color: black; font-weight: bold" density="compact" variant="outlined" 
                    :items="userAuthStore.adminStaff.subjects" persistent-hint hint="Select the subjects students in this class will study">
                    <template v-slot:selection="{ item, index }">
                        <v-chip v-if="index < 1">
                          <span>{{ item.title }}</span>
                        </v-chip>
                        <span
                          v-if="index === 1"
                          class="text-grey text-caption align-self-center"
                        >
                          (+{{ subjects.length - 1 }} others)
                        </span>
                      </template>
                </v-select>
                </div>
            </div>
            <div class="select-container mt-5 w-100" >
                <v-text-field label="DATE ENROLLED" class="input-field" v-model="enrollmentDate"
                persistent-hint hint="The enrollment date of the students" density="compact" variant="outlined"
                type="date"
                />
            <v-text-field label="COMPLETION DATE" class="input-field mb-5" v-model="completionDate"
                persistent-hint hint="The expected completion date of the students" density="compact" variant="outlined"
                type="date"
                />
            </div>
            </div>
            <v-btn :loading="loading" :disabled="checkInput" @click.prevent="createClass" type="submit" class="submit-btn">SUBMIT</v-btn>
        </form>
    </div>

</template>

<style scoped>

.form{
    width: 90%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    max-width: 700px;
}

.field-container{
    overflow: auto;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    height: 45dvh;
    width: 100%;
    background-color: whitesmoke;
}
.info{
    font-size: .7rem;
    text-align: center;
    font-family: Verdana, Geneva, Tahoma, sans-serif;
    margin-bottom: 1em;
    color: red;
}

.class-name{
    max-height: 70px !important;
}

.info strong{
    font-size: .8rem;
    color: seagreen
}
.form-message{
    font-size: .8rem;
    margin-bottom: 1em;
    text-align: center;
    border: 1px solid;
    padding: .1em 1em;
}

.select-wrap{
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    width: 300px;
    margin-top: 1.5em;
}

.select-container{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.input-field{
    margin-top: 1.5em;
    width: 300px;
}

.submit-btn{
    background-color: lightseagreen;
    color: white;
    font-weight: bold;
    margin-top: 3em;
    margin-bottom: 1em;
}


@media screen and (min-width: 776px) {
    .form{
        margin-top: 0em;
    }
    .info{
        margin-top: 0 !important;
    }
    .class-name{
        margin-top: 1em !important;
    }
    .select-container{
        flex-direction: row;
        justify-content: space-around;
    }
    .select-wrap, .input-field{
        margin-top: 0;
    }
    .input-field{
        margin: 0 1.5em;
    }
}


</style>


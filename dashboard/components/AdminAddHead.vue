<script setup lang="ts">
import axiosInstance from '../utils/axiosInstance';
import { ref, computed } from 'vue';

const userAuthStore = useUserAuthStore()
const headId = ref(null)
const dob = ref('')
const lastName = ref('')
const firstName = ref('')
const selectedRole = ref('')
const role = ref([
    'HEAD MASTER/MISTRESS', 'ASST. HEAD MASTER/MISTRESS', 'HEAD OF ACADEMICS', 'ASST. HEAD OF ACADEMIC'
]
)
const selectedGender = ref('')
const gender = ref([
    'MALE', 'FEMALE'
])
const formErrorMessage = ref('')
const formSuccessMessage = ref('')
const loading = ref(false)


const clearMessage = ()=>{
    setTimeout(()=>{
        formSuccessMessage.value = ''
        formErrorMessage.value = ''
    }, 10000)
}

const createHead = async()=>{
    loading.value = true
    formErrorMessage.value = ''
    formSuccessMessage.value = ''

    const formData = new FormData
    formData.append('firstName', firstName.value.trim())
    formData.append('lastName', lastName.value.trim())
    formData.append('headId', headId.value)
    formData.append('year', userAuthStore.activeAcademicYear)
    formData.append('type', 'create-head')
    formData.append('dob', dob.value.trim())
    formData.append('role', selectedRole.value)
    formData.append('gender', selectedGender.value)
    formData.append('term', userAuthStore.activeTerm.toString())

    try {
        const response = await axiosInstance.post("sch-admin/head", formData)
        if (response.status === 200){
            userAuthStore.adminHeads.unshift(response.data)
            formSuccessMessage.value = `Head with ID ${headId.value} created successfully`
            firstName.value = ''
            lastName.value = ''
            headId.value = null
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
    return !(firstName.value && lastName.value && headId.value && selectedGender.value && dob.value && selectedRole.value)
})


</script>

<template>
    <div class="flex-all w-100" style="overflow: hidden;">
        <div class="form" >
            <h2 v-if="formSuccessMessage" class="form-message" style="color: green">{{formSuccessMessage}}</h2>
            <h2 v-if="formErrorMessage" class="form-message" style="color: red">{{formErrorMessage}}</h2>
            <div class="field-container">
            
            <div class="select-container w-100 first">
                <v-text-field label="FIRST NAME" class="input-field" v-model="firstName" density="compact" variant="outlined"
                />
                <v-text-field label="LAST NAME" class="input-field" v-model="lastName" density="compact" variant="outlined"
                />
            </div>
            <div class="select-container w-100" >
                <v-text-field label="STAFF ID" class="input-field" v-model="headId"
                density="compact" variant="outlined"
                type="number"
                />
                <v-select
                label="ROLE" :items="role" v-model="selectedRole"
                class="input-field" variant="outlined" density="compact"
                />
            
            </div>
            <div class="select-container w-100" >
                <v-select
                label="GENDER" :items="gender" v-model="selectedGender"
                class="input-field" variant="outlined" density="compact"
                />
                <v-text-field label="DATE OF BIRTH" class="input-field" v-model="dob"
                density="compact" variant="outlined" prepend-icon="mdi-calendar"
                type="date"
                />
            </div>
            
            </div>
            
            <v-btn :loading="loading" :disabled="checkInput" @click="createHead" type="submit" class="submit-btn">SUBMIT</v-btn>
        </div>
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
    height: 55dvh;
    width: 100%;
    background-color: whitesmoke;
}

.form-message{
    font-size: .8rem;
    margin-bottom: 1em;
    text-align: center;
    border: 1px solid;
    padding: .1em 1em;
}
.select-container{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.input-field{
    margin-top: 1.5em;
    width: 300px !important;
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

@media screen and (min-width: 776px) {
    .form{
        margin-top: 0em;
    }
    .info{
        margin-top: 0 !important;
    }
    .first{
        margin-top: 3em !important;
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


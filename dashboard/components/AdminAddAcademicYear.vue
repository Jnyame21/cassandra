<script setup lang="ts">
import axiosInstance from '../utils/axiosInstance';
import { ref, computed } from 'vue';

const userAuthStore = useUserAuthStore()
const yearName = ref('')
const startDate = ref('')
const endDate = ref('')
const term1EndDate = ref('')
const term2StartDate = ref('')
const term2EndDate = ref('')
const term3StartDate = ref('')
const term3EndDate = ref('')
const formErrorMessage = ref('')
const formSuccessMessage = ref('')
const loading = ref(false)


const clearMessage = ()=>{
    setTimeout(()=>{
        formSuccessMessage.value = ''
        formErrorMessage.value = ''
    }, 10000)
}

const createYear = async()=>{
    loading.value = true
    formErrorMessage.value = ''
    formSuccessMessage.value = ''

    const formData = new FormData
    formData.append('startDate', startDate.value)
    formData.append('endDate', endDate.value)
    formData.append('year', userAuthStore.activeAcademicYear)
    formData.append('type', 'create-year')
    formData.append('yearName', yearName.value.trim())
    formData.append('term1EndDate', term1EndDate.value)
    formData.append('term2StartDate', term2StartDate.value)
    formData.append('term2EndDate', term2EndDate.value)
    formData.append('term3StartDate', term3StartDate.value)
    formData.append('term3EndDate', term3EndDate.value)
    formData.append('term', userAuthStore.activeTerm.toString())

    try {
        const response = await axiosInstance.post("sch-admin/data", formData)
        if (response.status === 200){
            userAuthStore.adminStaff.academicYears.unshift(response.data['new_year'])
            await userAuthStore.getUserData()
            .then(secondResponse => {
                formSuccessMessage.value = response.data.ms
                yearName.value = ''
                return Promise.resolve()
            })
            .catch(e =>{
                return Promise.reject(e)
            })
            await userAuthStore.getAdminData()
            
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

const checkInput1 = computed(()=>{
    return !(yearName.value && startDate.value && endDate.value && term1EndDate.value && term2StartDate.value && term2EndDate.value)
})

const checkInput2 = computed(()=>{
    return !(yearName.value && startDate.value && endDate.value && term1EndDate.value && term2StartDate.value && term2EndDate.value && term3StartDate.value && term3EndDate.value)
})


</script>

<template>
    <div class="flex-all w-100" style="overflow: hidden">
        <form class="form">
            <p class="info">You cannot delete a particular academic year after creation, so ensure accurate data input.</p>
            <h2 v-if="formSuccessMessage" class="form-message" style="color: green">{{formSuccessMessage}}</h2>
            <h2 v-if="formErrorMessage" class="form-message" style="color: red">{{formErrorMessage}}</h2>
            <!-- semesters -->
            <div class="fields-container" v-if="userAuthStore.userData && userAuthStore.userData['school']['semesters']">
                <v-text-field label="YEAR NAME" clearable class="input-field year-name" v-model="yearName" density="compact" variant="outlined"
                persistent-hint hint="Enter the name of the academic year" placeholder="eg. 2023-2024"
                />
                <div class="select-container mt-5 w-100">
                    <v-text-field label="START DATE" clearable class="input-field" v-model="startDate"
                    persistent-hint hint="The date the academic year starts" density="compact" variant="outlined"
                    type="date"
                    />
                    <v-text-field label="EXPECTED END DATE" clearable class="input-field" v-model="endDate"
                    persistent-hint hint="The expected date the academic year ends" density="compact" variant="outlined"
                    type="date"
                    />
                </div>
                <p>FIRST SEMESTER</p>
                <div class="select-container w-100" >
                    <v-text-field label="EXPECTED END DATE" clearable class="input-field" v-model="term1EndDate"
                    persistent-hint hint="The expected date first semester ends" density="compact" variant="outlined"
                    type="date"
                    />
                </div>

                <p>SECOND SEMESTER</p>
                <div class="select-container w-100" >
                    <v-text-field label="START DATE" clearable class="input-field" v-model="term2StartDate"
                    persistent-hint hint="The date second semester starts" density="compact" variant="outlined"
                    type="date"
                    />
                    <v-text-field label="EXPECTED END DATE" clearable class="input-field" v-model="term2EndDate"
                    persistent-hint hint="The expected date second semester ends" density="compact" variant="outlined"
                    type="date"
                    />
                </div>
            </div>
            <v-btn v-if="userAuthStore.userData && userAuthStore.userData['school']['semesters']" :loading="loading" :disabled="checkInput1" @click.prevent="createYear" color="green" type="submit" class="submit-btn">SUBMIT</v-btn>

                <!-- trimesters -->
            <div class="fields-container" v-if="userAuthStore.userData && !userAuthStore.userData['school']['semesters']">
                <v-text-field label="YEAR NAME" clearable class="input-field year-name" v-model="yearName" density="compact" variant="outlined"
                persistent-hint hint="Enter the name of the academic year" placeholder="eg. 2023/2024"
                />
                <div class="select-container mt-5 w-100">
                    <v-text-field label="START DATE" clearable class="input-field" v-model="startDate"
                    persistent-hint hint="The date the academic year starts" density="compact" variant="outlined"
                    type="date"
                    />
                    <v-text-field label="EXPECTED END DATE" clearable class="input-field" v-model="endDate"
                    persistent-hint hint="The expected date the academic year ends" density="compact" variant="outlined"
                    type="date"
                    />
                </div>
                <p>FIRST TRIMESTER</p>
                <div class="select-container w-100" >
                    <v-text-field label="EXPECTED END DATE" clearable class="input-field" v-model="term1EndDate"
                    persistent-hint hint="The expected date first trimester ends" density="compact" variant="outlined"
                    type="date"
                    />
                </div>

                <p>SECOND TRIMESTER</p>
                <div class="select-container w-100" >
                    <v-text-field label="START DATE" clearable class="input-field" v-model="term2StartDate"
                    persistent-hint hint="The date second trimester starts" density="compact" variant="outlined"
                    type="date"
                    />
                    <v-text-field label="EXPECTED END DATE" clearable class="input-field" v-model="term2EndDate"
                    persistent-hint hint="The expected date second trimester ends" density="compact" variant="outlined"
                    type="date"
                    />
                </div>
                
                <p>THIRD TRIMESTER</p>
                <div class="select-container mb-5 w-100" >
                    <v-text-field label="START DATE" clearable class="input-field" v-model="term3StartDate"
                    persistent-hint hint="The date third trimester starts" density="compact" variant="outlined"
                    type="date"
                    />
                    <v-text-field label="EXPECTED END DATE" clearable class="input-field" v-model="term3EndDate"
                    persistent-hint hint="The expected date third trimester ends" density="compact" variant="outlined"
                    type="date"
                    />
                </div>
            </div>
            <v-btn v-if="userAuthStore.userData && !userAuthStore.userData['school']['semesters']" :loading="loading" :disabled="checkInput2" @click.prevent="createYear" color="green" type="submit" class="submit-btn">SUBMIT</v-btn>
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

.fields-container{
    overflow: auto;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    max-height: 45vh;
    max-height: 45dvh;
    width: 100%;
    background-color: whitesmoke;
}
.fields-container p{
    margin-top: 2em;
    font-family: Verdana, Geneva, Tahoma, sans-serif;
    font-size: .8rem;
    color: seagreen;
    font-weight: bold;
}
.info{
    font-size: .7rem;
    text-align: center;
    font-family: Verdana, Geneva, Tahoma, sans-serif;
    margin-bottom: 1em;
    color: red;
}

.year-name{
    height: 70px;
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

.select-container{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
}

.input-field{
    margin-top: 1.5em;
    max-width: 320px !important;
    max-height: 70px !important;
}

.submit-btn{
    margin-top: 2em;
    margin-bottom: 1em;
}

@media screen and (min-width: 776px) {
    .form{
        margin-top: 0em;
    }
    .fields-container p{
        margin-top: 3em;
        margin-bottom: 1.5em;
    }
    .info{
        margin-top: 0 !important;
    }
    .year-name{
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


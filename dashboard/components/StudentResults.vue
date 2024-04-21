<script setup lang="ts">
import {ref, computed} from "vue";
import axiosInstance from "../utils/axiosInstance";


const userAuthStore = useUserAuthStore()
const sectionPage = ref(userAuthStore.activeTerm)
const loading = ref(false)
const selectedAcademicYear: any = ref(null)
const counter = ref(0)


const checkInput = computed(()=>{
    return !selectedAcademicYear.value
})

const changeYear = async ()=>{
    if (counter.value === 0){
        if (selectedAcademicYear.value && selectedAcademicYear.value !== userAuthStore.activeAcademicYear){
            loading.value = true
            const formData = new FormData
            formData.append('year', selectedAcademicYear.value)
            await axiosInstance.post('st/data', formData)
            .then(response =>{
                userAuthStore.studentData.results.termOne = response.data['term_one']
                userAuthStore.studentData.results.termTwo = response.data['term_two']
                userAuthStore.studentData.results.termThree = response.data['term_three']
                loading.value = false
                counter.value = 1
            })
            .catch(e =>{
                loading.value = false
                return Promise.reject()
            })
        }
    }
    else if (counter.value===1){
        loading.value = true
        const formData = new FormData
        formData.append('year', selectedAcademicYear.value)
        await axiosInstance.post('st/data', formData)
        .then(response =>{
            userAuthStore.studentData.results.termOne = response.data['term_one']
            userAuthStore.studentData.results.termTwo = response.data['term_two']
            userAuthStore.studentData.results.termThree = response.data['term_three']
            loading.value = false
            counter.value = 1
        })
        .catch(e =>{
            loading.value = false
            return Promise.reject()
        })
    }
}

</script>

<template>
  <div class="sections-container">
    <div class="section-nav-container" v-if="userAuthStore.userData && userAuthStore.userData['school']['semesters']">
      <div class="d-flex flex-column justify-center align-center" v-if="userAuthStore.studentData.results.academicYears">
        <v-select :label="(userAuthStore.userData['current_yr']==='COMPLETED' || userAuthStore.userData['current_yr']=== 4) ? userAuthStore.studentData.results.academicYears[0].name : userAuthStore.activeAcademicYear" v-model="selectedAcademicYear" clearable 
        :items="userAuthStore.studentData.results.academicYears" class="select" density="compact" variant="outlined"
        item-title="name" item-value="name" :disabled="loading"
        />
        <v-btn @click="changeYear" :disabled="checkInput" :loading="loading" class="year-btn" size="small">CHANGE</v-btn>
      </div>
      
    </div>
      
    <div class="sections">
      <div :style="sectionPage===1 ? {'display': 'flex'}: {'display': 'none'}">
        <StudentTermResults />
      </div>
    </div>
  </div>
</template>

<style scoped>

.select{
    width: 250px;
    color: black !important;
    height: 40px;
}

.year-btn{
    background-color: seagreen;
    color: white;
    font-size: .6rem;
    font-weight: bold;
}

.year-btn:hover{
    background-color: mediumseagreen;
    color: yellow;
}

.section-nav-container{
  height: 30% !important;
}

.sections{
  height: 70% m !important;
}




</style>
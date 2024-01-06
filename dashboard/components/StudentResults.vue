<script setup lang="ts">
import {ref, computed} from "vue";
import axiosInstance from "../utils/axiosInstance";




const userAuthStore = useUserAuthStore()
const sectionPage = ref(userAuthStore.activeTerm)
const loading = ref(false)
const selectedAcademicYear: any = ref(null)
const counter = ref(0)


const changeTerm = (term: number)=>{
  sectionPage.value = term
}

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
    <div class="section-nav-container">
      <div class="d-flex flex-column justify-center align-center mt-7" v-if="userAuthStore.studentData.results.academicYears">
        <v-select :label="(userAuthStore.userData['current_yr']==='Graduated' || userAuthStore.userData['current_yr']=== 4) ? userAuthStore.studentData.results.academicYears[0].name : userAuthStore.activeAcademicYear" v-model="selectedAcademicYear" clearable 
        :items="userAuthStore.studentData.results.academicYears" class="select" density="compact" variant="outlined"
        item-title="name" item-value="name" :disabled="loading"
        />
        <v-btn @click="changeYear" :disabled="checkInput" :loading="loading" class="year-btn" size="x-small">CHANGE</v-btn>
      </div>
      <button class="nav-btn-1" @click="changeTerm(1)" :class="{'nav-btn-1-active': sectionPage===1}">SEMESTER 1</button>
      <button class="nav-btn-1" @click="changeTerm(2)" :class="{'nav-btn-1-active': sectionPage===2}">SEMESTER 2</button>
      <button v-if="userAuthStore.userData && userAuthStore.userData['academic_year']['sem_3_start_date']" class="nav-btn-1" @click="changeTerm(3)" :class="{'nav-btn-1-active': sectionPage===3}">SEMESTER 3</button>
    </div>
  
    <div class="sections">
      <div :style="sectionPage===1 ? {'display': 'flex'}: {'display': 'none'}">
        <StudentTermResults :term="'termOne'" :term-number="1" />
      </div>
      <div :style="sectionPage===2 ? {'display': 'flex'}: {'display': 'none'}">
        <StudentTermResults :term="'termTwo'" :term-number="2" />
      </div>
      <div :style="sectionPage===3 ? {'display': 'flex'}: {'display': 'none'}"
      v-if="userAuthStore.userData && userAuthStore.userData['academic_year']['sem_3_start_date']"
      >
        <StudentTermResults :term="'termThree'" :term-number="3" />
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
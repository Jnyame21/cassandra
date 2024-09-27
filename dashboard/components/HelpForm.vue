<script setup lang="ts">
import {ref} from "vue";
import axiosInstance from "../utils/axiosInstance";

const message = ref('')
const problem = ref('')
const loading = ref(false)

const clearMessage = ()=>{
  setTimeout(()=>{
      message.value = ''
    },10000)
}
const submitProblem = async ()=>{
  if (problem.value.length <= 5){
    message.value = 'Your message length must be more than five(5) characters'
    clearMessage()
  }else {
    loading.value = true
    message.value = 'Please wait as your submission is being sent....'

    const formData = new FormData
    formData.append('problem', problem.value)

    await axiosInstance.post('support', formData)
        .then(response =>{
            message.value = 'Submission successful! Our team will work on it and notify you.'
            loading.value = false
            problem.value = ''
            clearMessage()
        })
        .catch(error =>{
          message.value = 'Something went wrong! check your internet connection and try again'
          loading.value = false
          clearMessage()
          console.log(error)
        })
  }
}


</script>

<template>
  <div class="flex-all-c h-100 w-100">
    <v-card class="help-card">
      <v-card-text style="font-size: .8rem; font-family: Verdana, 'sans-serif'" :style="{'color': message==='Submission successful! Our team will work on it and notify you.'? 'yellow' : 'red'}" class="text-center" v-if="message">{{message}}</v-card-text>
      <v-form @submit.prevent="submitProblem">
        <v-textarea :disabled="loading" v-model="problem" class="area" placeholder="Enter the problem you are facing"></v-textarea>
        <v-card-actions class="d-flex justify-center">
          <v-btn type="submit" :loading="loading" class="help-btn">SUBMIT</v-btn>
        </v-card-actions>
      </v-form>
    </v-card>
  </div>
</template>

<style scoped>

.help-card{
  width: 90%;
  max-width: 700px !important;
  background-color: #333333;
}

.help-btn{
  background-color: white;
}
.area{
  color: white;
  font-family: Verdana, "sans-serif";
  font-size: .8rem;
}




</style>
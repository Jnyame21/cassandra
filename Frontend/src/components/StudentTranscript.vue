
<script setup lang="ts">
import { ref } from 'vue'
import axiosInstance from '../utils/axiosInstance';


const loading = ref(false)
const successMessage = ref('')
const errorMessage = ref('')

const userAuthStore = useUserAuthStore()

const clearMessage = ()=>{
    setTimeout(()=>{
        successMessage.value = ''
        errorMessage.value = ''
    }, 10000)
}

const getTranscript = async()=>{
    successMessage.value = ''
    errorMessage.value = ''
    loading.value = true 
    try{
        const response = await axiosInstance.post('st/transcript')
        if (response.status === 200){
            const a = document.createElement('a')
            a.href = response.data
            a.download = `${userAuthStore.userData['first_name']}_${userAuthStore.userData['last_name']}_transcript.docx`
            a.click()
            successMessage.value = 'Your transcript has been generated successfully and will be downloaded'
        }
    }
    catch{
        errorMessage.value = 'Something went wrong! check you internet connect'
        return Promise.reject()
    }
    finally{
        loading.value = false
        clearMessage()
    }
}

</script>


<template>
<div class="w-100 h-100 flex-all-c">
    <p style="color: green" v-if="successMessage" class="message">{{successMessage}}</p>
    <p v-if="errorMessage" style="color: red" class="message">{{errorMessage}}</p>
    <v-btn :loading="loading" @click="getTranscript()" color="green">DOWNLOAD</v-btn>
</div>
</template>


<style scoped>

.btn-container{
    margin-top: 3em;
}
.message{
    font-size: .7rem !important;
    text-align: center;
}

@media screen and (min-width: 576px) {
    .message{
        font-size: .8rem !important;
    }
    .btn-container p{
        font-size: .8rem;
    }
}


</style>
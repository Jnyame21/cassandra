
<script setup lang="ts">
import { ref, onBeforeMount, watch, computed } from 'vue'
import axiosInstance from '../utils/axiosInstance';


const userAuthStore = useUserAuthStore()
const formErrorMessage = ref('')
const formSuccessMessage = ref('')
const selectedStaff: any = ref([])
const headStaff: any = ref([])
const hodStaff: any = ref([])
const loading = ref(false)
const message: any = ref(null)
const teachersIds: any = ref([])
const multiple: any = ref(false)


onBeforeMount(()=>{
    if (userAuthStore.userData && userAuthStore.userData['staff_role']==='hod'){
        watch(()=> userAuthStore.hodSubjectAssignmentUpload.staff, (newValue, oldValue)=>{
            if(newValue){
                newValue.forEach((item: any) =>{
                    if (item['stf_id'] != userAuthStore.userData['staff_id']){
                        const staff_item = hodStaff.value.find(c => c['stf_id']===item['stf_id'])
                        if (!staff_item){
                            hodStaff.value.push(item)
                            teachersIds.value.push(item['stf_id'])
                        }
                    }
                })
            }
        })
    }
    else if (userAuthStore.userData && userAuthStore.userData['role']==='head'){
        watch(()=> userAuthStore.headNotificationsStaff, (newValue, oldValue)=>{
            if(newValue){
                newValue.forEach((item: any) =>{
                    const staff_item = teachersIds.value.find(c => c['staff_id']===item['staff_id'])
                    if (!staff_item){
                        headStaff.value.push(item)
                        teachersIds.value.push(item['staff_id'])
                    }
                    
                })
            }
        })
    }
})

const clearMessage = ()=>{
    setTimeout(()=>{
        formSuccessMessage.value = ''
        formErrorMessage.value = ''
    }, 8000)
}

const checkInput = computed(()=>{
    return !(selectedStaff.value.length >0 && message.value)
})


const sendMessage = async()=>{
    loading.value = true
    formErrorMessage.value = ''
    formSuccessMessage.value = ''
    const formData = new FormData()
    formData.append('message', message.value)
    formData.append('staff_ids', JSON.stringify(selectedStaff.value))
    formData.append('type', 'send')
    
    await axiosInstance.post('staff/notification', formData)
    .then(response =>{
        userAuthStore.staffNotifications = response.data
        selectedStaff.value = []
        multiple.value = false
        message.value = ''
        formSuccessMessage.value = 'Notice sent successfully'
        loading.value = false
        clearMessage()
    })
    .catch(e =>{
        formErrorMessage.value = 'Something went wrong! Try again later'
        loading.value = false
        clearMessage()
    })
}

const toggle = (value: boolean)=>{
    multiple.value = value

    if (multiple.value){
        selectedStaff.value = teachersIds.value
    }
    else{
        selectedStaff.value = []
    }
}

const closeOverlay = ()=>{
    const overlay = document.getElementById('staffMessage')
    if (overlay){
        selectedStaff.value = []
        formErrorMessage.value = ''
        formSuccessMessage.value = ''
        loading.value = false
        overlay.style.display = 'none'
        message.value = null

    }
}

</script>

<template>
    <button @click.prevent="closeOverlay()" class="close-btn flex-all">X</button>
<div class="flex-all-c w-100">
    <form class="form">
      <h2 v-if="formSuccessMessage" class="form-message" style="color: green">{{formSuccessMessage}}</h2>
      <h2 v-if="formErrorMessage" class="form-message" style="color: red">{{formErrorMessage}}</h2>
      
      <!-- Hod Select -->
        <v-select :disabled="loading" multiple v-model="selectedStaff" density="compact" chips class="select" label="TEACHER(S)" variant="outlined" 
        v-if="userAuthStore.userData['staff_role'] ==='hod' && hodStaff"
        :items="hodStaff" item-title="name" item-value="stf_id" persistent-hint hint="Select the teacher or teachers you want to send the notice to">
        <template v-slot:item="{ props, item }">
            <v-list-item v-bind="props" :subtitle="item.raw.stf_id"></v-list-item>
        </template>
        
        </v-select>
        
        <!-- head Select -->
        <v-select :disabled="loading" multiple v-model="selectedStaff" density="compact" chips class="select" label="STAFF" variant="outlined" 
        v-if="userAuthStore.userData['role'] === 'head' && userAuthStore.headNotificationsStaff"
        :items="headStaff" item-title="name" item-value="staff_id" persistent-hint hint="Select the staff you want to send the notice to">
        <template v-slot:item="{ props, item }">
            <v-list-item v-bind="props" :subtitle="item.raw.staff_id"></v-list-item>
        </template>

        </v-select>
        <v-btn size="x-small" :disabled="loading" @click="toggle(true)" v-if="!multiple" class="select-all">Select All</v-btn>
        <v-btn size="x-small" :disabled="loading" @click="toggle(false)" v-if="multiple" class="select-all">Unselect All</v-btn>

      <v-textarea :disabled="loading" v-model="message" clearable class="input-field" label="Enter your message" variant="outlined"/>
      <v-btn density="compact" :disabled="checkInput" @click.prevent="sendMessage()" :loading="loading" type="submit" class="send-btn">SEND</v-btn>
    </form>
</div>
</template>
  
<style scoped>

.no-data{
    margin-top: 10em;
    margin-left: 5em;
    font-size: .8rem;
}
.form{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
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

.form-message{
    font-size: .7rem;
    margin-top: .5em;
    text-align: center;
    border: 1px solid;
    padding: .1em 1em;
}

.select{
    font-weight: bold;
    margin-top: 1em;
    color: black;
    min-width: 200px;
    margin-bottom: 1em;
    overflow-y: auto;
    max-height: 150px;
}

.select-all{
    font-size: .6rem;
    color: white;
    text-align: center;
    font-family: monospace;
    background-color: mediumseagreen;
    margin-bottom: 5em;
}
.select-all:hover{
    background-color: lightseagreen;
}

.input-field{
    color: black;
    font-weight: bold;
    height: 100px;
    font-size: .7rem;
    font-family:monospace;
    width: 70%;
}

.send-btn{
    background-color: lightseagreen !important;
    color: white;
    font-weight: bold;
    margin-top: 4em;
}

.send-btn:hover{
    background-color: mediumseagreen !important;
    color: yellow;
}



</style>
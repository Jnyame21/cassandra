<script setup lang="ts">
import { ref, computed } from 'vue'
import axiosInstance from '../utils/axiosInstance';


const userAuthStore = useUserAuthStore()
const formErrorMessage = ref('')
const formSuccessMessage = ref('')
const selectedStaff: any = ref([])
const selectedStudents = ref([])
const selectedClass: any = ref(null)
const typeSelected: any = ref(null)
const loading = ref(false)
const message: any = ref(null)
const multiple: any = ref(false)


const clearMessage = () => {
    setTimeout(() => {
        formSuccessMessage.value = ''
        formErrorMessage.value = ''
    }, 8000)
}

const checkInput = computed(() => {
    if (typeSelected.value === 'staff') {
        return !(selectedStaff.value.length > 0 && message.value)
    } else if (typeSelected.value === 'student') {
        return !(selectedStudents.value.length > 0 && message.value)
    } else {
        return true
    }
})

const typeOptions = ref([
    { 'label': 'STUDENT', 'value': 'student' },
    { 'label': 'STAFF', 'value': 'staff' },
])

const getClassStudents = async () => {
    const formData = new FormData()
    formData.append('className', selectedClass.value)
    formData.append('type', 'getClassStudents')

    await axiosInstance.post('notification', formData)
        .then(response => {
            userAuthStore.notificationStudents = response.data
            closeOverlay('getStudentsOverlay')
            return;
        })
        .catch(e => {
            closeOverlay('getStudentsOverlay')
            formErrorMessage.value = "Something went wrong! Couldn't fetch students in the selected class. Try again"
            loading.value = false
            clearMessage()
        })
}

const initGetClassStudents = ()=>{
    if (!selectedClass.value) {
        return;
    }
    const overlay = document.getElementById('getStudentsOverlay')
    overlay ? overlay.style.display = 'flex' : null
    formErrorMessage.value = ''
    formSuccessMessage.value = ''
    setTimeout(()=>{
        getClassStudents()
    }, 1000)
}


const sendNotice = async () => {
    loading.value = true
    formErrorMessage.value = ''
    formSuccessMessage.value = ''
    const formData = new FormData()
    formData.append('content', message.value)
    typeSelected.value === 'staff' ? formData.append('ids', JSON.stringify(selectedStaff.value)) : null
    typeSelected.value === 'student' ? formData.append('ids', JSON.stringify(selectedStudents.value)) : null
    formData.append('type', 'send')

    await axiosInstance.post('notification', formData)
        .then(response => {
            userAuthStore.getNotifications()
            selectedStaff.value = []
            selectedStudents.value = []
            multiple.value = false
            message.value = ''
            formSuccessMessage.value = 'Notice sent successfully'
            loading.value = false
            clearMessage()
        })
        .catch(e => {
            formErrorMessage.value = 'Something went wrong! Try again later'
            loading.value = false
            clearMessage()
        })
}


const toggle = (value: boolean) => {
    multiple.value = value
    if (typeSelected.value === 'student') {
        if (multiple.value) {
            userAuthStore.notificationStudents.forEach(item =>{
                if (!selectedStudents.value.includes(item['st_id'])){
                    selectedStudents.value.push(item['st_id'])
                }
            })
        } else {
            selectedStudents.value = []
        }
    } else if (typeSelected.value === 'staff') {
        if (multiple.value) {
            userAuthStore.notificationStaff.forEach(item =>{
                if (!selectedStaff.value.includes(item['staff_id'])){
                    selectedStaff.value.push(item['staff_id'])
                }
            })
        } else {
            selectedStaff.value = []
        }
    }
}

const closeOverlay = (element: string) => {
    const overlay = document.getElementById(element)
    if (element === 'Notification') {
        selectedStaff.value = []
        selectedStudents.value = []
        formErrorMessage.value = ''
        formSuccessMessage.value = ''
        loading.value = false
        message.value = null
    }
    overlay ? overlay.style.display = 'none' : null
}



</script>

<template>
    <div class="overlay" id="getStudentsOverlay">
        <v-progress-circular color="blue" indeterminate></v-progress-circular>
    </div>
    <v-btn @click.prevent="closeOverlay('Notification')" size="small" color="red" class="close-btn">X</v-btn>
    <div class="no-data flex-all-c" v-if="!userAuthStore.notifications">
        <TheLoader/>
    </div>
    <div class="flex-all-c w-100 form-container" v-if="userAuthStore.notifications">
        <div class="message-container">
            <h2 v-if="formSuccessMessage" class="form-message" style="color: green">{{ formSuccessMessage }}</h2>
            <h2 v-if="formErrorMessage" class="form-message" style="color: red">{{ formErrorMessage }}</h2>
        </div>
        <form class="form">
            <v-select :disabled="loading" v-model="typeSelected" density="compact" class="select" label="SEND TO"
                :items="typeOptions" item-title="label" item-value="value">
            </v-select>

            <!-- Students -->
            <v-select :disabled="loading"
                v-if="typeSelected === 'student' && userAuthStore.notificationStudentsClasses && userAuthStore.notificationStudentsClasses.length > 0"
                v-model="selectedClass" density="compact" class="select" label="CLASS"
                :items="userAuthStore.notificationStudentsClasses" item-title="label" item-value="value"
                hint="Select the student(s) class" persistent-hint>
                <template v-slot:item="{ props, item }">
                    <v-list-item @click="initGetClassStudents" v-bind="props" :subtitle="item.raw.value"></v-list-item>
                </template>
            </v-select>

            <v-select :disabled="loading"
                v-if="typeSelected === 'student' && selectedClass && userAuthStore.notificationStudents && userAuthStore.notificationStudents.length > 0"
                v-model="selectedStudents" multiple density="compact" clearable class="select" label="STUDENT(S)"
                :items="userAuthStore.notificationStudents" item-title="label" item-value="st_id"
                hint="Select the student(s) you want to send the message to" persistent-hint>
                <template v-slot:item="{ props, item }">
                    <v-list-item v-bind="props" :subtitle="item.raw.st_id"></v-list-item>
                </template>
            </v-select>

            <!-- staff -->
            <v-select :disabled="loading"
                v-if="typeSelected === 'staff' && userAuthStore.notificationStaff && userAuthStore.notificationStaff.length > 0"
                v-model="selectedStaff" multiple density="compact" clearable class="select" label="STAFF(S)"
                :items="userAuthStore.notificationStaff" item-title="label" item-value="staff_id"
                hint="Select the staff(s) you want to send the message to" persistent-hint>
                <template v-slot:item="{ props, item }">
                    <v-list-item v-bind="props" :subtitle="item.raw.staff_id"></v-list-item>
                </template>
            </v-select>

            <v-btn size="small" color="blue" :disabled="loading" @click="toggle(true)" v-if="!multiple && typeSelected === 'student' && selectedClass && userAuthStore.notificationStudents && userAuthStore.notificationStudents.length > 0 || !multiple && typeSelected === 'staff' && userAuthStore.notificationStaff && userAuthStore.notificationStaff.length > 0 " class="mb-10 mt-3">Select
                All</v-btn>
            <v-btn size="small" color="blue" :disabled="loading" @click="toggle(false)" v-if="multiple && typeSelected === 'student' && selectedClass && userAuthStore.notificationStudents && userAuthStore.notificationStudents.length > 0 || multiple && typeSelected === 'staff' && userAuthStore.notificationStaff && userAuthStore.notificationStaff.length > 0 " class="mb-10 mt-3">Deselect
                All</v-btn>

            <v-textarea :disabled="loading" v-model="message" clearable class="input-field" label="Enter your message" variant="outlined" />
            <v-btn density="compact" :disabled="checkInput" @click.prevent="sendNotice()" :loading="loading" type="submit" color="green" class="send-btn mb-10">SEND</v-btn>
        </form>
    </div>
</template>

<style scoped>
#getStudentsOverlay .overlay {
    z-index: 10;
}

.form-container {
    height: 90dvh !important;
    overflow: hidden !important;
}

.message-container{
    height: 5%;
}

.no-data {
    margin-top: 10em;
    margin-left: 5em;
    font-size: .8rem;
}

.form {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    width: 100%;
    height: 95%;
    overflow-y: auto;
}

.close-btn {
    position: absolute;
    right: 0;
    top: 0;
}

.form-message {
    font-size: .7rem;
    margin-top: .5em;
    text-align: center;
    border: 1px solid;
    padding: .1em 1em;
}

.select {
    font-weight: bold;
    color: black;
    min-width: 200px;
    margin-top: .5em;
    margin-bottom: 1em;
}

.input-field {
    color: black;
    font-weight: bold;
    font-size: .7rem;
    font-family: monospace;
    width: 80%;
}



</style>
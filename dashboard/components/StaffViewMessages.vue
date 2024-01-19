
<script setup lang="ts">
import { ref } from 'vue';
import axiosInstance from '../utils/axiosInstance';


const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()
const loading = ref(false)

const closeOverlay = ()=>{
    const overlay = document.getElementById('staffMessage')
    if (overlay){
        overlay.style.display = 'none'
    }
}

const deleteMessage = async(messageId: number)=>{
    loading.value = true
    const formData = new FormData()
    formData.append('id', messageId.toString())
    formData.append('type', 'delete')

    await axiosInstance.post('staff/notification', formData)
    .then(response =>{
        userAuthStore.staffNotifications = response.data
        loading.value = false
    })
    .catch(e =>{
        loading.value = false
        return Promise.reject()
    })
}

</script>

<template>
    <button @click.prevent="closeOverlay()" class="close-btn flex-all">X</button>
    <p class="no-data" v-if="!userAuthStore.staffNotifications">Something went wrong. check you internet connection</p>
    <p class="no-data" v-if="userAuthStore.staffNotifications && userAuthStore.staffNotifications.length ===0 ">You have no notifications</p>

        <!-- Teacher Notifications -->
<div class="w-100" v-if="userAuthStore.userData['staff_role']==='teacher' && userAuthStore.staffNotifications && userAuthStore.staffNotifications.length >0 
    || userAuthStore.userData['staff_role']==='admin' && userAuthStore.staffNotifications && userAuthStore.staffNotifications.length >0">
    <v-virtual-scroll height="75dvh" :items="userAuthStore.staffNotifications">
        <template v-slot:default="{ item }">
            <v-list-item v-if="item['sent_by_hod']">
                <div class="message-item">
                    <img class="sender-img" :src="item['sent_by_hod']['img']">
                    <v-card class="message-card" >
                        <v-card-title class="title" v-if="userAuthStore.userData['staff_role']==='teacher' ">
                        From: HOD [ {{item['sent_by_hod']['user']['first_name']}} {{item['sent_by_hod']['user']['last_name']}} ]
                        </v-card-title>
                        <v-card-text class="content">{{ item['content'] }}</v-card-text>
                        <v-card-subtitle class="date-time">{{item['date_time']}}</v-card-subtitle>
                    </v-card>
                </div>
              </v-list-item>
            <v-list-item v-if="item['sent_by_head']">
                <div class="message-item">
                    <img class="sender-img" :src="item['sent_by_head']['img']">
                    <v-card class="message-card" >
                        <v-card-title class="title">
                            From: {{ item['sent_by_head']['role'] }} [ {{item['sent_by_head']['user']['first_name']}} {{item['sent_by_head']['user']['last_name']}} ]
                        </v-card-title>
                        <v-card-text class="content">{{ item['content'] }}</v-card-text>
                        <v-card-subtitle class="date-time">{{item['date_time']}}</v-card-subtitle>
                    </v-card>
                </div>
              </v-list-item>
        </template>
    </v-virtual-scroll>
</div>

    <!-- Hod Notifications -->
<div class="w-100" v-if="userAuthStore.userData['staff_role']==='hod' && userAuthStore.staffNotifications && userAuthStore.staffNotifications.length >0 ">
    <v-virtual-scroll height="75dvh" :items="userAuthStore.staffNotifications">
        <template v-slot:default="{ item }">
            <v-list-item v-if="item['sent_by_hod']">
                <div class="message-item ml-5 w-100">
                    <v-card class="sent-message-card">
                        <v-card-title class="title">
                            To: {{ item['send_to'].length }} [
                                <div>
                                <span v-for="(staff, i) in item['send_to']" :key="i">
                                    ({{ staff['user']['first_name'] }} {{ staff['user']['last_name'] }})
                                </span>
                                </div>
                            ]
                        </v-card-title>
                        <v-card-text class="content">{{ item['content'] }}</v-card-text>
                        <v-card-subtitle class="date-time">{{item['date_time']}}</v-card-subtitle>
                        <v-card-actions>
                            <v-btn @click="deleteMessage(item['id'])" class="btn" size="x-small">DELETE</v-btn>
                        </v-card-actions>
                    </v-card>
                </div>
            </v-list-item>
            <v-list-item v-if="item['sent_by_head']">
                <div class="message-item">
                    <img class="sender-img" :src="elementsStore.getBaseUrl+item['sent_by_head']['img']">
                    <v-card class="message-card" >
                        <v-card-title class="title">
                            From: {{ item['sent_by_head']['role'] }} [ {{item['sent_by_head']['user']['first_name']}} {{item['sent_by_head']['user']['last_name']}} ]
                        </v-card-title>
                        <v-card-text class="content">{{ item['content'] }}</v-card-text>
                        <v-card-subtitle class="date-time">{{item['date_time']}}</v-card-subtitle>
                    </v-card>
                </div>
            </v-list-item>
        </template>
    </v-virtual-scroll>
</div>

    <!-- Head Notifications -->
<div class="w-100" v-if="userAuthStore.userData['role']==='head' && userAuthStore.staffNotifications && userAuthStore.staffNotifications.length >0 ">
    <v-virtual-scroll height="75dvh" :items="userAuthStore.staffNotifications">
        <template v-slot:default="{ item }">
            <v-list-item v-if="item['sent_by_head']">
                <div class="message-item ml-5 w-100">
                    <v-card class="sent-message-card">
                        <v-card-title class="title">
                            To: {{ item['send_to'].length }} [
                                <div>
                                <span v-for="(staff, i) in item['send_to']" :key="i">
                                    ({{ staff['user']['first_name'] }} {{ staff['user']['last_name'] }})
                                </span>
                                </div>
                            ]
                        </v-card-title>
                        <v-card-text class="content">{{ item['content'] }}</v-card-text>
                        <v-card-subtitle class="date-time">{{item['date_time']}}</v-card-subtitle>
                        <v-card-actions>
                            <v-btn @click="deleteMessage(item['id'])" class="btn" size="x-small">DELETE</v-btn>
                        </v-card-actions>
                    </v-card>
                </div>
            </v-list-item>
        </template>
    </v-virtual-scroll>
</div>
</template>


<style scoped>

.no-data{
    margin-top: 10em;
    font-size: .7rem;
    color: red;
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

.message-item{
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 2em;
}
.message-card, .sent-message-card{
    background-color: seagreen;
    width: 90%;
}

.sender-img{
    width: 30px;
    height: 30px;
    border-radius: 50%;
    margin-right: .5em;
}
.title{
    color: yellow;
    font-size: .8rem;
    font-family: Verdana, Geneva, Tahoma, sans-serif;
}
.title span{
    margin-right: .5em;
    font-size: .55rem;
}
.title div{
    display: flex;
    flex-wrap: wrap;
}
.content{
    color: white;
    font-size: .9rem;
}
.date-time{
    font-size: .6rem;
    color: yellow;
}
.btn{
    background-color: mediumseagreen;
    color: white;
    font-weight: bold;
}
.btn:hover{
    background-color: lightseagreen;
}



</style>
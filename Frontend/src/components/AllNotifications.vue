
<script setup lang="ts">
import { ref } from 'vue';
import axiosInstance from '../utils/axiosInstance';


const userAuthStore = useUserAuthStore()
const loading = ref(0)

const closeOverlay = ()=>{
    const overlay = document.getElementById('Notification')
    if (overlay){
        overlay.style.display = 'none'
    }
}

const deleteMessage = async(notificationId: number, item_index: number)=>{
    loading.value = item_index+1
    const formData = new FormData()
    formData.append('id', notificationId.toString())
    formData.append('type', 'delete')

    await axiosInstance.post('notification', formData)
    .then(response =>{
        userAuthStore.notifications = userAuthStore.notifications.filter(item => item['id'] !== notificationId)
        loading.value = 0
    })
    .catch(e =>{
        loading.value = 0
        return Promise.reject()
    })
}

</script>

<template>
    <v-btn @click.prevent="closeOverlay()" size="small" color="red" class="close-btn">X</v-btn>
    <p class="no-data" v-if="!userAuthStore.notifications">Something went wrong. check you internet connection</p>
    <p class="no-data" v-if="userAuthStore.notifications && userAuthStore.notifications.length ===0 ">You have no notifications</p>

    <div class="w-100" v-if="userAuthStore.notifications && userAuthStore.notifications.length >0 ">
        <v-virtual-scroll height="80dvh" :items="userAuthStore.notifications">
            <template v-slot:default="{ item }">

                <!-- Head Messages -->
                <v-list-item v-if="item['from_head']">
                    <template v-slot:prepend>
                        <img class="sender-img" :src="item['from_head']['img']">
                    </template>
                    <v-card class="message-card">
                        <v-card-title class="title">
                            From: {{item['from_head']['user']['first_name']}} {{item['from_head']['user']['last_name']}}[{{item['from_head']['role']}}]
                        </v-card-title>
                        <v-card-text class="content">{{ item['content'] }}</v-card-text>
                        <v-card-subtitle class="date-time">{{item['date_time']}}</v-card-subtitle>
                    </v-card>
                </v-list-item>
    
                <!-- Staff Messages -->
                <v-list-item v-if="item['from_staff']">
                    <template v-slot:prepend>
                        <img class="sender-img" :src="item['from_staff']['img']">
                    </template>
                    <v-card class="message-card">
                        <v-card-title  class="title">
                            From: {{item['from_staff']['user']['first_name']}} {{item['from_staff']['user']['last_name']}}[{{item['from_staff']['role']}}]
                        </v-card-title>
                        <v-card-text class="content">{{ item['content'] }}</v-card-text>
                        <v-card-subtitle class="date-time">{{item['date_time']}}</v-card-subtitle>
                    </v-card>
                </v-list-item>
                <v-list-item v-if="item['to_staff'] && item['to_staff'].length > 0">
                    <v-card class="message-card">
                        <v-card-title class="title">
                            To: {{item['to_staff'].length}}
                        </v-card-title>
                        <v-slide-group show-arrows>
                            <v-slide-group-item v-for="(staff, staff_index) in item['to_staff']" :key="staff_index">
                                <v-list-item class="title">
                                    <template v-slot:prepend>
                                        <img class="sender-img" :src="staff['img']">
                                    </template>
                                    {{staff['user']['first_name']}} {{staff['user']['last_name']}}
                                </v-list-item>
                            </v-slide-group-item>
                        </v-slide-group>
                        <v-card-text class="content">{{ item['content'] }}</v-card-text>
                        <v-card-subtitle class="date-time">{{item['date_time']}}</v-card-subtitle>
                        <v-card-actions>
                            <v-btn @click="deleteMessage(item['id'], userAuthStore.notifications.indexOf(item))" :loading="loading === userAuthStore.notifications.indexOf(item)+1" size="small" class="delete-btn">DELETE</v-btn>
                        </v-card-actions>
                    </v-card>
                </v-list-item>

                <!-- Student Messages -->
                <v-list-item v-if="item['from_student']">
                    <template v-slot:prepend>
                        <img class="sender-img" :src="item['from_student']['img']">
                    </template>
                    <v-card class="message-card">
                        <v-card-title class="title">
                            From: {{item['from_student']['user']['first_name']}} {{item['from_student']['user']['last_name']}}[student]
                        </v-card-title>
                        <v-card-text class="content">{{ item['content'] }}</v-card-text>
                        <v-card-subtitle class="date-time">{{item['date_time']}}</v-card-subtitle>
                    </v-card>
                </v-list-item>
                <v-list-item v-if="item['to_student'] && item['to_student'].length > 0">
                    <v-card class="message-card">
                        <v-card-title class="title">
                            To: {{item['to_student'].length}}
                        </v-card-title>
                        <v-slide-group show-arrows>
                            <v-slide-group-item v-for="(st, st_index) in item['to_student']" :key="st_index">
                                <v-list-item class="title">
                                    <template v-slot:prepend>
                                        <img class="sender-img" :src="st['img']">
                                    </template>
                                    {{st['user']['first_name']}} {{st['user']['last_name']}}
                                </v-list-item>
                            </v-slide-group-item>
                        </v-slide-group>
                        <v-card-text class="content">{{ item['content'] }}</v-card-text>
                        <v-card-subtitle class="date-time">{{item['date_time']}}</v-card-subtitle>
                        <v-card-actions>
                            <v-btn @click="deleteMessage(item['id'])" :loading="loading === userAuthStore.notifications.indexOf(item)+1" size="small" class="delete-btn">DELETE</v-btn>
                        </v-card-actions>
                    </v-card>
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

.message-card{
    margin-top: .5em;
    margin-bottom: 1em;
    background-color: seagreen;
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

.content{
    color: white;
    font-size: .9rem;
}

.date-time{
    font-size: .6rem;
    color: yellow;
}

.delete-btn{
    background-color: white;
}


</style>
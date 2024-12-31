<script setup lang="ts">
import { useUserAuthStore } from '@/stores/userAuthStore'
const userAuthStore = useUserAuthStore()


</script>

<template>
  <div class="flex-all-c school-info-container">
    <p class="name mb-4">{{ userAuthStore.userData['school']['name'] }} </p>
    <img class="img" :src="userAuthStore.userData['school']['logo']">
  </div>
</template>

<style scoped>

.school-info-container{
  width: 100%;
  padding: 10px;
  height: 190px;
}

.school-info-container .img{
  border-radius: 30%;
  width: 100px;
}

.school-info-container .name{
  font-size: .9rem;
  font-family: Verdana, Geneva, Tahoma, sans-serif;
  font-weight: bold;
  color: white;
  text-align: center;
}


</style>
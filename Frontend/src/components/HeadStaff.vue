<script setup lang="ts">
import { useUserAuthStore } from '@/stores/userAuthStore'
import { useElementsStore } from '@/stores/elementsStore'
import TheLoader from '@/components/TheLoader.vue'
import { computed } from 'vue'
const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()

const staff = computed(() => {
  return userAuthStore.headData.staff
})

const maleStaff = computed(() => {
  return staff.value?.filter(item => item.gender.toLocaleLowerCase() === 'male').length || 0
})

const femaleStaff = computed(() => {
  return staff.value?.filter(item => item.gender.toLocaleLowerCase() === 'female').length || 0
})


</script>

<template>
  <div class="content-wrapper" v-show="elementsStore.activePage === 'HeadStaff'" :class="{ 'is-active-page': elementsStore.activePage === 'HeadStaff' }">
    <TheLoader :func="userAuthStore.getHeadData" v-if="!staff"/>
    <div class="content-header info" v-if="staff">
      <div class="content-header-text">
        TOTAL NUMBER OF STAFF:
        <span class="content-header-text-value">
          {{ staff.length }}
        </span>
      </div>
      <div class="content-header-text">
        MALE STAFF:
        <span class="content-header-text-value">
          {{ maleStaff }} [{{ ((maleStaff / staff.length) * 100).toFixed(1) }}%]
        </span>
      </div>
      <div class="content-header-text">
        FEMALE STAFF:
        <span class="content-header-text-value">
          {{ femaleStaff }} [{{ ((femaleStaff / staff.length) * 100).toFixed(1) }}%]
        </span>
      </div>
    </div>
    <v-table fixed-header class="table" v-if="staff">
      <thead>
        <tr>
          <th class="table-head">NAME</th>
          <th class="table-head">ROLE</th>
          <th class="table-head">GENDER</th>
          <th class="table-head">SUBJECTS</th>
          <th class="table-head" v-if="userAuthStore.userData['school']['has_departments']">DEPARTMENT</th>
          <th class="table-head">CONTACT</th>
          <th class="table-head">ALT CONTACT</th>
          <th class="table-head">IMAGE</th>
          <th class="table-head">ADDRESS</th>
          <th class="table-head">EMAIL</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(_staff, index) in staff" :key="index">
          <td class="table-data">
            <v-btn class="mr-2" size="x-small" v-if="_staff['staff_id'] === userAuthStore.userData['staff_id']" color="black">YOU</v-btn>{{ _staff['user'] }}
            <v-list-item-subtitle>{{ _staff['staff_id'] }}</v-list-item-subtitle>
          </td>
          <td class="table-data">
            {{ _staff['role'] }}
          </td>
          <td class="table-data">
            {{ _staff['gender'] }}
          </td>
          <td class="table-data">
            <p v-for="(_subject, ind) in _staff['subjects']" :key="ind">{{ _subject }}</p>
          </td>
          <td class="table-data" v-if="userAuthStore.userData['school']['has_departments']">
            {{ _staff['department'] }}
          </td>
          <td class="table-data">
            {{ _staff['contact'] }}
          </td>
          <td class="table-data">
            {{ _staff['alt_contact'] }}
          </td>
          <td class="table-data">
            <img class="profile-img" :src="_staff['img']">
          </td>
          <td class="table-data">
            {{ _staff['address'] }}
          </td>
          <td class="table-data">
            {{ _staff['email'] }}
          </td>
        </tr>
      </tbody>
    </v-table>
  </div>
</template>

<style scoped>

.info {
  height: 25% !important;
}

@media screen and (min-width: 400px) {
  .info {
    height: 20% !important;
  }
  .content-header-text {
    font-size: .75rem !important;
  }
}

@media screen and (min-width: 576px) {
  .content-header-text {
    font-size: .8rem !important;
  }
}

@media screen and (min-width: 767px) {
  .content-header-text {
    font-size: .85rem !important;
  }
}

@media screen and (min-width: 1000px) {
  .content-header-text {
    font-size: .9rem !important;
  }
}

@media screen and (min-width: 1200px) {
  .content-header-text {
    font-size: 1rem !important;
  }
}


</style>
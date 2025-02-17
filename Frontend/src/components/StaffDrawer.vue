
<script setup lang="ts">
import { useUserAuthStore } from '@/stores/userAuthStore';
import { useElementsStore } from '@/stores/elementsStore';
import SchoolProfile from './SchoolProfile.vue';

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()

const drawer = document.getElementById('staffDrawer')
document.addEventListener('click', (event: MouseEvent)=>{
  if (drawer?.style.display !== 'none'){
    if (!drawer?.contains(event?.target as Node)){
      elementsStore.drawer = false
    }
  }
})


</script>


<template>
    <div id="staffDrawer" class="drawer-container" v-show="elementsStore.drawer">
      <v-list class="drawer-list">
        <SchoolProfile/>
        
        <v-card-title class="drawer-head">SCHOOL INFORMATION</v-card-title>
        <v-list-item class="drawer-item" prepend-icon="mdi-school-outline">
          <v-list-item-title class="drawer-title">
            SHORT NAME
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['school']['short_name'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item class="drawer-item" prepend-icon="mdi-code-tags">
          <v-list-item-title class="drawer-title">
            CODE 
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['school']['code'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item class="drawer-item" prepend-icon="mdi-home-map-marker">
          <v-list-item-title class="drawer-title">
            POSTAL ADDRESS 
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['school']['postal_address'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item class="drawer-item" prepend-icon="mdi-phone-outline">
          <v-list-item-title class="drawer-title">
            PHONE NUMBER 
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['school']['contact'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item class="drawer-item" prepend-icon="mdi-home-outline">
          <v-list-item-title class="drawer-title">
            ADDRESS 
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['school']['address'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item class="drawer-item" prepend-icon="mdi-email-outline">
          <v-list-item-title class="drawer-title">
            EMAIL 
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['school']['email'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-card-title class="drawer-head">STAFF INFORMATION</v-card-title>
        <v-list-item class="drawer-item" prepend-icon="mdi-account-circle-outline">
          <v-list-item-title class="drawer-title">
            USERNAME
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['username'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item class="drawer-item" v-if="userAuthStore.userData['school']['staff_id'] && userAuthStore.userData['staff_id']" prepend-icon="mdi-card-account-details-outline">
          <v-list-item-title class="drawer-title">
            STAFF ID
          </v-list-item-title>
          <v-list-item-subtitle v-if="userAuthStore.userData['role']==='staff'" class="drawer-subtitle">
            {{ userAuthStore.userData['staff_id'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item class="drawer-item" prepend-icon="mdi-account-outline">
          <v-list-item-title class="drawer-title">
            ROLE
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['staff_role'].toUpperCase() }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item class="drawer-item" prepend-icon="mdi-briefcase-clock-outline">
          <v-list-item-title class="drawer-title">
            DATE EMPLOYED
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['date_enrolled'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-card-title class="drawer-head">ACADEMIC CALENDAR</v-card-title>
        <v-list-item class="drawer-item" prepend-icon="mdi-calendar-outline">
          <v-list-item-title class="drawer-title">
            ACADEMIC YEAR START DATE
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['academic_year']['start_date'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item class="drawer-item" prepend-icon="mdi-calendar-outline">
          <v-list-item-title class="drawer-title">
            1st {{ userAuthStore.userData['academic_year']['period_division'] }} END DATE
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['academic_year']['term_1_end_date'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item class="drawer-item" prepend-icon="mdi-calendar-outline">
          <v-list-item-title class="drawer-title">
            2nd {{ userAuthStore.userData['academic_year']['period_division'] }} START DATE
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['academic_year']['term_2_start_date'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item class="drawer-item" prepend-icon="mdi-calendar-outline">
          <v-list-item-title class="drawer-title">
            2nd {{ userAuthStore.userData['academic_year']['period_division'] }} END DATE
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['academic_year']['term_2_end_date'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item class="drawer-item" v-if="userAuthStore.userData['academic_year']['no_of_divisions'] > 2 " prepend-icon="mdi-calendar-outline">
          <v-list-item-title class="drawer-title">
            3rd {{ userAuthStore.userData['academic_year']['period_division'] }} START DATE
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['academic_year']['term_3_start_date'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item class="drawer-item" v-if="userAuthStore.userData['academic_year']['no_of_divisions'] > 2 " prepend-icon="mdi-calendar-outline">
          <v-list-item-title class="drawer-title">
            3rd {{ userAuthStore.userData['academic_year']['period_division'] }} END DATE
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['academic_year']['term_3_end_date'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item class="drawer-item" prepend-icon="mdi-calendar-outline">
          <v-list-item-title class="drawer-title">
            ACADEMIC YEAR END DATE
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['academic_year']['end_date'] }}
          </v-list-item-subtitle>
        </v-list-item>
        
        <v-card-title class="drawer-head">PERSONAL INFORMATION</v-card-title>
        <v-list-item class="drawer-item" prepend-icon="mdi-badge-account">
          <v-list-item-title class="drawer-title">
            TITLE
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['title'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item class="drawer-item" prepend-icon="mdi-account-outline">
          <v-list-item-title class="drawer-title">
            FIRST NAME
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['first_name'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item class="drawer-item" prepend-icon="mdi-account-outline">
          <v-list-item-title class="drawer-title">
            LAST NAME
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['last_name'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item class="drawer-item" v-if="userAuthStore.userData['gender'].toLowerCase() === 'male'" prepend-icon="mdi-gender-male">
          <v-list-item-title class="drawer-title">
            GENDER
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['gender'] }}
          </v-list-item-subtitle>
        </v-list-item>
        <v-list-item class="drawer-item" v-if="userAuthStore.userData['gender'].toLowerCase() === 'female'" prepend-icon="mdi-gender-female">
          <v-list-item-title class="drawer-title">
            GENDER
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['gender'] }}
          </v-list-item-subtitle>
        </v-list-item>
        <v-list-item class="drawer-item" v-if="['other', 'none'].includes(userAuthStore.userData['gender'].toLowerCase())" prepend-icon="mdi-gender-male-female">
          <v-list-item-title class="drawer-title">
            GENDER
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['gender'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item class="drawer-item" prepend-icon="mdi-calendar-account">
          <v-list-item-title class="drawer-title">
            DATE OF BIRTH
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['dob'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item class="drawer-item" prepend-icon="mdi-hand-heart">
          <v-list-item-title class="drawer-title">
            RELIGION
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['religion'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item class="drawer-item" prepend-icon="mdi-phone-outline">
          <v-list-item-title class="drawer-title">
            PHONE NUMBER
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['contact'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item class="drawer-item" prepend-icon="mdi-phone-outline">
          <v-list-item-title class="drawer-title">
            SECOND PHONE NUMBER
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['alt_contact'] }}
          </v-list-item-subtitle>
        </v-list-item>
        
        <v-list-item class="drawer-item" prepend-icon="mdi-map-marker-outline">
          <v-list-item-title class="drawer-title">
            HOME CITY/TOWN
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['pob'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item class="drawer-item" prepend-icon="mdi-map-outline">
          <v-list-item-title class="drawer-title">
            REGION
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['region'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item class="drawer-item" prepend-icon="mdi-flag-variant-outline">
          <v-list-item-title class="drawer-title">
            NATIONALITY
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['nationality'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item class="drawer-item" prepend-icon="mdi-home-outline">
          <v-list-item-title class="drawer-title">
            RESIDENTIAL ADDRESS
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['address'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item class="drawer-item" prepend-icon="mdi-email-outline">
          <v-list-item-title class="drawer-title">
            EMAIL
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['email'] }}
          </v-list-item-subtitle>
        </v-list-item>
      </v-list>
    </div>
</template>


<style scoped>


</style>
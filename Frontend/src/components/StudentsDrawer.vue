<script setup lang="ts">
import { useUserAuthStore } from '@/stores/userAuthStore';
import { useElementsStore } from '@/stores/elementsStore';

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()

const drawer = document.getElementById('studentDrawer')

document.addEventListener('click', (event: any)=>{
  if (drawer?.style.display !== 'none'){
    if (!drawer?.contains(event.target)){
      elementsStore.drawer = false
    }
  }
})

</script>


<template>
    <div id="studentDrawer" class="drawer-container" v-show="elementsStore.drawer">
      <v-list class="drawer-list" v-if="userAuthStore.userData">
        <v-card-title class="drawer-head">STUDENT INFORMATION</v-card-title>
        
        <v-list-item class="drawer-item" prepend-icon="mdi-account">
          <v-list-item-title class="drawer-title">
            USERNAME
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['username'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item class="drawer-item" v-if="userAuthStore.userData['st_id']" prepend-icon="mdi-card-account-details-outline">
          <v-list-item-title class="drawer-title">STUDENT ID</v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['st_id'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item v-if="userAuthStore.userData['program']" class="drawer-item" prepend-icon="mdi-book-open-outline">
          <v-list-item-title class="drawer-title">
            PROGRAM
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['program'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item class="drawer-item" prepend-icon="mdi-book-open-outline">
          <v-list-item-title class="drawer-title">
            CLASS
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['st_class'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item v-if="userAuthStore.userData['index_no']" class="drawer-item" prepend-icon="mdi-account-details">
          <v-list-item-title class="drawer-title">
            INDEX NUMBER
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['index_no'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item class="drawer-item" prepend-icon="mdi-information-outline">
          <v-list-item-title class="drawer-title">
            CURRENT FORM
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['current_yr'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-card-title class="drawer-head">ACADEMIC CALENDAR</v-card-title>
        <v-list-item class="drawer-item" prepend-icon="mdi-calendar">
          <v-list-item-title class="drawer-title">
            ACADEMIC YEAR START DATE
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['academic_year']['start_date'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item class="drawer-item" prepend-icon="mdi-calendar">
          <v-list-item-title class="drawer-title">
            1st {{ userAuthStore.userData['academic_year']['period_division']['name'] }} END DATE
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['academic_year']['term_1_end_date'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item class="drawer-item" prepend-icon="mdi-calendar">
          <v-list-item-title class="drawer-title">
            2nd {{ userAuthStore.userData['academic_year']['period_division']['name'] }} START DATE
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['academic_year']['term_2_start_date'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item class="drawer-item" prepend-icon="mdi-calendar">
          <v-list-item-title class="drawer-title">
            2nd {{ userAuthStore.userData['academic_year']['period_division']['name'] }} END DATE
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['academic_year']['term_2_end_date'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item class="drawer-item" v-if="userAuthStore.userData['academic_year']['period_division']['name'] !== 'SEMESTER' " prepend-icon="mdi-calendar">
          <v-list-item-title class="drawer-title">
            3rd {{ userAuthStore.userData['academic_year']['period_division']['name'] }} START DATE
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['academic_year']['term_3_start_date'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item class="drawer-item" v-if="userAuthStore.userData['academic_year']['period_division']['name'] !== 'SEMESTER' " prepend-icon="mdi-calendar">
          <v-list-item-title class="drawer-title">
            3rd {{ userAuthStore.userData['academic_year']['period_division']['name'] }} END DATE
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['academic_year']['term_3_end_date'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item class="drawer-item" prepend-icon="mdi-calendar">
          <v-list-item-title class="drawer-title">
            ACADEMIC YEAR END DATE
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['academic_year']['end_date'] }}
          </v-list-item-subtitle>
        </v-list-item>
        
        <v-card-title class="drawer-head">PERSONAL INFORMATION</v-card-title>
        <v-list-item class="drawer-item" prepend-icon="mdi-account">
          <v-list-item-title class="drawer-title">
            FIRST NAME
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['first_name'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item class="drawer-item" prepend-icon="mdi-account">
          <v-list-item-title class="drawer-title">
            LAST NAME
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['last_name'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item class="drawer-item" prepend-icon="mdi-gender-male-female">
          <v-list-item-title class="drawer-title">
            GENDER
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['gender'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item class="drawer-item" prepend-icon="mdi-calendar-outline">
          <v-list-item-title class="drawer-title">
            DATE OF BIRTH
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['dob'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item class="drawer-item" prepend-icon="mdi-phone">
          <v-list-item-title class="drawer-title">
            CONTACT
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['contact'] }}
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

        <v-list-item class="drawer-item" prepend-icon="mdi-map-marker">
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

        <v-list-item class="drawer-item" prepend-icon="mdi-flag-variant">
          <v-list-item-title class="drawer-title">
            NATIONALITY
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['nationality'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item class="drawer-item" prepend-icon="mdi-home-outline">
          <v-list-item-title class="drawer-title">
            ADDRESS
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['address'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-card-title class="drawer-head">GUARDIAN INFORMATION</v-card-title>
        <v-list-item class="drawer-item" prepend-icon="mdi-account-outline">
          <v-list-item-title class="drawer-title">
            FIRST NAME
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['guardian_first_name'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item class="drawer-item" prepend-icon="mdi-account-outline">
          <v-list-item-title class="drawer-title">
            LAST NAME
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['guardian_last_name'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item class="drawer-item" prepend-icon="mdi-gender-male-female">
          <v-list-item-title class="drawer-title">
            GENDER
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['guardian_gender'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item class="drawer-item" prepend-icon="mdi-home-outline">
          <v-list-item-title class="drawer-title">
            OCCUPATION
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['guardian_occupation'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item class="drawer-item" prepend-icon="mdi-phone">
          <v-list-item-title class="drawer-title">
            CONTACT
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['guardian_contact'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item class="drawer-item" prepend-icon="mdi-email-outline">
          <v-list-item-title class="drawer-title">
            EMAIL
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['guardian_email'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item class="drawer-item" prepend-icon="mdi-flag-variant">
          <v-list-item-title class="drawer-title">
            NATIONALITY
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['guardian_nationality'] }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item class="drawer-item" prepend-icon="mdi-home-outline">
          <v-list-item-title class="drawer-title">
            ADDRESS
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData['guardian_address'] }}
          </v-list-item-subtitle>
        </v-list-item>
      </v-list>
    </div>
</template>


<style scoped>



</style>
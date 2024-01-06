
<script setup lang="ts">
const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()


</script>


<template>
    <section>
      <v-navigation-drawer style="background-color: yellow; width: max-content; height: max-content"  v-model="elementsStore.drawer" temporary>
        <v-list class="pa-0 ma-0" v-if="userAuthStore.userData">
          <v-card-title class="title-head">IDENTITY</v-card-title>
          <v-list-item >
            <template v-slot:prepend>
              <v-icon icon="mdi-account" />
            </template>
            <v-list-item-title class="title">USERNAME</v-list-item-title>
            <v-list-item-subtitle class="subtitle">{{ userAuthStore.userData['username'] }}</v-list-item-subtitle>
          </v-list-item>
          <v-list-item>
            <template v-slot:prepend>
              <v-icon icon="mdi-card-account-details-outline" />
            </template>
            <v-list-item-title class="title">STAFF ID</v-list-item-title>
            <v-list-item-subtitle v-if="userAuthStore.userData['role']==='staff'" class="subtitle">{{ userAuthStore.userData['staff_id'] }}</v-list-item-subtitle>
            <v-list-item-subtitle v-if="userAuthStore.userData['role']==='head'" class="subtitle">{{ userAuthStore.userData['head_id'] }}</v-list-item-subtitle>
          </v-list-item>
          <v-list-item>
            <template v-slot:prepend>
              <v-icon icon="mdi-account-outline" />
            </template>
            <v-list-item-title class="title">ROLE</v-list-item-title>
            <v-list-item-subtitle v-if="userAuthStore.userData['role']==='staff'" class="subtitle">{{ userAuthStore.userData['staff_role'] }}</v-list-item-subtitle>
            <v-list-item-subtitle v-if="userAuthStore.userData['role']==='head'" class="subtitle">{{ userAuthStore.userData['head_role'] }}</v-list-item-subtitle>
          </v-list-item>
          <v-list-item v-if="userAuthStore.userData['role']=='staff' && userAuthStore.userData['staff_role'] !=='admin' " >
            <template v-slot:prepend>
              <v-icon icon="mdi-book-open-outline" />
            </template>
            <v-list-item-title class="title">SUBJECT(S)</v-list-item-title>
            <v-list-item-title class="subtitle">
              <p class="subjects" v-for="(subject, i) in userAuthStore.userData['subjects']" :key="i">{{subject['name']}}</p>
            </v-list-item-title>
          </v-list-item>
          <v-card-title class="title-head">PERSONAL INFORMATION</v-card-title>
          <v-list-item>
            <template v-slot:prepend>
              <v-icon icon="mdi-account-outline" />
            </template>
            <v-list-item-title class="title">FIRST NAME</v-list-item-title>
            <v-list-item-subtitle class="subtitle">{{ userAuthStore.userData['first_name'] }}</v-list-item-subtitle>
          </v-list-item>
          <v-list-item>
            <template v-slot:prepend>
              <v-icon icon="mdi-account" />
            </template>
            <v-list-item-title class="title">LAST NAME</v-list-item-title>
            <v-list-item-subtitle class="subtitle">{{ userAuthStore.userData['last_name'] }}</v-list-item-subtitle>
          </v-list-item>
          <v-list-item >
            <template v-slot:prepend>
              <v-icon icon="mdi-map-marker" />
            </template>
            <v-list-item-title class="title">HOME CITY/TOWN</v-list-item-title>
            <v-list-item-subtitle class="subtitle">{{ userAuthStore.userData['pob'] }}</v-list-item-subtitle>
          </v-list-item>
          <v-list-item >
            <template v-slot:prepend>
              <v-icon icon="mdi-calendar-outline" />
            </template>
            <v-list-item-title class="title">DATE OF BIRTH</v-list-item-title>
            <v-list-item-subtitle class="subtitle">{{ userAuthStore.userData['dob'] }}</v-list-item-subtitle>
          </v-list-item>
          <v-list-item >
            <template v-slot:prepend>
              <v-icon icon="mdi-gender-male-female" />
            </template>
            <v-list-item-title class="title">GENDER</v-list-item-title>
            <v-list-item-subtitle class="subtitle">{{ userAuthStore.userData['gender'] }}</v-list-item-subtitle>
          </v-list-item>
          <v-list-item>
            <template v-slot:prepend>
              <v-icon icon="mdi-map-outline" />
            </template>
            <v-list-item-title class="title">REGION</v-list-item-title>
            <v-list-item-subtitle class="subtitle">{{ userAuthStore.userData['region'] }}</v-list-item-subtitle>
          </v-list-item>
          <v-list-item >
            <template v-slot:prepend>
              <v-icon icon="mdi-flag-variant" />
            </template>
            <v-list-item-title class="title">NATIONALITY</v-list-item-title>
            <v-list-item-subtitle class="subtitle">{{ userAuthStore.userData['nationality'] }}</v-list-item-subtitle>
          </v-list-item>
          <v-list-item >
            <template v-slot:prepend>
              <v-icon icon="mdi-phone" />
            </template>
            <v-list-item-title class="title">PHONE NUMBER</v-list-item-title>
            <v-list-item-subtitle class="subtitle">{{ userAuthStore.userData['contact'] }}</v-list-item-subtitle>
          </v-list-item>
          <v-list-item >
            <template v-slot:prepend>
              <v-icon icon="mdi-email-outline" />
            </template>
            <v-list-item-title class="title">EMAIL</v-list-item-title>
            <v-list-item-subtitle class="subtitle">{{ userAuthStore.userData['email'] }}</v-list-item-subtitle>
          </v-list-item>
          <v-list-item >
            <template v-slot:prepend>
              <v-icon icon="mdi-home-outline" />
            </template>
            <v-list-item-title class="title">ADDRESS</v-list-item-title>
            <v-list-item-subtitle class="subtitle">{{ userAuthStore.userData['address'] }}</v-list-item-subtitle>
          </v-list-item>
        </v-list>
      </v-navigation-drawer>
    </section>
</template>


<style scoped>

.title-head{
  font-size: .8rem;
  background-color: seagreen;
  color: yellow;
  font-weight: bold;
}

.title{
  font-size: .8rem;
  font-family: Verdana, Geneva, Tahoma, sans-serif;
}

.subtitle{
  font-size: .75rem;
}

.subjects{
  font-size: .55rem;
  text-transform: uppercase;
}

</style>
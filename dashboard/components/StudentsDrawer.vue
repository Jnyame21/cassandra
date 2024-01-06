<script setup lang="ts">

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()


</script>


<template>
    <section>
      <v-navigation-drawer style="height: max-content; width: max-content" v-model="elementsStore.drawer" temporary>
        <v-list class="pa-0 ma-0" v-if="userAuthStore.userData" style="overflow-y: scroll; height: 100vh">
          <v-card-title class="title-head">IDENTITY</v-card-title>
          <v-list-item style="background-color: yellow">
            <template v-slot:prepend>
              <v-icon size="small" icon="mdi-account" />
            </template>
            <v-list-item-title class="title">USERNAME</v-list-item-title>
            <v-list-item-subtitle class="subtitle">{{ userAuthStore.userData['username'] }}</v-list-item-subtitle>
          </v-list-item>
          <v-list-item style="background-color: yellow">
            <template v-slot:prepend>
              <v-icon size="small" icon="mdi-card-account-details-outline" />
            </template>
            <v-list-item-title class="title">STUDENT ID</v-list-item-title>
            <v-list-item-subtitle class="subtitle">{{ userAuthStore.userData['st_id'] }}</v-list-item-subtitle>
          </v-list-item>
          <v-list-item style="background-color: yellow">
            <template v-slot:prepend>
              <v-icon size="small" icon="mdi-book-open-outline" />
            </template>
            <v-list-item-title class="title">PROGRAM</v-list-item-title>
            <v-list-item-subtitle class="subtitle">{{ userAuthStore.userData['program'] }}</v-list-item-subtitle>
          </v-list-item>
          <v-list-item style="background-color: yellow">
            <template v-slot:prepend>
              <v-icon size="small" icon="mdi-book-open-outline" />
            </template>
            <v-list-item-title class="title">CLASS</v-list-item-title>
            <v-list-item-subtitle class="subtitle">{{ userAuthStore.userData['st_class'] }}</v-list-item-subtitle>
          </v-list-item>
          <v-list-item style="background-color: yellow">
            <template v-slot:prepend>
              <v-icon size="small" icon="mdi-account-details" />
            </template>
            <v-list-item-title class="title">INDEX NUMBER</v-list-item-title>
            <v-list-item-subtitle class="subtitle">{{ userAuthStore.userData['index_no'] }}</v-list-item-subtitle>
          </v-list-item>
          <v-list-item style="background-color: yellow">
            <template v-slot:prepend>
              <v-icon size="small" icon="mdi-information-outline" />
            </template>
            <v-list-item-title class="title">CURRENT YEAR</v-list-item-title>
            <v-list-item-subtitle class="subtitle">{{ userAuthStore.userData['current_yr'] }}</v-list-item-subtitle>
          </v-list-item>
          <v-card-title class="title-head">PERSONAL INFORMATION</v-card-title>
          <v-list-item style="background-color: yellow">
            <template v-slot:prepend>
              <v-icon size="small" icon="mdi-account" />
            </template>
            <v-list-item-title class="title">FIRST NAME</v-list-item-title>
            <v-list-item-subtitle class="subtitle">{{ userAuthStore.userData['first_name'] }}</v-list-item-subtitle>
          </v-list-item>
          <v-list-item style="background-color: yellow">
            <template v-slot:prepend>
              <v-icon size="small" icon="mdi-account" />
            </template>
            <v-list-item-title class="title">LAST NAME</v-list-item-title>
            <v-list-item-subtitle class="subtitle">{{ userAuthStore.userData['last_name'] }}</v-list-item-subtitle>
          </v-list-item>
          <v-list-item style="background-color: yellow">
            <template v-slot:prepend>
              <v-icon size="small" icon="mdi-phone" />
            </template>
            <v-list-item-title class="title">CONTACT</v-list-item-title>
            <v-list-item-subtitle class="subtitle">{{ userAuthStore.userData['contact'] }}</v-list-item-subtitle>
          </v-list-item>
          <v-list-item style="background-color: yellow">
            <template v-slot:prepend>
              <v-icon size="small" icon="mdi-email-outline" />
            </template>
            <v-list-item-title class="title">EMAIL</v-list-item-title>
            <v-list-item-subtitle class="subtitle">{{ userAuthStore.userData['email'] }}</v-list-item-subtitle>
          </v-list-item>
          <v-list-item style="background-color: yellow">
            <template v-slot:prepend>
              <v-icon size="small" icon="mdi-map-marker" />
            </template>
            <v-list-item-title class="title">HOME CITY/TOWN</v-list-item-title>
            <v-list-item-subtitle class="subtitle">{{ userAuthStore.userData['pob'] }}</v-list-item-subtitle>
          </v-list-item>
          <v-list-item style="background-color: yellow">
            <template v-slot:prepend>
              <v-icon size="small" icon="mdi-calendar-outline" />
            </template>
            <v-list-item-title class="title">DATE OF BIRTH</v-list-item-title>
            <v-list-item-subtitle class="subtitle">{{ userAuthStore.userData['dob'] }}</v-list-item-subtitle>
          </v-list-item>
          <v-list-item style="background-color: yellow">
            <template v-slot:prepend>
              <v-icon size="small" icon="mdi-gender-male-female" />
            </template>
            <v-list-item-title class="title">GENDER</v-list-item-title>
            <v-list-item-subtitle class="subtitle">{{ userAuthStore.userData['gender'] }}</v-list-item-subtitle>
          </v-list-item>
          <v-list-item style="background-color: yellow">
            <template v-slot:prepend>
              <v-icon size="small" icon="mdi-map-outline" />
            </template>
            <v-list-item-title class="title">REGION</v-list-item-title>
            <v-list-item-subtitle class="subtitle">{{ userAuthStore.userData['region'] }}</v-list-item-subtitle>
          </v-list-item>
          <v-list-item style="background-color: yellow">
            <template v-slot:prepend>
              <v-icon size="small" icon="mdi-flag-variant" />
            </template>
            <v-list-item-title class="title">NATIONALITY</v-list-item-title>
            <v-list-item-subtitle class="subtitle">{{ userAuthStore.userData['nationality'] }}</v-list-item-subtitle>
          </v-list-item>
          <v-list-item style="background-color: yellow">
            <template v-slot:prepend>
              <v-icon size="small" icon="mdi-home-outline" />
            </template>
            <v-list-item-title class="title">ADDRESS</v-list-item-title>
            <v-list-item-subtitle class="subtitle">{{ userAuthStore.userData['address'] }}</v-list-item-subtitle>
          </v-list-item>
          <v-card-title class="title-head">GUARDIAN INFORMATION</v-card-title>
          <v-list-item style="background-color: yellow">
            <template v-slot:prepend>
              <v-icon size="small" icon="mdi-account-outline" />
            </template>
            <v-list-item-title class="title">NAME</v-list-item-title>
            <v-list-item-subtitle class="subtitle">{{ userAuthStore.userData['guardian'] }}</v-list-item-subtitle>
          </v-list-item>
          <v-list-item style="background-color: yellow">
            <template v-slot:prepend>
              <v-icon size="small" icon="mdi-gender-male-female" />
            </template>
            <v-list-item-title class="title">GENDER</v-list-item-title>
            <v-list-item-subtitle class="subtitle">{{ userAuthStore.userData['guardian_gender'] }}</v-list-item-subtitle>
          </v-list-item>
          <v-list-item style="background-color: yellow">
            <template v-slot:prepend>
              <v-icon size="small" icon="mdi-home-outline" />
            </template>
            <v-list-item-title class="title">OCCUPATION</v-list-item-title>
            <v-list-item-subtitle class="subtitle">{{ userAuthStore.userData['guardian_occupation'] }}</v-list-item-subtitle>
          </v-list-item>
          <v-list-item style="background-color: yellow">
            <template v-slot:prepend>
              <v-icon size="small" icon="mdi-flag-variant" />
            </template>
            <v-list-item-title class="title">NATIONALITY</v-list-item-title>
            <v-list-item-subtitle class="subtitle">{{ userAuthStore.userData['guardian_nationality'] }}</v-list-item-subtitle>
          </v-list-item>
          <v-list-item style="background-color: yellow">
            <template v-slot:prepend>
              <v-icon size="small" icon="mdi-email-outline" />
            </template>
            <v-list-item-title class="title">EMAIL</v-list-item-title>
            <v-list-item-subtitle class="subtitle">{{ userAuthStore.userData['guardian_email'] }}</v-list-item-subtitle>
          </v-list-item>
          <v-list-item style="background-color: yellow">
            <template v-slot:prepend>
              <v-icon size="small" icon="mdi-phone" />
            </template>
            <v-list-item-title class="title">CONTACT</v-list-item-title>
            <v-list-item-subtitle class="subtitle">{{ userAuthStore.userData['guardian_contact'] }}</v-list-item-subtitle>
          </v-list-item>
          <v-list-item style="background-color: yellow">
            <template v-slot:prepend>
              <v-icon size="small" icon="mdi-home-outline" />
            </template>
            <v-list-item-title class="title">ADDRESS</v-list-item-title>
            <v-list-item-subtitle class="subtitle">{{ userAuthStore.userData['guardian_address'] }}</v-list-item-subtitle>
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

</style>
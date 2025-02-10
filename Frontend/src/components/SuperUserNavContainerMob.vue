<script setup lang="ts">
import { useUserAuthStore } from '@/stores/userAuthStore';
import { useElementsStore } from '@/stores/elementsStore';

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()

const changePage = (page_name: string) => {
    elementsStore.activePage = page_name
}

const showOverlay = () => {
  const overlay = document.getElementById('LogoutOverlay')
  if (overlay) {
    overlay.style.display = 'flex'
  }
}

</script>
<template>
    <div class="nav-container-drawer" v-show="elementsStore.navDrawer">
        <v-list class="nav-list-container">
            <v-list-item class="nav-item nav-link" @click="changePage('SuperUserSchools')"
                prepend-icon="mdi-account-group-outline">
                SCHOOLS
            </v-list-item>

            <v-list-item class="nav-item nav-link" @click="changePage('SuperUserLevels')"
                prepend-icon="mdi-account-group-outline">
                LEVELS
            </v-list-item>

            <v-list-item class="nav-item nav-link" @click="changePage('SuperUserSubjects')"
                prepend-icon="mdi-account-group-outline">
                SUBJECTS
            </v-list-item>

            <v-list-item class="nav-item nav-link" @click="changePage('SuperUserPrograms')"
                prepend-icon="mdi-account-group-outline">
                PROGRAMS
            </v-list-item>

            <v-list-item class="nav-item nav-link" @click="changePage('SuperUserGradingSystemRanges')"
                prepend-icon="mdi-account-group-outline">
                GRADING SYSTEM RANGES
            </v-list-item>

            <v-list-item class="nav-item nav-link" @click="changePage('SuperUserGradingSystems')"
                prepend-icon="mdi-account-group-outline">
                GRADING SYSTEMS
            </v-list-item>

            <v-list-group>
                <template v-slot:activator="{ props }">
                    <v-list-item v-bind="props" class="nav-item" prepend-icon="mdi-book-open-outline">
                        DEPARMENTS
                    </v-list-item>
                </template>
                <v-list-item class="nav-title nav-link"
                    v-for="school in Object.keys(userAuthStore.superUserData.departments)" :key="school"
                    @click="changePage(`SuperUserDepartments,${school}`)">
                    {{ school }}
                </v-list-item>
            </v-list-group>

            <v-list-group>
                <template v-slot:activator="{ props }">
                    <v-list-item v-bind="props" class="nav-item" prepend-icon="mdi-book-open-outline">
                        CLASSES
                    </v-list-item>
                </template>
                <v-list-item class="nav-title nav-link"
                    v-for="school in Object.keys(userAuthStore.superUserData.classes)" :key="school"
                    @click="changePage(`SuperUserClasses,${school}`)">
                    {{ school }}
                </v-list-item>
            </v-list-group>

            <v-list-group>
                <template v-slot:activator="{ props }">
                    <v-list-item v-bind="props" class="nav-item" prepend-icon="mdi-book-open-outline">
                        ACADEMIC YEARS
                    </v-list-item>
                </template>
                <v-list-item class="nav-title nav-link"
                    v-for="school in Object.keys(userAuthStore.superUserData.academicYears)" :key="school"
                    @click="changePage(`SuperUserAcademicYears,${school}`)">
                    {{ school }}
                </v-list-item>
            </v-list-group>

            <v-list-item class="nav-item nav-link" @click="changePage('SuperUserStaffRoles')"
                prepend-icon="mdi-account-group-outline">
                STAFF ROLES
            </v-list-item>

            <v-list-group>
                <template v-slot:activator="{ props }">
                    <v-list-item v-bind="props" class="nav-item" prepend-icon="mdi-book-open-outline">
                        STAFF
                    </v-list-item>
                </template>
                <v-list-item class="nav-title nav-link" v-for="school in Object.keys(userAuthStore.superUserData.staff)"
                    :key="school" @click="changePage(`SuperUserStaff,${school}`)">
                    {{ school }}
                </v-list-item>
            </v-list-group>
            
            <div class="flex-all mt-15">
                <v-btn @click="showOverlay()" size="small" color="red" variant="flat"
                    prepend-icon="mdi-logout">LOGOUT</v-btn>
            </div>
        </v-list>
    </div>
</template>

<style scoped>
</style>
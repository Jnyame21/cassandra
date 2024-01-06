<script setup lang="ts">

definePageMeta({
    middleware: ['check-staff']
})

useHead({
  meta: [
    {name: "robots", content: "no-index"}
  ],
})

const userAuthStore = useUserAuthStore()
const rozmachAuth: any = ref(null)
const activePage = ref('page1')

onBeforeUnmount(()=>{
  document.body.style.overflow = 'auto'
})

onBeforeMount(()=>{
  if (userAuthStore.isAuthenticated && userAuthStore.userData){
    document.title = "EduAAP"
  }
  document.body.style.overflow = 'hidden'
  rozmachAuth.value = localStorage.getItem('RozmachAuth')
  if (rozmachAuth.value){
    rozmachAuth.value = JSON.parse(rozmachAuth.value)
  }

})


const hidOverlay = ()=>{
  const overlay = document.getElementById('welcome')
  if (overlay){
    if (rozmachAuth.value && !rozmachAuth.value.last_login){
      showOverlay()
      rozmachAuth.value.last_login = true
      localStorage.setItem('RozmachAuth', JSON.stringify(rozmachAuth))
    }
    overlay.style.display = 'none'
  }
}

const showOverlay = ()=>{
  const overlay = document.getElementById('welcome')
  overlay? overlay.style.display = 'flex' : null
}

const changePage = (page: string)=>{
  activePage.value = page
}


</script>

<template>
    <!-- Welcome Overlay-->
  <div id="welcome" class="welcome-overlay" v-if="rozmachAuth && !rozmachAuth['last_login'] && userAuthStore.userData && userAuthStore.userData['role']==='staff' ">
    <v-card class="card flex-all-c">
      <v-card-title id="school-name">{{userAuthStore.userData['school']['name']}}</v-card-title>
      <v-card-text style="font-size: .9rem; font-family: sans-serif; text-align: left; line-height: 1.5">
        <p style="text-align: center"><strong>Welcome {{userAuthStore.userData['first_name']+' '+userAuthStore.userData['last_name']}}!</strong></p>
        <p>We're thrilled to have you on board as part of our dedicated teaching team. Your passion, expertise, and commitment to education are greatly appreciated.
          This is your personalized dashboard, designed to make your teaching experience as smooth and rewarding as possible.
          Here, you'll find all the tools and resources you need to inspire and guide your students to success. Feel free to explore and familiarize yourself with your dashboard.</p>
        <p>If you have any questions or need assistance, our support team is always here to help.</p>
      </v-card-text>
      <v-card-actions class="flex-all">
        <v-btn class="overlay-btn" elevation="4" @click="hidOverlay()">OK</v-btn>
      </v-card-actions>
    </v-card>
  </div>    
  <TheHeader/>
  <main class="main">
    
     <!-- Tabs -->
    <div class="pages-container">

      <div class="page-nav-container">
        <!-- Head -->
        <button class="nav-btn" @click="changePage('page1')" :class="{'nav-btn-active': activePage==='page1'}"
        v-if="userAuthStore.userData && userAuthStore.userData['role'] && userAuthStore.userData['role'] === 'head'"
        ><v-icon icon="mdi-eye"/>
          OVERVIEW
        </button>
        
        <button class="nav-btn" @click="changePage('page2')" :class="{'nav-btn-active': activePage==='page2'}"
        v-if="userAuthStore.userData && userAuthStore.userData['role'] && userAuthStore.userData['role'] === 'head'"
        ><v-icon icon="mdi-account"/>
          DEPARTMENTS
        </button>

        <button class="nav-btn" @click="changePage('page3')" :class="{'nav-btn-active': activePage==='page3'}"
        v-if="userAuthStore.userData && userAuthStore.userData['role'] && userAuthStore.userData['role'] === 'head'"
        ><v-icon icon="mdi-account-group-outline"/>
          STUDENTS
        </button>

        <button class="nav-btn" @click="changePage('page4')" :class="{'nav-btn-active': activePage==='page4'}"
        v-if="userAuthStore.userData && userAuthStore.userData['role'] && userAuthStore.userData['role'] === 'head'"
        ><v-icon icon="mdi-chart-bar"/>
          ANALYTICS
        </button>

        <button class="nav-btn" @click="changePage('page5')" :class="{'nav-btn-active': activePage==='page5'}"
        v-if="userAuthStore.userData && userAuthStore.userData['role'] && userAuthStore.userData['role'] === 'head'"
        ><v-icon icon="mdi-alert-octagon-outline"/>
          HELP
        </button>


        <!-- Staff -->
        <button class="nav-btn" @click="changePage('page1')" :class="{'nav-btn-active': activePage==='page1'}"
        v-if="userAuthStore.userData && userAuthStore.userData['staff_role']=== 'teacher' || userAuthStore.userData && userAuthStore.userData['staff_role']=== 'hod'"
        ><v-icon icon="mdi-book-open-outline"/>
          COURSEWORK
        </button>

        <button class="nav-btn" @click="changePage('page2')" :class="{'nav-btn-active': activePage==='page2'}"
        v-if="userAuthStore.userData && userAuthStore.userData['staff_role']=== 'teacher' || userAuthStore.userData && userAuthStore.userData['staff_role']=== 'hod' "
        ><v-icon icon="mdi-account-group-outline"/>
          STUDENTS
        </button>

        <button class="nav-btn" @click="changePage('page3')" :class="{'nav-btn-active': activePage==='page3'}"
        v-if="userAuthStore.userData && userAuthStore.userData['staff_role']=== 'teacher' || userAuthStore.userData && userAuthStore.userData['staff_role']=== 'hod' "
        ><v-icon icon="mdi-chart-bar"/>
          ANALYTICS
        </button>

        <button class="nav-btn" @click="changePage('page4')" :class="{'nav-btn-active': activePage==='page4'}"
        v-if="userAuthStore.userData && userAuthStore.userData['staff_role']=== 'hod'"
        ><v-icon icon="mdi-account-multiple"/>
          TEACHERS
        </button>
        
        <button class="nav-btn" @click="changePage('page5')" :class="{'nav-btn-active': activePage==='page5'}"
        v-if="userAuthStore.userData && userAuthStore.userData['staff_role']=== 'hod' "
        ><v-icon icon="mdi-chart-line"/>
          PERFORMANCE
        </button>


        <!-- Admin -->
        <button class="nav-btn" @click="changePage('page1')" :class="{'nav-btn-active': activePage==='page1'}"
        v-if="userAuthStore.userData && userAuthStore.userData['staff_role']=== 'admin'"
        ><v-icon icon="mdi-account-group-outline"/>
          STUDENTS
        </button>

        <button class="nav-btn" @click="changePage('page2')" :class="{'nav-btn-active': activePage==='page2'}"
        v-if="userAuthStore.userData && userAuthStore.userData['staff_role']=== 'admin' "
        ><v-icon icon="mdi-account-multiple"/>
          TEACHERS
        </button>

        <!-- Admin -->

        <button class="nav-btn" @click="changePage('page6')" :class="{'nav-btn-active': activePage==='page6'}"
        v-if="userAuthStore.userData && userAuthStore.userData['role']=== 'staff' "
        ><v-icon icon="mdi-alert-octagon-outline"/>
          HELP
        </button>
      </div>

      <!-- Pages -->

      <!-- Head -->
      <div class="pages" :style="activePage==='page1' ? {'display': 'flex'}: {'display': 'none'}"
      v-if="userAuthStore.userData && userAuthStore.userData['role'] && userAuthStore.userData['role'] === 'head'"
      ><HeadOverview />
      </div>

      <div class="pages" :style="activePage==='page2' ? {'display': 'flex'}: {'display': 'none'}"
      v-if="userAuthStore.userData && userAuthStore.userData['role'] && userAuthStore.userData['role']=== 'head'"
      ><HeadDepartments />
      </div>

      <div class="pages" :style="activePage==='page3' ? {'display': 'flex'}: {'display': 'none'}"
      v-if="userAuthStore.userData && userAuthStore.userData['role'] && userAuthStore.userData['role']=== 'head'"
      ><HeadStudents />
      </div>

      <div class="pages" :style="activePage==='page4' ? {'display': 'flex'}: {'display': 'none'}"
      v-if="userAuthStore.userData && userAuthStore.userData['role'] && userAuthStore.userData['role']=== 'head'"
      ><HeadPerformance />
      </div>

      <div class="pages" :style="activePage==='page5' ? {'display': 'flex'}: {'display': 'none'}"
      v-if="userAuthStore.userData && userAuthStore.userData['role'] && userAuthStore.userData['role']=== 'head' "
      ><HelpForm />
      </div>


        <!-- Staff -->
      <div class="pages" :style="activePage==='page1' ? {'display': 'flex'}: {'display': 'none'}"
      v-if="userAuthStore.userData && userAuthStore.userData['staff_role']=== 'teacher' || userAuthStore.userData && userAuthStore.userData['staff_role']=== 'hod' "
      ><TeacherCourseWork />
      </div>

      <div class="pages" :style="activePage==='page2' ? {'display': 'flex'}: {'display': 'none'}"
      v-if="userAuthStore.userData && userAuthStore.userData['staff_role']=== 'teacher' || userAuthStore.userData && userAuthStore.userData['staff_role']=== 'hod' "
      ><TeacherStudents />
      </div>

      <div class="pages" :style="activePage==='page3' ? {'display': 'flex'}: {'display': 'none'}"
      v-if="userAuthStore.userData && userAuthStore.userData['staff_role']=== 'teacher' || userAuthStore.userData && userAuthStore.userData['staff_role']=== 'hod' "
      ><TeacherAnalytics />
      </div>

      <div class="pages" :style="activePage==='page4' ? {'display': 'flex'}: {'display': 'none'}"
      v-if="userAuthStore.userData && userAuthStore.userData['staff_role']=== 'hod'"
      ><HodTeachers />
      </div>

      <div class="pages" :style="activePage==='page5' ? {'display': 'flex'}: {'display': 'none'}"
      v-if="userAuthStore.userData && userAuthStore.userData['staff_role']=== 'hod' "
      ><HodPerformance />
      </div>

      <!-- Admin -->
      <div class="pages" :style="activePage==='page1' ? {'display': 'flex'}: {'display': 'none'}"
      v-if="userAuthStore.userData && userAuthStore.userData['staff_role']=== 'admin' "
      ><AdminStudents />
      </div>

      <div class="pages" :style="activePage==='page2' ? {'display': 'flex'}: {'display': 'none'}"
      v-if="userAuthStore.userData && userAuthStore.userData['staff_role']=== 'admin' "
      ><AdminStaff />
      </div>
        <!-- Admin -->

      <div class="pages" :style="activePage==='page6' ? {'display': 'flex'}: {'display': 'none'}"
      v-if="userAuthStore.userData && userAuthStore.userData['role'] && userAuthStore.userData['role']=== 'staff' "
      ><HelpForm />
      </div>
    </div>

  </main>
  <TheFooter />
</template>

<style scoped>

.welcome-overlay{
  display: flex;
  position: absolute;
  align-items: center;
  justify-content: center;
  height: 100%;
  z-index: 2;
  width: 100%;
  background-color: rgba(0,0,0,0.5);
}

.card{
  width: 80%;
  max-width: 700px;
}

#school-name{
  font-size: .7rem;
  font-family: Verdana, "sans-serif";
  text-align: center;
  font-weight: bold;
  text-transform: uppercase;
  color: #007bff;
}
.overlay-btn{
  background-color: lightseagreen;
  color: white;
}
.overlay-btn:hover{
  background-color: mediumseagreen;
  color: yellow;
}


</style>
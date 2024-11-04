<script setup lang="ts">
import 'chart.js/auto'
import { ref } from 'vue';
import axiosInstance from '../utils/axiosInstance';
import { AxiosError } from 'axios';
import { getAttendanceData } from '~/utils/util';
import { Bar } from 'vue-chartjs';

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()
const formErrorMessage = ref('')
const attendanceUploadDate:any = ref(null)
const currentLabels:any = ref([])
const currentDatasets:any = ref([])
const selectedStudents:any = ref([])
const academicYearStartDate = new Date(userAuthStore.userData['academic_year']['start_date'])
const academicYearEndDate = new Date(userAuthStore.userData['academic_year']['end_date'])
const academic_year = userAuthStore.activeAcademicYear
const attendances = ref(getAttendanceData(academicYearStartDate, academicYearEndDate));
const chartData = ref({
  labels: currentLabels.value,
  datasets: [
    {
      label: 'TOTAL ATTENDANCE',
      data: currentDatasets.value,
      borderColor: 'rgba(75, 192, 192, 1)',
      borderWidth: 2,
    },
  ],
})
const chartOptions = ref({
  responsive: true,
})

interface Props {
  className: string;
  classIndex: number;
  students: any[];
}

const props = defineProps<Props>()
const className = props.className
const classIndex = props.classIndex || 0
const students = props.students

const changeAnalysis = (type:string, month:string='', week:string='')=>{
  currentLabels.value = []
  currentDatasets.value = []
  const labelName = ref('')
  if (type === 'year'){
    attendances.value.forEach(item =>{
      currentLabels.value.push(item['month'])
      currentDatasets.value.push(item['studentsPresent'])
    })
    labelName.value = 'TOTAL ATTENDANCE'
  }
  else if (type === 'month'){
    const attendanceMonth = attendances.value.find(item => item['month'] === month)
    if (attendanceMonth){
      attendanceMonth['weeks'].forEach(item =>{
        currentLabels.value.push(item['week'])
        currentDatasets.value.push(item['studentsPresent'])
      })
      labelName.value = 'TOTAL ATTENDANCE'
    }
  }
  else if (type === 'week'){
    const attendanceMonth = attendances.value.find(item => item['month'] === month)
    if (attendanceMonth){
      const attendanceWeek = attendanceMonth['weeks'].find(item => item['week']===week)
      if (attendanceWeek){
        attendanceWeek['days'].forEach(item =>{
          currentLabels.value.push(item['day'])
          currentDatasets.value.push(item['studentsPresent'])
        })
        labelName.value = 'STUDENTS PRESENT'
      }
    }
  }
  currentLabels.value.length === 0 ? labelName.value = 'NO DATA' : null
  currentDatasets.value.every(item => item === 0) ? labelName.value = 'NO DATA' : null
  chartData.value = {
    labels: currentLabels.value,
    datasets: [
      {
        label: labelName.value,
        data: currentDatasets.value,
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 2,
      },
    ],
  }
}

watch(()=>userAuthStore.teacherData.studentsattendance?.[classIndex]?.attendances, (newValue, oldValue)=>{
  if (newValue){
    attendances.value = getAttendanceData(academicYearStartDate, academicYearEndDate)
    let date:any = null
    let dayNumber = 0
    let dayName = ''
    let weekNumber = 0
    let monthName = ''
    let numberOfStudentsPresents = 0
    if (newValue.length > 0){
      newValue.forEach(item =>{
        numberOfStudentsPresents = item['students_present'].length
        date = new Date(item['date'].toString())
        dayNumber = date.getDate()
        dayName = date.toLocaleString('default', {'weekday': 'long'})
        weekNumber = Math.ceil(dayNumber /7 )
        monthName = date.toLocaleString('default', {'month': 'long'}).toUpperCase()
        const attendanceMonth = attendances.value.find(month => month['month'] === monthName)
        if (attendanceMonth){
          const monthIndex = attendances.value.indexOf(attendanceMonth)
          attendances.value[monthIndex]['studentsPresent'] += numberOfStudentsPresents
          const attendanceWeek = attendanceMonth['weeks'].find(week => week['week'].split(' ')[1] === weekNumber.toString())
          if (attendanceWeek){
            const attendanceWeekIndex = attendanceMonth['weeks'].indexOf(attendanceWeek)
            attendances.value[monthIndex]['weeks'][attendanceWeekIndex]['studentsPresent'] += numberOfStudentsPresents
            const attendanceDay = attendanceWeek['days'].find(day => day['day'] === dayName.toUpperCase())
            if (attendanceDay){
              const attendanceDayIndex = attendanceWeek['days'].indexOf(attendanceDay)
              attendances.value[monthIndex]['weeks'][attendanceWeekIndex]['days'][attendanceDayIndex]['studentsPresent'] += numberOfStudentsPresents
            }
          }
        }
      })
      changeAnalysis('year')
    }else{
      currentLabels.value = []
      currentDatasets.value = []
      chartData.value = {
        labels: currentLabels.value,
        datasets: [
          {
            label: 'NO DATA',
            data: currentDatasets.value,
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 2,
          },
        ],
      }
    }
  }
}, {'immediate': true, 'deep': 1})

const clearMessage = ()=>{
  setTimeout(()=>{
    formErrorMessage.value = ''
  }, 10000)
}

const uploadAttendance = async()=>{
  if (new Date(attendanceUploadDate.value) < academicYearStartDate || new Date(attendanceUploadDate.value) > academicYearEndDate) {
    formErrorMessage.value = `The attendance date must be between the academic year start date and end date, which are ${academicYearStartDate.toDateString()} and ${academicYearEndDate.toDateString()} respectively.`;
    clearMessage();
    return;
  }else if ([0, 6].includes(new Date(attendanceUploadDate.value).getDay())) {
    formErrorMessage.value = "Attendance dates cannot fall on weekends (Saturday and Sunday)!"
    clearMessage();
    return;
  }
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData
  formData.append('className', className)
  formData.append('absentStudents', selectedStudents.value)
  formData.append('year', userAuthStore.activeAcademicYear)
  formData.append('term', userAuthStore.activeTerm)
  formData.append('type', 'create')
  formData.append('date', attendanceUploadDate.value)

  try{
    const response = await axiosInstance.post('teacher/students/attendance', formData)
    userAuthStore.teacherData.studentsattendance?.[classIndex].attendances.unshift(response.data)
    userAuthStore.teacherData.studentsattendance?.[classIndex].attendances.sort((a, b) => new Date(b.date) - new Date(a.date))
    selectedStudents.value = []
    attendanceUploadDate.value = null
    elementsStore.HideLoadingOverlay()
    elementsStore.ShowOverlay('Operation successful', 'green', null, null)
  }
  catch(error){
    elementsStore.HideLoadingOverlay()
    if (error instanceof AxiosError){
      if(error.response){
        if (error.response.status === 400 && error.response.data.message){
          elementsStore.ShowOverlay(error.response.data.message, 'red', null, null)
        }else{
          elementsStore.ShowOverlay('Oops! something went wrong. Try again later', 'red', null, null)
        }
      }
      else if (!error.response && (error.code === 'ECONNABORTED' || !navigator.onLine)){
        elementsStore.ShowOverlay('A network error occurred! Please check you internet connection', 'red', null, null)
      }
      else{
        elementsStore.ShowOverlay('An unexpected error occurred!', 'red', null, null)
      }
    }
  }
}

const deleteAttendance = async(index:number, date:string)=>{
  const formData = new FormData
  formData.append('className', className)
  formData.append('year', userAuthStore.activeAcademicYear)
  formData.append('date', date)
  formData.append('type', 'delete')
  formData.append('term', userAuthStore.activeTerm.toString())
  elementsStore.ShowLoadingOverlay()
  try {
    await axiosInstance.post('teacher/students/attendance', formData)
    userAuthStore.teacherData.studentsattendance?.[classIndex]?.attendances?.splice(index, 1)
    elementsStore.HideLoadingOverlay()
  }
  catch(error) {
    elementsStore.HideLoadingOverlay()
    if (error instanceof AxiosError){
      if(error.response){
        if (error.response.status === 400 && error.response.data.message){
          elementsStore.ShowOverlay(error.response.data.message, 'red', null, null)
        }else{
          elementsStore.ShowOverlay('Oops! something went wrong. Try again later', 'red', null, null)
        }
      }
      else if (!error.response && (error.code === 'ECONNABORTED' || !navigator.onLine)){
        elementsStore.ShowOverlay('A network error occurred! Please check you internet connection', 'red', null, null)
      }
      else{
        elementsStore.ShowOverlay('An unexpected error occurred!', 'red', null, null)
      }
    }
  }
}

const showOverlay = (element:string)=>{
  const overlay = document.getElementById(element)
  overlay ? overlay.style.display = 'flex' : null
}

const hidOverlay = (element:string)=>{
  const overlay = document.getElementById(element)
  overlay ? overlay.style.display = "none" : null

  selectedStudents.value  = null
  attendanceUploadDate.value = null
  formErrorMessage.value = ''
}

const checkInput = computed(()=>{
  return !(attendanceUploadDate.value)
})

</script>

<template>
  <div class="content-wrapper" v-show="elementsStore.activePage ===`TeacherStudentsAttendance,${className},${classIndex}` ">
    <!-- Attendance overlay -->
      <div :id="`studentAttendanceOverlay${className}${classIndex}`" class="overlay" v-if="userAuthStore.teacherData.studentsattendance?.length > 0">
        <div class="overlay-card attendance-upload">
            <v-btn @click="hidOverlay(`studentAttendanceOverlay${className}${classIndex}`)" color="red" size="small" class="close-btn" variant="flat">X</v-btn>
            <p class="form-message" style="color: red" v-if="formErrorMessage">{{ formErrorMessage }}</p>
            <v-text-field
            label="DATE"
            class="input-field"
            v-model="attendanceUploadDate"
            hint="select the date for the class attendance"
            persistent-hint
            clearable
            variant="solo-filled"
            type="date"
            density="compact"
            />
            <v-select v-if="students" clearable multiple chips v-model="selectedStudents" class="select" label="STUDENTS" 
            :items="students" item-title="name" item-value="st_id" variant="solo-filled" density="comfortable" persistent-hint hint="Select the students who did not attend class for the specified date">
              <template v-slot:item="{ props, item }">
                  <v-list-item v-bind="props" :subtitle="item.raw.st_id"></v-list-item>
              </template>
            </v-select>
            <v-btn :disabled="checkInput" @click="uploadAttendance" size="small" variant="flat" color="black"  class="mb-5" type="submit">UPLOAD</v-btn>
          </div>
      </div>

      <!-- Analytics overlay -->
      <div :id="`teacherStudentsAttendanceAnalyticsOverlay${className}${classIndex}`" class="overlay" v-if="userAuthStore.teacherData.studentsattendance?.length > 0" >
        <div class="overlay-card flex-all-c">
          <v-btn class="close-btn" @click="hidOverlay(`teacherStudentsAttendanceAnalyticsOverlay${className}${classIndex}`)" size="small" variant="flat" color="red" >X</v-btn>
          <div class="chart-info-wrapper flex-all-c">
            <v-list class="info-container">
              <v-list-item class="nav-title nav-link" @click="changeAnalysis('year')">
                {{ academic_year }}
              </v-list-item>
              <v-list-group v-for="(month, index) in attendances" :key="index">
                <template v-slot:activator="{ props }">
                    <v-list-item v-bind="props" prepend-icon="mdi-calendar" class="nav-item">
                       {{ month['month'] }}
                    </v-list-item>
                </template>
                <v-list-item class="nav-title nav-link" @click="changeAnalysis('month', month['month'])">
                  {{ month['month'] }}
                </v-list-item>
                <v-list-item class="nav-title nav-link" v-for="(week, ind) in month['weeks']" :key="ind" @click="changeAnalysis('week', month['month'], week['week'])">
                    {{ week['week'] }}
                </v-list-item>
              </v-list-group>
            </v-list>
            <div class="chart-container flex-all-c">
              <Bar
              class="chart"
              :options="chartOptions"
              :data="chartData"
              />
            </div>
          </div>
        </div>
      </div>
      <div class="content-header" v-if="userAuthStore.teacherData.studentsattendance?.length > 0 ">
        <span class="content-header-title">{{ className}} STUDENTS ATTENDANCE FOR THE {{ academic_year }} ACADEMIC YEAR</span>
      </div>
      <div class="content-header btn-container" v-if="userAuthStore.teacherData.studentsattendance?.length > 0 ">
        <v-btn class="mr-3" @click="showOverlay(`studentAttendanceOverlay${className}${classIndex}`)" :size="elementsStore.btnSize1" color="blue" varaint="flat" >ADD ATTENDANCE</v-btn>
        <v-btn class="ml-3" @click="showOverlay(`teacherStudentsAttendanceAnalyticsOverlay${className}${classIndex}`)" :size="elementsStore.btnSize1" color="blue" varaint="flat" >SUMMARY</v-btn>
      </div>
      <h4 class="no-data" v-if="userAuthStore.teacherData.studentsattendance?.[classIndex]?.attendances?.length === 0 ">
        <p>No data yet</p>
      </h4>
      <v-table class="table" fixed-header v-if="userAuthStore.teacherData.studentsattendance?.[classIndex]?.attendances?.length > 0">
        <thead>
        <tr>
          <th class="table-head">DATE</th>
          <th class="table-head">STUDENTS PRESENT</th>
          <th class="table-head">STUDENTS ABSENT</th>
          <th class="table-head">ACTION</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(attend, index) in userAuthStore.teacherData.studentsattendance[classIndex].attendances" :key="index">
          <td class="table-data">{{attend['date']}}</td>
          <td style=" padding: 0">
            <v-list class="pa-0">
              <v-list-group>
                <template v-slot:activator="{ props }">
                  <v-list-item class="title" v-bind="props">
                    <v-icon icon="mdi-account-circle" />{{attend['students_present'].length}} STUDENTS
                  </v-list-item>
                </template>
                  <v-virtual-scroll class="v-scroll" height="22vh" :items="attend['students_present']">
                    <template v-slot:default="{ item }" >
                      <v-list-item style="position: relative">
                        <v-list-item-title>
                          <p class="user-name">{{ item['user']['first_name'] }} {{item['user']['last_name']}}</p>
                        </v-list-item-title>
                        <v-list-item-subtitle>
                          <p class="user-name">{{item['st_id']}}</p>
                        </v-list-item-subtitle>
                      </v-list-item>
                    </template>
                  </v-virtual-scroll>
              </v-list-group>
            </v-list>
          </td>
          <td style="padding: 0">
            <v-list class="pa-0">
              <v-list-group>
                <template v-slot:activator="{ props }">
                  <v-list-item class="title" v-bind="props">
                    <v-icon icon="mdi-account-circle" />{{attend['students_absent'].length}} STUDENTS
                  </v-list-item>
                </template>
                  <v-virtual-scroll class="v-scroll" height="22vh" :items="attend['students_absent']">
                    <template v-slot:default="{ item }" >
                      <v-list-item style="position: relative">
                        <v-list-item-title>
                          <p class="user-name">{{ item['user']['first_name'] }} {{item['user']['last_name']}}</p>
                        </v-list-item-title>
                        <v-list-item-subtitle>
                          <p class="user-name">{{item['st_id']}}</p>
                        </v-list-item-subtitle>
                      </v-list-item>
                    </template>
                  </v-virtual-scroll>
              </v-list-group>
            </v-list>
          </td>
          <td class="table-data">
            <v-btn @click="elementsStore.ShowDeletionOverlay(()=> deleteAttendance(index, attend['date']))" variant="flat" icon="mdi-delete" size="x-small" color="red"/>
          </td>
        </tr>
        </tbody>
      </v-table>
  </div>
</template>

<style scoped>

.content-header{
  min-height: 15% !important;
}
.btn-container{
  min-height: 10% !important;
}
.table{
  height: 75% !important;
}
.overlay-card{
  max-width: 1200px !important;
  height: 80% !important;
  max-height: 1000px !important;
}
.chart-info-wrapper {
  height: 93% !important;
  width: 100%;
  padding-left: .5em;
  padding-right: .5em;
  margin-top: .5em;
  align-items: flex-start !important;
  overflow: hidden;
}
.info-container{
  height: 25% !important;
  background-color: #333333;
  width: 100%;
  overflow-y: auto;
}
.nav-item, .nav-title{
  min-height: 35px !important;
}
.chart-container{
  height: 75% !important;
  margin-top: .5em;
  width: 100%;
  margin-right: .5em !important;
}
.attendance-upload{
  max-width: 600px !important;
  height: 80% !important;
  max-height: 450px !important;
}
@media screen and (min-width: 360px) {
  .content-header{
    min-height: 10% !important;
  }
  .table{
    height: 80% !important;
  }

}
@media screen and (min-width: 576px) {
  .overlay-card{
    height: 90% !important;
    width: 95% !important;
  }
}
@media screen and (min-width: 767px) {
  .content-header{
    min-height: 15% !important;
  }
  .btn-container{
    min-height: 10% !important;
  }
  .table{
    height: 75% !important;
  }
  .overlay-card{
    height: 95% !important;
  }
}
@media screen and (min-width: 1200px) {
  .content-header-title{
    font-size: 1.2rem !important;
  }
  .content-header{
    min-height: 15% !important;
  }
  .btn-container{
    min-height: 15% !important;
  }
  .table{
    height: 70% !important;
  }
}


</style>


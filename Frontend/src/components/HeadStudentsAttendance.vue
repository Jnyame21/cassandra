<script setup lang="ts">
import 'chart.js/auto'
import { getAttendanceData, getWeekNumberInMonth } from '@/utils/util';
import { Bar } from 'vue-chartjs';
import { useUserAuthStore } from '@/stores/userAuthStore'
import { useElementsStore } from '@/stores/elementsStore'
import { defineProps, computed, watch, ref } from 'vue'
import NoData from './NoData.vue';

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()
const currentLabels: any = ref([])
const currentDatasets: any = ref([])
const academic_year = userAuthStore.activeAcademicYear
const academic_term = userAuthStore.activeTerm
const academicTermStartDate = new Date(
  academic_term === 1
    ? userAuthStore.userData['academic_year']['start_date']
    : academic_term === 2
    ? userAuthStore.userData['academic_year']['term_2_start_date']
    : userAuthStore.userData['academic_year']['term_3_start_date']
);

const academicTermEndDate = new Date(
  academic_term === 1
    ? userAuthStore.userData['academic_year']['term_1_end_date']
    : academic_term === 2
    ? userAuthStore.userData['academic_year']['term_2_end_date']
    : userAuthStore.userData['academic_year']['term_3_end_date']
);

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
}

const props = defineProps<Props>()
const className = props.className

const attendances = ref(getAttendanceData(academicTermStartDate, academicTermEndDate))

const attendanceData = computed(()=>{
  return userAuthStore.headData.studentsAttendance[className]
})

const changeAnalysis = (type: string, month: string = '', week: string = '') => {
  currentLabels.value = []
  currentDatasets.value = []
  const labelName = ref('')
  if (type === 'year') {
    attendances.value.forEach(item => {
      currentLabels.value.push(item['month'])
      currentDatasets.value.push(item['studentsPresent'])
    })
    labelName.value = 'TOTAL ATTENDANCE'
  }
  else if (type === 'month') {
    const attendanceMonth = attendances.value.find(item => item['month'] === month)
    if (attendanceMonth) {
      attendanceMonth['weeks'].forEach((item: any) => {
        currentLabels.value.push(item['week'])
        currentDatasets.value.push(item['studentsPresent'])
      })
      labelName.value = 'TOTAL ATTENDANCE'
    }
  }
  else if (type === 'week') {
    const attendanceMonth = attendances.value.find(item => item['month'] === month)
    if (attendanceMonth) {
      const attendanceWeek = attendanceMonth['weeks'].find((item: any) => item['week'] === week)
      if (attendanceWeek) {
        attendanceWeek['days'].forEach((item: any) => {
          currentLabels.value.push(item['day'])
          currentDatasets.value.push(item['studentsPresent'])
        })
        labelName.value = 'STUDENTS PRESENT'
      }
    }
  }
  if (currentLabels.value.length === 0) {
    labelName.value = 'NO DATA'
  }
  else if (currentDatasets.value.every((item: any) => item === 0)) {
    labelName.value = 'NO DATA'
  }
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

watch(() => userAuthStore.headData.studentsAttendance[className], (newValue) => {
  if (newValue) {
    attendances.value = getAttendanceData(academicTermStartDate, academicTermEndDate)
    let date: any = null
    let dayName = ''
    let weekNumber = 0
    let monthName = ''
    let numberOfStudentsPresents = 0
    if (newValue.length > 0) {
      newValue.forEach((item: any) => {
        numberOfStudentsPresents = item.students_present.length
        date = new Date(item.date.toString())
        dayName = date.toLocaleString('default', { 'weekday': 'short' })
        weekNumber = getWeekNumberInMonth(date)
        monthName = date.toLocaleString('default', { 'month': 'long' }).toUpperCase()
        const attendanceMonth = attendances.value.find(month => month.month === monthName)
        if (attendanceMonth) {
          const monthIndex = attendances.value.indexOf(attendanceMonth)
          attendances.value[monthIndex].studentsPresent += numberOfStudentsPresents
          const attendanceWeek = attendanceMonth.weeks.find(week => week.week.split(' ')[1] === weekNumber.toString())
          if (attendanceWeek) {
            const attendanceWeekIndex = attendanceMonth.weeks.indexOf(attendanceWeek)
            attendances.value[monthIndex].weeks[attendanceWeekIndex].studentsPresent += numberOfStudentsPresents
            const attendanceDay = attendanceWeek.days.find(day => day.day.split('(')[0] === dayName.toUpperCase())
            if (attendanceDay) {
              const attendanceDayIndex = attendanceWeek.days.indexOf(attendanceDay)
              attendances.value[monthIndex].weeks[attendanceWeekIndex].days[attendanceDayIndex].studentsPresent += numberOfStudentsPresents
            }
          }
        }
      })
      changeAnalysis('year')
    }
    else {
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
}, { 'immediate': true, 'deep': 1 })

const showOverlay = (element: string) => {
  const overlay = document.getElementById(element)
  if (overlay) {
    overlay.style.display = 'flex'
  }
}

const hidOverlay = (element: string) => {
  const overlay = document.getElementById(element)
  if (overlay) {
    overlay.style.display = "none"
  }
}


</script>

<template>
  <div class="content-wrapper" v-show="elementsStore.activePage === `HeadStudentsAttendance,${className}`" :class="{ 'is-active-page': elementsStore.activePage === `HeadStudentsAttendance,${className}` }">
    
    <!-- Analytics overlay -->
    <div :id="`HeadStudentsAttendanceAnalyticsOverlay${className}`" class="overlay">
      <div class="overlay-card flex-all-c">
        <v-btn class="close-btn" @click="hidOverlay(`HeadStudentsAttendanceAnalyticsOverlay${className}`)" size="small" variant="flat" color="red">
          X
        </v-btn>
        <div class="chart-info-wrapper flex-all-c">
          <v-list class="info-container">
            <v-list-item class="nav-title nav-link" @click="changeAnalysis('year')">
              {{ userAuthStore.userData['academic_year']['period_division'] }} {{ academic_term }}
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
              <v-list-item class="nav-title nav-link" v-for="(week, ind) in month['weeks']" :key="ind"
                @click="changeAnalysis('week', month['month'], week['week'])">
                {{ week['week'] }}
              </v-list-item>
            </v-list-group>
          </v-list>
          <div class="chart-container flex-all-c">
            <Bar class="chart" :options="chartOptions" :data="chartData" />
          </div>
        </div>
      </div>
    </div>

    <div class="content-header">
      <span class="content-header-title">{{ className }} STUDENTS ATTENDANCE FOR THE {{ academic_year }} ACADEMIC YEAR {{ userAuthStore.userData['academic_year']['period_division'] }} {{ userAuthStore.activeTerm }}</span>
    </div>
    <div class="content-header btn-container">
      <v-btn class="ml-3" @click="showOverlay(`HeadStudentsAttendanceAnalyticsOverlay${className}`)" :size="elementsStore.btnSize1" color="blue" varaint="flat">
        SUMMARY
      </v-btn>
    </div>
    <NoData message="NO DATA" v-if="attendanceData.length === 0" />
    <v-table class="table" fixed-header v-if="attendanceData.length > 0">
      <thead>
        <tr>
          <th class="table-head">DATE</th>
          <th class="table-head">STUDENTS PRESENT</th>
          <th class="table-head">STUDENTS ABSENT</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(_attendance, index) in attendanceData" :key="index">
          <td class="table-data">{{ _attendance.date }}</td>
          <td style=" padding: 0">
            <v-list class="pa-0">
              <v-list-group>
                <template v-slot:activator="{ props }">
                  <v-list-item class="title" v-bind="props">
                    <v-icon icon="mdi-account-circle" />{{ _attendance.students_present.length }} STUDENTS
                  </v-list-item>
                </template>
                <v-virtual-scroll class="v-scroll" height="22vh" :items="_attendance.students_present">
                  <template v-slot:default="{ item }">
                    <v-list-item style="position: relative">
                      <v-list-item-title>
                        <p class="user-name">{{ item.user }}</p>
                      </v-list-item-title>
                      <v-list-item-subtitle>
                        <p class="user-name">{{ item.st_id }}</p>
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
                    <v-icon icon="mdi-account-circle" />{{ _attendance['students_absent'].length }} STUDENTS
                  </v-list-item>
                </template>
                <v-virtual-scroll class="v-scroll" height="22vh" :items="_attendance.students_absent">
                  <template v-slot:default="{ item }">
                    <v-list-item style="position: relative">
                      <v-list-item-title>
                        <p class="user-name">{{ item.user }}</p>
                      </v-list-item-title>
                      <v-list-item-subtitle>
                        <p class="user-name">{{ item.st_id }}</p>
                      </v-list-item-subtitle>
                    </v-list-item>
                  </template>
                </v-virtual-scroll>
              </v-list-group>
            </v-list>
          </td>
        </tr>
      </tbody>
    </v-table>
  </div>
</template>

<style scoped>

.content-header {
  min-height: 15% !important;
}
.btn-container {
  min-height: 10% !important;
}
.overlay-card {
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
.info-container {
  height: 25% !important;
  background-color: #333333;
  width: 100%;
  overflow-y: auto;
}
.nav-item,
.nav-title {
  min-height: 35px !important;
}
.chart-container {
  height: 75% !important;
  margin-top: .5em;
  width: 100%;
  margin-right: .5em !important;
}

@media screen and (min-width: 576px) {
  .overlay-card {
    height: 90% !important;
    width: 95% !important;
  }
}

@media screen and (min-width: 767px) {
  .overlay-card {
    height: 95% !important;
  }
}

@media screen and (min-width: 1200px) {
  .content-header-title {
    font-size: 1.2rem !important;
  }
}


</style>

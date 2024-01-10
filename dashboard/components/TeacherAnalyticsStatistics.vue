
<script setup lang="ts">
import 'chart.js/auto'
import { Bar } from 'vue-chartjs'
import { defineProps, ref, computed } from 'vue'

interface student {
    score: number;
    [key: string]: any;
}

interface Props {
    studentsData: student[];
}

const { studentsData } = defineProps<Props>()


const userAuthStore = useUserAuthStore()
// Chart
const first5 = ref(studentsData.slice(0, 5))
const last5 = ref(studentsData.slice(-5))
const gradeA1 = ref(studentsData.filter(student => student.score >=80))
const gradeB2 = ref(studentsData.filter(student => student.score >=75 && student.score <80))
const gradeB3 = ref(studentsData.filter(student => student.score >=70 && student.score <75))
const gradeC4 = ref(studentsData.filter(student => student.score >=65 && student.score <70))
const gradeC5 = ref(studentsData.filter(student => student.score >=60 && student.score <65))
const gradeC6 = ref(studentsData.filter(student => student.score >=55 && student.score <60))
const gradeD7 = ref(studentsData.filter(student => student.score >=50 && student.score <55))
const gradeE8 = ref(studentsData.filter(student => student.score >=40 && student.score <50))
const gradeF9 = ref(studentsData.filter(student => student.score <40))

const labels = ref(['A1', 'B2', 'B3', 'C4', 'C5', 'C6', 'D7', 'E8', 'F9'])
const points = ref([gradeA1.value.length, gradeB2.value.length, gradeB3.value.length, gradeC4.value.length, gradeC5.value.length, gradeC6.value.length, gradeD7.value.length, gradeE8.value.length, gradeF9.value.length])

const chartData = ref({
    labels: labels.value,
    datasets: [
    {
      label: 'Number of Students',
      data: points.value,
      borderColor: 'rgba(75, 192, 192, 1)',
      borderWidth: 2,
      fill: false,
    },
  ],
})


const chartOptions = ref({
    responsive: true,
})


const studentsScore = ref(studentsData.map(student => Number(student.score)))
const sum = ref(studentsScore.value.reduce((acc, sc) => acc + sc , 0))
const st_len = ref(studentsScore.value.length)
const avg_score = ref((sum.value/st_len.value).toFixed(2))
const max_score = ref(Math.max(...studentsScore.value))
const min_score = ref(Math.min(...studentsScore.value))
const passedCount = computed(()=>{
    return studentsScore.value.filter(sc => sc >= 50).length
})
const failedCount = computed(()=>{
    return studentsScore.value.filter(sc => sc < 50).length
})
const st_A = computed(()=>{
    return studentsScore.value.filter(sc => sc >= 80).length
})
const st_B = computed(()=>{
    return studentsScore.value.filter(sc => sc >= 70 && sc < 80).length
})
const st_C = computed(()=>{
    return studentsScore.value.filter(sc => sc >= 60 && sc < 70).length
})
const st_D = computed(()=>{
    return studentsScore.value.filter(sc => sc >= 50 && sc < 60).length
})

</script>

<template>
<div class="flex-all-c w-100">
    <p v-if="userAuthStore.userData && userAuthStore.userData['school']['semesters']" class="notice"><span style="color: red">NOTE: </span>This analytics is based on SEMESTER {{userAuthStore.activeTerm}} of the {{userAuthStore.activeAcademicYear}} academic year.</p>
    <p v-if="userAuthStore.userData && !userAuthStore.userData['school']['semesters']" class="notice"><span style="color: red">NOTE: </span>This analytics is based on TRIMESTER {{userAuthStore.activeTerm}} of the {{userAuthStore.activeAcademicYear}} academic year.</p>
    <Bar
        class="chart"
        :options="chartOptions"
        :data="chartData"
        :fill="false"
    />
    <div class="table-container">
        <v-table class="analytics-table" density="comfortable">
            <tbody>
                <tr>
                    <td class="table-data">Total Students</td>
                    <td class="table-data-value">{{studentsScore.length}}</td>
                </tr>
                <tr>
                    <td class="table-data">Highest Score</td>
                    <td class="table-data-value">{{max_score}}</td>
                </tr>
                <tr>
                    <td class="table-data">Average Score</td>
                    <td class="table-data-value">{{avg_score}}</td>
                </tr>
                <tr>
                    <td class="table-data">Lowest Score</td>
                    <td class="table-data-value">{{min_score}}</td>
                </tr>
                <tr>
                    <td class="table-data">Grade A Students (>=80)</td>
                    <td class="table-data-value">{{st_A}} ({{ ((st_A/studentsScore.length)*100).toFixed(2) }}%)</td>
                </tr>
                <tr>
                    <td class="table-data">Grade B Students (70-79)</td>
                    <td class="table-data-value">{{st_B}} ({{ ((st_B/studentsScore.length)*100).toFixed(2) }}%)</td>
                </tr>
                <tr>
                    <td class="table-data">Grade C Students (60-69)</td>
                    <td class="table-data-value">{{st_C}} ({{ ((st_C/studentsScore.length)*100).toFixed(2) }}%)</td>
                </tr>
                <tr>
                    <td class="table-data">Grade D Students (50-59)</td>
                    <td class="table-data-value">{{st_D}} ({{ ((st_D/studentsScore.length)*100).toFixed(2) }}%)</td>
                </tr>
                <tr>
                    <td class="table-data">Passed Students (>=50)</td>
                    <td class="table-data-value">{{passedCount}} ({{ ((passedCount/studentsScore.length)*100).toFixed(2) }}%)</td>
                </tr>
                <tr>
                    <td class="table-data">Failed Students (&lt;50)</td>
                    <td class="table-data-value">{{failedCount}} ({{ ((failedCount/studentsScore.length)*100).toFixed(2) }}%)</td>
                </tr>
                <tr v-if="studentsScore.length > 10" class="table-title-container" style="position: relative">
                    <td>Justice</td>
                    <td class="table-title">top 5 students</td>
                </tr>
                <tr v-for="(st, i) in first5" :key="i">
                    <td v-if="studentsScore.length > 10" class="table-data">{{ st['student']['user']['first_name']}} {{ st['student']['user']['last_name']}}[{{ st['student']['st_id']}}]</td>
                    <td v-if="studentsScore.length > 10" class="table-data-value">{{st['score']}}</td>
                </tr>
                <tr v-if="studentsScore.length > 10" class="table-title-container" style="position: relative">
                    <td>Justice</td>
                    <td class="table-title">last 5 students</td>
                </tr>
                <tr v-for="(st, i) in last5" :key="i">
                    <td v-if="studentsScore.length > 10" class="table-data">{{ st['student']['user']['first_name']}} {{ st['student']['user']['last_name']}}[{{ st['student']['st_id']}}]</td>
                    <td v-if="studentsScore.length > 10" class="table-data-value">{{st['score']}}</td>
                </tr>
            </tbody>
        </v-table>
    </div>
</div>
</template>

<style scoped>

@import url('../assets/css/tables.css');

.chart{
    max-width: 800px !important;
    max-height: 300px !important;
    margin-top: 1em;

}
.analytics-table{
    margin-bottom: 2em;
    
}
.table-container{
    margin-top: 3em;
    overflow: hidden;
    max-width: 600px !important;
    width: 100%;
    border: 1px solid whitesmoke;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.notice{
    font-size: .5rem;
    text-align: center;
    margin-top: 2em;
}

@media screen and (min-width: 576px) {

    .notice{
        font-size: .6rem;
    }    
}
@media screen and (min-width: 767px) {

    .notice{
        font-size: .7rem;
    }    
}

</style>
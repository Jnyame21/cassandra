
<script setup lang="ts">
import 'chart.js/auto'
import { Bar } from 'vue-chartjs'
import { defineProps, ref, computed } from 'vue'
import TheLoader from './TheLoader.vue';

interface student {
    score: number;
    [key: string]: any;
}

interface Props {
    year: {
        term_one: student[];
        term_two: student[];
        term_three: student[];
    }
}
const { year } = defineProps<Props>()

const termOneTotal = ref(year['term_one']).value.length
const termTwoTotal = ref(year['term_two']).value.length
const termThreeTotal = ref(year['term_three']).value.length
const userAuthStore = useUserAuthStore()


// Graph Data

// Term One
const termOneGradeA1 = computed(()=>{
    const gradeA1 = ref(year['term_one'].filter(student => student.score >=80 )).value.length
    return ((gradeA1 / termOneTotal)*100).toFixed(1)
})
const termOneGradeB2 = computed(()=>{
    const gradeB2 = ref(year['term_one'].filter(student => student.score >=75 && student.score <80 )).value.length
    return ((gradeB2 / termOneTotal)*100).toFixed(1)
})
const termOneGradeB3 = computed(()=>{
    const gradeB3 = ref(year['term_one'].filter(student => student.score >=70 && student.score <75 )).value.length
    return ((gradeB3 / termOneTotal)*100).toFixed(1)
})
const termOneGradeC4 = computed(()=>{
    const gradeC4 = ref(year['term_one'].filter(student => student.score >=65 && student.score <70 )).value.length
    return ((gradeC4 / termOneTotal)*100).toFixed(1)
})
const termOneGradeC5 = computed(()=>{
    const gradeC5 = ref(year['term_one'].filter(student => student.score >=60 && student.score <65 )).value.length
    return ((gradeC5 / termOneTotal)*100).toFixed(1)
})
const termOneGradeC6 = computed(()=>{
    const gradeC6 = ref(year['term_one'].filter(student => student.score >=55 && student.score <60 )).value.length
    return ((gradeC6 / termOneTotal)*100).toFixed(1)
})
const termOneGradeD7 = computed(()=>{
    const gradeD7 = ref(year['term_one'].filter(student => student.score >=50 && student.score <55 )).value.length
    return ((gradeD7 / termOneTotal)*100).toFixed(1)
})
const termOneGradeE8 = computed(()=>{
    const gradeE8 = ref(year['term_one'].filter(student => student.score >=40 && student.score <50 )).value.length
    return ((gradeE8 / termOneTotal)*100).toFixed(1)
})
const termOneGradeF9 = computed(()=>{
    const gradeF9 = ref(year['term_one'].filter(student => student.score <40 )).value.length
    return ((gradeF9 / termOneTotal)*100).toFixed(1)
})


// Term Two
const termTwoGradeA1 = computed(()=>{
    const gradeA1 = ref(year['term_two'].filter(student => student.score >=80 )).value.length
    return ((gradeA1 / termTwoTotal)*100).toFixed(1)
})
const termTwoGradeB2 = computed(()=>{
    const gradeB2 = ref(year['term_two'].filter(student => student.score >=75 && student.score <80 )).value.length
    return ((gradeB2 / termTwoTotal)*100).toFixed(1)
})
const termTwoGradeB3 = computed(()=>{
    const gradeB3 = ref(year['term_two'].filter(student => student.score >=70 && student.score <75 )).value.length
    return ((gradeB3 / termTwoTotal)*100).toFixed(1)
})
const termTwoGradeC4 = computed(()=>{
    const gradeC4 = ref(year['term_two'].filter(student => student.score >=65 && student.score <70 )).value.length
    return ((gradeC4 / termTwoTotal)*100).toFixed(1)
})
const termTwoGradeC5 = computed(()=>{
    const gradeC5 = ref(year['term_two'].filter(student => student.score >=60 && student.score <65 )).value.length
    return ((gradeC5 / termTwoTotal)*100).toFixed(1)
})
const termTwoGradeC6 = computed(()=>{
    const gradeC6 = ref(year['term_two'].filter(student => student.score >=55 && student.score <60 )).value.length
    return ((gradeC6 / termTwoTotal)*100).toFixed(1)
})
const termTwoGradeD7 = computed(()=>{
    const gradeD7 = ref(year['term_two'].filter(student => student.score >=50 && student.score <55 )).value.length
    return ((gradeD7 / termTwoTotal)*100).toFixed(1)
})
const termTwoGradeE8 = computed(()=>{
    const gradeE8 = ref(year['term_two'].filter(student => student.score >=40 && student.score <50 )).value.length
    return ((gradeE8 / termTwoTotal)*100).toFixed(1)
})
const termTwoGradeF9 = computed(()=>{
    const gradeF9 = ref(year['term_two'].filter(student => student.score <40 )).value.length
    return ((gradeF9 / termTwoTotal)*100).toFixed(1)
})

// Term Three
const termThreeGradeA1 = computed(()=>{
    const gradeA1 = ref(year['term_three'].filter(student => student.score >=80 )).value.length
    return ((gradeA1 / termThreeTotal)*100).toFixed(1)
})
const termThreeGradeB2 = computed(()=>{
    const gradeB2 = ref(year['term_three'].filter(student => student.score >=75 && student.score <80 )).value.length
    return ((gradeB2 / termThreeTotal)*100).toFixed(1)
})
const termThreeGradeB3 = computed(()=>{
    const gradeB3 = ref(year['term_three'].filter(student => student.score >=70 && student.score <75 )).value.length
    return ((gradeB3 / termThreeTotal)*100).toFixed(1)
})
const termThreeGradeC4 = computed(()=>{
    const gradeC4 = ref(year['term_three'].filter(student => student.score >=65 && student.score <70 )).value.length
    return ((gradeC4 / termThreeTotal)*100).toFixed(1)
})
const termThreeGradeC5 = computed(()=>{
    const gradeC5 = ref(year['term_three'].filter(student => student.score >=60 && student.score <65 )).value.length
    return ((gradeC5 / termThreeTotal)*100).toFixed(1)
})
const termThreeGradeC6 = computed(()=>{
    const gradeC6 = ref(year['term_three'].filter(student => student.score >=55 && student.score <60 )).value.length
    return ((gradeC6 / termThreeTotal)*100).toFixed(1)
})
const termThreeGradeD7 = computed(()=>{
    const gradeD7 = ref(year['term_three'].filter(student => student.score >=50 && student.score <55 )).value.length
    return ((gradeD7 / termThreeTotal)*100).toFixed(1)
})
const termThreeGradeE8 = computed(()=>{
    const gradeE8 = ref(year['term_three'].filter(student => student.score >=40 && student.score <50 )).value.length
    return ((gradeE8 / termThreeTotal)*100).toFixed(1)
})
const termThreeGradeF9 = computed(()=>{
    const gradeF9 = ref(year['term_three'].filter(student => student.score <40 )).value.length
    return ((gradeF9 / termThreeTotal)*100).toFixed(1)
})


const labels = ref(['A1', 'B2', 'B3', 'C4', 'C5', 'C6', 'D7', 'E8', 'F9'])
const termOnePoints = ref([termOneGradeA1.value, termOneGradeB2.value, termOneGradeB3.value, termOneGradeC4.value, termOneGradeC5.value, termOneGradeC6.value, termOneGradeD7.value, termOneGradeE8.value, termOneGradeF9.value])
const termTwoPoints = ref([termTwoGradeA1.value, termTwoGradeB2.value, termTwoGradeB3.value, termTwoGradeC4.value, termTwoGradeC5.value, termTwoGradeC6.value, termTwoGradeD7.value, termTwoGradeE8.value, termTwoGradeF9.value])
const termThreePoints = ref([termThreeGradeA1.value, termThreeGradeB2.value, termThreeGradeB3.value, termThreeGradeC4.value, termThreeGradeC5.value, termThreeGradeC6.value, termThreeGradeD7.value, termThreeGradeE8.value, termThreeGradeF9.value])


const chartData1 = ref({
    labels: labels.value,
    datasets: [
    {
      label: 'Semester 1 Rate(%)',
      data: termOnePoints.value,
      borderColor: 'green',
      backgroundColor: 'green',
      borderWidth: 2,
      fill: false,
    },
    {
      label: 'Semester 2 Rate(%)',
      data: termTwoPoints.value,
      borderColor: 'blue',
      backgroundColor: 'blue',
      borderWidth: 2,
      fill: false,
    },
  ],
})

const chartData2 = ref({
    labels: labels.value,
    datasets: [
    {
      label: 'Trimester 1 Rate(%)',
      data: termOnePoints.value,
      borderColor: 'green',
      backgroundColor: 'green',
      borderWidth: 2,
      fill: false,
    },
    {
      label: 'Trimester 2 Rate(%)',
      data: termTwoPoints.value,
      borderColor: 'blue',
      backgroundColor: 'blue',
      borderWidth: 2,
      fill: false,
    },
    {
      label: 'Trimester 3 Rate(%)',
      data: termThreePoints.value,
      borderColor: 'indigo',
      backgroundColor: 'indigo',
      borderWidth: 2,
      fill: false,
    },
  ],
})


const chartOptions = ref({
    responsive: true,
})

// Table data

// Term One
const termOneScores = ref(year['term_one'].map(student => student.score))

const termOneAvgScore = computed(()=>{
    const sum = termOneScores.value.reduce((sum, current) => sum + current, 0)
    return (sum / termOneScores.value.length).toFixed(0)
})

const termOneMaxScore = computed(()=>{
    return Math.max(...termOneScores.value)
})

const termOneMinScore = computed(()=>{
    return Math.min(...termOneScores.value)
})

const termOnePass = computed(()=>{
    return year['term_one'].filter(student => student['score'] >= 50).length
})
const termOneWeakPass = computed(()=>{
    return year['term_one'].filter(student => student['score'] < 50  && student['score'] >=40).length
})
const termOneFail = computed(()=>{
    return year['term_one'].filter(student => student['score'] < 40).length
})

// Term Two
const termTwoScores = ref(year['term_two'].map(student => student.score))

const termTwoAvgScore = computed(()=>{
    const sum = termTwoScores.value.reduce((sum, current) => sum + current, 0)
    return (sum / termTwoScores.value.length).toFixed(0)
})

const termTwoMaxScore = computed(()=>{
    return Math.max(...termTwoScores.value)
})
const termTwoMinScore = computed(()=>{
    return Math.min(...termTwoScores.value)
})

const termTwoPass = computed(()=>{
    return year['term_two'].filter(student => student['score'] >= 50).length
})
const termTwoWeakPass = computed(()=>{
    return year['term_two'].filter(student => student['score'] < 50  && student['score'] >=40).length
})
const termTwoFail = computed(()=>{
    return year['term_two'].filter(student => student['score'] < 40).length
})

// Term Three
const termThreeScores = ref(year['term_three'].map(student => student.score))

const termThreeAvgScore = computed(()=>{
    const sum = termThreeScores.value.reduce((sum, current) => sum + current, 0)
    return (sum / termThreeScores.value.length).toFixed(0)
})

const termThreeMaxScore = computed(()=>{
    return Math.max(...termThreeScores.value)
})

const termThreeMinScore = computed(()=>{
    return Math.min(...termThreeScores.value)
})

const termThreePass = computed(()=>{
    return year['term_three'].filter(student => student['score'] >= 50).length
})
const termThreeWeakPass = computed(()=>{
    return year['term_three'].filter(student => student['score'] < 50  && student['score'] >=40).length
})
const termThreeFail = computed(()=>{
    return year['term_three'].filter(student => student['score'] < 40).length
})


</script>

<template>
<div class="flex-all-c w-100 h-100">
    <TheLoader v-if="!year || year && year['term_one'].length ===0" />

    <Bar
    v-if="year && userAuthStore.userData['school']['semesters']  && year['term_one'].length >0 || year && !userAuthStore.userData['academic_year']['sem_3_start_date'] && year['term_two'].length >0 "
    class="chart"
    :options="chartOptions"
    :data="chartData1"
    :fill="false"
    />

    <Bar
    v-if="year && !userAuthStore.userData['school']['semesters']  && year['term_one'].length >0 || year && userAuthStore.userData['academic_year']['sem_3_start_date'] && year['term_two'].length >0 || year && userAuthStore.userData['academic_year']['sem_3_start_date'] && year['term_three'].length >0"
    class="chart"
    :options="chartOptions"
    :data="chartData2"
    :fill="false"
    />

    <div class="table-container">

        <!-- Term Three -->
        <div class="term-table" v-if="year['term_three'] && year['term_three'].length >0">
            <v-table density="comfortable">
                <tbody >
                    <tr class="term-three table-title-container" style="position: relative">
                        <td>Justice</td>
                        <td class="table-title term-three" v-if="!userAuthStore.userData['school']['semesters']">trimester 3</td>
                    </tr>
                    <tr class="term-three">
                        <td class="table-data">Highest Score</td>
                        <td class="table-data-value">{{termThreeMaxScore}}</td>
                    </tr>
                    <tr class="term-three">
                        <td class="table-data">Average Score</td>
                        <td class="table-data-value">{{termThreeAvgScore}}</td>
                    </tr>
                    <tr class="term-three">
                        <td class="table-data">Lowest Score</td>
                        <td class="table-data-value">{{termThreeMinScore}}</td>
                    </tr>
                    <tr class="term-three">
                        <td class="table-data">pass( score&gt;50 ) rate</td>
                        <td class="table-data-value">
                            [{{ ((termThreePass/termThreeTotal)*100).toFixed(1) }}%]
                        </td>
                    </tr>
                    <tr class="term-three">
                        <td class="table-data">weak pass( 50&lt;=score&gt;=40 ) rate</td>
                        <td class="table-data-value">
                            [{{ ((termThreeWeakPass/termThreeTotal)*100).toFixed(1) }}%]
                        </td>
                    </tr>
                    <tr class="term-three">
                        <td class="table-data">fail( score&lt;40 ) rate</td>
                        <td class="table-data-value">
                            [{{ ((termThreeFail/termThreeTotal)*100).toFixed(1) }}%]
                        </td>
                    </tr>
                </tbody>
            </v-table>
        </div>

        <!-- Term Two -->
        <div class="term-table" v-if="year['term_two'] && year['term_two'].length >0">
            <v-table density="comfortable">
                <tbody >
                    <tr class="term-two table-title-container" style="position: relative">
                        <td>Justice</td>
                        <td class="table-title term-two" v-if="userAuthStore.userData['school']['semesters']">semester 2</td>
                        <td class="table-title term-two" v-if="!userAuthStore.userData['school']['semesters']">trimester 2</td>
                    </tr>
                    <tr class="term-two">
                        <td class="table-data">Highest Score</td>
                        <td class="table-data-value">{{termTwoMaxScore}}</td>
                    </tr>
                    <tr class="term-two">
                        <td class="table-data">Average Score</td>
                        <td class="table-data-value">{{termTwoAvgScore}}</td>
                    </tr>
                    <tr class="term-two" v-if="termTwoMinScore">
                        <td class="table-data">Lowest Score</td>
                        <td class="table-data-value">{{termTwoMinScore}}</td>
                    </tr>
                    <tr class="term-two">
                        <td class="table-data">pass( score&gt;50 ) rate</td>
                        <td class="table-data-value">
                            [{{ ((termTwoPass/termTwoTotal)*100).toFixed(1) }}%]
                        </td>
                    </tr>
                    <tr class="term-two">
                        <td class="table-data">weak pass( 50&lt;=score&gt;=40 ) rate</td>
                        <td class="table-data-value">
                            [{{ ((termTwoWeakPass/termTwoTotal)*100).toFixed(1) }}%]
                        </td>
                    </tr>
                    <tr class="term-two">
                        <td class="table-data">fail( score&lt;40 ) rate</td>
                        <td class="table-data-value">
                            [{{ ((termTwoFail/termTwoTotal)*100).toFixed(1) }}%]
                        </td>
                    </tr>
                </tbody>
            </v-table>
        </div>

        <!-- Term One -->
        <div class="term-table" v-if="year['term_one'] && year['term_one'].length >0">
            <v-table density="comfortable">
                <tbody >
                    <tr class="term-one table-title-container" style="position: relative">
                        <td>Justice</td>
                        <td class="table-title term-one" v-if="userAuthStore.userData['school']['semesters']">semester 1</td>
                        <td class="table-title term-one" v-if="!userAuthStore.userData['school']['semesters']">trimester 1</td>
                    </tr>
                    <tr class="term-one">
                        <td class="table-data">Highest Score</td>
                        <td class="table-data-value">{{termOneMaxScore}}</td>
                    </tr>
                    <tr class="term-one">
                        <td class="table-data">Average Score</td>
                        <td class="table-data-value">{{termOneAvgScore}}</td>
                    </tr>
                    <tr class="term-one">
                        <td class="table-data">Lowest Score</td>
                        <td class="table-data-value">{{termOneMinScore}}</td>
                    </tr>
                    <tr class="term-one">
                        <td class="table-data">pass( score&gt;50 ) rate</td>
                        <td class="table-data-value">
                            [{{ ((termOnePass/termOneTotal)*100).toFixed(1) }}%]
                        </td>
                    </tr>
                    <tr class="term-one">
                        <td class="table-data">weak pass( 50&lt;=score&gt;=40 ) rate</td>
                        <td class="table-data-value">
                            [{{ ((termOneWeakPass/termOneTotal)*100).toFixed(1) }}%]
                        </td>
                    </tr>
                    <tr class="term-one">
                        <td class="table-data">fail( score&lt;40 ) rate</td>
                        <td class="table-data-value">
                            [{{ ((termOneFail/termOneTotal)*100).toFixed(1) }}%]
                        </td>
                    </tr>
                </tbody>
            </v-table>
        </div>
    </div>
</div>
</template>

<style scoped>

@import url('../assets/css/tables.css');

.chart{
    max-width: 800px !important;
    max-height: 300px !important;
}
.table-container{
    margin-top: 3em;
    overflow: hidden;
    width: 100%;
    border: 1px solid whitesmoke;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.term-table{
    margin-bottom: 2em;
    border: 1px solid;
}
.term-one{
    color: green !important;
}
.term-two{
    color: blue !important;
}
.term-three{
    color: indigo !important;
}

@media screen and (min-width: 767px) {
    .table-container{
        flex-direction: row;
        justify-content: space-evenly;
    }
}

</style>
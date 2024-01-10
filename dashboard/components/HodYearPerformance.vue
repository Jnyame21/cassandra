<script setup lang="ts">

import 'chart.js/auto'
import { Bar } from 'vue-chartjs'
import { defineProps, ref, computed } from 'vue'


interface student {
    name: string;
    score: number;
    st_id: string;
}

interface Props {
    year: {
        term_one: student[];
        term_two: student[];
        term_three: student[];
    }
}

const userAuthStore = useUserAuthStore()
const { year } = defineProps<Props>()


// Graph Data

// Term One
const termOneGradeA1 = ref(year['term_one'].filter(student => student.score >=80)).value.length
const termOneGradeB2 = ref(year['term_one'].filter(student => student.score >=75 && student.score <80)).value.length
const termOneGradeB3 = ref(year['term_one'].filter(student => student.score >=70 && student.score <75)).value.length
const termOneGradeC4 = ref(year['term_one'].filter(student => student.score >=65 && student.score <70)).value.length
const termOneGradeC5 = ref(year['term_one'].filter(student => student.score >=60 && student.score <65)).value.length
const termOneGradeC6 = ref(year['term_one'].filter(student => student.score >=55 && student.score <60)).value.length
const termOneGradeD7 = ref(year['term_one'].filter(student => student.score >=50 && student.score <55)).value.length
const termOneGradeE8 = ref(year['term_one'].filter(student => student.score >=40 && student.score <50)).value.length
const termOneGradeF9 = ref(year['term_one'].filter(student => student.score <40)).value.length

// Term Two
const termTwoGradeA1 = ref(year['term_two'].filter(student => student.score >=80)).value.length
const termTwoGradeB2 = ref(year['term_two'].filter(student => student.score >=75 && student.score <80)).value.length
const termTwoGradeB3 = ref(year['term_two'].filter(student => student.score >=70 && student.score <75)).value.length
const termTwoGradeC4 = ref(year['term_two'].filter(student => student.score >=65 && student.score <70)).value.length
const termTwoGradeC5 = ref(year['term_two'].filter(student => student.score >=60 && student.score <65)).value.length
const termTwoGradeC6 = ref(year['term_two'].filter(student => student.score >=55 && student.score <60)).value.length
const termTwoGradeD7 = ref(year['term_two'].filter(student => student.score >=50 && student.score <55)).value.length
const termTwoGradeE8 = ref(year['term_two'].filter(student => student.score >=40 && student.score <50)).value.length
const termTwoGradeF9 = ref(year['term_two'].filter(student => student.score <40)).value.length

// Term Three
const termThreeGradeA1 = ref(year['term_three'].filter(student => student.score >=80)).value.length
const termThreeGradeB2 = ref(year['term_three'].filter(student => student.score >=75 && student.score <80)).value.length
const termThreeGradeB3 = ref(year['term_three'].filter(student => student.score >=70 && student.score <75)).value.length
const termThreeGradeC4 = ref(year['term_three'].filter(student => student.score >=65 && student.score <70)).value.length
const termThreeGradeC5 = ref(year['term_three'].filter(student => student.score >=60 && student.score <65)).value.length
const termThreeGradeC6 = ref(year['term_three'].filter(student => student.score >=55 && student.score <60)).value.length
const termThreeGradeD7 = ref(year['term_three'].filter(student => student.score >=50 && student.score <55)).value.length
const termThreeGradeE8 = ref(year['term_three'].filter(student => student.score >=40 && student.score <50)).value.length
const termThreeGradeF9 = ref(year['term_three'].filter(student => student.score <40)).value.length
const labels = ref(['A1', 'B2', 'B3', 'C4', 'C5', 'C6', 'D7', 'E8', 'F9'])
const termOnePoints = ref([termOneGradeA1, termOneGradeB2, termOneGradeB3, termOneGradeC4, termOneGradeC5, termOneGradeC6, termOneGradeD7, termOneGradeE8, termOneGradeF9])
const termTwoPoints = ref([termTwoGradeA1, termTwoGradeB2, termTwoGradeB3, termTwoGradeC4, termTwoGradeC5, termTwoGradeC6, termTwoGradeD7, termTwoGradeE8, termTwoGradeF9])
const termThreePoints = ref([termThreeGradeA1, termThreeGradeB2, termThreeGradeB3, termThreeGradeC4, termThreeGradeC5, termThreeGradeC6, termThreeGradeD7, termThreeGradeE8, termThreeGradeF9])

const chartData1 = ref({
    labels: labels.value,
    datasets: [
    {
      label: 'Semester 1',
      data: termOnePoints.value,
      borderColor: 'green',
      backgroundColor: 'green',
      borderWidth: 2,
      fill: false,
    },
    {
      label: 'Semester 2',
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
      label: 'Semester 1',
      data: termOnePoints.value,
      borderColor: 'green',
      backgroundColor: 'green',
      borderWidth: 2,
      fill: false,
    },
    {
      label: 'Semester 2',
      data: termTwoPoints.value,
      borderColor: 'blue',
      backgroundColor: 'blue',
      borderWidth: 2,
      fill: false,
    },
    {
      label: 'Semester 3',
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
const termOneTotal = ref(year['term_one']).value.length
const termOneTop5 = ref(year['term_one']).value.slice(0, 5)
const termOneLast5 = ref(year['term_one']).value.slice(-5)
const termOneScores = ref(year['term_one'].map(student => Number(student.score)))

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
const termTwoTotal = ref(year['term_two']).value.length
const termTwoTop5 = ref(year['term_two']).value.slice(0, 5)
const termTwoLast5 = ref(year['term_two']).value.slice(-5)
const termTwoScores = ref(year['term_two'].map(student => Number(student.score)))

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
const termThreeTotal = ref(year['term_three']).value.length
const termThreeTop5 = ref(year['term_three']).value.slice(0, 5)
const termThreeLast5 = ref(year['term_three']).value.slice(-5)
const termThreeScores = ref(year['term_three'].map(student => Number(student.score)))

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
    <TheLoader v-if="!year || year && year['term_one'].length ===0 "  />

    <Bar
    v-if="year && userAuthStore.userData['school']['semesters']  && year['term_one'].length >0 "
    class="chart"
    :options="chartOptions"
    :data="chartData1"
    :fill="false"
    />

    <Bar
    v-if="year && !userAuthStore.userData['school']['semesters']  && year['term_one'].length >0 "
    class="chart"
    :options="chartOptions"
    :data="chartData2"
    :fill="false"
    />
    <div class="table-container" v-if="year && year['term_one'].length >0">

        <!-- Term Three -->
        <div class="term-table" v-if="year['term_three'] && year['term_three'].length >0">
            <v-table density="comfortable">
                <tbody >
                    <tr class="term-three table-title-container" style="position: relative">
                        <td>Justice</td>
                        <td class="table-title term-three" v-if="userAuthStore.userData && !userAuthStore.userData['school']['semesters']">TRIMESTER 3</td>
                    </tr>
                    <tr class="term-three">
                        <td class="table-data">Total Students</td>
                        <td class="table-data-value">{{termThreeTotal}}</td>
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
                        <td class="table-data">pass (score&gt;=50)</td>
                        <td class="table-data-value">
                            {{termThreePass}}
                            [{{ ((termThreePass/termThreeTotal)*100).toFixed(1) }}%]
                        </td>
                    </tr>
                    <tr class="term-three">
                        <td class="table-data">weak pass (50&lt;score&gt;=40)</td>
                        <td class="table-data-value">
                            {{termThreeWeakPass}}
                            [{{ ((termThreeWeakPass/termThreeTotal)*100).toFixed(1) }}%]
                        </td>
                    </tr>
                    <tr class="term-three">
                        <td class="table-data">fail (score&lt;40)</td>
                        <td class="table-data-value">
                            {{termThreeFail}}
                            [{{ ((termThreeFail/termThreeTotal)*100).toFixed(1) }}%]
                        </td>
                    </tr>
                    <tr v-if="termThreeTotal > 15" class="table-title-container" style="position: relative">
                        <td>Justice</td>
                        <td class="subtitle">top 5 students</td>
                    </tr>
                    <tr class="term-three" v-for="(st, i) in termThreeTop5" :key="i">
                        <td v-if="termThreeTotal > 15" class="table-data">{{st['name']}} [{{st['st_id']}}]</td>
                        <td v-if="termThreeTotal > 15" class="table-data-value">{{st['score']}}</td>
                    </tr>
                    <tr v-if="termThreeTotal > 15" class="table-title-container" style="position: relative">
                        <td>Justice</td>
                        <td class="subtitle">last 5 students</td>
                    </tr>
                    <tr class="term-three" v-for="(st, i) in termThreeLast5" :key="i">
                        <td v-if="termThreeTotal > 15" class="table-data">{{st['name']}} [{{st['st_id']}}]</td>
                        <td v-if="termThreeTotal > 15" class="table-data-value">{{st['score']}}</td>
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
                        <td class="table-title term-two" v-if="userAuthStore.userData && userAuthStore.userData['school']['semesters']">SEMESTER 2</td>
                        <td class="table-title term-two" v-if="userAuthStore.userData && !userAuthStore.userData['school']['semesters']">TRIMESTER 2</td>
                    </tr>
                    <tr class="term-two">
                        <td class="table-data">Total Students</td>
                        <td class="table-data-value">{{termTwoTotal}}</td>
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
                        <td class="table-data">pass (score&gt;=50)</td>
                        <td class="table-data-value">
                            {{termTwoPass}}
                            [{{ ((termTwoPass/termTwoTotal)*100).toFixed(1) }}%]
                        </td>
                    </tr>
                    <tr class="term-two">
                        <td class="table-data">weak pass (50&lt;score&gt;=40)</td>
                        <td class="table-data-value">
                            {{termTwoWeakPass}}
                            [{{ ((termTwoWeakPass/termTwoTotal)*100).toFixed(1) }}%]
                        </td>
                    </tr>
                    <tr class="term-two">
                        <td class="table-data">fail (score&lt;40)</td>
                        <td class="table-data-value">
                            {{termTwoFail}}
                            [{{ ((termTwoFail/termTwoTotal)*100).toFixed(1) }}%]
                        </td>
                    </tr>
                    <tr v-if="termTwoTotal > 15" class="table-title-container" style="position: relative">
                        <td>Justice</td>
                        <td class="subtitle">top 5 students</td>
                    </tr>
                    <tr class="term-two" v-for="(st, i) in termTwoTop5" :key="i">
                        <td v-if="termTwoTotal > 15" class="table-data">{{st['name']}} [{{st['st_id']}}]</td>
                        <td v-if="termTwoTotal > 15" class="table-data-value">{{st['score']}}</td>
                    </tr>
                    <tr v-if="termTwoTotal > 15" class="table-title-container" style="position: relative">
                        <td>Justice</td>
                        <td class="subtitle">last 5 students</td>
                    </tr>
                    <tr class="term-two" v-for="(st, i) in termTwoLast5" :key="i">
                        <td v-if="termTwoTotal > 15" class="table-data">{{st['name']}} [{{st['st_id']}}]</td>
                        <td v-if="termTwoTotal > 15" class="table-data-value">{{st['score']}}</td>
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
                        <td class="table-title term-one" v-if="userAuthStore.userData && userAuthStore.userData['school']['semesters']">SEMESTER 1</td>
                        <td class="table-title term-one" v-if="userAuthStore.userData && !userAuthStore.userData['school']['semesters']">TRIMESTER 1</td>
                    </tr>
                    <tr class="term-one">
                        <td class="table-data">Total Students</td>
                        <td class="table-data-value">{{termOneTotal}}</td>
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
                        <td class="table-data">pass (score&gt;=50)</td>
                        <td class="table-data-value">
                            {{termOnePass}}
                            [{{ ((termOnePass/termOneTotal)*100).toFixed(1) }}%]
                        </td>
                    </tr>
                    <tr class="term-one">
                        <td class="table-data">weak pass (50&lt;score&gt;=40)</td>
                        <td class="table-data-value">
                            {{termOneWeakPass}}
                            [{{ ((termOneWeakPass/termOneTotal)*100).toFixed(1) }}%]
                        </td>
                    </tr>
                    <tr class="term-one">
                        <td class="table-data">fail (score&lt;40)</td>
                        <td class="table-data-value">
                            {{termOneFail}}
                            [{{ ((termOneFail/termOneTotal)*100).toFixed(1) }}%]
                        </td>
                    </tr>
                    <tr v-if="termOneTotal > 15" class="table-title-container" style="position: relative">
                        <td>Justice</td>
                        <td class="subtitle">top 5 students</td>
                    </tr>
                    <tr class="term-one" v-for="(st, i) in termOneTop5" :key="i">
                        <td v-if="termOneTotal > 15" class="table-data">{{st['name']}} [{{st['st_id']}}]</td>
                        <td v-if="termOneTotal > 15" class="table-data-value">{{st['score']}}</td>
                    </tr>
                    <tr v-if="termOneTotal > 15" class="table-title-container" style="position: relative">
                        <td>Justice</td>
                        <td class="subtitle">last 5 students</td>
                    </tr>
                    <tr class="term-one" v-for="(st, i) in termOneLast5" :key="i">
                        <td v-if="termOneTotal > 15" class="table-data">{{st['name']}} [{{st['st_id']}}]</td>
                        <td v-if="termOneTotal > 15" class="table-data-value">{{st['score']}}</td>
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

@media screen and (min-width: 768px) {
    .table-container{
        flex-direction: row;
        justify-content: space-evenly;
    }
}

</style>
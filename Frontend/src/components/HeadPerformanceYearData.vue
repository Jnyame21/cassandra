<script setup lang="ts">

import 'chart.js/auto'
import { Bar } from 'vue-chartjs'
import { defineProps, ref, computed } from 'vue'



interface Props {
    year: {
        term_one: string[];
        term_two: string[];
        term_three: string[];
    }
}

const userAuthStore = useUserAuthStore()
const { year } = defineProps<Props>()
const termOne = ref(year['term_one'].map(str => Number(str)))
const termTwo = ref(year['term_two'].map(str => Number(str)))
const termThree = ref(year['term_three'].map(str => Number(str)))

// Graph Data

// Term One
const termOneGradeA1 = termOne.value.filter(score => score >=80).length
const termOneGradeB2 = termOne.value.filter(score => score >=75 && score <80).length
const termOneGradeB3 = termOne.value.filter(score => score >=70 && score <75).length
const termOneGradeC4 = termOne.value.filter(score => score >=65 && score <70).length
const termOneGradeC5 = termOne.value.filter(score => score >=60 && score <65).length
const termOneGradeC6 = termOne.value.filter(score => score >=55 && score <60).length
const termOneGradeD7 = termOne.value.filter(score => score >=50 && score <55).length
const termOneGradeE8 = termOne.value.filter(score => score >=40 && score <50).length
const termOneGradeF9 = termOne.value.filter(score => score <40).length

// Term Two
const termTwoGradeA1 = termTwo.value.filter(score => score >=80).length
const termTwoGradeB2 = termTwo.value.filter(score => score >=75 && score <80).length
const termTwoGradeB3 = termTwo.value.filter(score => score >=70 && score <75).length
const termTwoGradeC4 = termTwo.value.filter(score => score >=65 && score <70).length
const termTwoGradeC5 = termTwo.value.filter(score => score >=60 && score <65).length
const termTwoGradeC6 = termTwo.value.filter(score => score >=55 && score <60).length
const termTwoGradeD7 = termTwo.value.filter(score => score >=50 && score <55).length
const termTwoGradeE8 = termTwo.value.filter(score => score >=40 && score <50).length
const termTwoGradeF9 = termTwo.value.filter(score => score <40).length

// Term Three
const termThreeGradeA1 = termThree.value.filter(score => score >=80).length
const termThreeGradeB2 = termThree.value.filter(score => score >=75 && score <80).length
const termThreeGradeB3 = termThree.value.filter(score => score >=70 && score <75).length
const termThreeGradeC4 = termThree.value.filter(score => score >=65 && score <70).length
const termThreeGradeC5 = termThree.value.filter(score => score >=60 && score <65).length
const termThreeGradeC6 = termThree.value.filter(score => score >=55 && score <60).length
const termThreeGradeD7 = termThree.value.filter(score => score >=50 && score <55).length
const termThreeGradeE8 = termThree.value.filter(score => score >=40 && score <50).length
const termThreeGradeF9 = termThree.value.filter(score => score <40).length

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
      label: 'Trimester 1',
      data: termOnePoints.value,
      borderColor: 'green',
      backgroundColor: 'green',
      borderWidth: 2,
      fill: false,
    },
    {
      label: 'Trimester 2',
      data: termTwoPoints.value,
      borderColor: 'blue',
      backgroundColor: 'blue',
      borderWidth: 2,
      fill: false,
    },
    {
      label: 'Trimester 3',
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
const termOneTotal = termOne.value.length

const termOneAvgScore = computed(()=>{
    const sum = termOne.value.reduce((sum, current) => sum + current, 0)
    return (sum / termOne.value.length).toFixed(0)
})

const termOneMaxScore = computed(()=>{
    return Math.max(...termOne.value)
})

const termOneMinScore = computed(()=>{
    return Math.min(...termOne.value)
})

const termOnePass = computed(()=>{
    return termOne.value.filter(score => score >= 50).length
})
const termOneWeakPass = computed(()=>{
    return termOne.value.filter(score => score < 50  && score >=40).length
})
const termOneFail = computed(()=>{
    return termOne.value.filter(score => score< 40).length
})

// Term Two
const termTwoTotal = termTwo.value.length

const termTwoAvgScore = computed(()=>{
    const sum = termTwo.value.reduce((sum, current) => sum + current, 0)
    return (sum / termTwo.value.length).toFixed(0)
})

const termTwoMaxScore = computed(()=>{
    return Math.max(...termTwo.value)
})
const termTwoMinScore = computed(()=>{
    return Math.min(...termTwo.value)
})

const termTwoPass = computed(()=>{
    return termTwo.value.filter(score => score >= 50).length
})
const termTwoWeakPass = computed(()=>{
    return termTwo.value.filter(score => score < 50  && score >=40).length
})
const termTwoFail = computed(()=>{
    return termTwo.value.filter(score => score < 40).length
})

// Term Three
const termThreeTotal = termThree.value.length

const termThreeAvgScore = computed(()=>{
    const sum = termThree.value.reduce((sum, current) => sum + current, 0)
    return (sum / termThree.value.length).toFixed(0)
})

const termThreeMaxScore = computed(()=>{
    return Math.max(...termThree.value)
})

const termThreeMinScore = computed(()=>{
    return Math.min(...termThree.value)
})

const termThreePass = computed(()=>{
    return termThree.value.filter(score => score >= 50).length
})
const termThreeWeakPass = computed(()=>{
    return termThree.value.filter(score => score < 50  && score >=40).length
})
const termThreeFail = computed(()=>{
    return termThree.value.filter(score => score < 40).length
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
                </tbody>
            </v-table>
        </div>
    </div>
</div>
</template>

<style scoped>

@import url('../assets/css/tables.css');

.chart{
    max-width: 1200px !important;
    max-height: 300px !important;
}
.table-container{
    margin-top: 3em;
    overflow: hidden;
    width: 100%;
    border: 1px solid whitesmoke;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.term-table{
    margin-bottom: 2em;
    border: 1px solid;
    width: 90%;
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
    .term-table{
        min-width: 300px;
        max-width: 800px;
    }
}



</style>
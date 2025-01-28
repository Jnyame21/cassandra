<script setup lang="ts">
import axiosInstance from '../utils/axiosInstance';
import { AxiosError } from 'axios';
import { useUserAuthStore } from '@/stores/userAuthStore'
import { useElementsStore } from '@/stores/elementsStore'
import { computed, ref } from 'vue'
const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()
const className = ref('')
const classStudentsYear = ref('')
const classLevelIdentifer = ref('')
const classProgramIdentifer = ref('')
const classSubjectIdentifers = ref<string[]>([])
const classIndex = ref('')
const classId = ref('')
const addRemoveType = ref('')
const subjectOptions = ref<string[]>([])
const linkToClassOptions = ref<LinkToClass[]>([])
const linkToClassId = ref('')
const classHeadTeacherId = ref('')

interface Prop {
  schoolIdentifier: string;
}
interface LinkToClass {
  id: number;
  identifier: string;
}

const props = defineProps<Prop>()
const schoolIdentifer = props.schoolIdentifier

const classes = computed(() => {
  return userAuthStore.superUserData.classes[schoolIdentifer]
})

const createClass = async () => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', 'create')
  formData.append('name', className.value);
  formData.append('levelIdentifier', classLevelIdentifer.value);
  formData.append('schoolIdentifier', schoolIdentifer);
  formData.append('programIdentifier', classProgramIdentifer.value);
  formData.append('studentsYear', classStudentsYear.value.toString());

  try {
    const response = await axiosInstance.post('superuser/classes', formData)
    userAuthStore.superUserData.classes[schoolIdentifer].unshift(response.data)
    elementsStore.HideLoadingOverlay()
    elementsStore.ShowOverlay('Operation successful!', 'green', null, null)
  }
  catch (error) {
    elementsStore.HideLoadingOverlay()
    if (error instanceof AxiosError) {
      if (error.response) {
        if (error.response.status === 400 && error.response.data.message) {
          elementsStore.ShowOverlay(error.response.data.message, 'red', null, null)
        } else {
          elementsStore.ShowOverlay('Oops! something went wrong. Try again later', 'red', null, null)
        }
      }
      else if (!error.response && (error.code === 'ECONNABORTED' || !navigator.onLine)) {
        elementsStore.ShowOverlay('A network error occurred! Please check you internet connection', 'red', null, null)
      }
      else {
        elementsStore.ShowOverlay('An unexpected error occurred!', 'red', null, null)
      }
    }
  }
}

const addRemoveSubject = async () => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', addRemoveType.value)
  formData.append('classId', classId.value.toString());
  formData.append('subjectIdentifiers', JSON.stringify(classSubjectIdentifers.value));

  try {
    await axiosInstance.post('superuser/classes', formData)
    if (addRemoveType.value === 'addSubject') {
      classSubjectIdentifers.value.forEach(item => userAuthStore.superUserData.classes[schoolIdentifer][Number(classIndex.value)].subjects.push(item))
    }
    else if (addRemoveType.value === 'removeSubject') {
      classSubjectIdentifers.value.forEach(item => userAuthStore.superUserData.classes[schoolIdentifer][Number(classIndex.value)].subjects.splice(userAuthStore.superUserData.classes[schoolIdentifer][Number(classIndex.value)].subjects.indexOf(item), 1))
    }
    classSubjectIdentifers.value = []
    classIndex.value = ''
    classId.value = ''
    closeOverlay(`SuperUserAddRemoveSubjectFromClassOverlay,${schoolIdentifer}`)
    elementsStore.HideLoadingOverlay()
  }
  catch (error) {
    elementsStore.HideLoadingOverlay()
    if (error instanceof AxiosError) {
      if (error.response) {
        if (error.response.status === 400 && error.response.data.message) {
          elementsStore.ShowOverlay(error.response.data.message, 'red', null, null)
        } else {
          elementsStore.ShowOverlay('Oops! something went wrong. Try again later', 'red', null, null)
        }
      }
      else if (!error.response && (error.code === 'ECONNABORTED' || !navigator.onLine)) {
        elementsStore.ShowOverlay('A network error occurred! Please check you internet connection', 'red', null, null)
      }
      else {
        elementsStore.ShowOverlay('An unexpected error occurred!', 'red', null, null)
      }
    }
  }
}

const setClassHeadTeacher = async () => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', 'setClassHeadTeacher')
  formData.append('classId', classId.value);
  formData.append('schoolIdentifier', schoolIdentifer);
  formData.append('staffId', classHeadTeacherId.value);
  try {
    const response = await axiosInstance.post('superuser/classes', formData)
    userAuthStore.superUserData.classes[schoolIdentifer][Number(classIndex.value)].head_teacher = response.data
    classIndex.value = ''
    classId.value = ''
    closeOverlay(`SuperUserLinkClassOrSetClassHeadTeacherOverlay,${schoolIdentifer}`)
    elementsStore.HideLoadingOverlay()
  }
  catch (error) {
    elementsStore.HideLoadingOverlay()
    if (error instanceof AxiosError) {
      if (error.response) {
        if (error.response.status === 400 && error.response.data.message) {
          elementsStore.ShowOverlay(error.response.data.message, 'red', null, null)
        } else {
          elementsStore.ShowOverlay('Oops! something went wrong. Try again later', 'red', null, null)
        }
      }
      else if (!error.response && (error.code === 'ECONNABORTED' || !navigator.onLine)) {
        elementsStore.ShowOverlay('A network error occurred! Please check you internet connection', 'red', null, null)
      }
      else {
        elementsStore.ShowOverlay('An unexpected error occurred!', 'red', null, null)
      }
    }
  }
}

const linkClass = async () => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', 'linkClass')
  formData.append('id', classId.value);
  formData.append('toClassId', linkToClassId.value);
  try {
    const response = await axiosInstance.post('superuser/classes', formData)
    userAuthStore.superUserData.classes[schoolIdentifer][Number(classIndex.value)].linked_class = response.data
    classIndex.value = ''
    classId.value = ''
    linkToClassId.value = ''
    closeOverlay(`SuperUserLinkClassOrSetClassHeadTeacherOverlay,${schoolIdentifer}`)
    elementsStore.HideLoadingOverlay()
  }
  catch (error) {
    elementsStore.HideLoadingOverlay()
    if (error instanceof AxiosError) {
      if (error.response) {
        if (error.response.status === 400 && error.response.data.message) {
          elementsStore.ShowOverlay(error.response.data.message, 'red', null, null)
        } else {
          elementsStore.ShowOverlay('Oops! something went wrong. Try again later', 'red', null, null)
        }
      }
      else if (!error.response && (error.code === 'ECONNABORTED' || !navigator.onLine)) {
        elementsStore.ShowOverlay('A network error occurred! Please check you internet connection', 'red', null, null)
      }
      else {
        elementsStore.ShowOverlay('An unexpected error occurred!', 'red', null, null)
      }
    }
  }
}

const deleteOrRemoveItem = async (delete_or_remove_type: string, class_index: number, class_id: number) => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', delete_or_remove_type)
  formData.append('classId', class_id.toString());

  try {
    await axiosInstance.post('superuser/classes', formData)
    if (delete_or_remove_type === 'deleteClass'){
      userAuthStore.superUserData.classes[schoolIdentifer].splice(class_index, 1)
    }
    else if (delete_or_remove_type === 'removeClassHeadTeacher'){
      userAuthStore.superUserData.classes[schoolIdentifer][class_index].head_teacher = null
    }
    else if (delete_or_remove_type === 'removeLinkedClass'){
      userAuthStore.superUserData.classes[schoolIdentifer][class_index].linked_class = null
    }
    elementsStore.HideLoadingOverlay()
  }
  catch (error) {
    elementsStore.HideLoadingOverlay()
    if (error instanceof AxiosError) {
      if (error.response) {
        if (error.response.status === 400 && error.response.data.message) {
          elementsStore.ShowOverlay(error.response.data.message, 'red', null, null)
        } else {
          elementsStore.ShowOverlay('Oops! something went wrong. Try again later', 'red', null, null)
        }
      }
      else if (!error.response && (error.code === 'ECONNABORTED' || !navigator.onLine)) {
        elementsStore.ShowOverlay('A network error occurred! Please check you internet connection', 'red', null, null)
      }
      else {
        elementsStore.ShowOverlay('An unexpected error occurred!', 'red', null, null)
      }
    }
  }
}


const closeOverlay = (element: string) => {
  classHeadTeacherId.value = ''
  addRemoveType.value = ''
  classIndex.value = ''
  classId.value = ''
  subjectOptions.value = []
  linkToClassOptions.value = []
  linkToClassId.value = ''
  const overlay = document.getElementById(element)
  if (overlay) {
    overlay.style.display = 'none'
  }
}

const showOverlay = (element: string, type_option: string = '', class_index: number = 0, class_id: number = 0, subjects: string[] = [], link_to_classes: LinkToClass[] = []) => {
  addRemoveType.value = type_option
  classIndex.value = class_index.toString()
  classId.value = class_id.toString()
  subjectOptions.value = subjects
  linkToClassOptions.value = link_to_classes
  const overlay = document.getElementById(element)
  if (overlay) {
    overlay.style.display = 'flex'
  }
}


</script>

<template>
  <div class="content-wrapper" v-show="elementsStore.activePage === `SuperUserClasses,${schoolIdentifer}`"
    :class="{ 'is-active-page': elementsStore.activePage === `SuperUserClasses,${schoolIdentifer}` }">

    <!-- class subjects overlay -->
    <div :id="`SuperUserSubjectsUnderClassOverlay,${schoolIdentifer}`" class="overlay upload">
      <div class="overlay-card">
        <v-btn @click="closeOverlay(`SuperUserSubjectsUnderClassOverlay,${schoolIdentifer}`)" color="red" size="small"
          variant="flat" class="close-btn">
          X
        </v-btn>
        <div class="overlay-card-info-container"></div>
        <div class="overlay-card-content-container">
          <p class="subject-card" v-for="(subject, index) in subjectOptions" :key=index>{{ subject }}</p>
        </div>
      </div>
    </div>

    <!-- class creation overlay -->
    <div :id="`SuperUserCreateClassOverlay,${schoolIdentifer}`" class="overlay upload">
      <div class="overlay-card">
        <v-btn @click="closeOverlay(`SuperUserCreateClassOverlay,${schoolIdentifer}`)" color="red" size="small" variant="flat" class="close-btn">
          X
        </v-btn>
        <div class="overlay-card-info-container"></div>
        <div class="overlay-card-content-container">
          <v-text-field class="input-field" v-model="className" label="NAME" clearable />
          <v-text-field class="input-field" v-model.number="classStudentsYear" label="STUDENTS YEAR" type="number"
            clearable />
          <v-select class="select"
            :items="userAuthStore.superUserData.levels.filter(item => item.schools.includes(schoolIdentifer)).map(item => item.identifier)"
            label="LEVEL" v-model="classLevelIdentifer" density="comfortable" persistent-hint hint="Select the level"
            variant="solo-filled" clearable />
          <v-select class="select" v-if="userAuthStore.superUserData.levels.find(item=> item.identifier === classLevelIdentifer)?.has_programs"
            :items="userAuthStore.superUserData.programs.filter(item => item.schools.includes(schoolIdentifer) && item.level === classLevelIdentifer).map(item => ({'title': item.name, 'value': item.identifier}))"
            label="PROGRAM" item-title="title" item-value="value" v-model="classProgramIdentifer" density="comfortable" persistent-hint
            hint="Select the program" variant="solo-filled" clearable 
          />
        </div>
        <div class="overlay-card-action-btn-container">
          <v-btn @click="createClass" :disabled="!(className && classStudentsYear && classLevelIdentifer)"
            :ripple="false" variant="flat" type="submit" color="black" size="small"
            append-icon="mdi-checkbox-marked-circle">
            SUBMIT
          </v-btn>
        </div>
      </div>
    </div>

    <!-- add/remove subject from class overlay -->
    <div :id="`SuperUserAddRemoveSubjectFromClassOverlay,${schoolIdentifer}`" class="overlay upload">
      <div class="overlay-card">
        <v-btn @click="closeOverlay(`SuperUserAddRemoveSubjectFromClassOverlay,${schoolIdentifer}`)" color="red"
          size="small" variant="flat" class="close-btn">
          X
        </v-btn>
        <div class="overlay-card-info-container"></div>
        <div class="overlay-card-content-container">
          <v-select class="select" v-if="addRemoveType === 'addSubject'" :items="subjectOptions" label="SUBJECT"
            v-model="classSubjectIdentifers" variant="solo-filled" density="comfortable" persistent-hint
            hint="Select the subject you want to add" multiple clearable />
          <v-select class="select" v-if="addRemoveType === 'removeSubject'" :items="subjectOptions" label="SUBJECT"
            v-model="classSubjectIdentifers" variant="solo-filled" density="comfortable" persistent-hint
            hint="Select the subject you want to remove" multiple clearable />
        </div>
        <div class="overlay-card-action-btn-container">
          <v-btn @click="addRemoveSubject" :disabled="!(classSubjectIdentifers.length > 0)" :ripple="false"
            variant="flat" type="submit" color="black" size="small" append-icon="mdi-checkbox-marked-circle">
            SUBMIT
          </v-btn>
        </div>
      </div>
    </div>

    <!-- link class and class head teacher overlay overlay -->
    <div :id="`SuperUserLinkClassOrSetClassHeadTeacherOverlay,${schoolIdentifer}`" class="overlay upload">
      <div class="overlay-card">
        <v-btn @click="closeOverlay(`SuperUserLinkClassOrSetClassHeadTeacherOverlay,${schoolIdentifer}`)" color="red" size="small" variant="flat" class="close-btn">
          X
        </v-btn>
        <div class="overlay-card-info-container"></div>
        <div class="overlay-card-content-container" v-if="addRemoveType ==='linkClass'">
          <v-select class="select" :items="linkToClassOptions" label="TO CLASS" v-model="linkToClassId"
            variant="solo-filled" density="comfortable" persistent-hint item-title="identifier" item-value="id"
            hint="Select the class you want to link to this class" clearable />
        </div>
        <div class="overlay-card-content-container" v-if="addRemoveType ==='setClassHeadTeacher'">
          <v-select class="select" :items="userAuthStore.superUserData.staff[schoolIdentifer].filter(item=> item.roles.map(subItem=> subItem.split('|').slice(1).map(sub=> sub.trim()).join(' | ')).includes(userAuthStore.superUserData.classes[schoolIdentifer][Number(classIndex)].level)).map(item=> ({'title': item.user, 'value': item.staff_id}))" 
            variant="solo-filled" density="comfortable" persistent-hint item-title="title" item-value="value" label="CLASS HEAD TEACHER" v-model="classHeadTeacherId"
            hint="Select the staff you want him/her to be the head teacher of the class" clearable>
            <template v-slot:item="{ props, item }">
              <v-list-item v-bind="props" :subtitle="item.raw.value"></v-list-item>
            </template>
          </v-select>
        </div>
        <div class="overlay-card-action-btn-container" v-if="addRemoveType ==='linkClass'">
          <v-btn @click="linkClass" :disabled="!(linkToClassId)" :ripple="false" variant="flat" type="submit" color="black" size="small" append-icon="mdi-checkbox-marked-circle">
            SUBMIT
          </v-btn>
        </div>
        <div class="overlay-card-action-btn-container" v-if="addRemoveType ==='setClassHeadTeacher'">
          <v-btn @click="setClassHeadTeacher()" :disabled="!(classHeadTeacherId)" :ripple="false" variant="flat" type="submit" color="black" size="small" append-icon="mdi-checkbox-marked-circle">
            SUBMIT
          </v-btn>
        </div>
      </div>
    </div>

    <div class="content-header">
      <v-btn @click="showOverlay(`SuperUserCreateClassOverlay,${schoolIdentifer}`)" color="blue"
        :size="elementsStore.btnSize1">
        CREATE CLASS
      </v-btn>
    </div>
    <div class="no-data" v-if="classes.length === 0">
      <p>NO DATA</p>
    </div>
    <v-table fixed-header class="table" v-if="classes.length > 0">
      <thead>
        <tr>
          <th class="table-head">ID</th>
          <th class="table-head">NAME</th>
          <th class="table-head">STUDENTS YEAR</th>
          <th class="table-head">LEVEL</th>
          <th class="table-head">PROGRAM</th>
          <th class="table-head">SUBJECTS</th>
          <th class="table-head">IDENTIFIER</th>
          <th class="table-head">HEAD TEACHER</th>
          <th class="table-head">LINKED CLASS</th>
          <th class="table-head">ACTION</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(_class, index) in classes" :key="index">
          <td class="table-data">{{ _class.id }}</td>
          <td class="table-data">
            <v-chip :size="elementsStore.btnSize1">{{ _class.name }}</v-chip>
          </td>
          <td class="table-data">
            <v-chip :size="elementsStore.btnSize1">{{ _class.students_year }}</v-chip>
          </td>
          <td class="table-data">
            <v-chip :size="elementsStore.btnSize1">{{ _class.level.split('|')[0] }}</v-chip>
          </td>
          <td class="table-data">
            <v-chip :size="elementsStore.btnSize1">{{ _class.program?.split('|')[0] }}</v-chip>
          </td>
          <td class="table-data flex-all">
            <v-btn @click="showOverlay(`SuperUserSubjectsUnderClassOverlay,${schoolIdentifer}`, '', 0, _class.id, _class.subjects)" size="x-small" color="blue" variant="flat">
              VIEW SUBJECTS
            </v-btn>
            <v-icon class="ml-2" v-if="userAuthStore.superUserData.schools" icon="mdi-plus" color="blue"
              @click="showOverlay(`SuperUserAddRemoveSubjectFromClassOverlay,${schoolIdentifer}`, 'addSubject', index, _class.id, userAuthStore.superUserData.subjects.map(item => item.identifier).filter(item => !_class.subjects.includes(item)))"
            />
            <v-icon class="ma-2" v-if="userAuthStore.superUserData.schools" icon="mdi-minus" color="blue"
              @click="showOverlay(`SuperUserAddRemoveSubjectFromClassOverlay,${schoolIdentifer}`, 'removeSubject', index, _class.id, _class.subjects)"
            />
          </td>
          <td class="table-data">
            <v-chip :size="elementsStore.btnSize1">{{ _class.identifier }}</v-chip>
          </td>
          <td class="table-data flex-all">
            <v-chip class="chip-link" v-if="_class.head_teacher" @click="showOverlay(`SuperUserLinkClassOrSetClassHeadTeacherOverlay,${schoolIdentifer}`, 'setClassHeadTeacher', index, _class.id, [], [])" :size="elementsStore.btnSize1">
              {{ _class.head_teacher.user }}[ {{ _class.head_teacher.staff_id }} ]
            </v-chip>
            <v-chip class="chip-link" v-if="!_class.head_teacher" @click="showOverlay(`SuperUserLinkClassOrSetClassHeadTeacherOverlay,${schoolIdentifer}`, 'setClassHeadTeacher', index, _class.id, [], [])" color="blue" :size="elementsStore.btnSize1">
              SET CLASS HEAD TEACHER
            </v-chip>
            <v-icon v-if="_class.head_teacher" class="ma-2" icon="mdi-delete" size="x-small" color="red"
              @click="elementsStore.ShowDeletionOverlay(() => deleteOrRemoveItem('removeClassHeadTeacher', index, _class.id), 'Are you sure you want to remove the class head teacher?')"
            />
          </td>
          <td class="table-data">
            <v-btn v-if="!_class.linked_class" size="x-small" color="blue" variant="flat"
              @click="showOverlay(`SuperUserLinkClassOrSetClassHeadTeacherOverlay,${schoolIdentifer}`, 'linkClass', index, _class.id, [], userAuthStore.superUserData.classes[schoolIdentifer].filter(item => item.id !== _class.id && item.students_year === _class.students_year + 1 && item.program === _class.program).map(item => ({ 'id': item.id, 'identifier': item.name })))">
              LINK CLASS
            </v-btn>
            <v-chip class="chip-link" v-if="_class.linked_class" :size="elementsStore.btnSize1" :text="`${_class.linked_class.split('|')[0]} ${_class.linked_class.split('|')[2]}`"
              @click="showOverlay(`SuperUserLinkClassOrSetClassHeadTeacherOverlay,${schoolIdentifer}`, 'linkClass', index, _class.id, [], userAuthStore.superUserData.classes[schoolIdentifer].filter(item => item.id !== _class.id && item.students_year === _class.students_year + 1 && item.program === _class.program).map(item => ({ 'id': item.id, 'identifier': item.name })))"
            />
            <v-icon class="ml-2" v-if="_class.linked_class" icon="mdi-delete" color="red" size="x-small"
              @click="elementsStore.ShowDeletionOverlay(() => deleteOrRemoveItem('removeLinkedClass', index, _class.id), 'Are you sure you want to remove the class that has been linked to this class?')"
            />
          </td>
          <td class="table-data flex-all" style="display: flex">
            <v-btn class="ma-2" variant="flat" icon="mdi-delete" size="x-small" color="red"
              @click="elementsStore.ShowDeletionOverlay(() => deleteOrRemoveItem('deleteClass', index, _class.id), 'Are you sure you want to delete this class. The process cannot be reversed')"
            />
          </td>
        </tr>
      </tbody>
    </v-table>
  </div>
</template>

<style scoped>
.overlay-card {
  max-width: 600px !important;
}

.overlay-card-info-container {
  margin-top: 3em !important;
}
</style>
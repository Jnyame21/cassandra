import{aT as a,G as s,q as t}from"./entry.eZbnTIXg.js";const i=a((f,r)=>{{const e=s();if(e.isAuthenticated&&e.userData){if(e.userData.role==="staff"&&e.userData.staff_role!="admin"&&!e.staffSubjectAssignment.termOne&&(e.getTeacherSubjectAssignments(),e.getTeacherStudentsAttendance(),e.getTeacherStudentResults(),e.staffNotification()),e.userData.staff_role==="hod"&&!e.staffSubjectAssignment.termOne&&(e.getHodData(),e.getHodPerformance(),e.staffNotification()),e.userData.role==="head"&&!e.headDepartments&&(e.getHeadData(),e.getHeadStudentsPerformance(),e.staffNotification()),e.userData.staff_role==="admin"&&!e.adminClasses.yearOne&&(e.getAdminData(),e.staffNotification()),e.userData.role==="student")return t("/student")}else return t("/")}});export{i as default};

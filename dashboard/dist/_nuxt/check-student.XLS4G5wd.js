import{aT as a,G as s,q as e}from"./entry.eZbnTIXg.js";const f=a((r,u)=>{{const t=s();if(t.isAuthenticated&&t.userData){if(t.userData.role==="student"&&!t.studentData.subjects)t.getStudentData();else if(t.userData.role==="staff")return e("/staff")}else return e("/")}});export{f as default};

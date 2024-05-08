import{E as w,d as v,F as x,e as A,G as k,H as V,I as S,c as F,v as m,x as o,z as u,A as h,J as I,t as p,K as s,y as _,L as g,B as C,C as E,D as M,_ as N}from"./7KyJguAr.js";import{u as b}from"./SCYtYpnd.js";import{_ as B}from"./BjgX_BOC.js";import{V as D,a as y}from"./BcuiPEUV.js";import{V as T}from"./9_bobrbN.js";function L(a,t){const{title:r,titleTemplate:e,...l}=a;return b({title:r,titleTemplate:e,_flatMeta:l},{...t,transform(i){const d=w({...i._flatMeta});return delete i._flatMeta,{...i,meta:d}}})}const f=a=>(E("data-v-577def06"),a=a(),M(),a),P={class:"container img-container flex-c align-center justify-center",style:{height:"100dvh"}},U={style:{height:"90dvh"},class:"row-wrapper"},O={class:"flex-all-c form-container"},G=f(()=>o("h1",{class:"portal-name"},"ACADEMIC ACCESS POINT",-1)),R=f(()=>o("img",{class:"sch-logo",src:B,alt:"school logo"},null,-1)),j={class:"flex-c align-center",style:{"background-color":"transparent"}},H={class:"form-message-container"},z={key:0,class:"form-message",style:{color:"yellow"}},J={key:1,class:"form-message",style:{color:"red"}},K=f(()=>o("footer",{class:"footer-container"},[o("h6",{class:"footer-text"},"© 2024")],-1)),W=v({__name:"index",setup(a){const t=x();L({title:"EduAAP  | LOGIN",description:"Login to your Academic Access Point (AAP)"}),b({meta:[{name:"robots",content:"index, follow"}]}),A(()=>{document.body.style.overflow="auto"}),k(()=>{document.body.style.overflow="hidden"});const r=V(),e=S({form:!1,username:"",password:"",loading:!1,visible:!1,lockField:!1});let l=F(()=>!(e.username&&e.password));const i=async()=>{e.loading=!0,e.lockField=!0,await t.userLogin(e.username,e.password).then(d=>{t.isAuthenticated&&t.userData.role==="staff"||t.isAuthenticated&&t.userData.role==="head"?(e.password="",e.loading=!1,setTimeout(()=>{r.push("/staff")},2e3)):t.isAuthenticated&&t.userData.role==="student"&&(e.password="",e.loading=!1,setTimeout(()=>{r.push("/student")},2e3))}).catch(d=>{e.loading=!1,e.lockField=!1,setTimeout(()=>{t.message=""},6e3)})};return(d,n)=>(p(),m("div",P,[o("div",U,[o("section",O,[G,R,o("div",j,[u(D,{class:"flex-c justify-start align-center",onSubmit:I(i,["prevent"])},{default:h(()=>[o("div",H,[s(t).message&&s(t).isAuthenticated?(p(),m("h6",z,_(s(t).message),1)):g("",!0),s(t).message&&!s(t).isAuthenticated?(p(),m("h6",J,_(s(t).message),1)):g("",!0)]),u(y,{disabled:e.lockField,class:"form-text-field username",modelValue:e.username,"onUpdate:modelValue":n[0]||(n[0]=c=>e.username=c),label:"USERNAME",hint:"Enter your username",density:"comfortable",type:"text",clearable:"",onFocus:s(l),"prepend-inner-icon":"mdi-account-outline"},null,8,["disabled","modelValue","onFocus"]),u(y,{"append-inner-icon":e.visible?"mdi-eye-off-outline":"mdi-eye-outline","onClick:appendInner":n[1]||(n[1]=c=>e.visible=!e.visible),disabled:e.lockField,type:e.visible?"text":"password",clearable:"",onFocus:s(l),density:"comfortable",class:"form-text-field password",hint:"Enter your password",modelValue:e.password,"onUpdate:modelValue":n[2]||(n[2]=c=>e.password=c),label:"PASSWORD","prepend-inner-icon":"mdi-lock-outline"},null,8,["append-inner-icon","disabled","type","onFocus","modelValue"]),u(T,{class:"submit-btn",type:"submit","prepend-icon":"mdi-lock-open-outline",loading:e.loading,disabled:s(l)},{default:h(()=>[C("LOGIN ")]),_:1},8,["loading","disabled"])]),_:1})])])]),K]))}}),Z=N(W,[["__scopeId","data-v-577def06"]]);export{Z as default};

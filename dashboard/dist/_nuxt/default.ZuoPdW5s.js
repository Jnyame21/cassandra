import{u as _}from"./vue.f36acd1f.CNtWgH9V.js";import{h as C,i as k,u as P,V,a as x,b}from"./VCard.e_5Kor9o.js";import{M as S,am as w,O as A,an as B,ax as I,z as s,d as M,H as E,G as T,r as L,T as N,A as r,t as g,x as u,K as v,v as O,y as f,L as R,B as m,aU as $,C as D,D as U,_ as z}from"./entry.eZbnTIXg.js";import{m as H,u as K,V as p}from"./index.j44zehaE.js";const Y=S({...H(),...C({fullHeight:!0}),...w()},"VApp"),j=A()({name:"VApp",props:Y(),setup(t,e){let{slots:l}=e;const o=B(t),{layoutClasses:i,getLayoutItem:d,items:c,layoutRef:y}=k(t),{rtlClasses:a}=I();return K(()=>{var n;return s("div",{ref:y,class:["v-application",o.themeClasses.value,i.value,a.value,t.class],style:[t.style]},[s("div",{class:"v-application__wrap"},[(n=l.default)==null?void 0:n.call(l)])])}),{getLayoutItem:d,items:c,theme:o}}}),F=t=>(D("data-v-193e325b"),t=t(),U(),t),G={class:"container",style:{"background-color":"white"}},q={id:"logout",class:"overlay"},J={key:0},Q={id:"session-alert",class:"overlay"},W={class:"overlay-card d-flex flex-column align-center"},X=F(()=>u("h4",{id:"company-name"},"Rozmach",-1)),Z={class:"overlay-text"},ee=M({__name:"default",setup(t){_({link:[{rel:"icon",href:"/login_logo.jpg"}],htmlAttrs:{lang:"en"}});const e=P(),l=E(),o=T(),i=L(!1),d=async()=>{const a=document.getElementById("session-alert");a&&e.overlayPath&&e.logout?(o.logoutUser(),await l.push(`${e.overlayPath}`),a.style.display="none",e.overlayMessage="",e.overlayMessageColor=null,e.overlayPath=null,e.logout=null):a&&e.overlayPath&&!e.logout?(await l.push(`${e.overlayPath}`),a.style.display="none",e.overlayMessage="",e.overlayPath=null,e.overlayMessageColor=null,e.logout=null):a&&!e.overlayPath&&!e.logout&&(a.style.display="none",e.overlayMessage="",e.overlayMessageColor=null,e.overlayPath=null,e.logout=null)},c=()=>{const a=document.getElementById("logout");a&&(a.style.display="none")},y=async()=>{const a=document.getElementById("logout");i.value=!0,o.logoutUser(),o.message="Your have been logged out!",await l.push(e.overlayPath),i.value=!1,a&&(a.style.display="none"),setTimeout(()=>{e.overlayPath=null,o.message=""},5e3)};return(a,n)=>(g(),N(j,{style:{"background-color":"seagreen"}},{default:r(()=>[u("div",G,[u("div",q,[s(b,{class:"d-flex flex-column align-center"},{default:r(()=>[s(V,{style:{"font-size":".8rem","font-family":"sans-serif","text-align":"left","line-height":"1.2","font-weight":"bold"}},{default:r(()=>[v(o).userData?(g(),O("p",J,f(v(o).userData.first_name)+"! are you sure you want to logout?",1)):R("",!0)]),_:1}),s(x,null,{default:r(()=>[s(p,{class:"overlay-btn mr-5",elevation:"4",onClick:n[0]||(n[0]=h=>y())},{default:r(()=>[m("YES")]),_:1}),s(p,{disabled:i.value,class:"overlay-btn ml-5",elevation:"4",onClick:c},{default:r(()=>[m("NO")]),_:1},8,["disabled"])]),_:1})]),_:1})]),u("div",Q,[u("div",W,[X,u("p",Z,f(v(e).overlayMessage),1),u("div",null,[s(p,{class:"overlay-btn",onClick:n[1]||(n[1]=h=>d())},{default:r(()=>[m("OK")]),_:1})])])]),$(a.$slots,"default",{},void 0,!0)])]),_:3}))}}),le=z(ee,[["__scopeId","data-v-193e325b"]]);export{le as default};

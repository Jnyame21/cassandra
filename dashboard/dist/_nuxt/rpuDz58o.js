import{u as C}from"./-UxRPX4R.js";import{h as P,i as V,u as k,V as x,a as I,b}from"./bYNn1PhK.js";import{N as w,an as S,P as B,ao as A,ay as M,z as s,d as E,I as N,G as T,r as U,e as L,U as R,A as n,t as f,x as r,L as m,v as $,y as h,M as D,B as p,aV as O,C as z,D as H,_ as Y}from"./CJhruBnl.js";import{m as j,u as F,V as g}from"./D_w_0sjn.js";const G=window.setInterval,K=w({...j(),...P({fullHeight:!0}),...S()},"VApp"),q=B()({name:"VApp",props:K(),setup(o,e){let{slots:l}=e;const t=A(o),{layoutClasses:u,getLayoutItem:i,items:d,layoutRef:y}=V(o),{rtlClasses:v}=M();return F(()=>{var a;return s("div",{ref:y,class:["v-application",t.themeClasses.value,u.value,v.value,o.class],style:[o.style]},[s("div",{class:"v-application__wrap"},[(a=l.default)==null?void 0:a.call(l)])])}),{getLayoutItem:i,items:d,theme:t}}}),J=o=>(z("data-v-a043159b"),o=o(),H(),o),Q={class:"container",style:{"background-color":"white"}},W={id:"logout",class:"overlay"},X={key:0},Z={id:"session-alert",class:"overlay"},ee={class:"overlay-card d-flex flex-column align-center"},ae=J(()=>r("h4",{id:"company-name"},"Rozmach",-1)),te={class:"overlay-text"},oe=E({__name:"default",setup(o){C({link:[{rel:"icon",href:"/login_logo.jpg"}],htmlAttrs:{lang:"en"}});const e=k(),l=N(),t=T(),u=U(!1);let i=0;i=G(()=>{t.startUpServer()},60*1e3),L(()=>{clearInterval(i)});const d=async()=>{const a=document.getElementById("session-alert");a&&e.overlayPath&&e.logout?(t.logoutUser(),await l.push(`${e.overlayPath}`),a.style.display="none",e.overlayMessage="",e.overlayMessageColor=null,e.overlayPath=null,e.logout=null):a&&e.overlayPath&&!e.logout?(await l.push(`${e.overlayPath}`),a.style.display="none",e.overlayMessage="",e.overlayPath=null,e.overlayMessageColor=null,e.logout=null):a&&!e.overlayPath&&!e.logout&&(a.style.display="none",e.overlayMessage="",e.overlayMessageColor=null,e.overlayPath=null,e.logout=null)},y=()=>{const a=document.getElementById("logout");a&&(a.style.display="none")},v=async()=>{const a=document.getElementById("logout");u.value=!0,t.logoutUser(),t.message="Your have been logged out!",await l.push(e.overlayPath),u.value=!1,a&&(a.style.display="none"),setTimeout(()=>{e.overlayPath=null,t.message=""},5e3)};return(a,c)=>(f(),R(q,{style:{"background-color":"seagreen"}},{default:n(()=>[r("div",Q,[r("div",W,[s(b,{class:"d-flex flex-column align-center"},{default:n(()=>[s(x,{style:{"font-size":".8rem","font-family":"sans-serif","text-align":"left","line-height":"1.2","font-weight":"bold"}},{default:n(()=>[m(t).userData?(f(),$("p",X,h(m(t).userData.first_name)+"! are you sure you want to logout?",1)):D("",!0)]),_:1}),s(I,null,{default:n(()=>[s(g,{class:"mr-5",color:"red",elevation:"4",onClick:c[0]||(c[0]=_=>v())},{default:n(()=>[p("YES")]),_:1}),s(g,{disabled:u.value,color:"blue",class:"ml-5",elevation:"4",onClick:y},{default:n(()=>[p("NO")]),_:1},8,["disabled"])]),_:1})]),_:1})]),r("div",Z,[r("div",ee,[ae,r("p",te,h(m(e).overlayMessage),1),r("div",null,[s(g,{class:"overlay-btn",onClick:c[1]||(c[1]=_=>d())},{default:n(()=>[p("OK")]),_:1})])])]),O(a.$slots,"default",{},void 0,!0)])]),_:3}))}}),ue=Y(oe,[["__scopeId","data-v-a043159b"]]);export{ue as default};
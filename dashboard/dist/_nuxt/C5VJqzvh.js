import{b0 as X,M as b,af as A,r as N,aD as we,e as Y,U as K,aI as me,ag as it,aR as P,c,a3 as D,aE as Ie,b1 as ge,b2 as lt,b3 as ot,b4 as rt,K as he,z as v,V as ut,an as M,O as T,ao as G,au as Be,aj as E,Q as ct,ae as Ee,ad as dt,I as vt,P as Pe,o as ft,as as Te,a5 as mt,aX as gt,S as Ve,b5 as ht,ar as y,ai as ne,b6 as bt,b7 as yt,b8 as Ct,Z as pt,a$ as Le,aG as St,ay as $e,ac as Re,b9 as kt,ba as be,a1 as Ne,aB as _t,bb as xt,bc as ye,ak as wt,aq as It,g as Bt}from"./DvwhNQh0.js";const ze=["top","bottom"],Et=["start","end","left","right"];function Pt(e,t){let[a,n]=e.split(" ");return n||(n=X(ze,a)?"start":X(Et,a)?"top":"center"),{side:Ce(a,t),align:Ce(n,t)}}function Ce(e,t){return e==="start"?t?"right":"left":e==="end"?t?"left":"right":e}function hn(e){return{side:{center:"center",top:"bottom",bottom:"top",left:"right",right:"left"}[e.side],align:e.align}}function bn(e){return{side:e.side,align:{center:"center",top:"bottom",bottom:"top",left:"right",right:"left"}[e.align]}}function yn(e){return{side:e.align,align:e.side}}function Cn(e){return X(ze,e.side)?"y":"x"}const H=b({class:[String,Array],style:{type:[String,Array,Object],default:null}},"component");function $(e){const t=A("useRender");t.render=e}function Tt(e){let t=arguments.length>1&&arguments[1]!==void 0?arguments[1]:"content";const a=N(),n=N();if(we){const i=new ResizeObserver(s=>{s.length&&(t==="content"?n.value=s[0].contentRect:n.value=s[0].target.getBoundingClientRect())});Y(()=>{i.disconnect()}),K(a,(s,l)=>{l&&(i.unobserve(me(l)),n.value=void 0),s&&i.observe(me(s))},{flush:"post"})}return{resizeRef:a,contentRect:it(n)}}const Oe=b({border:[Boolean,Number,String]},"border");function Ae(e){let t=arguments.length>1&&arguments[1]!==void 0?arguments[1]:P();return{borderClasses:c(()=>{const n=D(e)?e.value:e.border,i=[];if(n===!0||n==="")i.push(`${t}--border`);else if(typeof n=="string"||n===0)for(const s of String(n).split(" "))i.push(`border-${s}`);return i})}}const Vt=[null,"default","comfortable","compact"],De=b({density:{type:String,default:"default",validator:e=>Vt.includes(e)}},"density");function Me(e){let t=arguments.length>1&&arguments[1]!==void 0?arguments[1]:P();return{densityClasses:c(()=>`${t}--density-${e.density}`)}}const Ge=b({elevation:{type:[Number,String],validator(e){const t=parseInt(e);return!isNaN(t)&&t>=0&&t<=24}}},"elevation");function He(e){return{elevationClasses:c(()=>{const a=D(e)?e.value:e.elevation,n=[];return a==null||n.push(`elevation-${a}`),n})}}const ie=b({rounded:{type:[Boolean,Number,String],default:void 0}},"rounded");function le(e){let t=arguments.length>1&&arguments[1]!==void 0?arguments[1]:P();return{roundedClasses:c(()=>{const n=D(e)?e.value:e.rounded,i=[];if(n===!0||n==="")i.push(`${t}--rounded`);else if(typeof n=="string"||n===0)for(const s of String(n).split(" "))i.push(`rounded-${s}`);return i})}}const W=b({tag:{type:String,default:"div"}},"tag");function oe(e){return Ie(()=>{const t=[],a={};if(e.value.background)if(ge(e.value.background)){if(a.backgroundColor=e.value.background,!e.value.text&&lt(e.value.background)){const n=ot(e.value.background);if(n.a==null||n.a===1){const i=rt(n);a.color=i,a.caretColor=i}}}else t.push(`bg-${e.value.background}`);return e.value.text&&(ge(e.value.text)?(a.color=e.value.text,a.caretColor=e.value.text):t.push(`text-${e.value.text}`)),{colorClasses:t,colorStyles:a}})}function q(e,t){const a=c(()=>({text:D(e)?e.value:t?e[t]:null})),{colorClasses:n,colorStyles:i}=oe(a);return{textColorClasses:n,textColorStyles:i}}function pe(e,t){const a=c(()=>({background:D(e)?e.value:t?e[t]:null})),{colorClasses:n,colorStyles:i}=oe(a);return{backgroundColorClasses:n,backgroundColorStyles:i}}const Lt=["elevated","flat","tonal","outlined","text","plain"];function $t(e,t){return v(ut,null,[e&&v("span",{key:"overlay",class:`${t}__overlay`},null),v("span",{key:"underlay",class:`${t}__underlay`},null)])}const We=b({color:String,variant:{type:String,default:"elevated",validator:e=>Lt.includes(e)}},"variant");function Rt(e){let t=arguments.length>1&&arguments[1]!==void 0?arguments[1]:P();const a=c(()=>{const{variant:s}=he(e);return`${t}--variant-${s}`}),{colorClasses:n,colorStyles:i}=oe(c(()=>{const{variant:s,color:l}=he(e);return{[["elevated","flat"].includes(s)?"background":"text"]:l}}));return{colorClasses:n,colorStyles:i,variantClasses:a}}const je=b({divided:Boolean,...Oe(),...H(),...De(),...Ge(),...ie(),...W(),...M(),...We()},"VBtnGroup"),Se=T()({name:"VBtnGroup",props:je(),setup(e,t){let{slots:a}=t;const{themeClasses:n}=G(e),{densityClasses:i}=Me(e),{borderClasses:s}=Ae(e),{elevationClasses:l}=He(e),{roundedClasses:r}=le(e);Be({VBtn:{height:"auto",color:E(e,"color"),density:E(e,"density"),flat:!0,variant:E(e,"variant")}}),$(()=>v(e.tag,{class:["v-btn-group",{"v-btn-group--divided":e.divided},n.value,s.value,i.value,l.value,r.value,e.class],style:e.style},a))}}),Nt=b({modelValue:{type:null,default:void 0},multiple:Boolean,mandatory:[Boolean,String],max:Number,selectedClass:String,disabled:Boolean},"group"),zt=b({value:null,disabled:Boolean,selectedClass:String},"group-item");function Ot(e,t){let a=arguments.length>2&&arguments[2]!==void 0?arguments[2]:!0;const n=A("useGroupItem");if(!n)throw new Error("[Vuetify] useGroupItem composable must be used inside a component setup function");const i=ct();Ee(Symbol.for(`${t.description}:id`),i);const s=dt(t,null);if(!s){if(!a)return s;throw new Error(`[Vuetify] Could not find useGroup injection with symbol ${t.description}`)}const l=E(e,"value"),r=c(()=>!!(s.disabled.value||e.disabled));s.register({id:i,value:l,disabled:r},n),Y(()=>{s.unregister(i)});const o=c(()=>s.isSelected(i)),m=c(()=>o.value&&[s.selectedClass.value,e.selectedClass]);return K(o,h=>{n.emit("group:selected",{value:h})}),{id:i,isSelected:o,toggle:()=>s.select(i,!o.value),select:h=>s.select(i,h),selectedClass:m,value:l,disabled:r,group:s}}function At(e,t){let a=!1;const n=vt([]),i=Pe(e,"modelValue",[],u=>u==null?[]:Fe(n,mt(u)),u=>{const d=Mt(n,u);return e.multiple?d:d[0]}),s=A("useGroup");function l(u,d){const p=u,g=Symbol.for(`${t.description}:id`),k=gt(g,s==null?void 0:s.vnode).indexOf(d);k>-1?n.splice(k,0,p):n.push(p)}function r(u){if(a)return;o();const d=n.findIndex(p=>p.id===u);n.splice(d,1)}function o(){const u=n.find(d=>!d.disabled);u&&e.mandatory==="force"&&!i.value.length&&(i.value=[u.id])}ft(()=>{o()}),Y(()=>{a=!0});function m(u,d){const p=n.find(g=>g.id===u);if(!(d&&(p!=null&&p.disabled)))if(e.multiple){const g=i.value.slice(),x=g.findIndex(f=>f===u),k=~x;if(d=d??!k,k&&e.mandatory&&g.length<=1||!k&&e.max!=null&&g.length+1>e.max)return;x<0&&d?g.push(u):x>=0&&!d&&g.splice(x,1),i.value=g}else{const g=i.value.includes(u);if(e.mandatory&&g)return;i.value=d??!g?[u]:[]}}function h(u){if(e.multiple,i.value.length){const d=i.value[0],p=n.findIndex(k=>k.id===d);let g=(p+u)%n.length,x=n[g];for(;x.disabled&&g!==p;)g=(g+u)%n.length,x=n[g];if(x.disabled)return;i.value=[n[g].id]}else{const d=n.find(p=>!p.disabled);d&&(i.value=[d.id])}}const C={register:l,unregister:r,selected:i,select:m,disabled:E(e,"disabled"),prev:()=>h(n.length-1),next:()=>h(1),isSelected:u=>i.value.includes(u),selectedClass:c(()=>e.selectedClass),items:c(()=>n),getItemIndex:u=>Dt(n,u)};return Ee(t,C),C}function Dt(e,t){const a=Fe(e,[t]);return a.length?e.findIndex(n=>n.id===a[0]):-1}function Fe(e,t){const a=[];return t.forEach(n=>{const i=e.find(l=>Te(n,l.value)),s=e[n];(i==null?void 0:i.value)!=null?a.push(i.id):s!=null&&a.push(s.id)}),a}function Mt(e,t){const a=[];return t.forEach(n=>{const i=e.findIndex(s=>s.id===n);if(~i){const s=e[i];a.push(s.value!=null?s.value:i)}}),a}const Xe=Symbol.for("vuetify:v-btn-toggle"),Gt=b({...je(),...Nt()},"VBtnToggle");T()({name:"VBtnToggle",props:Gt(),emits:{"update:modelValue":e=>!0},setup(e,t){let{slots:a}=t;const{isSelected:n,next:i,prev:s,select:l,selected:r}=At(e,Xe);return $(()=>{const o=Se.filterProps(e);return v(Se,Ve({class:["v-btn-toggle",e.class]},o,{style:e.style}),{default:()=>{var m;return[(m=a.default)==null?void 0:m.call(a,{isSelected:n,next:i,prev:s,select:l,selected:r})]}})}),{next:i,prev:s,select:l}}});const Ht=b({defaults:Object,disabled:Boolean,reset:[Number,String],root:[Boolean,String],scoped:Boolean},"VDefaultsProvider"),Z=T(!1)({name:"VDefaultsProvider",props:Ht(),setup(e,t){let{slots:a}=t;const{defaults:n,disabled:i,reset:s,root:l,scoped:r}=ht(e);return Be(n,{reset:s,root:l,scoped:r,disabled:i}),()=>{var o;return(o=a.default)==null?void 0:o.call(a)}}}),Wt=["x-small","small","default","large","x-large"],re=b({size:{type:[String,Number],default:"default"}},"size");function ue(e){let t=arguments.length>1&&arguments[1]!==void 0?arguments[1]:P();return Ie(()=>{let a,n;return X(Wt,e.size)?a=`${t}--size-${e.size}`:e.size&&(n={width:y(e.size),height:y(e.size)}),{sizeClasses:a,sizeStyles:n}})}const jt=b({color:String,start:Boolean,end:Boolean,icon:ne,...H(),...re(),...W({tag:"i"}),...M()},"VIcon"),ee=T()({name:"VIcon",props:jt(),setup(e,t){let{attrs:a,slots:n}=t;const i=N(),{themeClasses:s}=G(e),{iconData:l}=bt(c(()=>i.value||e.icon)),{sizeClasses:r}=ue(e),{textColorClasses:o,textColorStyles:m}=q(E(e,"color"));return $(()=>{var C,u;const h=(C=n.default)==null?void 0:C.call(n);return h&&(i.value=(u=yt(h).filter(d=>d.type===Ct&&d.children&&typeof d.children=="string")[0])==null?void 0:u.children),v(l.value.component,{tag:e.tag,icon:l.value.icon,class:["v-icon","notranslate",s.value,r.value,o.value,{"v-icon--clickable":!!a.onClick,"v-icon--start":e.start,"v-icon--end":e.end},e.class],style:[r.value?void 0:{fontSize:y(e.size),height:y(e.size),width:y(e.size)},m.value,e.style],role:a.onClick?"button":void 0,"aria-hidden":!a.onClick},{default:()=>[h]})}),{}}});function qe(e,t){const a=N(),n=pt(!1);if(Le){const i=new IntersectionObserver(s=>{n.value=!!s.find(l=>l.isIntersecting)},t);Y(()=>{i.disconnect()}),K(a,(s,l)=>{l&&(i.unobserve(l),n.value=!1),s&&i.observe(s)},{flush:"post"})}return{intersectionRef:a,isIntersecting:n}}const Ft=b({bgColor:String,color:String,indeterminate:[Boolean,String],modelValue:{type:[Number,String],default:0},rotate:{type:[Number,String],default:0},width:{type:[Number,String],default:4},...H(),...re(),...W({tag:"div"}),...M()},"VProgressCircular"),Xt=T()({name:"VProgressCircular",props:Ft(),setup(e,t){let{slots:a}=t;const n=20,i=2*Math.PI*n,s=N(),{themeClasses:l}=G(e),{sizeClasses:r,sizeStyles:o}=ue(e),{textColorClasses:m,textColorStyles:h}=q(E(e,"color")),{textColorClasses:C,textColorStyles:u}=q(E(e,"bgColor")),{intersectionRef:d,isIntersecting:p}=qe(),{resizeRef:g,contentRect:x}=Tt(),k=c(()=>Math.max(0,Math.min(100,parseFloat(e.modelValue)))),f=c(()=>Number(e.width)),S=c(()=>o.value?Number(e.size):x.value?x.value.width:Math.max(f.value,32)),B=c(()=>n/(1-f.value/S.value)*2),I=c(()=>f.value/S.value*B.value),R=c(()=>y((100-k.value)/100*i));return St(()=>{d.value=s.value,g.value=s.value}),$(()=>v(e.tag,{ref:s,class:["v-progress-circular",{"v-progress-circular--indeterminate":!!e.indeterminate,"v-progress-circular--visible":p.value,"v-progress-circular--disable-shrink":e.indeterminate==="disable-shrink"},l.value,r.value,m.value,e.class],style:[o.value,h.value,e.style],role:"progressbar","aria-valuemin":"0","aria-valuemax":"100","aria-valuenow":e.indeterminate?void 0:k.value},{default:()=>[v("svg",{style:{transform:`rotate(calc(-90deg + ${Number(e.rotate)}deg))`},xmlns:"http://www.w3.org/2000/svg",viewBox:`0 0 ${B.value} ${B.value}`},[v("circle",{class:["v-progress-circular__underlay",C.value],style:u.value,fill:"transparent",cx:"50%",cy:"50%",r:n,"stroke-width":I.value,"stroke-dasharray":i,"stroke-dashoffset":0},null),v("circle",{class:"v-progress-circular__overlay",fill:"transparent",cx:"50%",cy:"50%",r:n,"stroke-width":I.value,"stroke-dasharray":i,"stroke-dashoffset":R.value},null)]),a.default&&v("div",{class:"v-progress-circular__content"},[a.default({value:k.value})])]})),{}}}),qt=b({height:[Number,String],maxHeight:[Number,String],maxWidth:[Number,String],minHeight:[Number,String],minWidth:[Number,String],width:[Number,String]},"dimension");function Ut(e){return{dimensionStyles:c(()=>({height:y(e.height),maxHeight:y(e.maxHeight),maxWidth:y(e.maxWidth),minHeight:y(e.minHeight),minWidth:y(e.minWidth),width:y(e.width)}))}}const ke={center:"center",top:"bottom",bottom:"top",left:"right",right:"left"},Ue=b({location:String},"location");function Ye(e){let t=arguments.length>1&&arguments[1]!==void 0?arguments[1]:!1,a=arguments.length>2?arguments[2]:void 0;const{isRtl:n}=$e();return{locationStyles:c(()=>{if(!e.location)return{};const{side:s,align:l}=Pt(e.location.split(" ").length>1?e.location:`${e.location} center`,n.value);function r(m){return a?a(m):0}const o={};return s!=="center"&&(t?o[ke[s]]=`calc(100% - ${r(s)}px)`:o[s]=0),l!=="center"?t?o[ke[l]]=`calc(100% - ${r(l)}px)`:o[l]=0:(s==="center"?o.top=o.left="50%":o[{top:"left",bottom:"left",left:"top",right:"top"}[s]]="50%",o.transform={top:"translateX(-50%)",bottom:"translateX(-50%)",left:"translateY(-50%)",right:"translateY(-50%)",center:"translate(-50%, -50%)"}[s]),o})}}const Yt=b({absolute:Boolean,active:{type:Boolean,default:!0},bgColor:String,bgOpacity:[Number,String],bufferValue:{type:[Number,String],default:0},clickable:Boolean,color:String,height:{type:[Number,String],default:4},indeterminate:Boolean,max:{type:[Number,String],default:100},modelValue:{type:[Number,String],default:0},reverse:Boolean,stream:Boolean,striped:Boolean,roundedBar:Boolean,...H(),...Ue({location:"top"}),...ie(),...W(),...M()},"VProgressLinear"),Kt=T()({name:"VProgressLinear",props:Yt(),emits:{"update:modelValue":e=>!0},setup(e,t){let{slots:a}=t;const n=Pe(e,"modelValue"),{isRtl:i,rtlClasses:s}=$e(),{themeClasses:l}=G(e),{locationStyles:r}=Ye(e),{textColorClasses:o,textColorStyles:m}=q(e,"color"),{backgroundColorClasses:h,backgroundColorStyles:C}=pe(c(()=>e.bgColor||e.color)),{backgroundColorClasses:u,backgroundColorStyles:d}=pe(e,"color"),{roundedClasses:p}=le(e),{intersectionRef:g,isIntersecting:x}=qe(),k=c(()=>parseInt(e.max,10)),f=c(()=>parseInt(e.height,10)),S=c(()=>parseFloat(e.bufferValue)/k.value*100),B=c(()=>parseFloat(n.value)/k.value*100),I=c(()=>i.value!==e.reverse),R=c(()=>e.indeterminate?"fade-transition":"slide-x-transition"),j=c(()=>e.bgOpacity==null?e.bgOpacity:parseFloat(e.bgOpacity));function J(_){if(!g.value)return;const{left:V,right:Q,width:L}=g.value.getBoundingClientRect(),F=I.value?L-_.clientX+(Q-L):_.clientX-V;n.value=Math.round(F/L*k.value)}return $(()=>v(e.tag,{ref:g,class:["v-progress-linear",{"v-progress-linear--absolute":e.absolute,"v-progress-linear--active":e.active&&x.value,"v-progress-linear--reverse":I.value,"v-progress-linear--rounded":e.rounded,"v-progress-linear--rounded-bar":e.roundedBar,"v-progress-linear--striped":e.striped},p.value,l.value,s.value,e.class],style:[{bottom:e.location==="bottom"?0:void 0,top:e.location==="top"?0:void 0,height:e.active?y(f.value):0,"--v-progress-linear-height":y(f.value),...r.value},e.style],role:"progressbar","aria-hidden":e.active?"false":"true","aria-valuemin":"0","aria-valuemax":e.max,"aria-valuenow":e.indeterminate?void 0:B.value,onClick:e.clickable&&J},{default:()=>[e.stream&&v("div",{key:"stream",class:["v-progress-linear__stream",o.value],style:{...m.value,[I.value?"left":"right"]:y(-f.value),borderTop:`${y(f.value/2)} dotted`,opacity:j.value,top:`calc(50% - ${y(f.value/4)})`,width:y(100-S.value,"%"),"--v-progress-linear-stream-to":y(f.value*(I.value?1:-1))}},null),v("div",{class:["v-progress-linear__background",h.value],style:[C.value,{opacity:j.value,width:y(e.stream?S.value:100,"%")}]},null),v(Re,{name:R.value},{default:()=>[e.indeterminate?v("div",{class:"v-progress-linear__indeterminate"},[["long","short"].map(_=>v("div",{key:_,class:["v-progress-linear__indeterminate",_,u.value],style:d.value},null))]):v("div",{class:["v-progress-linear__determinate",u.value],style:[d.value,{width:y(B.value,"%")}]},null)]}),a.default&&v("div",{class:"v-progress-linear__content"},[a.default({value:B.value,buffer:S.value})])]})),{}}}),Jt=b({loading:[Boolean,String]},"loader");function Qt(e){let t=arguments.length>1&&arguments[1]!==void 0?arguments[1]:P();return{loaderClasses:c(()=>({[`${t}--loading`]:e.loading}))}}function pn(e,t){var n;let{slots:a}=t;return v("div",{class:`${e.name}__loader`},[((n=a.default)==null?void 0:n.call(a,{color:e.color,isActive:e.active}))||v(Kt,{absolute:e.absolute,active:e.active,color:e.color,height:"2",indeterminate:!0},null)])}const Zt=["static","relative","fixed","absolute","sticky"],en=b({position:{type:String,validator:e=>Zt.includes(e)}},"position");function tn(e){let t=arguments.length>1&&arguments[1]!==void 0?arguments[1]:P();return{positionClasses:c(()=>e.position?`${t}--${e.position}`:void 0)}}function nn(){const e=A("useRoute");return c(()=>{var t;return(t=e==null?void 0:e.proxy)==null?void 0:t.$route})}function Sn(){var e,t;return(t=(e=A("useRouter"))==null?void 0:e.proxy)==null?void 0:t.$router}function an(e,t){const a=kt("RouterLink"),n=c(()=>!!(e.href||e.to)),i=c(()=>(n==null?void 0:n.value)||be(t,"click")||be(e,"click"));if(typeof a=="string")return{isLink:n,isClickable:i,href:E(e,"href")};const s=e.to?a.useLink(e):void 0,l=nn();return{isLink:n,isClickable:i,route:s==null?void 0:s.route,navigate:s==null?void 0:s.navigate,isActive:s&&c(()=>{var r,o,m;return e.exact?l.value?((m=s.isExactActive)==null?void 0:m.value)&&Te(s.route.value.query,l.value.query):(o=s.isExactActive)==null?void 0:o.value:(r=s.isActive)==null?void 0:r.value}),href:c(()=>e.to?s==null?void 0:s.route.value.href:e.href)}}const sn=b({href:String,replace:Boolean,to:[String,Object],exact:Boolean},"router");let te=!1;function kn(e,t){let a=!1,n,i;we&&(Ne(()=>{window.addEventListener("popstate",s),n=e==null?void 0:e.beforeEach((l,r,o)=>{te?a?t(o):o():setTimeout(()=>a?t(o):o()),te=!0}),i=e==null?void 0:e.afterEach(()=>{te=!1})}),_t(()=>{window.removeEventListener("popstate",s),n==null||n(),i==null||i()}));function s(l){var r;(r=l.state)!=null&&r.replaced||(a=!0,setTimeout(()=>a=!1))}}function ln(e,t){K(()=>{var a;return(a=e.isActive)==null?void 0:a.value},a=>{e.isLink.value&&a&&t&&Ne(()=>{t(!0)})},{immediate:!0})}const ae=Symbol("rippleStop"),on=80;function _e(e,t){e.style.transform=t,e.style.webkitTransform=t}function se(e){return e.constructor.name==="TouchEvent"}function Ke(e){return e.constructor.name==="KeyboardEvent"}const rn=function(e,t){var C;let a=arguments.length>2&&arguments[2]!==void 0?arguments[2]:{},n=0,i=0;if(!Ke(e)){const u=t.getBoundingClientRect(),d=se(e)?e.touches[e.touches.length-1]:e;n=d.clientX-u.left,i=d.clientY-u.top}let s=0,l=.3;(C=t._ripple)!=null&&C.circle?(l=.15,s=t.clientWidth/2,s=a.center?s:s+Math.sqrt((n-s)**2+(i-s)**2)/4):s=Math.sqrt(t.clientWidth**2+t.clientHeight**2)/2;const r=`${(t.clientWidth-s*2)/2}px`,o=`${(t.clientHeight-s*2)/2}px`,m=a.center?r:`${n-s}px`,h=a.center?o:`${i-s}px`;return{radius:s,scale:l,x:m,y:h,centerX:r,centerY:o}},U={show(e,t){var d;let a=arguments.length>2&&arguments[2]!==void 0?arguments[2]:{};if(!((d=t==null?void 0:t._ripple)!=null&&d.enabled))return;const n=document.createElement("span"),i=document.createElement("span");n.appendChild(i),n.className="v-ripple__container",a.class&&(n.className+=` ${a.class}`);const{radius:s,scale:l,x:r,y:o,centerX:m,centerY:h}=rn(e,t,a),C=`${s*2}px`;i.className="v-ripple__animation",i.style.width=C,i.style.height=C,t.appendChild(n);const u=window.getComputedStyle(t);u&&u.position==="static"&&(t.style.position="relative",t.dataset.previousPosition="static"),i.classList.add("v-ripple__animation--enter"),i.classList.add("v-ripple__animation--visible"),_e(i,`translate(${r}, ${o}) scale3d(${l},${l},${l})`),i.dataset.activated=String(performance.now()),setTimeout(()=>{i.classList.remove("v-ripple__animation--enter"),i.classList.add("v-ripple__animation--in"),_e(i,`translate(${m}, ${h}) scale3d(1,1,1)`)},0)},hide(e){var s;if(!((s=e==null?void 0:e._ripple)!=null&&s.enabled))return;const t=e.getElementsByClassName("v-ripple__animation");if(t.length===0)return;const a=t[t.length-1];if(a.dataset.isHiding)return;a.dataset.isHiding="true";const n=performance.now()-Number(a.dataset.activated),i=Math.max(250-n,0);setTimeout(()=>{a.classList.remove("v-ripple__animation--in"),a.classList.add("v-ripple__animation--out"),setTimeout(()=>{var r;e.getElementsByClassName("v-ripple__animation").length===1&&e.dataset.previousPosition&&(e.style.position=e.dataset.previousPosition,delete e.dataset.previousPosition),((r=a.parentNode)==null?void 0:r.parentNode)===e&&e.removeChild(a.parentNode)},300)},i)}};function Je(e){return typeof e>"u"||!!e}function z(e){const t={},a=e.currentTarget;if(!(!(a!=null&&a._ripple)||a._ripple.touched||e[ae])){if(e[ae]=!0,se(e))a._ripple.touched=!0,a._ripple.isTouch=!0;else if(a._ripple.isTouch)return;if(t.center=a._ripple.centered||Ke(e),a._ripple.class&&(t.class=a._ripple.class),se(e)){if(a._ripple.showTimerCommit)return;a._ripple.showTimerCommit=()=>{U.show(e,a,t)},a._ripple.showTimer=window.setTimeout(()=>{var n;(n=a==null?void 0:a._ripple)!=null&&n.showTimerCommit&&(a._ripple.showTimerCommit(),a._ripple.showTimerCommit=null)},on)}else U.show(e,a,t)}}function xe(e){e[ae]=!0}function w(e){const t=e.currentTarget;if(t!=null&&t._ripple){if(window.clearTimeout(t._ripple.showTimer),e.type==="touchend"&&t._ripple.showTimerCommit){t._ripple.showTimerCommit(),t._ripple.showTimerCommit=null,t._ripple.showTimer=window.setTimeout(()=>{w(e)});return}window.setTimeout(()=>{t._ripple&&(t._ripple.touched=!1)}),U.hide(t)}}function Qe(e){const t=e.currentTarget;t!=null&&t._ripple&&(t._ripple.showTimerCommit&&(t._ripple.showTimerCommit=null),window.clearTimeout(t._ripple.showTimer))}let O=!1;function Ze(e){!O&&(e.keyCode===ye.enter||e.keyCode===ye.space)&&(O=!0,z(e))}function et(e){O=!1,w(e)}function tt(e){O&&(O=!1,w(e))}function nt(e,t,a){const{value:n,modifiers:i}=t,s=Je(n);if(s||U.hide(e),e._ripple=e._ripple??{},e._ripple.enabled=s,e._ripple.centered=i.center,e._ripple.circle=i.circle,xt(n)&&n.class&&(e._ripple.class=n.class),s&&!a){if(i.stop){e.addEventListener("touchstart",xe,{passive:!0}),e.addEventListener("mousedown",xe);return}e.addEventListener("touchstart",z,{passive:!0}),e.addEventListener("touchend",w,{passive:!0}),e.addEventListener("touchmove",Qe,{passive:!0}),e.addEventListener("touchcancel",w),e.addEventListener("mousedown",z),e.addEventListener("mouseup",w),e.addEventListener("mouseleave",w),e.addEventListener("keydown",Ze),e.addEventListener("keyup",et),e.addEventListener("blur",tt),e.addEventListener("dragstart",w,{passive:!0})}else!s&&a&&at(e)}function at(e){e.removeEventListener("mousedown",z),e.removeEventListener("touchstart",z),e.removeEventListener("touchend",w),e.removeEventListener("touchmove",Qe),e.removeEventListener("touchcancel",w),e.removeEventListener("mouseup",w),e.removeEventListener("mouseleave",w),e.removeEventListener("keydown",Ze),e.removeEventListener("keyup",et),e.removeEventListener("dragstart",w),e.removeEventListener("blur",tt)}function un(e,t){nt(e,t,!1)}function cn(e){delete e._ripple,at(e)}function dn(e,t){if(t.value===t.oldValue)return;const a=Je(t.oldValue);nt(e,t,a)}const vn={mounted:un,unmounted:cn,updated:dn},fn=b({active:{type:Boolean,default:void 0},symbol:{type:null,default:Xe},flat:Boolean,icon:[Boolean,String,Function,Object],prependIcon:ne,appendIcon:ne,block:Boolean,slim:Boolean,stacked:Boolean,ripple:{type:[Boolean,Object],default:!0},text:String,...Oe(),...H(),...De(),...qt(),...Ge(),...zt(),...Jt(),...Ue(),...en(),...ie(),...sn(),...re(),...W({tag:"button"}),...M(),...We({variant:"elevated"})},"VBtn"),_n=T()({name:"VBtn",directives:{Ripple:vn},props:fn(),emits:{"group:selected":e=>!0},setup(e,t){let{attrs:a,slots:n}=t;const{themeClasses:i}=G(e),{borderClasses:s}=Ae(e),{colorClasses:l,colorStyles:r,variantClasses:o}=Rt(e),{densityClasses:m}=Me(e),{dimensionStyles:h}=Ut(e),{elevationClasses:C}=He(e),{loaderClasses:u}=Qt(e),{locationStyles:d}=Ye(e),{positionClasses:p}=tn(e),{roundedClasses:g}=le(e),{sizeClasses:x,sizeStyles:k}=ue(e),f=Ot(e,e.symbol,!1),S=an(e,a),B=c(()=>{var _;return e.active!==void 0?e.active:S.isLink.value?(_=S.isActive)==null?void 0:_.value:f==null?void 0:f.isSelected.value}),I=c(()=>(f==null?void 0:f.disabled.value)||e.disabled),R=c(()=>e.variant==="elevated"&&!(e.disabled||e.flat||e.border)),j=c(()=>{if(!(e.value===void 0||typeof e.value=="symbol"))return Object(e.value)===e.value?JSON.stringify(e.value,null,0):e.value});function J(_){var V;I.value||S.isLink.value&&(_.metaKey||_.ctrlKey||_.shiftKey||_.button!==0||a.target==="_blank")||((V=S.navigate)==null||V.call(S,_),f==null||f.toggle())}return ln(S,f==null?void 0:f.select),$(()=>{var ce,de;const _=S.isLink.value?"a":e.tag,V=!!(e.prependIcon||n.prepend),Q=!!(e.appendIcon||n.append),L=!!(e.icon&&e.icon!==!0),F=(f==null?void 0:f.isSelected.value)&&(!S.isLink.value||((ce=S.isActive)==null?void 0:ce.value))||!f||((de=S.isActive)==null?void 0:de.value);return wt(v(_,{type:_==="a"?void 0:"button",class:["v-btn",f==null?void 0:f.selectedClass.value,{"v-btn--active":B.value,"v-btn--block":e.block,"v-btn--disabled":I.value,"v-btn--elevated":R.value,"v-btn--flat":e.flat,"v-btn--icon":!!e.icon,"v-btn--loading":e.loading,"v-btn--slim":e.slim,"v-btn--stacked":e.stacked},i.value,s.value,F?l.value:void 0,m.value,C.value,u.value,p.value,g.value,x.value,o.value,e.class],style:[F?r.value:void 0,h.value,d.value,k.value,e.style],disabled:I.value||void 0,href:S.href.value,onClick:J,value:j.value},{default:()=>{var ve;return[$t(!0,"v-btn"),!e.icon&&V&&v("span",{key:"prepend",class:"v-btn__prepend"},[n.prepend?v(Z,{key:"prepend-defaults",disabled:!e.prependIcon,defaults:{VIcon:{icon:e.prependIcon}}},n.prepend):v(ee,{key:"prepend-icon",icon:e.prependIcon},null)]),v("span",{class:"v-btn__content","data-no-activator":""},[!n.default&&L?v(ee,{key:"content-icon",icon:e.icon},null):v(Z,{key:"content-defaults",disabled:!L,defaults:{VIcon:{icon:e.icon}}},{default:()=>{var fe;return[((fe=n.default)==null?void 0:fe.call(n))??e.text]}})]),!e.icon&&Q&&v("span",{key:"append",class:"v-btn__append"},[n.append?v(Z,{key:"append-defaults",disabled:!e.appendIcon,defaults:{VIcon:{icon:e.appendIcon}}},n.append):v(ee,{key:"append-icon",icon:e.appendIcon},null)]),!!e.loading&&v("span",{key:"loader",class:"v-btn__loader"},[((ve=n.loader)==null?void 0:ve.call(n))??v(Xt,{color:typeof e.loading=="boolean"?void 0:e.loading,indeterminate:!0,size:"23",width:"2"},null)])]}}),[[It("ripple"),!I.value&&e.ripple,null]])}),{}}}),xn=b({transition:{type:[Boolean,String,Object],default:"fade-transition",validator:e=>e!==!0}},"transition"),wn=(e,t)=>{let{slots:a}=t;const{transition:n,disabled:i,...s}=e,{component:l=Re,...r}=typeof n=="object"?n:{};return Bt(l,Ve(typeof n=="string"?{name:i?"":n}:r,s,{disabled:i}),a)};function mn(e,t){if(!Le)return;const a=t.modifiers||{},n=t.value,{handler:i,options:s}=typeof n=="object"?n:{handler:n,options:{}},l=new IntersectionObserver(function(){var C;let r=arguments.length>0&&arguments[0]!==void 0?arguments[0]:[],o=arguments.length>1?arguments[1]:void 0;const m=(C=e._observe)==null?void 0:C[t.instance.$.uid];if(!m)return;const h=r.some(u=>u.isIntersecting);i&&(!a.quiet||m.init)&&(!a.once||h||m.init)&&i(h,r,o),h&&a.once?st(e,t):m.init=!0},s);e._observe=Object(e._observe),e._observe[t.instance.$.uid]={init:!1,observer:l},l.observe(e)}function st(e,t){var n;const a=(n=e._observe)==null?void 0:n[t.instance.$.uid];a&&(a.observer.unobserve(e),delete e._observe[t.instance.$.uid])}const In={mounted:mn,unmounted:st};export{At as A,zt as B,re as C,ue as D,Ot as E,Pt as F,hn as G,bn as H,yn as I,Cn as J,xn as K,kn as L,wn as M,Tt as N,In as O,Ue as P,en as Q,vn as R,Ye as S,tn as T,Jt as U,_n as V,Qt as W,pn as X,ee as a,W as b,Z as c,Oe as d,De as e,qt as f,Ge as g,ie as h,sn as i,We as j,an as k,Ae as l,H as m,Rt as n,Me as o,Ut as p,He as q,le as r,$t as s,q as t,$ as u,pe as v,Sn as w,Ce as x,Xt as y,Nt as z};

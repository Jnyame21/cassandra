import{bc as o,r as c,aF as d,U as f,e as v,aX as l,aY as i,bd as h,be as m}from"./entry.eZbnTIXg.js";function b(t,a={}){const e=a.head||o();if(e)return e.ssr?e.push(t,a):p(e,t,a)}function p(t,a,e={}){const s=c(!1),n=c({});d(()=>{n.value=s.value?{}:h(a)});const r=t.push(n.value,e);return f(n,u=>{r.patch(u)}),m()&&(v(()=>{r.dispose()}),l(()=>{s.value=!0}),i(()=>{s.value=!1})),r}export{b as u};

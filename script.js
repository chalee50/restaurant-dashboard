const SECTIONS = [
  ["menu","เมนู","🍜"],["tables","โต๊ะ","🪑"],["order","ออเดอร์","🧾"],
  ["kitchen","ครัว","🔥"],["checkout","เช็คบิล","💵"],["report","รายงาน","📊"]
];
const TABLE_STATUSES = ["ว่าง","มีลูกค้า","รอเช็คบิล"];
const ORDER_STATUSES = ["รอทำ","กำลังทำ","เสร็จแล้ว"];

function loadDB(){
  try{
    const raw = localStorage.getItem("restaurant_db");
    if(raw) return JSON.parse(raw);
  }catch(e){ console.error(e); }
  return {
    menu:[
      {id:1,name:"ผัดกะเพราหมู",category:"จานเดียว",price:50,out:false},
      {id:2,name:"ข้าวผัดปู",category:"จานเดียว",price:60,out:false},
      {id:3,name:"ข้าวผัดกุ้ง",category:"จานเดียว",price:65,out:false},
      {id:4,name:"ข้าวมันไก่",category:"จานเดียว",price:45,out:false},
      {id:5,name:"ข้าวหมูแดง",category:"จานเดียว",price:50,out:false},
      {id:6,name:"ข้าวขาหมู",category:"จานเดียว",price:55,out:false},
      {id:7,name:"ต้มยำกุ้ง",category:"ต้ม/แกง",price:120,out:false},
      {id:8,name:"ต้มข่าไก่",category:"ต้ม/แกง",price:90,out:false},
      {id:9,name:"แกงเขียวหวานไก่",category:"ต้ม/แกง",price:80,out:false},
      {id:10,name:"แกงส้มผักรวม",category:"ต้ม/แกง",price:70,out:false},
      {id:11,name:"ยำวุ้นเส้น",category:"ยำ/สลัด",price:70,out:false},
      {id:12,name:"ยำมาม่า",category:"ยำ/สลัด",price:60,out:false},
      {id:13,name:"ส้มตำไทย",category:"ยำ/สลัด",price:50,out:false},
      {id:14,name:"ลาบหมู",category:"ยำ/สลัด",price:65,out:false},
      {id:15,name:"ไก่ทอดหาดใหญ่",category:"ทอด/ปิ้งย่าง",price:90,out:false},
      {id:16,name:"หมูปิ้ง",category:"ทอด/ปิ้งย่าง",price:40,out:false},
      {id:17,name:"ปีกไก่ทอด",category:"ทอด/ปิ้งย่าง",price:70,out:false},
      {id:18,name:"ปลาหมึกย่าง",category:"ทอด/ปิ้งย่าง",price:100,out:false},
      {id:19,name:"ผัดไทยกุ้งสด",category:"ผัด",price:70,out:false},
      {id:20,name:"ผัดซีอิ๊วหมู",category:"ผัด",price:55,out:false},
      {id:21,name:"ผัดผักบุ้งไฟแดง",category:"ผัด",price:45,out:false},
      {id:22,name:"คะน้าหมูกรอบ",category:"ผัด",price:60,out:false},
      {id:23,name:"ก๋วยเตี๋ยวเรือ",category:"ก๋วยเตี๋ยว",price:45,out:false},
      {id:24,name:"ก๋วยเตี๋ยวต้มยำ",category:"ก๋วยเตี๋ยว",price:50,out:false},
      {id:25,name:"บะหมี่เกี๊ยวหมูแดง",category:"ก๋วยเตี๋ยว",price:55,out:false},
      {id:26,name:"ชาเย็น",category:"เครื่องดื่ม",price:25,out:false},
      {id:27,name:"กาแฟเย็น",category:"เครื่องดื่ม",price:30,out:false},
      {id:28,name:"น้ำมะนาว",category:"เครื่องดื่ม",price:25,out:false},
      {id:29,name:"ข้าวเหนียวมะม่วง",category:"ของหวาน",price:60,out:false},
      {id:30,name:"บัวลอยไข่หวาน",category:"ของหวาน",price:40,out:false},
    ],
    tables:Array.from({length:10},(_,i)=>({id:i+1,status:"ว่าง"})),
    orders:{}, sales:[]
  };
}
let db = loadDB();
function save(){ try{ localStorage.setItem("restaurant_db", JSON.stringify(db)); }catch(e){ console.error(e); } }
let curTable = null, curOut = 0;

function go(id){
  document.querySelectorAll("section").forEach(s=>s.classList.toggle("active", s.id===id));
  document.querySelectorAll("nav button").forEach(b=>b.classList.toggle("active", b.dataset.id===id));
  const found = SECTIONS.find(s=>s[0]===id);
  document.getElementById("pageTitle").textContent = found ? found[1] : "";
  render();
}
document.getElementById("nav").innerHTML = SECTIONS.map(([id,label,ic])=>`<button data-id="${id}" onclick="go('${id}')"><span class="ic">${ic}</span><span>${label}</span></button>`).join("");
document.getElementById("main").innerHTML = SECTIONS.map(([id])=>`<section id="${id}"></section>`).join("");

function nextId(list){ return list.reduce((m,i)=>Math.max(m,i.id),0)+1; }
function esc(s){ return String(s).replace(/[<>&"]/g,c=>({"<":"&lt;",">":"&gt;","&":"&amp;",'"':"&quot;"}[c])); }

// ---------- เมนู ----------
function renderMenu(){
  const rows = db.menu.map(m=>`<tr>
    <td>${m.id}</td><td>${esc(m.name)}</td><td>${esc(m.category)}</td><td>${m.price.toFixed(2)}</td>
    <td>${m.out?'<span class="badge b-bill">หมด</span>':'<span class="badge b-free">มี</span>'}</td>
    <td>
      <button class="btn sm gray" onclick="toggleStock(${m.id})">สลับสถานะ</button>
      <button class="btn sm" onclick="editPrice(${m.id})">แก้ราคา</button>
      <button class="btn sm red" onclick="delMenu(${m.id})">ลบ</button>
    </td></tr>`).join("");
  document.getElementById("menu").innerHTML = `
    <div class="card"><h3>เพิ่มเมนูใหม่</h3>
      <div class="row">
        <input id="mName" placeholder="ชื่อเมนู">
        <input id="mCat" placeholder="หมวดหมู่">
        <input id="mPrice" type="number" min="0" step="0.01" placeholder="ราคา" style="width:6rem">
        <button class="btn" onclick="addMenu()">เพิ่ม</button>
      </div>
    </div>
    <div class="card"><table><tr><th>ID</th><th>ชื่อ</th><th>หมวดหมู่</th><th>ราคา</th><th>สถานะ</th><th>จัดการ</th></tr>${rows}</table></div>`;
}
function addMenu(){
  const name=document.getElementById("mName").value.trim();
  const cat=document.getElementById("mCat").value.trim();
  const price=parseFloat(document.getElementById("mPrice").value);
  if(!name || !cat || isNaN(price) || price<0){ alert("กรอกข้อมูลให้ครบและถูกต้อง"); return; }
  db.menu.push({id:nextId(db.menu),name,category:cat,price,out:false});
  save(); renderMenu();
}
function toggleStock(id){ const m=db.menu.find(x=>x.id===id); if(m){ m.out=!m.out; save(); renderMenu(); } }
function editPrice(id){
  const m=db.menu.find(x=>x.id===id); if(!m) return;
  const p=parseFloat(prompt("ราคาใหม่:", m.price));
  if(!isNaN(p) && p>=0){ m.price=p; save(); renderMenu(); }
}
function delMenu(id){ if(confirm("ลบเมนูนี้?")){ db.menu=db.menu.filter(x=>x.id!==id); save(); renderMenu(); } }

// ---------- โต๊ะ ----------
function statusBadge(s){ return s==="ว่าง"?"b-free":(s==="มีลูกค้า"?"b-occ":"b-bill"); }
function renderTables(){
  const cards = db.tables.map(t=>`
    <div class="card row" style="justify-content:space-between">
      <span>โต๊ะ ${t.id} <span class="badge ${statusBadge(t.status)}">${t.status}</span></span>
      <select onchange="setTable(${t.id}, this.value)">
        ${TABLE_STATUSES.map(s=>`<option ${s===t.status?"selected":""}>${s}</option>`).join("")}
      </select>
    </div>`).join("");
  document.getElementById("tables").innerHTML = cards;
}
function setTable(id, status){ const t=db.tables.find(x=>x.id===id); if(t){ t.status=status; save(); renderTables(); } }

// ---------- ออเดอร์ ----------
function renderOrder(){
  const opts = db.tables.map(t=>`<option value="${t.id}" ${curTable===t.id?"selected":""}>โต๊ะ ${t.id} (${t.status})</option>`).join("");
  const menuOpts = db.menu.filter(m=>!m.out).map(m=>`<option value="${m.id}">${esc(m.name)} - ${m.price}฿</option>`).join("");
  const items = curTable ? (db.orders[curTable]||[]) : [];
  const rows = items.map((it,i)=>`<tr>
    <td>${esc(it.name)}</td><td>${it.price.toFixed(2)}</td>
    <td><button class="btn sm gray" onclick="qty(${i},-1)">-</button> ${it.qty} <button class="btn sm gray" onclick="qty(${i},1)">+</button></td>
    <td>${(it.price*it.qty).toFixed(2)}</td><td>${it.status}</td>
    <td><button class="btn sm red" onclick="qty(${i},-999)">ลบ</button></td></tr>`).join("");
  const subtotal = items.reduce((s,i)=>s+i.price*i.qty,0);
  document.getElementById("order").innerHTML = `
    <div class="card row">เลือกโต๊ะ:
      <select onchange="pickTable(this.value)"><option value="">-- เลือก --</option>${opts}</select>
    </div>
    ${curTable?`
    <div class="card"><div class="row">
      <select id="oMenu">${menuOpts||'<option disabled>ไม่มีเมนูว่าง</option>'}</select>
      <input id="oQty" type="number" min="1" value="1" style="width:4rem">
      <button class="btn" onclick="addOrder()">เพิ่มรายการ</button>
    </div></div>
    <div class="card"><table><tr><th>รายการ</th><th>ราคา</th><th>จำนวน</th><th>รวม</th><th>สถานะ</th><th></th></tr>${rows||'<tr><td colspan="6" class="sub">ยังไม่มีรายการ</td></tr>'}</table>
    <p><b>ยอดรวม: ${subtotal.toFixed(2)} บาท</b></p></div>`:""}
  `;
}
function pickTable(v){ curTable = v?parseInt(v):null; renderOrder(); }
function addOrder(){
  const menuId = parseInt(document.getElementById("oMenu").value);
  const qty = parseInt(document.getElementById("oQty").value);
  const m = db.menu.find(x=>x.id===menuId);
  if(!m || m.out || !qty || qty<1){ alert("เลือกเมนูและจำนวนให้ถูกต้อง"); return; }
  if(!db.orders[curTable]) db.orders[curTable]=[];
  db.orders[curTable].push({menuId:m.id,name:m.name,price:m.price,qty,status:"รอทำ",time:new Date().toLocaleTimeString('th-TH')});
  const t = db.tables.find(x=>x.id===curTable);
  if(t && t.status==="ว่าง") t.status="มีลูกค้า";
  save(); renderOrder();
}
function qty(i,delta){
  const items = db.orders[curTable];
  if(delta<=-999){ items.splice(i,1); }
  else { items[i].qty += delta; if(items[i].qty<=0) items.splice(i,1); }
  save(); renderOrder();
}

// ---------- ครัว ----------
function renderKitchen(){
  let pending=[];
  for(const tid in db.orders){ db.orders[tid].forEach((it,i)=>{ if(it.status!=="เสร็จแล้ว") pending.push({tid,i,it}); }); }
  pending.sort((a,b)=>a.it.time.localeCompare(b.it.time));
  const rows = pending.map(p=>`<tr>
    <td>${p.it.time}</td><td>โต๊ะ ${p.tid}</td><td>${esc(p.it.name)}</td><td>${p.it.qty}</td>
    <td><span class="badge ${p.it.status==='รอทำ'?'b-wait':(p.it.status==='กำลังทำ'?'b-doing':'b-done')}">${p.it.status}</span></td>
    <td><button class="btn sm" onclick="advance('${p.tid}',${p.i})">ถัดไป</button></td></tr>`).join("");
  document.getElementById("kitchen").innerHTML = `<div class="card"><table><tr><th>เวลา</th><th>โต๊ะ</th><th>เมนู</th><th>จำนวน</th><th>สถานะ</th><th></th></tr>${rows||'<tr><td colspan="6" class="sub">ไม่มีออเดอร์ค้าง</td></tr>'}</table></div>`;
}
function advance(tid,i){
  const it = db.orders[tid][i];
  const idx = ORDER_STATUSES.indexOf(it.status);
  it.status = ORDER_STATUSES[Math.min(idx+1, ORDER_STATUSES.length-1)];
  save(); renderKitchen();
}

// ---------- เช็คบิล ----------
function renderCheckout(){
  const opts = db.tables.map(t=>`<option value="${t.id}" ${curOut===t.id?"selected":""}>โต๊ะ ${t.id}</option>`).join("");
  const items = curOut ? (db.orders[curOut]||[]) : [];
  const subtotal = items.reduce((s,i)=>s+i.price*i.qty,0);
  document.getElementById("checkout").innerHTML = `
    <div class="card row">เลือกโต๊ะ: <select onchange="pickOut(this.value)"><option value="">-- เลือก --</option>${opts}</select></div>
    ${curOut && items.length ? `
    <div class="card">
      <table>${items.map(i=>`<tr><td>${esc(i.name)}</td><td>${i.qty} x ${i.price}</td><td>${(i.qty*i.price).toFixed(2)}</td></tr>`).join("")}</table>
      <div class="row">ส่วนลด% <input id="cDisc" type="number" value="0" style="width:4rem">
        ภาษี% <input id="cTax" type="number" value="7" style="width:4rem">
        ค่าบริการ% <input id="cSvc" type="number" value="10" style="width:4rem">
        <button class="btn" onclick="calcBill()">คำนวณ</button></div>
      <div id="billOut"></div>
    </div>`: (curOut?'<p class="sub">โต๊ะนี้ยังไม่มีรายการ</p>':'')}
  `;
}
function pickOut(v){ curOut=v?parseInt(v):null; renderCheckout(); }
function calcBill(){
  const items = db.orders[curOut]||[];
  const subtotal = items.reduce((s,i)=>s+i.price*i.qty,0);
  const disc = parseFloat(document.getElementById("cDisc").value)||0;
  const tax = parseFloat(document.getElementById("cTax").value)||0;
  const svc = parseFloat(document.getElementById("cSvc").value)||0;
  const discAmt = subtotal*disc/100;
  const afterDisc = subtotal-discAmt;
  const svcAmt = afterDisc*svc/100;
  const taxAmt = (afterDisc+svcAmt)*tax/100;
  const total = afterDisc+svcAmt+taxAmt;
  document.getElementById("billOut").innerHTML = `
    <div class="card">
      <p class="sub">ยอดรวม: ${subtotal.toFixed(2)} | ส่วนลด: -${discAmt.toFixed(2)} | ค่าบริการ: ${svcAmt.toFixed(2)} | ภาษี: ${taxAmt.toFixed(2)}</p>
      <p class="sub" style="margin-bottom:.1rem">ยอดสุทธิ</p>
      <p class="total-figure">${total.toFixed(2)} บาท</p>
      <button class="btn" onclick="confirmBill(${subtotal},${disc},${discAmt},${svc},${svcAmt},${tax},${taxAmt},${total})">ยืนยันปิดบิล</button>
    </div>`;
}
function confirmBill(subtotal,disc,discAmt,svc,svcAmt,tax,taxAmt,total){
  const items = db.orders[curOut]||[];
  db.sales.push({date:new Date().toISOString().slice(0,10), time:new Date().toLocaleTimeString('th-TH'),
    tableId:curOut, items:JSON.parse(JSON.stringify(items)),
    bill:{subtotal,disc,discAmt,svc,svcAmt,tax,taxAmt,total}});
  db.orders[curOut]=[];
  const t=db.tables.find(x=>x.id===curOut); if(t) t.status="ว่าง";
  save(); curOut=null; renderCheckout(); alert("ปิดบิลสำเร็จ!");
}

// ---------- รายงาน ----------
function renderReport(){
  const today = new Date().toISOString().slice(0,10);
  const todaySales = db.sales.filter(s=>s.date===today);
  const totalAmt = todaySales.reduce((s,r)=>s+r.bill.total,0);
  const qtyByName = {};
  db.sales.forEach(r=>r.items.forEach(i=>{ qtyByName[i.name]=(qtyByName[i.name]||0)+i.qty; }));
  const top = Object.entries(qtyByName).sort((a,b)=>b[1]-a[1]).slice(0,5);
  document.getElementById("report").innerHTML = `
    <div class="card"><h3>ยอดขายวันนี้ (${today})</h3><p>จำนวนบิล: ${todaySales.length} | ยอดรวม: ${totalAmt.toFixed(2)} บาท</p></div>
    <div class="card"><h3>เมนูขายดี</h3>
      ${top.length? '<ol>'+top.map(([n,q])=>`<li>${esc(n)} — ขายได้ ${q} รายการ</li>`).join("")+'</ol>' : '<p class="sub">ยังไม่มีข้อมูล</p>'}
    </div>`;
}

function render(){
  const active = document.querySelector("section.active");
  if(!active) return;
  ({menu:renderMenu, tables:renderTables, order:renderOrder, kitchen:renderKitchen, checkout:renderCheckout, report:renderReport})[active.id]();
}
go("menu");

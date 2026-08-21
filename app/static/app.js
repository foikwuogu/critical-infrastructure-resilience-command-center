const $=x=>document.getElementById(x);
let currentAssets=[];

async function api(u,o={}){const r=await fetch(u,o);if(!r.ok)throw Error(await r.text());return r.json()}
function setbar(id,val){$(id).style.width=Math.max(0,Math.min(100,val))+"%"}
function riskClass(asset){return asset.failure_probability>=.65?"critical":asset.failure_probability>=.35?"high":"good"}
function posture(score){return score>=75?"Strong":score>=55?"Watch":score>=35?"Elevated":"Critical"}
function formatScenario(result){return `Before: ${result.before}\nAfter: ${result.after}\nChange: ${result.change}\n\n${result.explanation.decision_rule}\nHuman review required: ${result.explanation.human_review_required?"Yes":"No"}`}

function renderAssets(){
 const query=$("assetSearch").value.trim().toLowerCase(),filter=$("assetFilter").value,tb=$("assetRows");
 const rows=currentAssets.filter(a=>{
  const risk=riskClass(a);
  const matchesFilter=filter==="all"||risk===filter;
  const matchesQuery=[a.name,a.zone,a.asset_type,a.crypto_algorithm,a.pqc_status].some(v=>String(v).toLowerCase().includes(query));
  return matchesFilter&&matchesQuery;
 });
 tb.innerHTML=rows.map(a=>{const rc=riskClass(a);return `<tr><td><b>${a.name}</b><br><span>${a.asset_type}</span></td><td>${a.zone}</td><td>${a.criticality}</td><td>${a.health}</td><td><span class="risk-badge ${rc} ${rc}-bg">${(a.failure_probability*100).toFixed(1)}%</span></td><td>${a.rul_hours}h</td><td>${a.crypto_algorithm}</td><td>${a.pqc_status} (${a.pqc_readiness})</td><td>${a.identity_trust}</td></tr>`}).join("")||`<tr><td colspan="9">No assets match the current filter.</td></tr>`;
 const critical=currentAssets.filter(a=>riskClass(a)==="critical").length,high=currentAssets.filter(a=>riskClass(a)==="high").length,legacy=currentAssets.filter(a=>a.pqc_status==="legacy").length;
 $("assetSummary").innerHTML=`<div class="mini-stat"><span>Total assets</span><b>${currentAssets.length}</b></div><div class="mini-stat"><span>Critical risk</span><b class="critical">${critical}</b></div><div class="mini-stat"><span>High risk</span><b class="high">${high}</b></div><div class="mini-stat"><span>Legacy crypto</span><b>${legacy}</b></div>`;
}

async function refresh(){
 try{
  const r=await api("/api/resilience");
  $("overall").textContent=r.overall;$("cyber").textContent=r.cyber;$("physical").textContent=r.physical;$("pqc").textContent=r.pqc;$("availability").textContent=r.availability+"%";
  $("posture").textContent=posture(r.overall);$("overallHint").textContent=posture(r.overall)+" posture";$("updated").textContent="Updated "+new Date().toLocaleTimeString([], {hour:"2-digit",minute:"2-digit"});
  setbar("barCyber",r.cyber);setbar("barPqc",r.pqc);setbar("barPhysical",r.physical);setbar("barAvailability",r.availability);
  $("txtCyber").textContent=r.cyber;$("txtPqc").textContent=r.pqc;$("txtPhysical").textContent=r.physical;$("txtAvailability").textContent=r.availability;
  currentAssets=await api("/api/assets");renderAssets();
  const m=await api("/api/migration"),mq=$("migrationContent");mq.innerHTML=`<p>Legacy: <b>${m.legacy}</b> &nbsp; Planned: <b>${m.planned}</b> &nbsp; Migrated: <b>${m.migrated}</b></p>`+m.priority.map(x=>`<div class="queue"><div class="queue-head"><b>${x.asset}</b><span>Readiness ${x.readiness}</span></div><small>${x.algorithm} | criticality ${x.criticality}</small></div>`).join("");
  const ev=await api("/api/events"),e=$("eventList");e.innerHTML=ev.slice(0,10).map(x=>`<div class="event ${x.severity}"><b>${x.severity}: ${x.title}</b><br><span>${x.category} | impact ${x.operational_impact}</span><br>${x.description}</div>`).join("")||"<p>No incidents recorded.</p>";
 }catch(e){$("scenario").textContent=e.message}
}
document.querySelectorAll("[data-s]").forEach(b=>b.onclick=async()=>{b.disabled=true;try{const r=await api("/api/scenarios/"+b.dataset.s,{method:"POST"});$("scenario").textContent=formatScenario(r);await refresh()}catch(e){$("scenario").textContent=e.message}finally{b.disabled=false}});
$("reset").onclick=async()=>{await api("/api/reset",{method:"POST"});$("scenario").textContent="Digital twin reset.";await refresh()};
$("assetSearch").addEventListener("input",renderAssets);$("assetFilter").addEventListener("change",renderAssets);
refresh();setInterval(refresh,15000);

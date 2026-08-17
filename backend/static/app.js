const $ = id => document.getElementById(id); let current = null;
const missions = ["Find something alive that you normally walk past.", "Look for a flower and see how many insects visit it.", "Find a tree older than you and observe its bark for one minute.", "Listen quietly for three different natural sounds.", "Find two plants growing in different conditions.", "Look closely at one leaf. What tiny details did you miss?"];
$("dailyMission").textContent = missions[Math.floor(Math.random() * missions.length)];
$("discover").onclick = () => $("file").click();

$("file").onchange = async () => {
    const f = $("file").files[0]; if (!f) return;
    $("discover").disabled = true; $("discover").textContent = "🌿 Looking closer...";
    try {
        const fd = new FormData(); fd.append("image", f);
        const r = await fetch("/api/analyze", { method: "POST", body: fd }); const j = await r.json();
        if (!r.ok || !j.success) throw Error(j.detail || "Analysis failed");
        current = j.data; showResult(current, f);
    } catch (e) { toast(e.message) } finally { $("discover").disabled = false; $("discover").textContent = "📷 Discover nature"; $("file").value = "" }
};

function showResult(d, f) {
    $("name").textContent = d.name || "Nature discovery"; $("scientific").textContent = d.scientific_name || "";
    $("confidence").textContent = `${d.confidence ?? "?"}% confidence`; $("description").textContent = d.description || "";
    $("role").textContent = d.ecological_role || ""; $("fact").textContent = d.interesting_fact || "Take a closer look and see what you discover.";
    $("look").textContent = d.look_closer || ""; $("mission").textContent = d.nature_mission || "Spend a few minutes observing this part of nature.";
    $("missionType").textContent = d.mission_type || "observe"; $("reward").textContent = `+${Number(d.xp_reward) || 10} XP`;
    $("connection").textContent = d.connection_message || "You just noticed a small part of the ecosystem around you.";
    if (d.safety_note) { $("safety").textContent = "⚠️ " + d.safety_note; $("safety").classList.remove("hidden") } else $("safety").classList.add("hidden");
    $("photo").src = URL.createObjectURL(f); $("modal").classList.remove("hidden"); document.body.style.overflow = "hidden";
}
function close() { $("modal").classList.add("hidden"); document.body.style.overflow = "" }
$("close").onclick = close; $("backdrop").onclick = close;

$("save").onclick = async () => {
    if (!current) return; $("save").disabled = true; $("save").textContent = "Saving...";
    try {
        const r = await fetch("/api/observations", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(current) });
        const j = await r.json(); if (!r.ok || !j.success) throw Error(j.detail || "Could not save");
        close(); toast(`✨ +${Number(current.xp_reward) || 10} XP · Discovery saved!`); load();
    } catch (e) { toast(e.message) } finally { $("save").disabled = false; $("save").textContent = "✓ Save discovery" }
};

async function load() {
    try {
        const r = await fetch("/api/observations"), j = await r.json(); if (!r.ok || !j.success) throw Error("Could not load discoveries");
        const a = j.data || [], xp = a.reduce((s, x) => s + (Number(x.xp_reward) || 0), 0);
        $("total").textContent = `${a.length} total`; $("countPill").textContent = `🌿 ${a.length} ${a.length === 1 ? "discovery" : "discoveries"}`;
        $("xp").textContent = xp; $("plants").textContent = a.filter(x => x.category === "plant").length;
        $("animals").textContent = a.filter(x => ["bird", "insect", "animal", "fungi"].includes(x.category)).length;
        let level = "🌱 Beginner", start = 0, next = 100; if (xp >= 500) { level = "🦋 Biodiversity Guardian"; start = 500; next = 1000 } else if (xp >= 250) { level = "🌳 Naturalist"; start = 250; next = 500 } else if (xp >= 100) { level = "🌿 Explorer"; start = 100; next = 250 }
        $("level").textContent = level; $("bar").style.width = `${Math.min(100, Math.max(0, (xp - start) / (next - start) * 100))}%`; $("levelText").textContent = xp >= 500 ? "Maximum level reached · Keep exploring!" : `${xp - start} / ${next - start} XP to next level`;
        $("list").innerHTML = a.length ? a.slice(0, 10).map(x => `<article><div><h3>${esc(x.name || "Unknown")}</h3><p>${esc(x.scientific_name || x.category || "Nature")}</p></div><span class="badge">+${Number(x.xp_reward) || 10} XP</span></article>`).join("") : `<div class="empty">🌱<br><small>Your discoveries will appear here.</small></div>`;
    } catch (e) { toast(e.message) }
}
function esc(x) { return String(x).replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;").replaceAll("'", "&#039;") }
function toast(x) { $("toast").textContent = x; $("toast").classList.add("show"); setTimeout(() => $("toast").classList.remove("show"), 2600) }
$("refresh").onclick = load;
const nav = document.querySelector("nav");
const navButtons = [...nav.querySelectorAll("button")];
function setNav(index) {
    nav.style.setProperty("--nav-index", index);
    navButtons.forEach((b, i) => b.classList.toggle("active", i === index));
    if (index === 0) window.scrollTo({ top: 0, behavior: "smooth" });
    if (index === 1) $(".mission")?.scrollIntoView({ behavior: "smooth", block: "center" });
    if (index === 2) $("list")?.scrollIntoView({ behavior: "smooth", block: "start" });
}
navButtons[0].onclick = () => setNav(0);
navButtons[1].onclick = () => setNav(1);
navButtons[2].onclick = () => setNav(2);
let navStartX = 0;
nav.addEventListener("touchstart", e => { navStartX = e.touches[0].clientX }, { passive: true });
nav.addEventListener("touchend", e => {
    const dx = e.changedTouches[0].clientX - navStartX;
    if (Math.abs(dx) < 45) return;
    const current = navButtons.findIndex(b => b.classList.contains("active"));
    setNav(Math.max(0, Math.min(2, current + (dx < 0 ? 1 : -1))));
}, { passive: true });
load();

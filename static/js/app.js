document.addEventListener("DOMContentLoaded", function () {
    initCyclops();
});

if (document.readyState === "complete" || document.readyState === "interactive") {
    initCyclops();
}

function initCyclops() {
    if (window.cyclopsInitialized) {
        return;
    }
    window.cyclopsInitialized = true;
    fetchIncidents();
}

const templatesDict = {
    bank: "URGENTE: Notificacion de Seguridad Bancaria. Su cuenta ha sido bloqueada temporalmente por actividad inusual en las ultimas 24 horas. Para reactivar su acceso y evitar la suspension definitiva de sus fondos, ingrese de inmediato al enlace y verifique sus credenciales bancarias: https://banco-seguridad-verificacion.com/login?id=92847. Si no completa la verificacion antes de 24 horas, sus activos seran retenidos.",
    creds: "ALERTA CRITICA DE TI: Su contraseña institucional expira el dia de hoy. De no actualizar sus datos de acceso inmediatamente, perdera comunicacion corporativa y sus cuentas seran restringidas. Haga clic aqui para confirmar su identidad: https://portal-soporte-autenticacion-corporativa.net/auth. Requerido por el area de Seguridad Informatica.",
    meet: "Estimado equipo, les comparto la agenda para la sesion de planeacion trimestral del proximo martes en la sala de conferencias B. Revisaremos los avances de los objetivos anuales y definiremos los siguientes entregables del proyecto. Agradezco confirmar su asistencia con anticipacion. Saludos cordiales.",
    notice: "Apreciados colaboradores, les recordamos que este viernes se llevara a cabo la jornada de bienestar y capacitacion interna. Las actividades daran inicio a las nueve de la mañana en el auditorio central. Esperamos contar con su participacion activa. Atentamente, Direccion de Talento Humano."
};

document.addEventListener("click", function (e) {
    const target = e.target;
    if (!target) {
        return;
    }

    const tplBtn = target.closest(".btn-template-choice");
    if (tplBtn) {
        const tplKey = tplBtn.getAttribute("data-template-key");
        const area = document.getElementById("email-text-input");
        if (area && templatesDict[tplKey]) {
            area.value = templatesDict[tplKey];
            area.focus();
        }
        return;
    }

    const clearBtn = target.closest("#btn-clear-text");
    if (clearBtn) {
        const area = document.getElementById("email-text-input");
        if (area) {
            area.value = "";
        }
        resetPanels();
        return;
    }

    const analyzeBtn = target.closest("#btn-analyze-email");
    if (analyzeBtn) {
        const area = document.getElementById("email-text-input");
        const rawText = area ? area.value.trim() : "";
        if (!rawText) {
            alert("Por favor ingrese o seleccione un mensaje para analizar.");
            return;
        }
        performAnalysis(rawText, analyzeBtn);
        return;
    }

    const tabBtn = target.closest(".tab-btn");
    if (tabBtn) {
        const tabTarget = tabBtn.getAttribute("data-tab");
        const tabButtons = document.querySelectorAll(".tab-btn");
        const tabPanels = document.querySelectorAll(".tab-panel");
        tabButtons.forEach(function (b) { b.classList.remove("active"); });
        tabPanels.forEach(function (p) { p.classList.remove("active"); });
        tabBtn.classList.add("active");
        const targetPanel = document.getElementById(tabTarget);
        if (targetPanel) {
            targetPanel.classList.add("active");
        }
        if (tabTarget === "tab-soc") {
            fetchIncidents();
        }
        return;
    }

    const docBtn = target.closest(".doc-nav-btn");
    if (docBtn) {
        const docTarget = docBtn.getAttribute("data-doc");
        const docButtons = document.querySelectorAll(".doc-nav-btn");
        const docCards = document.querySelectorAll(".doc-card");
        docButtons.forEach(function (b) { b.classList.remove("active"); });
        docCards.forEach(function (c) { c.classList.remove("active"); });
        docBtn.classList.add("active");
        const targetCard = document.getElementById(docTarget);
        if (targetCard) {
            targetCard.classList.add("active");
        }
        return;
    }

    const socActionBtn = target.closest(".soc-action-btn");
    if (socActionBtn) {
        const incId = socActionBtn.getAttribute("data-incident-id");
        const actType = socActionBtn.getAttribute("data-action-type");
        resolveIncidentAction(incId, actType);
        return;
    }
});

function resetPanels() {
    document.getElementById("val-char-count").innerText = "-";
    document.getElementById("val-url-count").innerText = "-";
    document.getElementById("val-has-url").innerText = "-";
    document.getElementById("val-urgency-score").innerText = "-";
    document.getElementById("val-url-density").innerText = "-";
    document.getElementById("val-urgency-density").innerText = "-";
    document.getElementById("val-is-threat").innerText = "-";

    const verdictBanner = document.getElementById("verdict-banner");
    verdictBanner.className = "verdict-banner";
    verdictBanner.style.backgroundColor = "#F8FAFD";
    verdictBanner.style.borderColor = "#DDE8F4";
    verdictBanner.style.color = "#64748B";

    document.getElementById("verdict-title").innerText = "Esperando Analisis";
    document.getElementById("verdict-desc").innerText = "Ingrese un texto y presione Ejecutar Analisis de Seguridad";
    document.getElementById("verdict-risk-pill").innerText = "INACTIVO";
    document.getElementById("verdict-risk-pill").style.backgroundColor = "#E2E8F0";
    document.getElementById("verdict-risk-pill").style.color = "#475569";

    document.getElementById("prob-progress-fill").style.width = "0%";
    document.getElementById("prob-progress-fill").style.backgroundColor = "#CBD5E1";
    document.getElementById("prob-value-text").innerText = "0.0%";

    const rulesContainer = document.getElementById("decision-rules-container");
    rulesContainer.innerHTML = '<div class="empty-state">Ejecute un analisis para visualizar la secuencia logica de decision en niveles.</div>';
    document.getElementById("execution-time-label").innerText = "Latencia: -";
}

function performAnalysis(text, analyzeBtn) {
    if (analyzeBtn) {
        analyzeBtn.disabled = true;
        analyzeBtn.innerText = "Analizando...";
    }

    fetch("/api/analyze", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            raw_text: text,
            reporter_id: "emp.usr.001"
        })
    })
    .then(function (res) { return res.json(); })
    .then(function (data) {
        if (analyzeBtn) {
            analyzeBtn.disabled = false;
            analyzeBtn.innerText = "Ejecutar Analisis de Seguridad";
        }
        updateUIWithResults(data);
    })
    .catch(function () {
        if (analyzeBtn) {
            analyzeBtn.disabled = false;
            analyzeBtn.innerText = "Ejecutar Analisis de Seguridad";
        }
        alert("Error al conectar con el motor de inferencia CYCLOPS SENTINEL.");
    });
}

function updateUIWithResults(data) {
    const meta = data.metadata;
    const evalData = data.evaluation;

    document.getElementById("val-char-count").innerText = meta.char_count;
    document.getElementById("val-url-count").innerText = meta.url_count;
    document.getElementById("val-has-url").innerText = meta.has_url === 1 ? "SI" : "NO";
    document.getElementById("val-urgency-score").innerText = meta.urgency_score;
    document.getElementById("val-url-density").innerText = meta.url_density + "%";
    document.getElementById("val-urgency-density").innerText = meta.urgency_density + "%";
    document.getElementById("val-is-threat").innerText = meta.is_threat ? "POSITIVO" : "NEGATIVO";

    const isThreatTile = document.getElementById("tile-is-threat");
    if (meta.is_threat) {
        isThreatTile.style.borderColor = "#FCA5A5";
        document.getElementById("val-is-threat").style.color = "#991B1B";
    } else {
        isThreatTile.style.borderColor = "#6EE7B7";
        document.getElementById("val-is-threat").style.color = "#065F46";
    }

    const banner = document.getElementById("verdict-banner");
    const vTitle = document.getElementById("verdict-title");
    const vDesc = document.getElementById("verdict-desc");
    const vPill = document.getElementById("verdict-risk-pill");
    const fill = document.getElementById("prob-progress-fill");
    const pVal = document.getElementById("prob-value-text");

    pVal.innerText = evalData.confidence_score + "%";
    fill.style.width = evalData.confidence_score + "%";

    banner.className = "verdict-banner";
    if (evalData.risk_level === "CRITICO") {
        banner.classList.add("verdict-critical");
        vPill.style.backgroundColor = "#FEE2E2";
        vPill.style.color = "#991B1B";
        fill.style.backgroundColor = "#EF4444";
    } else if (evalData.risk_level === "MEDIO") {
        banner.classList.add("verdict-medium");
        vPill.style.backgroundColor = "#FEF3C7";
        vPill.style.color = "#92400E";
        fill.style.backgroundColor = "#F59E0B";
    } else {
        banner.classList.add("verdict-safe");
        vPill.style.backgroundColor = "#D1FAE5";
        vPill.style.color = "#065F46";
        fill.style.backgroundColor = "#10B981";
    }

    vTitle.innerText = evalData.classification;
    vDesc.innerText = evalData.summary;
    vPill.innerText = "RIESGO " + evalData.risk_level;

    const container = document.getElementById("decision-rules-container");
    container.innerHTML = "";
    evalData.decision_levels.forEach(function (lvl) {
        const card = document.createElement("div");
        card.className = "rule-level-card";
        card.innerHTML = '<div class="rule-header"><span class="rule-title">' + lvl.level + '</span><span class="rule-badge">' + lvl.status + '</span></div><div class="rule-details">' + lvl.details + '</div>';
        container.appendChild(card);
    });

    document.getElementById("execution-time-label").innerText = "Latencia Inferencia: " + data.execution_time_ms + " ms";
    fetchIncidents();
}

function fetchIncidents() {
    fetch("/api/incidents")
    .then(function (res) { return res.json(); })
    .then(function (data) {
        renderIncidentsTable(data.incidents);
        const badge = document.getElementById("badge-soc-count");
        if (badge) {
            badge.innerText = data.pending_count;
        }
    })
    .catch(function () {});
}

function renderIncidentsTable(incidents) {
    const tbody = document.getElementById("soc-incidents-tbody");
    if (!tbody) { return; }
    if (!incidents || incidents.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="empty-state">No hay incidentes registrados en el sistema.</td></tr>';
        return;
    }

    tbody.innerHTML = "";
    incidents.forEach(function (inc) {
        const tr = document.createElement("tr");
        const conf = inc.evaluation ? inc.evaluation.confidence_score + "%" : "-";
        const risk = inc.evaluation ? inc.evaluation.risk_level : inc.alert_level;

        let statusBadge = '<span style="background-color: #E2E8F0; color: #475569; padding: 4px 8px; border-radius: 9999px; font-weight: 700; font-size: 11px;">' + inc.status + '</span>';
        if (inc.status === "PENDING_SOC_REVIEW") {
            statusBadge = '<span style="background-color: #FEF3C7; color: #92400E; padding: 4px 8px; border-radius: 9999px; font-weight: 700; font-size: 11px;">REVISION SOC</span>';
        } else if (inc.status === "RESOLVED_QUARANTINE" || inc.status === "AUTO_MITIGATED_QUARANTINE") {
            statusBadge = '<span style="background-color: #FEE2E2; color: #991B1B; padding: 4px 8px; border-radius: 9999px; font-weight: 700; font-size: 11px;">CUARENTENA</span>';
        } else if (inc.status === "RESOLVED_FALSE_POSITIVE" || inc.status === "MARKED_AS_SAFE") {
            statusBadge = '<span style="background-color: #D1FAE5; color: #065F46; padding: 4px 8px; border-radius: 9999px; font-weight: 700; font-size: 11px;">SEGURO</span>';
        }

        let actionButtons = '-';
        if (inc.status === "PENDING_SOC_REVIEW" || inc.status === "PENDING_ANALYSIS") {
            actionButtons = '<div style="display: flex; gap: 6px;"><button class="btn-action-small btn-threat-confirm soc-action-btn" data-incident-id="' + inc.id + '" data-action-type="CONFIRMED_THREAT">Aislar</button><button class="btn-action-small btn-safe-confirm soc-action-btn" data-incident-id="' + inc.id + '" data-action-type="FALSE_POSITIVE">Restaurar</button></div>';
        }

        const sender = inc.metadata ? inc.metadata.anonymized_sender : "usuario@corporativo.com";

        tr.innerHTML = '<td><strong>' + inc.id + '</strong></td><td>' + sender + '</td><td>' + inc.reported_at + '</td><td>' + conf + '</td><td>' + risk + '</td><td>' + statusBadge + '</td><td>' + actionButtons + '</td>';
        tbody.appendChild(tr);
    });
}

function resolveIncidentAction(incidentId, action) {
    fetch("/api/incidents/" + incidentId + "/resolve", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ action: action })
    })
    .then(function (res) { return res.json(); })
    .then(function () {
        fetchIncidents();
    });
}

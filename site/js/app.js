// Dashboard of the site and cloud region layers, read from data/dashboard.json.
(function () {
  "use strict";

  var COLOURS = { site: "--site", cloud_region: "--region" };
  var LABELS = { site: "Site", cloud_region: "Cloud region" };
  var STATUS = { operational: "Operational", under_construction: "Under construction", planned: "Planned", unclear: "Unclear" };
  var RULE_STATUS = { in_force: "In force", pending: "Pending", rescinded: "Rescinded", announced: "Announced", enforcement: "Enforcement" };
  var COVERS = { chip_export: "Export of chips", chip_transit: "Export, transshipment and transit of chips",
    remote_access: "Remote access through the cloud", use_in_country: "Use of chips in the country", guidance: "Guidance" };

  var state = { records: [], rules: [], map: null, layer: null };
  var el = function (id) { return document.getElementById(id); };

  function escape(text) {
    return String(text == null ? "" : text).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function colour(layer) {
    return getComputedStyle(document.documentElement).getPropertyValue(COLOURS[layer]).trim();
  }

  function fill(select, values) {
    values.sort().forEach(function (v) {
      var option = document.createElement("option");
      option.value = v;
      option.textContent = v;
      select.appendChild(option);
    });
  }

  function unique(list) {
    return list.filter(function (v, i) { return v && list.indexOf(v) === i; });
  }

  function selected() {
    var firm = el("firm").value, role = el("role").value, country = el("country").value;
    var words = el("search").value.trim().toLowerCase();
    return state.records.filter(function (r) {
      if (r.layer === "site" && !el("show-sites").checked) return false;
      if (r.layer === "cloud_region" && !el("show-regions").checked) return false;
      if (country && r.country !== country) return false;
      if (firm && !r.roles.some(function (x) { return x.firm === firm && (!role || x.role === role); })) return false;
      if (!firm && role && !r.roles.some(function (x) { return x.role === role; })) return false;
      if (words) {
        var text = [r.name, r.city, r.country, r.note].join(" ").toLowerCase();
        if (text.indexOf(words) < 0) return false;
      }
      return true;
    });
  }

  function roleText(r) {
    return r.roles.map(function (x) {
      return escape(x.firm) + (x.origin ? " (origin " + escape(x.origin) + ")" : "") + ": " + escape(x.role);
    }).join("<br>");
  }

  function place(r) {
    return escape([r.city, r.country].filter(Boolean).join(", "));
  }

  function mw(r) {
    if (!r.capacity_mw) return "";
    return escape(r.capacity_mw) + (r.capacity_basis && r.capacity_basis !== "unspecified" ? " (" + escape(r.capacity_basis) + ")" : "");
  }

  function number(value) {
    return Number(value).toLocaleString("en-GB");
  }

  function aiText(x) {
    return "AI chips: " + (x.count ? escape(number(x.count)) + " " : "") + escape(x.chips) + ", " + escape(x.access) +
      " by " + escape(x.firm) + ", " + escape(x.status);
  }

  function timelineText(stages) {
    var shown = stages.filter(function (t, i) { return i === 0 || t.mw !== stages[i - 1].mw; });
    if (!shown.length) return "";
    return "<br>IT power over time, from Epoch's timeline: " + shown.map(function (t) {
      return escape(t.date) + " " + escape(number(t.mw)) + " MW";
    }).join(", ");
  }

  function epochText(e) {
    return "Epoch AI estimate: " + escape(number(e.mw)) + " MW of IT power and about " + escape(number(e.h100e)) +
      " H100 equivalents" + (e.chips ? ", chips " + escape(e.chips.replace(/,/g, ", ")) : "") +
      (e.users ? ", users " + escape(e.users) : "") + ", as " + escape(e.name) + ". <a href='" + escape(e.page) +
      "' rel='noopener' target='_blank'>Epoch page</a>" + timelineText(e.timeline || []);
  }

  function drawTable(rows) {
    el("rows").innerHTML = rows.map(function (r) {
      return "<tr><td><span class='tag " + r.layer + "'>" + LABELS[r.layer] + "</span> " +
        (r.level === "B" ? "<span class='tag level'>Level B</span> " : "") + escape(r.name) +
        (r.note ? "<span class='quote'>" + escape(r.note) + "</span>" : "") +
        (r.capacity || []).map(function (x) {
          return "<span class='quote'>Capacity: " + escape(x.mw) + " MW (" + escape(x.basis) + ", " + escape(x.stage.replace(/_/g, " ")) +
            ", " + escape(x.date) + "). <a href='" + escape(x.source) + "' rel='noopener' target='_blank'>Source</a></span>";
        }).join("") +
        (r.ai || []).map(function (x) {
          return "<span class='quote'>" + aiText(x) + ". <a href='" + escape(x.source) + "' rel='noopener' target='_blank'>Source</a></span>";
        }).join("") +
        (r.epoch ? "<span class='quote'>" + epochText(r.epoch) + "</span>" : "") + "</td>" +
        "<td>" + roleText(r) + "</td><td>" + place(r) + "</td><td>" + (STATUS[r.status] || escape(r.status)) + "</td>" +
        "<td>" + mw(r) + "</td><td><a href='" + escape(r.source) + "' rel='noopener' target='_blank'>Page</a>" +
        "<span class='quote'>“" + escape(r.quote) + "” (" + escape(r.check) + ")</span></td></tr>";
    }).join("");
  }

  function drawMap(rows) {
    state.layer.clearLayers();
    var groups = {};
    rows.forEach(function (r) {
      if (!r.point) return;
      var key = r.point.join(",");
      (groups[key] = groups[key] || []).push(r);
    });
    Object.keys(groups).forEach(function (key) {
      var group = groups[key];
      var hasSite = group.some(function (r) { return r.layer === "site"; });
      var marker = L.circleMarker(group[0].point, {
        radius: Math.min(5 + group.length * 1.5, 16), weight: 1, color: "#ffffff", fillOpacity: 0.85,
        fillColor: colour(hasSite ? "site" : "cloud_region")
      });
      var local = state.rules.filter(function (x) { return (x.applies_in || []).indexOf(group[0].iso3) >= 0; });
      marker.bindPopup("<strong>" + place(group[0]) + "</strong><br>" + group.map(function (r) {
        return LABELS[r.layer] + ": " + escape(r.name) + "<br><small>" + roleText(r) + "</small>";
      }).join("<hr>") + "<hr><small>" + (local.length ? "Rules recorded for this country: " + local.map(function (x) {
        return escape(x.instrument) + " (" + (COVERS[x.covers] || escape(x.covers)) + ", " + (RULE_STATUS[x.status] || escape(x.status)) + ")";
      }).join("; ") : "No rules specific to this country recorded yet") + ". US export rules apply to US-origin chips everywhere.</small>");
      state.layer.addLayer(marker);
    });
  }

  function draw() {
    var rows = selected();
    drawTable(rows);
    drawMap(rows);
    var sites = rows.filter(function (r) { return r.layer === "site"; }).length;
    var countries = unique(rows.map(function (r) { return r.country; })).length;
    el("counts").textContent = sites + " sites and " + (rows.length - sites) + " cloud regions shown, in " +
      countries + " countries and territories.";
  }

  function drawRules() {
    el("rules").innerHTML = state.rules.map(function (x) {
      return "<tr><td>" + escape(x.instrument) + (x.note ? "<span class='quote'>" + escape(x.note) + "</span>" : "") + "</td>" +
        "<td>" + escape(x.jurisdiction) + ((x.applies_in || []).join() === "all" ? "" : "<span class='quote'>Applies in " + ((x.applies_in || []).length > 6 ? x.applies_in.length + " countries" :
          escape((x.applies_in || []).join(", "))) + "</span>") + "</td><td>" + (COVERS[x.covers] || escape(x.covers)) + "</td>" +
        "<td>" + (RULE_STATUS[x.status] || escape(x.status)) + (x.date ? " (" + escape(x.date) + ")" : "") + "</td>" +
        "<td><a href='" + escape(x.source) + "' rel='noopener' target='_blank'>Page</a><span class='quote'>“" +
        escape(x.quote) + "” (" + escape(x.check) + ")</span></td></tr>";
    }).join("");
  }

  function drawSummary(data) {
    var sites = data.records.filter(function (r) { return r.layer === "site"; });
    var firms = [], ai = (data.ai_without_site || []).length;
    sites.forEach(function (r) {
      ai += (r.ai || []).length;
      r.roles.forEach(function (x) { firms.push(x.firm); });
    });
    var tiles = [
      ["Sites", sites.length],
      ["Cloud regions", data.records.length - sites.length],
      ["Countries and territories", unique(data.records.map(function (r) { return r.country; })).length],
      ["Firms with a role at a site", unique(firms).length],
      ["Reports of AI chips", ai],
      ["Rules recorded", (data.rules || []).length]
    ];
    el("summary").innerHTML = tiles.map(function (t) {
      return "<div class='tile'><span class='value'>" + escape(number(t[1])) + "</span><span class='label'>" + escape(t[0]) + "</span></div>";
    }).join("");
  }

  function drawUnplaced(list) {
    el("ai-without-site").innerHTML = list.map(function (x) {
      return "<tr><td>" + escape(x.firm) + "</td><td>" + (x.count ? escape(number(x.count)) + " " : "") + escape(x.chips) +
        (x.note ? "<span class='quote'>" + escape(x.note) + "</span>" : "") + "</td><td>" + escape(x.access) + "</td>" +
        "<td>" + escape(x.status) + (x.date ? " (" + escape(x.date) + ")" : "") + "</td>" +
        "<td><a href='" + escape(x.source) + "' rel='noopener' target='_blank'>Page</a><span class='quote'>“" +
        escape(x.quote) + "” (" + escape(x.check) + ")</span></td></tr>";
    }).join("");
  }

  function drawCustomers(list) {
    el("customers").innerHTML = list.map(function (x) {
      var amount = x.share ? escape(Math.round(Number(x.share) * 1000) / 10) + " percent of revenue" : escape(x.revenue);
      return "<tr><td>" + escape(x.firm) + "</td><td>" + escape(x.customer) +
        (x.description ? "<span class='quote'>" + escape(x.description) + "</span>" : "") +
        (x.identified_as ? "<span class='quote'>Identified as " + escape(x.identified_as) + "</span>" : "") + "</td>" +
        "<td>" + amount + (x.note ? "<span class='quote'>" + escape(x.note) + "</span>" : "") + "</td><td>" + escape(x.period) + "</td>" +
        "<td><a href='" + escape(x.source) + "' rel='noopener' target='_blank'>Page</a><span class='quote'>“" +
        escape(x.quote) + "” (" + escape(x.check) + ")</span></td></tr>";
    }).join("");
  }

  function start(data) {
    state.records = data.records;
    state.rules = data.rules || [];
    drawSummary(data);
    drawRules();
    drawUnplaced(data.ai_without_site || []);
    drawCustomers(data.customers || []);
    el("built").textContent = "Data built on " + data.built + ".";
    var firms = [], roles = [], countries = [];
    data.records.forEach(function (r) {
      countries.push(r.country);
      r.roles.forEach(function (x) { firms.push(x.firm); roles.push(x.role); });
    });
    fill(el("firm"), unique(firms));
    fill(el("role"), unique(roles));
    fill(el("country"), unique(countries));
    state.map = L.map("map", { worldCopyJump: true }).setView([20, 40], 2);
    L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 12, attribution: "© OpenStreetMap contributors"
    }).addTo(state.map);
    state.layer = L.layerGroup().addTo(state.map);
    ["show-sites", "show-regions", "firm", "role", "country"].forEach(function (id) { el(id).addEventListener("change", draw); });
    el("search").addEventListener("input", draw);
    draw();
  }

  fetch("data/dashboard.json")
    .then(function (response) { return response.json(); })
    .then(start)
    .catch(function () { el("counts").textContent = "The data file could not be read."; });
})();

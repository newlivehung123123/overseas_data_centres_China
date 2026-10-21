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

  function drawTable(rows) {
    el("rows").innerHTML = rows.map(function (r) {
      return "<tr><td><span class='tag " + r.layer + "'>" + LABELS[r.layer] + "</span> " + escape(r.name) +
        (r.note ? "<span class='quote'>" + escape(r.note) + "</span>" : "") +
        (r.capacity || []).map(function (x) {
          return "<span class='quote'>Capacity: " + escape(x.mw) + " MW (" + escape(x.basis) + ", " + escape(x.stage.replace(/_/g, " ")) +
            ", " + escape(x.date) + "). <a href='" + escape(x.source) + "' rel='noopener' target='_blank'>Source</a></span>";
        }).join("") +
        (r.ai || []).map(function (x) {
          return "<span class='quote'>AI chips: " + escape(Number(x.count).toLocaleString("en-GB")) + " " + escape(x.chips) +
            ", " + escape(x.access) + " by " + escape(x.firm) + ", " + escape(x.status) + "</span>";
        }).join("") + "</td>" +
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
        "<td>" + escape(x.jurisdiction) + ((x.applies_in || []).join() === "all" ? "" : "<span class='quote'>Applies in " + escape((x.applies_in || []).join(", ")) + "</span>") + "</td><td>" + (COVERS[x.covers] || escape(x.covers)) + "</td>" +
        "<td>" + (RULE_STATUS[x.status] || escape(x.status)) + (x.date ? " (" + escape(x.date) + ")" : "") + "</td>" +
        "<td><a href='" + escape(x.source) + "' rel='noopener' target='_blank'>Page</a><span class='quote'>“" +
        escape(x.quote) + "” (" + escape(x.check) + ")</span></td></tr>";
    }).join("");
  }

  function start(data) {
    state.records = data.records;
    state.rules = data.rules || [];
    drawRules();
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

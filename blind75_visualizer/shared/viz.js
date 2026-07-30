/* Blind 75 Visualizer — step player + live input driver
   Each animated problem page defines:
     window.INPUT_SCHEMA = [{name, label, type, default, maxLen}, ...]
     window.generateSteps = function(arg1, arg2, ...) { ...; return steps; }
   then calls window.initVizForm() once both are defined and viz.js is
   loaded. Steps are computed live in the browser from whatever the user
   types in — nothing is fetched, nothing runs server-side.

   step shape:
   {
     line: <source line to highlight>,
     narration: "<html-safe string>",
     rows: [ { label: "nums", items: [{ v, state }] }, ... ],
     map: { label: "seen", items: [{ v, added }] } | null
   }
   state is one of: "", "current", "hit", "done", "pending" */

(function () {
  "use strict";

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text !== undefined) e.textContent = text;
    return e;
  }

  function renderRow(items, showIndex) {
    var row = el("div", "cell-row");
    if (!items || !items.length) {
      row.appendChild(el("div", "set-empty", "(empty)"));
      return row;
    }
    items.forEach(function (item, i) {
      var cell = el("div", "cell " + (item.state || ""));
      if (showIndex) cell.appendChild(el("span", "idx", String(i)));
      cell.appendChild(document.createTextNode(item.v));
      row.appendChild(cell);
    });
    return row;
  }

  function renderRowsBlock(container, rows) {
    container.innerHTML = "";
    (rows || []).forEach(function (r) {
      var wrap = el("div", "row-block");
      wrap.appendChild(el("div", "row-label", r.label));
      wrap.appendChild(renderRow(r.items, true));
      container.appendChild(wrap);
    });
  }

  function renderMapPanel(container, labelEl, map) {
    container.innerHTML = "";
    if (!map || !map.items || !map.items.length) {
      container.appendChild(el("div", "set-empty", "(empty)"));
    } else {
      map.items.forEach(function (item) {
        container.appendChild(el("span", "set-chip" + (item.added ? " new" : ""), String(item.v)));
      });
    }
    if (labelEl) labelEl.textContent = map ? map.label : "";
  }

  function StepPlayer(root, steps) {
    this.root = root;
    this.steps = steps;
    this.i = 0;
    this.timer = null;
    this.speed = 700;

    this.codeLines = Array.prototype.slice.call(root.querySelectorAll("[data-code-line]"));
    this.rowsContainer = root.querySelector("[data-viz-rows]");
    this.mapContainer = root.querySelector("[data-viz-map]");
    this.mapLabel = root.querySelector("[data-viz-map-label]");
    this.mapBlock = root.querySelector("[data-viz-map-block]");
    this.narration = root.querySelector("[data-viz-narration]");
    this.counter = root.querySelector("[data-viz-counter]");

    this.btnPlay = root.querySelector("[data-viz-play]");
    this.btnPrev = root.querySelector("[data-viz-prev]");
    this.btnNext = root.querySelector("[data-viz-next]");
    this.btnReset = root.querySelector("[data-viz-reset]");
    this.speedSelect = root.querySelector("[data-viz-speed]");

    var self = this;
    if (this.btnPlay) this.btnPlay.addEventListener("click", function () { self.toggle(); });
    if (this.btnPrev) this.btnPrev.addEventListener("click", function () { self.pause(); self.go(self.i - 1); });
    if (this.btnNext) this.btnNext.addEventListener("click", function () { self.pause(); self.go(self.i + 1); });
    if (this.btnReset) this.btnReset.addEventListener("click", function () { self.pause(); self.go(0); });
    if (this.speedSelect) {
      this.speedSelect.addEventListener("change", function () {
        self.speed = parseInt(self.speedSelect.value, 10);
        if (self.timer) { self.pause(); self.play(); }
      });
    }

    this.render();
  }

  StepPlayer.prototype.setSteps = function (steps) {
    this.pause();
    this.steps = steps;
    this.i = 0;
    this.render();
  };

  StepPlayer.prototype.go = function (idx) {
    if (idx < 0) return;
    if (idx >= this.steps.length) { this.pause(); return; }
    this.i = idx;
    this.render();
  };

  StepPlayer.prototype.render = function () {
    var step = this.steps[this.i];

    this.codeLines.forEach(function (lineEl) {
      var n = parseInt(lineEl.getAttribute("data-code-line"), 10);
      lineEl.classList.toggle("active", n === step.line);
    });

    if (this.rowsContainer) renderRowsBlock(this.rowsContainer, step.rows);
    if (this.mapContainer) {
      if (step.map) {
        if (this.mapBlock) this.mapBlock.style.display = "";
        renderMapPanel(this.mapContainer, this.mapLabel, step.map);
      } else if (this.mapBlock) {
        this.mapBlock.style.display = "none";
      }
    }
    if (this.narration) this.narration.innerHTML = step.narration || "";
    if (this.counter) this.counter.textContent = (this.i + 1) + " / " + this.steps.length;

    if (this.btnPrev) this.btnPrev.disabled = this.i === 0;
    if (this.btnNext) this.btnNext.disabled = this.i === this.steps.length - 1;
  };

  StepPlayer.prototype.play = function () {
    if (this.timer || this.i >= this.steps.length - 1) return;
    var self = this;
    if (this.btnPlay) this.btnPlay.textContent = "Pause";
    this.timer = setInterval(function () {
      if (self.i >= self.steps.length - 1) { self.pause(); return; }
      self.go(self.i + 1);
    }, this.speed);
  };

  StepPlayer.prototype.pause = function () {
    if (this.timer) clearInterval(this.timer);
    this.timer = null;
    if (this.btnPlay) this.btnPlay.textContent = "Play";
  };

  StepPlayer.prototype.toggle = function () {
    if (this.timer) this.pause();
    else this.play();
  };

  window.StepPlayer = StepPlayer;

  /* ---------- input parsing (used by generated per-page driver code) ---------- */

  window.VizInput = {
    "int-array": function (raw, maxLen) {
      maxLen = maxLen || 30;
      var parts = raw.split(",").map(function (s) { return s.trim(); }).filter(function (s) { return s.length > 0; });
      if (parts.length === 0) throw new Error("Enter at least one number.");
      if (parts.length > maxLen) throw new Error("Keep it to " + maxLen + " numbers or fewer for a readable animation.");
      return parts.map(function (s) {
        if (!/^-?\d+$/.test(s)) throw new Error('"' + s + '" is not a valid integer.');
        return parseInt(s, 10);
      });
    },
    "string-array": function (raw, maxLen) {
      maxLen = maxLen || 12;
      var parts = raw.split(",").map(function (s) { return s.trim(); }).filter(function (s) { return s.length > 0; });
      if (parts.length === 0) throw new Error("Enter at least one word.");
      if (parts.length > maxLen) throw new Error("Keep it to " + maxLen + " words or fewer for a readable animation.");
      return parts;
    },
    "int": function (raw) {
      var s = raw.trim();
      if (!/^-?\d+$/.test(s)) throw new Error('"' + raw + '" is not a valid integer.');
      return parseInt(s, 10);
    },
    "string": function (raw, maxLen) {
      maxLen = maxLen || 40;
      if (raw.length === 0) throw new Error("This field can't be empty.");
      if (raw.length > maxLen) throw new Error("Keep it to " + maxLen + " characters or fewer for a readable animation.");
      return raw;
    }
  };

  /* ---------- generic form driver ----------
     Wires an input form + "Visualize" button to a page-local
     generateSteps(...) function, given window.INPUT_SCHEMA. */

  window.initVizForm = function () {
    var schema = window.INPUT_SCHEMA || [];
    var root = document.querySelector("[data-viz-root]");
    if (!root || !window.generateSteps) return;
    var errorEl = root.querySelector("[data-viz-error]");
    var player = null;

    function readArgs() {
      return schema.map(function (field) {
        var input = document.getElementById("field-" + field.name);
        return window.VizInput[field.type](input.value, field.maxLen);
      });
    }

    function run() {
      try {
        var args = readArgs();
        var steps = window.generateSteps.apply(null, args);
        if (!steps || !steps.length) throw new Error("No steps produced — try different input.");
        if (errorEl) { errorEl.hidden = true; errorEl.textContent = ""; }
        if (!player) player = new StepPlayer(root, steps);
        else player.setSteps(steps);
        window.__player = player;
      } catch (e) {
        if (errorEl) { errorEl.hidden = false; errorEl.textContent = e.message; }
      }
    }

    var btn = root.querySelector("[data-viz-run]");
    if (btn) btn.addEventListener("click", run);
    schema.forEach(function (field) {
      var input = document.getElementById("field-" + field.name);
      if (input) {
        input.addEventListener("keydown", function (e) {
          if (e.key === "Enter") run();
        });
      }
    });

    run();
  };
})();

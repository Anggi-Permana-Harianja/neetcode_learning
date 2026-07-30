/* Blind 75 Visualizer — step player
   Consumes a page-local `STEPS` array (defined inline on animated problem
   pages) and drives the code highlight + row/map panels. No fetch, no
   build step at runtime — everything needed is already in the page.

   STEPS[i] shape:
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

  document.addEventListener("DOMContentLoaded", function () {
    if (window.STEPS && window.STEPS.length) {
      var root = document.querySelector("[data-viz-root]");
      if (root) window.__player = new StepPlayer(root, window.STEPS);
    }
  });
})();

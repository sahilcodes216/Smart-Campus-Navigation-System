/**
 * Interactive SVG Campus Map Controller
 * Conforms to PRD Section 6.2, 6.4, 7, 8
 */

export class CampusMapController {
  constructor(options = {}) {
    this.container = options.container; // container element wrapping SVG
    this.svg = options.svg;             // SVG element
    this.locations = options.locations || [];
    this.categories = options.categories || [];
    this.router = options.router || null;
    this.onLocationSelect = options.onLocationSelect || (() => {});
    this.onRouteRequest = options.onRouteRequest || (() => {});

    this.selectedLocationId = null;
    this.activeCategoryFilter = null;

    // Viewport transform state
    this.viewBox = { x: 0, y: 0, w: 950, h: 800 };
    this.baseViewBox = { x: 0, y: 0, w: 950, h: 800 };
    this.currentZoom = 1;

    // Drag / Pan state
    this.isPanning = false;
    this.startPoint = { x: 0, y: 0 };

    this.init();
  }

  init() {
    if (!this.svg) return;

    this.markersGroup = this.svg.getElementById('map-markers-layer') || this.createGroup('map-markers-layer');
    this.routeGroup = this.svg.getElementById('map-route-layer') || this.createGroup('map-route-layer');

    this.renderMarkers();
    this.setupPanZoom();
  }

  createGroup(id) {
    const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    g.setAttribute('id', id);
    this.svg.appendChild(g);
    return g;
  }

  getCategoryColor(category) {
    // PRD: colored by category group in palette (pine, ink, moss)
    switch (category) {
      case 'academic':
      case 'classroom':
      case 'lab':
        return '#0E4B41'; // Pine
      case 'library':
      case 'admin':
      case 'auditorium':
        return '#16201C'; // Ink
      case 'cafeteria':
      case 'parking':
      default:
        return '#7C9A6B'; // Moss
    }
  }

  renderMarkers() {
    this.markersGroup.innerHTML = '';

    this.locations.forEach(loc => {
      const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
      g.setAttribute('class', 'map-marker');
      g.setAttribute('data-id', loc.id);
      g.setAttribute('data-category', loc.category);
      g.setAttribute('tabindex', '0');
      g.setAttribute('role', 'button');
      g.setAttribute('aria-label', `${loc.name}, ${loc.category}`);

      const color = this.getCategoryColor(loc.category);
      const isSelected = this.selectedLocationId === loc.id;
      const markerColor = isSelected ? '#E8552D' : color;

      // Pin Pinhead SVG
      g.innerHTML = `
        <title>${loc.name}</title>
        <g transform="translate(${loc.coords.x}, ${loc.coords.y})">
          <circle cx="0" cy="0" r="14" fill="${markerColor}" stroke="#F6F2E9" stroke-width="2.5" />
          <circle cx="0" cy="0" r="5" fill="#F6F2E9" />
          <text x="0" y="24" font-family="'JetBrains Mono', monospace" font-size="10" font-weight="600" 
                fill="#16201C" text-anchor="middle" class="marker-label" 
                style="paint-order: stroke; stroke: #F6F2E9; stroke-width: 3px; stroke-linejoin: round;">
            ${loc.name}
          </text>
        </g>
      `;

      if (isSelected) {
        g.classList.add('selected');
      }

      // Dimming check
      if (this.activeCategoryFilter && loc.category !== this.activeCategoryFilter) {
        g.classList.add('dimmed');
      }

      // Event handlers
      const selectAction = (e) => {
        e.stopPropagation();
        this.selectLocation(loc.id, true);
      };

      g.addEventListener('click', selectAction);
      g.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          selectAction(e);
        }
      });

      this.markersGroup.appendChild(g);
    });
  }

  selectLocation(locationId, triggerCallback = true) {
    this.selectedLocationId = locationId;

    // Update marker styling
    const markers = this.markersGroup.querySelectorAll('.map-marker');
    markers.forEach(m => {
      const id = m.getAttribute('data-id');
      const isSel = id === locationId;
      m.classList.toggle('selected', isSel);

      const circle = m.querySelector('circle');
      if (circle) {
        const cat = m.getAttribute('data-category');
        circle.setAttribute('fill', isSel ? '#E8552D' : this.getCategoryColor(cat));
      }
    });

    const target = this.locations.find(l => l.id === locationId);
    if (target) {
      this.panToPoint(target.coords.x, target.coords.y);
      if (triggerCallback) {
        this.onLocationSelect(target);
      }
    }
  }

  filterByCategory(category) {
    this.activeCategoryFilter = category;
    const markers = this.markersGroup.querySelectorAll('.map-marker');
    markers.forEach(m => {
      const cat = m.getAttribute('data-category');
      const dim = category && cat !== category;
      m.classList.toggle('dimmed', dim);
    });
  }

  drawRoute(pathNodes) {
    this.routeGroup.innerHTML = '';
    if (!pathNodes || pathNodes.length < 2) return;

    // Build SVG path data
    const d = pathNodes.map((pt, i) => `${i === 0 ? 'M' : 'L'} ${pt.x} ${pt.y}`).join(' ');

    const pathEl = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    pathEl.setAttribute('d', d);
    pathEl.setAttribute('class', 'map-route-line');
    this.routeGroup.appendChild(pathEl);

    // Add Start and End pinpoint markers
    const startPt = pathNodes[0];
    const endPt = pathNodes[pathNodes.length - 1];

    const markersHtml = `
      <!-- Start Pin -->
      <g transform="translate(${startPt.x}, ${startPt.y})">
        <circle cx="0" cy="0" r="10" fill="#0E4B41" stroke="#F6F2E9" stroke-width="2" />
        <text x="0" y="4" font-family="'JetBrains Mono', monospace" font-size="9" font-weight="700" fill="#FFFFFF" text-anchor="middle">A</text>
      </g>
      <!-- End Pin -->
      <g transform="translate(${endPt.x}, ${endPt.y})">
        <circle cx="0" cy="0" r="12" fill="#E8552D" stroke="#F6F2E9" stroke-width="2.5" />
        <text x="0" y="4" font-family="'JetBrains Mono', monospace" font-size="10" font-weight="700" fill="#FFFFFF" text-anchor="middle">B</text>
      </g>
    `;

    const gPins = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    gPins.innerHTML = markersHtml;
    this.routeGroup.appendChild(gPins);

    // Fit view to route bounds
    let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
    pathNodes.forEach(pt => {
      if (pt.x < minX) minX = pt.x;
      if (pt.x > maxX) maxX = pt.x;
      if (pt.y < minY) minY = pt.y;
      if (pt.y > maxY) maxY = pt.y;
    });

    const pad = 80;
    const w = Math.max(260, maxX - minX + pad * 2);
    const h = Math.max(200, maxY - minY + pad * 2);
    const cx = (minX + maxX) / 2;
    const cy = (minY + maxY) / 2;

    this.setViewBox(cx - w / 2, cy - h / 2, w, h);
  }

  clearRoute() {
    this.routeGroup.innerHTML = '';
  }

  // PAN & ZOOM HANDLING
  setupPanZoom() {
    const el = this.container || this.svg;

    // Mouse drag
    el.addEventListener('mousedown', (e) => {
      if (e.target.closest('.map-marker')) return;
      this.isPanning = true;
      el.classList.add('grabbing');
      this.startPoint = { x: e.clientX, y: e.clientY };
    });

    window.addEventListener('mousemove', (e) => {
      if (!this.isPanning) return;
      const dx = (e.clientX - this.startPoint.x) * (this.viewBox.w / el.clientWidth);
      const dy = (e.clientY - this.startPoint.y) * (this.viewBox.h / el.clientHeight);

      this.viewBox.x -= dx;
      this.viewBox.y -= dy;
      this.applyViewBox();
      this.startPoint = { x: e.clientX, y: e.clientY };
    });

    window.addEventListener('mouseup', () => {
      if (this.isPanning) {
        this.isPanning = false;
        el.classList.remove('grabbing');
      }
    });

    // Mouse wheel zoom
    el.addEventListener('wheel', (e) => {
      e.preventDefault();
      const zoomFactor = e.deltaY < 0 ? 0.85 : 1.15;
      this.zoom(zoomFactor, e.clientX, e.clientY);
    }, { passive: false });

    // Touch support (1 finger pan, 2 fingers pinch)
    let lastTouchDistance = null;
    let lastTouchPoint = null;

    el.addEventListener('touchstart', (e) => {
      if (e.touches.length === 1) {
        this.isPanning = true;
        lastTouchPoint = { x: e.touches[0].clientX, y: e.touches[0].clientY };
      } else if (e.touches.length === 2) {
        this.isPanning = false;
        lastTouchDistance = Math.hypot(
          e.touches[0].clientX - e.touches[1].clientX,
          e.touches[0].clientY - e.touches[1].clientY
        );
      }
    }, { passive: true });

    el.addEventListener('touchmove', (e) => {
      if (e.touches.length === 1 && this.isPanning && lastTouchPoint) {
        const dx = (e.touches[0].clientX - lastTouchPoint.x) * (this.viewBox.w / el.clientWidth);
        const dy = (e.touches[0].clientY - lastTouchPoint.y) * (this.viewBox.h / el.clientHeight);
        this.viewBox.x -= dx;
        this.viewBox.y -= dy;
        this.applyViewBox();
        lastTouchPoint = { x: e.touches[0].clientX, y: e.touches[0].clientY };
      } else if (e.touches.length === 2 && lastTouchDistance) {
        const dist = Math.hypot(
          e.touches[0].clientX - e.touches[1].clientX,
          e.touches[0].clientY - e.touches[1].clientY
        );
        const factor = lastTouchDistance / dist;
        this.zoom(Math.min(1.2, Math.max(0.8, factor)));
        lastTouchDistance = dist;
      }
    }, { passive: true });

    el.addEventListener('touchend', () => {
      this.isPanning = false;
      lastTouchDistance = null;
      lastTouchPoint = null;
    });
  }

  zoom(factor, clientX, clientY) {
    const el = this.container || this.svg;
    const rect = el.getBoundingClientRect();
    
    // Zoom focus point
    const px = clientX ? (clientX - rect.left) / rect.width : 0.5;
    const py = clientY ? (clientY - rect.top) / rect.height : 0.5;

    const newW = Math.min(1400, Math.max(300, this.viewBox.w * factor));
    const newH = newW * (this.baseViewBox.h / this.baseViewBox.w);

    const dx = (this.viewBox.w - newW) * px;
    const dy = (this.viewBox.h - newH) * py;

    this.viewBox.x += dx;
    this.viewBox.y += dy;
    this.viewBox.w = newW;
    this.viewBox.h = newH;

    this.applyViewBox();
  }

  zoomIn() {
    this.zoom(0.8);
  }

  zoomOut() {
    this.zoom(1.25);
  }

  panToPoint(x, y) {
    const w = 450;
    const h = w * (this.baseViewBox.h / this.baseViewBox.w);
    this.setViewBox(x - w / 2, y - h / 2, w, h);
  }

  resetView() {
    this.setViewBox(
      this.baseViewBox.x,
      this.baseViewBox.y,
      this.baseViewBox.w,
      this.baseViewBox.h
    );
  }

  setViewBox(x, y, w, h) {
    this.viewBox = { x, y, w, h };
    this.applyViewBox();
  }

  applyViewBox() {
    this.svg.setAttribute('viewBox', `${this.viewBox.x} ${this.viewBox.y} ${this.viewBox.w} ${this.viewBox.h}`);
  }
}

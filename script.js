/**
 * VENTUREPATH AI — CLIENT APPLICATION ENGINE
 * Full-stack interactive controller for venture discovery, roadmaps,
 * AI validation, budget planner, customer outreach, and dashboard sync.
 */

document.addEventListener('DOMContentLoaded', () => {
  'use strict';

  // State Management
  const AppState = {
    activeSlide: 1,
    totalSlides: 3,
    activeBusiness: 'Social Media Management & Reels Agency',
    selectedSkills: ['marketing', 'design'],
    budget: 15000,
    mode: 'all',
    timeCommitment: 'part-time',
    currentTemplateTab: 'whatsapp',
    templatesData: null,
    roadmapStages: [],
    leads: []
  };

  // DOM Elements Cache
  const UI = {
    toast: document.getElementById('toast'),
    toastMsg: document.getElementById('toast-message'),
    
    // Hero Slider
    slideKicker: document.getElementById('slide-kicker'),
    slideTitle: document.getElementById('slide-title'),
    slideDesc: document.getElementById('slide-desc'),
    currSlideNum: document.getElementById('curr-slide-num'),
    counterProgressBar: document.getElementById('counter-progress-bar'),
    prevSlideBtn: document.getElementById('prev-slide-btn'),
    nextSlideBtn: document.getElementById('next-slide-btn'),
    sculptureSlides: document.querySelectorAll('.sculpture-slide'),
    
    // Idea Finder
    ideaForm: document.getElementById('idea-discovery-form'),
    skillsCloud: document.getElementById('skills-cloud'),
    budgetSlider: document.getElementById('budget-slider'),
    budgetValBadge: document.getElementById('budget-val-badge'),
    sliderPresets: document.querySelectorAll('.slider-presets .preset-chip'),
    modeRadios: document.querySelectorAll('input[name="business_mode"]'),
    timeSelect: document.getElementById('time-commitment'),
    recommendationsContainer: document.getElementById('recommendations-container'),
    resultsCountBadge: document.getElementById('results-count-badge'),
    
    // Roadmap
    roadmapBusinessName: document.getElementById('roadmap-business-name'),
    roadmapPercentageBadge: document.getElementById('roadmap-percentage-badge'),
    roadmapProgressFill: document.getElementById('roadmap-progress-fill'),
    milestoneCompletedCount: document.getElementById('milestone-completed-count'),
    milestoneTotalCount: document.getElementById('milestone-total-count'),
    roadmapTimelineGrid: document.getElementById('roadmap-timeline-grid'),
    resetRoadmapBtn: document.getElementById('reset-roadmap-btn'),
    
    // Customers & Outreach
    outreachFounderName: document.getElementById('outreach-founder-name'),
    outreachBusinessName: document.getElementById('outreach-business-name'),
    outreachTargetProspect: document.getElementById('outreach-target-prospect'),
    outreachValueProp: document.getElementById('outreach-value-prop'),
    regenerateTemplatesBtn: document.getElementById('regenerate-templates-btn'),
    templateTabs: document.querySelectorAll('.template-tabs-header .tab-btn'),
    templateChannelBadge: document.getElementById('template-channel-badge'),
    templateTextBox: document.getElementById('template-text-box'),
    copyTemplateBtn: document.getElementById('copy-template-btn'),
    crmLeadsTable: document.getElementById('crm-leads-table'),
    addLeadBtn: document.getElementById('add-lead-btn'),
    discoveryQuestionsList: document.getElementById('discovery-questions-list'),
    
    // Validator
    validatorForm: document.getElementById('validator-form'),
    valTitle: document.getElementById('val-title'),
    valMarket: document.getElementById('val-market'),
    valProblem: document.getElementById('val-problem'),
    valPricing: document.getElementById('val-pricing'),
    valBudget: document.getElementById('val-budget'),
    runValidatorBtn: document.getElementById('run-validator-btn'),
    valOverallScore: document.getElementById('val-overall-score'),
    valVerdictPill: document.getElementById('val-verdict-pill'),
    valSummaryText: document.getElementById('val-summary-text'),
    valScoreProblem: document.getElementById('val-score-problem'),
    valBarProblem: document.getElementById('val-bar-problem'),
    valScoreDemand: document.getElementById('val-score-demand'),
    valBarDemand: document.getElementById('val-bar-demand'),
    valScoreMoat: document.getElementById('val-score-moat'),
    valBarMoat: document.getElementById('val-bar-moat'),
    valScoreFinance: document.getElementById('val-score-finance'),
    valBarFinance: document.getElementById('val-bar-finance'),
    valStrengthsList: document.getElementById('val-strengths-list'),
    valRisksList: document.getElementById('val-risks-list'),
    valExperimentsList: document.getElementById('val-experiments-list'),
    
    // Budget Planner
    budgetForm: document.getElementById('budget-calculator-form'),
    budgetPresetBtns: document.querySelectorAll('.presets-bar .chip-btn'),
    bStartingCapital: document.getElementById('b-starting-capital'),
    dispStartingCapital: document.getElementById('disp-starting-capital'),
    bEquipment: document.getElementById('b-equipment'),
    bMarketing: document.getElementById('b-marketing'),
    bRegistration: document.getElementById('b-registration'),
    bInventory: document.getElementById('b-inventory'),
    bMonthlyExpenses: document.getElementById('b-monthly-expenses'),
    dispMonthlyExpenses: document.getElementById('disp-monthly-expenses'),
    bSellingPrice: document.getElementById('b-selling-price'),
    bExpectedSales: document.getElementById('b-expected-sales'),
    dispTotalCapex: document.getElementById('disp-total-capex'),
    dispRemainingCash: document.getElementById('disp-remaining-cash'),
    dispRunwayMonths: document.getElementById('disp-runway-months'),
    dispBreakevenUnits: document.getElementById('disp-breakeven-units'),
    dispMonthlyRevenue: document.getElementById('disp-monthly-revenue'),
    dispMonthlyBurn: document.getElementById('disp-monthly-burn'),
    dispMonthlyProfit: document.getElementById('disp-monthly-profit'),
    barCapexEl: document.getElementById('bar-capex-el'),
    barBurnEl: document.getElementById('bar-burn-el'),
    barRevEl: document.getElementById('bar-rev-el'),
    
    // Resources
    resourceCatTabs: document.querySelectorAll('.category-tabs .cat-tab'),
    resourceSearchInput: document.getElementById('resource-search-input'),
    resourcesGridContainer: document.getElementById('resources-grid-container'),
    
    // Dashboard
    dashVentureName: document.getElementById('dash-venture-name'),
    dashVentureTagline: document.getElementById('dash-venture-tagline'),
    dashVentureBudget: document.getElementById('dash-venture-budget'),
    dashVentureDiff: document.getElementById('dash-venture-diff'),
    dashVentureMode: document.getElementById('dash-venture-mode'),
    dashProgressRing: document.getElementById('dash-progress-ring'),
    dashRingPercent: document.getElementById('dash-ring-percent'),
    dashMilestonesSummary: document.getElementById('dash-milestones-summary'),
    dashNextTaskName: document.getElementById('dash-next-task-name'),
    dashCashCushion: document.getElementById('dash-cash-cushion'),
    dashBreakevenMetric: document.getElementById('dash-breakeven-metric'),
    dashProfitMetric: document.getElementById('dash-profit-metric'),
    countIdentified: document.getElementById('count-identified'),
    countContacted: document.getElementById('count-contacted'),
    countReplied: document.getElementById('count-replied'),
    countConverted: document.getElementById('count-converted'),
    pipeIdentifiedLeads: document.getElementById('pipe-identified-leads'),
    pipeContactedLeads: document.getElementById('pipe-contacted-leads'),
    pipeRepliedLeads: document.getElementById('pipe-replied-leads'),
    pipeConvertedLeads: document.getElementById('pipe-converted-leads')
  };

  // Toast Notification Utility
  function showToast(message) {
    if (!UI.toast || !UI.toastMsg) return;
    UI.toastMsg.textContent = message;
    UI.toast.classList.add('show');
    clearTimeout(UI.toast._timeout);
    UI.toast._timeout = setTimeout(() => {
      UI.toast.classList.remove('show');
    }, 3200);
  }

  // =========================================================================
  // 1. HERO SLIDER CONTROLLER
  // =========================================================================
  const slidesContent = [
    {
      kicker: 'YOUR NEXT CHAPTER',
      title: 'BUILD YOUR<br><span class="highlight-line">OWN FUTURE.</span>',
      desc: 'From a business idea to your first customer. Discover your opportunity, build your roadmap, and turn your ambition into action.'
    },
    {
      kicker: 'VENTURE ARCHITECTURE',
      title: 'ENGINEERED FOR<br><span class="highlight-line">STUDENT FOUNDERS.</span>',
      desc: 'De-risk your business model before you write code or spend capital. Real market validation and verified unit economics.'
    },
    {
      kicker: 'FIRST 10 CUSTOMERS',
      title: 'EXECUTE WITH<br><span class="highlight-line">RELENTLESS PROOF.</span>',
      desc: 'Bridge the gap between raw concept and paying clients. Acquire early customers with respectful, high-conversion outreach.'
    }
  ];

  function updateHeroSlide(slideNum) {
    if (slideNum < 1) slideNum = AppState.totalSlides;
    if (slideNum > AppState.totalSlides) slideNum = 1;
    AppState.activeSlide = slideNum;

    // Update textual copy
    const data = slidesContent[slideNum - 1];
    if (UI.slideKicker) UI.slideKicker.textContent = data.kicker;
    if (UI.slideTitle) UI.slideTitle.innerHTML = data.title;
    if (UI.slideDesc) UI.slideDesc.textContent = data.desc;

    // Update slider bar & counter
    if (UI.currSlideNum) UI.currSlideNum.textContent = `0${slideNum}`;
    if (UI.counterProgressBar) {
      const pct = (slideNum / AppState.totalSlides) * 100;
      UI.counterProgressBar.style.width = `${pct}%`;
    }

    // Switch visual sculpture slide
    UI.sculptureSlides.forEach(slide => {
      const sIndex = parseInt(slide.getAttribute('data-slide'), 10);
      if (sIndex === slideNum) {
        slide.classList.add('active');
      } else {
        slide.classList.remove('active');
      }
    });
  }

  if (UI.prevSlideBtn) {
    UI.prevSlideBtn.addEventListener('click', () => updateHeroSlide(AppState.activeSlide - 1));
  }
  if (UI.nextSlideBtn) {
    UI.nextSlideBtn.addEventListener('click', () => updateHeroSlide(AppState.activeSlide + 1));
  }

  // =========================================================================
  // 2. BUSINESS IDEA FINDER CONTROLLER
  // =========================================================================
  function initIdeaFinder() {
    // Skill chips toggle
    if (UI.skillsCloud) {
      UI.skillsCloud.addEventListener('click', (e) => {
        const chip = e.target.closest('.skill-chip');
        if (!chip) return;
        chip.classList.toggle('active');
        
        const activeChips = UI.skillsCloud.querySelectorAll('.skill-chip.active');
        AppState.selectedSkills = Array.from(activeChips).map(c => c.getAttribute('data-skill'));
      });
    }

    // Budget slider live display
    if (UI.budgetSlider && UI.budgetValBadge) {
      UI.budgetSlider.addEventListener('input', (e) => {
        const val = parseInt(e.target.value, 10);
        AppState.budget = val;
        UI.budgetValBadge.textContent = `₹${val.toLocaleString('en-IN')}`;
        
        // Remove active preset if manual
        UI.sliderPresets.forEach(p => p.classList.remove('active'));
      });
    }

    // Budget presets
    UI.sliderPresets.forEach(chip => {
      chip.addEventListener('click', () => {
        UI.sliderPresets.forEach(p => p.classList.remove('active'));
        chip.classList.add('active');
        const amt = parseInt(chip.getAttribute('data-amount'), 10);
        AppState.budget = amt;
        if (UI.budgetSlider) UI.budgetSlider.value = amt;
        if (UI.budgetValBadge) UI.budgetValBadge.textContent = `₹${amt.toLocaleString('en-IN')}`;
      });
    });

    // Mode Radios
    UI.modeRadios.forEach(radio => {
      radio.addEventListener('change', (e) => {
        AppState.mode = e.target.value;
      });
    });

    // Time select
    if (UI.timeSelect) {
      UI.timeSelect.addEventListener('change', (e) => {
        AppState.timeCommitment = e.target.value;
      });
    }

    // Form submission
    if (UI.ideaForm) {
      UI.ideaForm.addEventListener('submit', (e) => {
        e.preventDefault();
        fetchRecommendations();
      });
    }

    // Initial load
    fetchRecommendations();
  }

  async function fetchRecommendations() {
    if (!UI.recommendationsContainer) return;
    
    UI.recommendationsContainer.innerHTML = `
      <div class="loading-state">
        <div class="spinner"></div>
        <span>Calculating venture viability and skill compatibility...</span>
      </div>
    `;

    try {
      const response = await fetch('/api/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          skills: AppState.selectedSkills,
          interests: ['creative', 'tech', 'services'],
          budget: AppState.budget,
          mode: AppState.mode,
          time: AppState.timeCommitment
        })
      });

      const data = await response.json();
      renderRecommendations(data.recommendations || []);
    } catch (err) {
      console.error(err);
      UI.recommendationsContainer.innerHTML = `
        <div class="panel" style="grid-column: 1 / -1; text-align: center; color: #E63946;">
          Failed to load venture models. Please verify backend server is active.
        </div>
      `;
    }
  }

  function renderRecommendations(ventures) {
    if (!UI.recommendationsContainer) return;
    if (UI.resultsCountBadge) {
      UI.resultsCountBadge.textContent = `${ventures.length} VENTURES READY`;
    }

    if (ventures.length === 0) {
      UI.recommendationsContainer.innerHTML = `
        <div class="panel" style="grid-column: 1 / -1; text-align: center; color: var(--text-secondary);">
          No venture models matched all chosen filters. Try relaxing your budget or mode constraints.
        </div>
      `;
      return;
    }

    UI.recommendationsContainer.innerHTML = ventures.map(v => {
      const isActive = v.name === AppState.activeBusiness;
      return `
        <div class="venture-card ${isActive ? 'is-active-choice' : ''}" data-id="${v.id}" data-name="${v.name}">
          <div>
            <div class="card-top-row">
              <span class="match-pill">${v.match_percentage}% MATCH</span>
              <span class="mode-badge">${v.mode.toUpperCase()}</span>
            </div>

            <h4 class="venture-card-title">${v.name}</h4>
            <div class="venture-card-tagline">${v.tagline}</div>
            <p class="venture-card-desc">${v.description}</p>
          </div>

          <div>
            <div class="venture-card-metrics">
              <div class="metric-box">
                <small>Min. Investment</small>
                <strong class="price">₹${v.budget.toLocaleString('en-IN')}</strong>
              </div>
              <div class="metric-box">
                <small>Difficulty</small>
                <strong>${v.difficulty}</strong>
              </div>
            </div>

            <div class="venture-card-actions">
              <button class="outline-action-btn btn-select ${isActive ? 'highlight-btn' : ''}" 
                      onclick="window.selectVentureByName('${v.name.replace(/'/g, "\\'")}')">
                ${isActive ? '✓ ACTIVE VENTURE' : 'SELECT VENTURE'}
              </button>
              <button class="outline-action-btn" title="Inspect Roadmap"
                      onclick="window.openRoadmapFor('${v.name.replace(/'/g, "\\'")}')">
                ROADMAP →
              </button>
            </div>
          </div>
        </div>
      `;
    }).join('');
  }

  window.selectVentureByName = async function(businessName) {
    try {
      const res = await fetch('/api/workspace/select-business', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ business_name: businessName })
      });
      const data = await res.json();
      if (data.success) {
        AppState.activeBusiness = businessName;
        showToast(`Selected "${businessName}" as active venture!`);
        fetchRecommendations();
        fetchRoadmap(businessName);
        fetchWorkspaceDashboard();
      }
    } catch (e) {
      console.error(e);
    }
  };

  window.openRoadmapFor = function(businessName) {
    window.selectVentureByName(businessName);
    const roadmapEl = document.getElementById('roadmap');
    if (roadmapEl) roadmapEl.scrollIntoView({ behavior: 'smooth' });
  };

  // =========================================================================
  // 3. 10-MILESTONE STARTUP ROADMAP CONTROLLER
  // =========================================================================
  async function fetchRoadmap(businessName) {
    const targetBusiness = businessName || AppState.activeBusiness;
    if (UI.roadmapBusinessName) UI.roadmapBusinessName.textContent = targetBusiness;

    try {
      const res = await fetch('/api/roadmap', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ business_name: targetBusiness })
      });
      const data = await res.json();
      renderRoadmap(data);
    } catch (err) {
      console.error(err);
    }
  }

  function renderRoadmap(data) {
    if (!UI.roadmapTimelineGrid) return;
    
    const stages = data.stages || [];
    AppState.roadmapStages = stages;

    // Update progress meter
    const pct = data.progress_percentage || 0;
    if (UI.roadmapPercentageBadge) UI.roadmapPercentageBadge.textContent = `${pct}% COMPLETE`;
    if (UI.roadmapProgressFill) UI.roadmapProgressFill.style.width = `${pct}%`;
    if (UI.milestoneCompletedCount) UI.milestoneCompletedCount.textContent = data.completed_count || 0;
    if (UI.milestoneTotalCount) UI.milestoneTotalCount.textContent = data.total_stages || 10;

    UI.roadmapTimelineGrid.innerHTML = stages.map(st => {
      const isCompleted = st.is_completed;
      return `
        <div class="milestone-item ${isCompleted ? 'completed' : ''}" id="milestone-card-${st.index}">
          <div class="milestone-header">
            <div class="milestone-left">
              <span class="milestone-index-badge">${isCompleted ? '✓' : `0${st.index + 1}`}</span>
              <div class="milestone-title-group">
                <h4>${st.title}</h4>
                <span class="milestone-timeline-tag">${st.estimated_timeline}</span>
              </div>
            </div>

            <label class="milestone-checkbox-label">
              <input type="checkbox" 
                     ${isCompleted ? 'checked' : ''} 
                     onchange="window.toggleMilestoneStep(${st.index}, this.checked)">
              <span>${isCompleted ? 'Completed' : 'Mark as Done'}</span>
            </label>
          </div>

          <ul class="milestone-tasks-list">
            ${st.tasks.map(t => `<li class="milestone-task-card">✦ ${t}</li>`).join('')}
          </ul>
        </div>
      `;
    }).join('');
  }

  window.toggleMilestoneStep = async function(stepIndex, isCompleted) {
    try {
      const res = await fetch('/api/workspace/toggle-milestone', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          business_name: AppState.activeBusiness,
          step_index: stepIndex,
          is_completed: isCompleted
        })
      });
      const data = await res.json();
      if (data.success) {
        showToast(isCompleted ? `Milestone 0${stepIndex + 1} marked complete!` : `Milestone 0${stepIndex + 1} reopened.`);
        fetchRoadmap(AppState.activeBusiness);
        fetchWorkspaceDashboard();
      }
    } catch (e) {
      console.error(e);
    }
  };

  if (UI.resetRoadmapBtn) {
    UI.resetRoadmapBtn.addEventListener('click', async () => {
      if (!confirm('Reset all milestone checkboxes for this venture?')) return;
      for (let i = 0; i < 10; i++) {
        await fetch('/api/workspace/toggle-milestone', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            business_name: AppState.activeBusiness,
            step_index: i,
            is_completed: false
          })
        });
      }
      showToast('Roadmap checklist has been reset.');
      fetchRoadmap(AppState.activeBusiness);
      fetchWorkspaceDashboard();
    });
  }

  // =========================================================================
  // 4. FIRST 10 CUSTOMERS ACQUISITION CONTROLLER
  // =========================================================================
  async function fetchOutreachTemplates() {
    try {
      const res = await fetch('/api/outreach', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          business_name: UI.outreachBusinessName ? UI.outreachBusinessName.value : AppState.activeBusiness,
          founder_name: UI.outreachFounderName ? UI.outreachFounderName.value : 'Abhishek',
          target_prospect: UI.outreachTargetProspect ? UI.outreachTargetProspect.value : 'Local Cafe Owner',
          niche: 'Hospitality & Retail',
          value_prop: UI.outreachValueProp ? UI.outreachValueProp.value : 'drive footfall through engaging Reels'
        })
      });
      const data = await res.json();
      AppState.templatesData = data;
      renderCurrentTemplateTab();
    } catch (e) {
      console.error(e);
    }
  }

  function renderCurrentTemplateTab() {
    if (!AppState.templatesData || !UI.templateTextBox) return;

    let text = '';
    let badge = 'WHATSAPP';

    if (AppState.currentTemplateTab === 'whatsapp') {
      text = AppState.templatesData.whatsapp_template;
      badge = 'WHATSAPP FORMAT (CASUAL & DIRECT)';
    } else if (AppState.currentTemplateTab === 'email') {
      const em = AppState.templatesData.email_template;
      text = `SUBJECT: ${em.subject}\n\n${em.body}`;
      badge = 'COLD EMAIL FORMAT (PROFESSIONAL & VALUE-FIRST)';
    } else if (AppState.currentTemplateTab === 'social') {
      text = AppState.templatesData.social_dm_template;
      badge = 'INSTAGRAM / LINKEDIN DM FORMAT';
    } else if (AppState.currentTemplateTab === 'followup') {
      text = AppState.templatesData.follow_up_template;
      badge = '3-DAY FOLLOW-UP FORMAT';
    }

    UI.templateTextBox.textContent = text;
    if (UI.templateChannelBadge) UI.templateChannelBadge.textContent = badge;
  }

  UI.templateTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      UI.templateTabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      AppState.currentTemplateTab = tab.getAttribute('data-tab');
      renderCurrentTemplateTab();
    });
  });

  if (UI.regenerateTemplatesBtn) {
    UI.regenerateTemplatesBtn.addEventListener('click', () => {
      fetchOutreachTemplates();
      showToast('Outreach copy refreshed with your details.');
    });
  }

  if (UI.copyTemplateBtn) {
    UI.copyTemplateBtn.addEventListener('click', async () => {
      const text = UI.templateTextBox ? UI.templateTextBox.textContent : '';
      if (!text) return;
      try {
        await navigator.clipboard.writeText(text);
        showToast('Template copied to clipboard!');
      } catch (err) {
        showToast('Text selected! Press Ctrl+C to copy.');
      }
    });
  }

  // Mini CRM Lead Management
  async function loadCRMLeads() {
    try {
      const res = await fetch('/api/workspace');
      const data = await res.json();
      AppState.leads = data.leads || [];
      renderCRMLeadsTable();
      renderDashboardPipeline();
    } catch (e) {
      console.error(e);
    }
  }

  function renderCRMLeadsTable() {
    if (!UI.crmLeadsTable) return;
    
    if (AppState.leads.length === 0) {
      UI.crmLeadsTable.innerHTML = `<p style="font-size: 0.8rem; color: var(--text-muted);">No prospects added yet. Click "+ Add Prospect" above.</p>`;
      return;
    }

    UI.crmLeadsTable.innerHTML = AppState.leads.map(lead => `
      <div class="lead-item-row" data-id="${lead.id}">
        <div class="lead-info-left">
          <strong>${lead.lead_name}</strong>
          <small>${lead.channel} • ${lead.notes || 'No notes'}</small>
        </div>
        <select class="lead-status-select" onchange="window.updateLeadStatus(${lead.id}, this.value)">
          <option value="Identified" ${lead.status === 'Identified' ? 'selected' : ''}>Identified</option>
          <option value="Contacted" ${lead.status === 'Contacted' ? 'selected' : ''}>Contacted</option>
          <option value="Replied" ${lead.status === 'Replied' ? 'selected' : ''}>Replied</option>
          <option value="Converted" ${lead.status === 'Converted' ? 'selected' : ''}>Converted (Paid)</option>
        </select>
      </div>
    `).join('');
  }

  window.updateLeadStatus = async function(leadId, newStatus) {
    try {
      await fetch('/api/workspace/update-lead-status', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: leadId, status: newStatus })
      });
      showToast(`Lead status updated to ${newStatus}`);
      loadCRMLeads();
    } catch (e) {
      console.error(e);
    }
  };

  if (UI.addLeadBtn) {
    UI.addLeadBtn.addEventListener('click', async () => {
      const name = prompt('Enter prospect business or contact name:');
      if (!name || !name.trim()) return;
      const channel = prompt('Enter outreach channel (e.g. WhatsApp, Instagram, In-Person):', 'WhatsApp') || 'WhatsApp';
      const notes = prompt('Enter brief context or hook:', 'Found via local search') || '';

      try {
        const res = await fetch('/api/workspace/add-lead', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ lead_name: name, channel: channel, notes: notes })
        });
        const data = await res.json();
        if (data.success) {
          showToast(`Added "${name}" to outreach pipeline!`);
          loadCRMLeads();
        }
      } catch (e) {
        console.error(e);
      }
    });
  }

  // =========================================================================
  // 5. BUSINESS IDEA VALIDATOR CONTROLLER
  // =========================================================================
  if (UI.validatorForm) {
    UI.validatorForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      
      const payload = {
        idea_title: UI.valTitle ? UI.valTitle.value : '',
        target_market: UI.valMarket ? UI.valMarket.value : '',
        problem_solved: UI.valProblem ? UI.valProblem.value : '',
        pricing: UI.valPricing ? UI.valPricing.value : '',
        budget: UI.valBudget ? parseInt(UI.valBudget.value, 10) : 10000
      };

      if (UI.runValidatorBtn) {
        UI.runValidatorBtn.disabled = true;
        UI.runValidatorBtn.innerHTML = `<span>ANALYZING WITH AI...</span> <div class="spinner" style="width:16px;height:16px;margin:0;"></div>`;
      }

      try {
        const res = await fetch('/api/validate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const data = await res.json();
        renderValidationResults(data.evaluation);
        showToast('Idea evaluated! Review your feasibility scores and risks below.');
      } catch (err) {
        console.error(err);
        showToast('Validation failed. Please check network connection.');
      } finally {
        if (UI.runValidatorBtn) {
          UI.runValidatorBtn.disabled = false;
          UI.runValidatorBtn.innerHTML = `<span>RUN FEASIBILITY STRESS-TEST</span> <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>`;
        }
      }
    });
  }

  function renderValidationResults(ev) {
    if (!ev) return;

    if (UI.valOverallScore) UI.valOverallScore.textContent = ev.overall_score;
    if (UI.valSummaryText) UI.valSummaryText.textContent = ev.summary;

    if (UI.valVerdictPill) {
      UI.valVerdictPill.textContent = ev.verdict;
      UI.valVerdictPill.className = `verdict-pill ${ev.verdict_badge || 'green'}`;
    }

    // 4 Vectors
    const scores = ev.scores || {};
    if (UI.valScoreProblem) UI.valScoreProblem.textContent = `${scores.problem_intensity || 80}%`;
    if (UI.valBarProblem) UI.valBarProblem.style.width = `${scores.problem_intensity || 80}%`;

    if (UI.valScoreDemand) UI.valScoreDemand.textContent = `${scores.market_demand || 75}%`;
    if (UI.valBarDemand) UI.valBarDemand.style.width = `${scores.market_demand || 75}%`;

    if (UI.valScoreMoat) UI.valScoreMoat.textContent = `${scores.defensibility || 65}%`;
    if (UI.valBarMoat) UI.valBarMoat.style.width = `${scores.defensibility || 65}%`;

    if (UI.valScoreFinance) UI.valScoreFinance.textContent = `${scores.financial_ease || 85}%`;
    if (UI.valBarFinance) UI.valBarFinance.style.width = `${scores.financial_ease || 85}%`;

    // Lists
    if (UI.valStrengthsList) {
      UI.valStrengthsList.innerHTML = (ev.strengths || []).map(s => `<li>${s}</li>`).join('');
    }
    if (UI.valRisksList) {
      UI.valRisksList.innerHTML = (ev.critical_risks || []).map(r => `<li>${r}</li>`).join('');
    }
    if (UI.valExperimentsList) {
      UI.valExperimentsList.innerHTML = (ev.validation_experiments || []).map((exp, i) => `<li>${i + 1}. ${exp}</li>`).join('');
    }
  }

  // =========================================================================
  // 6. STARTUP BUDGET & UNIT ECONOMICS CONTROLLER
  // =========================================================================
  function initBudgetPlanner() {
    // Range sliders live badge update
    if (UI.bStartingCapital && UI.dispStartingCapital) {
      UI.bStartingCapital.addEventListener('input', (e) => {
        UI.dispStartingCapital.textContent = `₹${parseInt(e.target.value, 10).toLocaleString('en-IN')}`;
        recalculateBudget();
      });
    }

    if (UI.bMonthlyExpenses && UI.dispMonthlyExpenses) {
      UI.bMonthlyExpenses.addEventListener('input', (e) => {
        UI.dispMonthlyExpenses.textContent = `₹${parseInt(e.target.value, 10).toLocaleString('en-IN')}`;
        recalculateBudget();
      });
    }

    // Number inputs recalculate on change
    const inputs = [UI.bEquipment, UI.bMarketing, UI.bRegistration, UI.bInventory, UI.bSellingPrice, UI.bExpectedSales];
    inputs.forEach(inp => {
      if (inp) inp.addEventListener('input', recalculateBudget);
    });

    // Preset Buttons
    UI.budgetPresetBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        UI.budgetPresetBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const pType = btn.getAttribute('data-preset');
        applyBudgetPreset(pType);
      });
    });

    recalculateBudget();
  }

  function applyBudgetPreset(pType) {
    if (pType === 'agency') {
      setBudgetInputs(20000, 4000, 3000, 1500, 2500, 3500, 1200, 15);
    } else if (pType === 'ecommerce') {
      setBudgetInputs(45000, 8000, 12000, 3000, 15000, 6000, 899, 35);
    } else if (pType === 'tutoring') {
      setBudgetInputs(8000, 1500, 1200, 800, 0, 1000, 3000, 4);
    }
    recalculateBudget();
  }

  function setBudgetInputs(cap, eq, mkt, reg, inv, burn, price, sales) {
    if (UI.bStartingCapital) { UI.bStartingCapital.value = cap; UI.dispStartingCapital.textContent = `₹${cap.toLocaleString('en-IN')}`; }
    if (UI.bEquipment) UI.bEquipment.value = eq;
    if (UI.bMarketing) UI.bMarketing.value = mkt;
    if (UI.bRegistration) UI.bRegistration.value = reg;
    if (UI.bInventory) UI.bInventory.value = inv;
    if (UI.bMonthlyExpenses) { UI.bMonthlyExpenses.value = burn; UI.dispMonthlyExpenses.textContent = `₹${burn.toLocaleString('en-IN')}`; }
    if (UI.bSellingPrice) UI.bSellingPrice.value = price;
    if (UI.bExpectedSales) UI.bExpectedSales.value = sales;
  }

  async function recalculateBudget() {
    const payload = {
      starting_capital: UI.bStartingCapital ? parseFloat(UI.bStartingCapital.value) : 20000,
      equipment_cost: UI.bEquipment ? parseFloat(UI.bEquipment.value) : 4000,
      marketing_cost: UI.bMarketing ? parseFloat(UI.bMarketing.value) : 3000,
      registration_cost: UI.bRegistration ? parseFloat(UI.bRegistration.value) : 1500,
      inventory_cost: UI.bInventory ? parseFloat(UI.bInventory.value) : 2500,
      monthly_expenses: UI.bMonthlyExpenses ? parseFloat(UI.bMonthlyExpenses.value) : 3500,
      selling_price: UI.bSellingPrice ? parseFloat(UI.bSellingPrice.value) : 1200,
      expected_sales: UI.bExpectedSales ? parseInt(UI.bExpectedSales.value, 10) : 15
    };

    try {
      const res = await fetch('/api/budget/calculate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      renderBudgetOutputs(data);
    } catch (e) {
      console.error(e);
    }
  }

  function renderBudgetOutputs(calc) {
    if (!calc) return;

    if (UI.dispTotalCapex) UI.dispTotalCapex.textContent = `₹${calc.total_startup_capex.toLocaleString('en-IN')}`;
    if (UI.dispRemainingCash) UI.dispRemainingCash.textContent = `₹${calc.remaining_capital.toLocaleString('en-IN')}`;
    if (UI.dispRunwayMonths) UI.dispRunwayMonths.textContent = `${calc.runway_months} Months`;
    if (UI.dispBreakevenUnits) UI.dispBreakevenUnits.textContent = `${calc.break_even_units} Units`;

    if (UI.dispMonthlyRevenue) UI.dispMonthlyRevenue.textContent = `₹${calc.estimated_monthly_revenue.toLocaleString('en-IN')}`;
    if (UI.dispMonthlyBurn) UI.dispMonthlyBurn.textContent = `-₹${calc.monthly_expenses.toLocaleString('en-IN')}`;
    
    if (UI.dispMonthlyProfit) {
      const isProf = calc.is_profitable;
      const profitVal = calc.estimated_monthly_profit;
      UI.dispMonthlyProfit.textContent = `${profitVal >= 0 ? '+' : ''}₹${profitVal.toLocaleString('en-IN')} / mo`;
      UI.dispMonthlyProfit.style.color = isProf ? '#22c55e' : '#E63946';
    }

    // Chart bars relative height
    const maxVal = Math.max(calc.total_startup_capex, calc.estimated_monthly_revenue, calc.monthly_expenses * 3, 10000);
    if (UI.barCapexEl) UI.barCapexEl.style.height = `${Math.min(100, Math.max(15, (calc.total_startup_capex / maxVal) * 100))}%`;
    if (UI.barBurnEl) UI.barBurnEl.style.height = `${Math.min(100, Math.max(15, ((calc.monthly_expenses * 2) / maxVal) * 100))}%`;
    if (UI.barRevEl) UI.barRevEl.style.height = `${Math.min(100, Math.max(15, (calc.estimated_monthly_revenue / maxVal) * 100))}%`;
  }

  // =========================================================================
  // 7. MENTOR & OFFICIAL RESOURCE DIRECTORY CONTROLLER
  // =========================================================================
  async function fetchResources(category = 'all', query = '') {
    if (!UI.resourcesGridContainer) return;

    try {
      const url = `/api/resources?category=${encodeURIComponent(category)}&q=${encodeURIComponent(query)}`;
      const res = await fetch(url);
      const data = await res.json();
      renderResources(data.resources || []);
    } catch (e) {
      console.error(e);
    }
  }

  function renderResources(list) {
    if (!UI.resourcesGridContainer) return;

    if (list.length === 0) {
      UI.resourcesGridContainer.innerHTML = `<div style="grid-column: 1 / -1; color: var(--text-muted); text-align: center; padding: 24px;">No matching verified resources found.</div>`;
      return;
    }

    UI.resourcesGridContainer.innerHTML = list.map(r => `
      <div class="resource-card">
        <div class="resource-card-top">
          <span class="resource-badge">${r.badge}</span>
          <h4 class="resource-title">${r.title}</h4>
          <p class="resource-desc">${r.description}</p>
          <ul class="resource-benefits-list">
            ${(r.benefits || []).map(b => `<li>✦ ${b}</li>`).join('')}
          </ul>
        </div>
        <a href="${r.url}" target="_blank" rel="noopener noreferrer" class="resource-link-btn">
          <span>VISIT OFFICIAL PORTAL</span>
          <span>↗</span>
        </a>
      </div>
    `).join('');
  }

  UI.resourceCatTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      UI.resourceCatTabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      const cat = tab.getAttribute('data-cat');
      const q = UI.resourceSearchInput ? UI.resourceSearchInput.value : '';
      fetchResources(cat, q);
    });
  });

  if (UI.resourceSearchInput) {
    UI.resourceSearchInput.addEventListener('input', (e) => {
      const activeTab = document.querySelector('.category-tabs .cat-tab.active');
      const cat = activeTab ? activeTab.getAttribute('data-cat') : 'all';
      fetchResources(cat, e.target.value);
    });
  }

  // =========================================================================
  // 8. DASHBOARD WORKSPACE SYNCHRONIZATION
  // =========================================================================
  async function fetchWorkspaceDashboard() {
    try {
      const res = await fetch('/api/workspace');
      const data = await res.json();
      renderDashboard(data);
    } catch (e) {
      console.error(e);
    }
  }

  function renderDashboard(data) {
    const biz = data.active_business || {};
    const summary = data.roadmap_summary || {};
    const budget = data.budget || {};

    if (UI.dashVentureName) UI.dashVentureName.textContent = biz.name || AppState.activeBusiness;
    if (UI.dashVentureTagline) UI.dashVentureTagline.textContent = biz.tagline || '';
    if (UI.dashVentureBudget) UI.dashVentureBudget.textContent = `₹${(biz.budget || 3000).toLocaleString('en-IN')}`;
    if (UI.dashVentureDiff) UI.dashVentureDiff.textContent = biz.difficulty || 'Beginner Friendly';
    if (UI.dashVentureMode) UI.dashVentureMode.textContent = (biz.mode || 'ONLINE').toUpperCase();

    // Circular Progress Ring (circumference: 2 * PI * 54 = 339.29)
    const pct = summary.percentage || 0;
    const circ = 339.29;
    const offset = circ - (pct / 100) * circ;
    if (UI.dashProgressRing) UI.dashProgressRing.style.strokeDashoffset = offset;
    if (UI.dashRingPercent) UI.dashRingPercent.textContent = `${pct}%`;
    if (UI.dashMilestonesSummary) UI.dashMilestonesSummary.textContent = `${summary.completed || 0} of ${summary.total || 10} Milestones`;

    // Next Task Name
    if (UI.dashNextTaskName && biz.roadmap_stages) {
      const nextIdx = summary.completed || 0;
      if (nextIdx < biz.roadmap_stages.length) {
        UI.dashNextTaskName.textContent = biz.roadmap_stages[nextIdx].tasks[0] || biz.roadmap_stages[nextIdx].title;
      } else {
        UI.dashNextTaskName.textContent = 'All initial roadmap milestones reached!';
      }
    }

    // Financial Metrics in Dashboard
    const cap = budget.starting_capital || 20000;
    const capex = (budget.equipment_cost || 4000) + (budget.marketing_cost || 3000) + (budget.registration_cost || 1500) + (budget.inventory_cost || 2500);
    const cushion = cap - capex;
    if (UI.dashCashCushion) UI.dashCashCushion.textContent = `₹${cushion.toLocaleString('en-IN')}`;
    
    const burn = budget.monthly_expenses || 3500;
    const price = budget.selling_price || 1200;
    const beUnits = price > 0 ? Math.ceil(burn / price) : 0;
    if (UI.dashBreakevenMetric) UI.dashBreakevenMetric.textContent = `${beUnits} Units / Mo`;

    const rev = price * (budget.expected_sales || 15);
    const net = rev - burn;
    if (UI.dashProfitMetric) {
      UI.dashProfitMetric.textContent = `${net >= 0 ? '+' : ''}₹${net.toLocaleString('en-IN')} / mo`;
      UI.dashProfitMetric.style.color = net >= 0 ? '#22c55e' : '#E63946';
    }

    // Pipeline Leads
    renderDashboardPipeline();
  }

  function renderDashboardPipeline() {
    const leads = AppState.leads || [];
    const identified = leads.filter(l => l.status === 'Identified');
    const contacted = leads.filter(l => l.status === 'Contacted');
    const replied = leads.filter(l => l.status === 'Replied');
    const converted = leads.filter(l => l.status === 'Converted');

    if (UI.countIdentified) UI.countIdentified.textContent = identified.length;
    if (UI.countContacted) UI.countContacted.textContent = contacted.length;
    if (UI.countReplied) UI.countReplied.textContent = replied.length;
    if (UI.countConverted) UI.countConverted.textContent = converted.length;

    renderPipelinePills(UI.pipeIdentifiedLeads, identified);
    renderPipelinePills(UI.pipeContactedLeads, contacted);
    renderPipelinePills(UI.pipeRepliedLeads, replied);
    renderPipelinePills(UI.pipeConvertedLeads, converted);
  }

  function renderPipelinePills(container, list) {
    if (!container) return;
    if (list.length === 0) {
      container.innerHTML = `<span style="font-size: 0.72rem; color: var(--text-muted); display: block; padding: 8px 0;">No prospects</span>`;
      return;
    }
    container.innerHTML = list.map(l => `
      <div class="pipe-lead-pill">
        <strong>${l.lead_name}</strong>
        <small>${l.channel}</small>
      </div>
    `).join('');
  }

  // =========================================================================
  // INITIALIZATION ON LOAD
  // =========================================================================
  initIdeaFinder();
  fetchRoadmap(AppState.activeBusiness);
  fetchOutreachTemplates();
  loadCRMLeads();
  initBudgetPlanner();
  fetchResources();
  fetchWorkspaceDashboard();

  console.log('✦ VenturePath AI initialized successfully.');
});

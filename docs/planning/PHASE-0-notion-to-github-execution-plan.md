# PHASE 0: Notion → GitHub Execution Plan

## Overview

This document defines the execution plan for bootstrapping GitHub project management artifacts (labels, milestones, issues, and a Projects v2 board) derived from the Notion export documentation in `docs/notion-export/**`.

**Source of Truth**: `docs/notion-export/**` (all `.md` files)  
**Target Branch**: `phase-0-notion-to-github`  
**Base Repository**: `Abuzhor/smart-grocery-logistics-platform`

---

## 1. Label Taxonomy

Labels are organized into categories with consistent prefixes for easy filtering and visualization.

### Phase Labels
| Label | Color | Description |
|-------|-------|-------------|
| `phase:0-bootstrap` | `#0E8A16` | PHASE 0: Project bootstrap and planning setup |
| `phase:1-foundation` | `#1D76DB` | PHASE 1: Core platform foundation |
| `phase:2-mvp` | `#5319E7` | PHASE 2: MVP features and launch |
| `phase:3-scale` | `#D93F0B` | PHASE 3: Scaling and optimization |
| `phase:4-global` | `#FBCA04` | PHASE 4: Global expansion |

### Domain Labels
| Label | Color | Description |
|-------|-------|-------------|
| `domain:catalog` | `#C5DEF5` | Catalog and product management |
| `domain:inventory` | `#BFD4F2` | Inventory management and tracking |
| `domain:ordering` | `#D4C5F9` | Order capture and orchestration |
| `domain:fulfillment` | `#C2E0C6` | Fulfillment and picking operations |
| `domain:routing` | `#FEF2C0` | Route optimization and delivery |
| `domain:partner` | `#F9D0C4` | Partner integration and management |
| `domain:workforce` | `#E99695` | Workforce and driver management |
| `domain:operations` | `#D73A4A` | Operations and monitoring |
| `domain:compliance` | `#0052CC` | Compliance and regulatory |
| `domain:platform` | `#5319E7` | Platform infrastructure |

### Type Labels
| Label | Color | Description |
|-------|-------|-------------|
| `type:documentation` | `#0075CA` | Documentation and planning |
| `type:architecture` | `#1D76DB` | Architecture and design decisions |
| `type:feature` | `#A2EEEF` | New feature implementation |
| `type:infrastructure` | `#D876E3` | Infrastructure and DevOps |
| `type:testing` | `#BFD4F2` | Testing and quality assurance |
| `type:security` | `#D93F0B` | Security and vulnerability fixes |
| `type:compliance-task` | `#0052CC` | Compliance implementation task |

### Priority Labels
| Label | Color | Description |
|-------|-------|-------------|
| `priority:critical` | `#B60205` | Critical - must be done immediately |
| `priority:high` | `#D93F0B` | High priority |
| `priority:medium` | `#FBCA04` | Medium priority |
| `priority:low` | `#0E8A16` | Low priority |

### Category Labels
| Label | Color | Description |
|-------|-------|-------------|
| `category:grocery` | `#C2E0C6` | Grocery and food items |
| `category:cold-chain` | `#BFD4F2` | Cold chain and refrigeration |
| `category:regulated` | `#0052CC` | Regulated items (age, prescription) |
| `category:services` | `#FEF2C0` | Service delivery (non-physical) |
| `category:b2b` | `#5319E7` | Business-to-business operations |

### Gate Labels
| Label | Color | Description |
|-------|-------|-------------|
| `gate:reliability` | `#0E8A16` | Reliability gate criteria |
| `gate:economics` | `#FBCA04` | Economics and unit profitability gate |
| `gate:trust` | `#D93F0B` | Trust and fraud prevention gate |
| `gate:compliance` | `#0052CC` | Compliance and regulatory gate |

---

## 2. Milestones

Milestones represent major phases of the platform development and expansion.

| Milestone | Due Date | Description |
|-----------|----------|-------------|
| **PHASE 0: Bootstrap & Planning** | +30 days | Project setup, planning artifacts, GitHub automation, initial documentation structure |
| **PHASE 1: Foundation** | +90 days | Core platform architecture, basic catalog, ordering, and fulfillment modules |
| **PHASE 2: MVP Launch** | +180 days | Single-city pilot with 2 categories, end-to-end workflows, payment integration |
| **PHASE 3: Scale & Optimize** | +270 days | Expand to 5-7 categories in city 1, second city launch, operational excellence |
| **PHASE 4: Global Expansion** | +365 days | Multi-country expansion, policy engine, compliance framework, localization |

---

## 3. Project Board Configuration (Projects v2)

### Board Name
`Smart Grocery Logistics Platform - Execution Board`

### Views
- **Main Kanban Board** (default)
- **By Phase** (grouped by phase labels)
- **By Domain** (grouped by domain labels)
- **By Priority** (sorted by priority)

### Status Columns (Kanban)

| Column | Description | Automation |
|--------|-------------|------------|
| **Backlog** | Issues identified but not yet ready for work | New issues start here |
| **Ready** | Issues refined and ready to be picked up | Manually moved from Backlog |
| **In Progress** | Issues actively being worked on | Auto-set when PR linked or assignee set |
| **Review** | Issues in code review or validation | Auto-set when PR in review |
| **Blocked** | Issues blocked by dependencies or decisions | Manually set with reason |
| **Done** | Issues completed and merged | Auto-set when PR merged or issue closed |

### Custom Fields
- **Phase** (Single select): PHASE 0, PHASE 1, PHASE 2, PHASE 3, PHASE 4
- **Domain** (Single select): Catalog, Inventory, Ordering, Fulfillment, Routing, Partner, Workforce, Operations, Compliance, Platform
- **Priority** (Single select): Critical, High, Medium, Low
- **Gate Criteria** (Multi-select): Reliability, Economics, Trust, Compliance
- **Notion Reference** (Text): Link to source Notion export file/section

---

## 4. Issue Mapping: Notion → GitHub Issues

This section maps Notion export sections to specific GitHub issues with traceability.

### Meta Issue
**Issue #1: PHASE 0 – Notion → GitHub Execution Plan**
- **Labels**: `phase:0-bootstrap`, `type:documentation`, `priority:critical`
- **Milestone**: PHASE 0: Bootstrap & Planning
- **Description**: Master tracking issue for PHASE 0 execution
- **Acceptance Criteria**:
  - [x] Execution plan document created
  - [ ] All labels created in repository
  - [ ] All milestones created
  - [ ] All mapped issues created with proper traceability
  - [ ] Projects v2 board configured
  - [ ] All issues added to project board
- **KPI References**: 
  - Setup completeness: 100% of artifacts created
  - Traceability: All issues link to source documentation
- **Source**: `docs/notion-export/index.md`, `docs/notion-export/00-executive-summary.md`

### PHASE 0 Issues (Bootstrap & Planning)

#### Issue #2: Bootstrap GitHub Project Automation
- **Labels**: `phase:0-bootstrap`, `type:infrastructure`, `priority:critical`
- **Milestone**: PHASE 0
- **Description**: Create automation scripts for bootstrapping GitHub artifacts
- **Acceptance Criteria**:
  - [ ] `scripts/planning/bootstrap_github.sh` created and tested
  - [ ] `scripts/planning/bootstrap_github.py` created and tested
  - [ ] Scripts are idempotent (safe to re-run)
  - [ ] Scripts print created artifacts with links
  - [ ] Documentation for running scripts added
- **KPI References**: Automation reliability: 100% success rate on re-runs
- **Source**: Requirements from problem statement
- **Related Issues**: #1

#### Issue #3: Define Vision and North Star Metrics
- **Labels**: `phase:0-bootstrap`, `type:documentation`, `priority:high`
- **Milestone**: PHASE 0
- **Description**: Document platform vision, goals, and north star metrics based on Notion export
- **Acceptance Criteria**:
  - [ ] Vision document created referencing Notion export
  - [ ] North star metrics defined (On-time delivery ≥95%, Payment success ≥99%, Cancellation ≤5%, CSAT ≥60)
  - [ ] Quarterly OKRs outlined
  - [ ] Go/No-Go decision criteria documented
- **KPI References**:
  - [On-time delivery ≥95%](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/07-metrics-and-gates.md#L3)
  - [Payment success ≥99%](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/07-metrics-and-gates.md#L4)
  - [Cancellation ≤3-5%](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/07-metrics-and-gates.md#L5)
  - [CSAT ≥60](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/07-metrics-and-gates.md#L6)
- **Source**: [`docs/notion-export/01-vision-and-goals.md`](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/01-vision-and-goals.md), [`docs/notion-export/07-metrics-and-gates.md`](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/07-metrics-and-gates.md)
- **Related Issues**: #1

#### Issue #4: Define Platform Scope and Category Taxonomy
- **Labels**: `phase:0-bootstrap`, `type:documentation`, `priority:high`, `domain:platform`
- **Milestone**: PHASE 0
- **Description**: Define platform scope, category classification, and operational packs
- **Acceptance Criteria**:
  - [ ] Category taxonomy documented (non-sensitive, cold-chain, regulated, scheduled services, B2B)
  - [ ] Operational packs defined for each category type
  - [ ] Category expansion roadmap created
  - [ ] Requirements matrix for each category documented
- **KPI References**:
  - Category coverage: Start with 2, expand to 5-7
  - Direct contribution margin: Positive per core category
- **Source**: [`docs/notion-export/03-platform-scope.md`](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/03-platform-scope.md)
- **Related Issues**: #1, #3

#### Issue #5: Document 90-Day City Launch Plan
- **Labels**: `phase:0-bootstrap`, `type:documentation`, `priority:high`
- **Milestone**: PHASE 0
- **Description**: Create detailed 90-day city launch plan with week-by-week breakdown
- **Acceptance Criteria**:
  - [ ] Week 1-2: Operating zone definition, metrics setup, category policies
  - [ ] Week 3-6: MVP (consumer/partner/workforce) + POD + settlements
  - [ ] Week 7-10: Pilot operations + ETA/routing optimization + CAPA
  - [ ] Week 11-13: Expand to 2 additional categories + payment/tax config
  - [ ] Gate criteria defined for each phase
- **KPI References**:
  - Launch timeline adherence: ≥90%
  - Pilot success rate: All 4 gates (reliability, economics, trust, compliance) passed
- **Source**: [`docs/notion-export/08-90-day-city-launch-plan.md`](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/08-90-day-city-launch-plan.md)
- **Related Issues**: #1, #3

#### Issue #6: Create Measurement Dictionary and KPI Definitions
- **Labels**: `phase:0-bootstrap`, `type:documentation`, `priority:high`, `domain:operations`
- **Milestone**: PHASE 0
- **Description**: Define all KPIs, calculation methods, and data sources
- **Acceptance Criteria**:
  - [ ] KPI dictionary created with definitions
  - [ ] Calculation methods documented for each metric
  - [ ] Data sources identified
  - [ ] Dashboard specifications outlined (daily ops, weekly unit economics, monthly partner health)
- **KPI References**:
  - [On-time delivery](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/13-measurement-dictionary.md#L3)
  - [Payment success](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/13-measurement-dictionary.md#L4)
  - [Cancellation rate](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/13-measurement-dictionary.md#L5)
  - [CSAT](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/13-measurement-dictionary.md#L6)
  - [Supply chain metrics](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/13-measurement-dictionary.md#L7)
- **Source**: [`docs/notion-export/13-measurement-dictionary.md`](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/13-measurement-dictionary.md), [`docs/notion-export/07-metrics-and-gates.md`](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/07-metrics-and-gates.md)
- **Related Issues**: #1, #3

#### Issue #7: Define Risk Management Framework and Controls
- **Labels**: `phase:0-bootstrap`, `type:documentation`, `priority:high`, `domain:compliance`
- **Milestone**: PHASE 0
- **Description**: Document top 10 risks and corresponding controls
- **Acceptance Criteria**:
  - [ ] Risk register created with top 10 risks
  - [ ] Controls defined (KYC/KYB, POD, audit trail, CAPA, separation of duties)
  - [ ] Risk thresholds established (fraud, disputes, payment, compliance)
  - [ ] Incident response procedures outlined
- **KPI References**:
  - Fraud rate: Within acceptable threshold
  - Dispute rate: Within acceptable threshold
  - Compliance violations: 0 critical
- **Source**: [`docs/notion-export/06-risks-and-controls.md`](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/06-risks-and-controls.md)
- **Related Issues**: #1

#### Issue #8: Document Technology Principles and Architecture
- **Labels**: `phase:0-bootstrap`, `type:architecture`, `priority:high`, `domain:platform`
- **Milestone**: PHASE 0
- **Description**: Define technology principles and high-level architecture
- **Acceptance Criteria**:
  - [ ] Architecture principles documented (domain-driven, event-driven, feature flags, multi-tenant ready)
  - [ ] Reliability requirements defined (SLAs, observability, DR, gradual rollout)
  - [ ] Security requirements documented (zero trust, encryption, data classification, audit)
  - [ ] Tech stack decisions captured in ADRs
- **KPI References**:
  - System availability: SLA targets per domain
  - MTTR: Mean time to resolution targets
  - Incident rate: Acceptable thresholds
- **Source**: [`docs/notion-export/10-technology-principles.md`](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/10-technology-principles.md)
- **Related Issues**: #1

#### Issue #9: Define Operations Governance and SOPs
- **Labels**: `phase:0-bootstrap`, `type:documentation`, `priority:medium`, `domain:operations`
- **Milestone**: PHASE 0
- **Description**: Create standard operating procedures and governance framework
- **Acceptance Criteria**:
  - [ ] Mandatory SOPs defined (fulfillment/substitution/return/recall + incident management + CAPA)
  - [ ] Partner governance documented (quality scores, audits, improvement plans)
  - [ ] Workforce governance documented (quality incentives, cancellation/delay policies)
  - [ ] Escalation procedures created
- **KPI References**:
  - Partner quality score: Minimum threshold
  - Workforce quality: Performance targets
  - Incident resolution: SLA compliance
- **Source**: [`docs/notion-export/11-operations-governance.md`](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/11-operations-governance.md), [`docs/notion-export/09-operating-pack-template.md`](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/09-operating-pack-template.md)
- **Related Issues**: #1

#### Issue #10: Document Revenue Model and Unit Economics
- **Labels**: `phase:0-bootstrap`, `type:documentation`, `priority:high`
- **Milestone**: PHASE 0
- **Description**: Define revenue streams and unit economics framework
- **Acceptance Criteria**:
  - [ ] Revenue model documented (commission + delivery fees + subscriptions + ads + B2B + compliance services)
  - [ ] Unit economics formula defined: Profit/Order = Revenue - (last mile + service + losses/fraud + support)
  - [ ] Pricing experiments framework created
  - [ ] Decision thresholds documented (no expansion for categories with sustained direct losses)
- **KPI References**:
  - Direct contribution margin: Positive per category
  - CAC vs LTV: Healthy ratio
  - Margin per order: Target thresholds
- **Source**: [`docs/notion-export/05-revenue-model.md`](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/05-revenue-model.md), [`docs/notion-export/12-economics.md`](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/12-economics.md)
- **Related Issues**: #1, #3

### PHASE 1 Issues (Foundation)

#### Issue #11: Setup Core Platform Infrastructure
- **Labels**: `phase:1-foundation`, `type:infrastructure`, `priority:critical`, `domain:platform`
- **Milestone**: PHASE 1
- **Description**: Set up foundational infrastructure and development environment
- **Acceptance Criteria**:
  - [ ] CI/CD pipeline configured
  - [ ] Development, staging, production environments set up
  - [ ] Observability stack deployed (logs, metrics, traces)
  - [ ] Security baseline implemented (encryption, secrets management, environment separation)
  - [ ] Feature flag system operational
- **KPI References**:
  - Deployment success rate: ≥99%
  - Environment uptime: ≥99.9%
  - Security audit: 0 critical findings
- **Source**: [`docs/notion-export/10-technology-principles.md`](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/10-technology-principles.md)
- **Related Issues**: #8

#### Issue #12: Implement Catalog Domain
- **Labels**: `phase:1-foundation`, `type:feature`, `priority:high`, `domain:catalog`
- **Milestone**: PHASE 1
- **Description**: Build catalog management system for products and services
- **Acceptance Criteria**:
  - [ ] Product catalog schema designed
  - [ ] Category management implemented
  - [ ] Product attributes and metadata support
  - [ ] Search and filtering capabilities
  - [ ] Multi-language support foundation
- **KPI References**:
  - Catalog completeness: 100% for pilot categories
  - Search relevance: User satisfaction metrics
- **Source**: [`docs/notion-export/03-platform-scope.md`](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/03-platform-scope.md)
- **Related Issues**: #4

#### Issue #13: Implement Inventory Domain
- **Labels**: `phase:1-foundation`, `type:feature`, `priority:high`, `domain:inventory`
- **Milestone**: PHASE 1
- **Description**: Build inventory tracking and availability system
- **Acceptance Criteria**:
  - [ ] Real-time inventory tracking
  - [ ] Stock availability checks
  - [ ] Reservation system for orders
  - [ ] Inventory accuracy monitoring
  - [ ] Partner inventory integration foundation
- **KPI References**:
  - [Inventory accuracy](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/13-measurement-dictionary.md#L7): Target ≥95%
- **Source**: [`docs/notion-export/03-platform-scope.md`](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/03-platform-scope.md)
- **Related Issues**: #4, #12

#### Issue #14: Implement Ordering Domain
- **Labels**: `phase:1-foundation`, `type:feature`, `priority:critical`, `domain:ordering`
- **Milestone**: PHASE 1
- **Description**: Build order capture and orchestration system
- **Acceptance Criteria**:
  - [ ] Order creation and validation
  - [ ] Shopping cart management
  - [ ] Order state machine implemented
  - [ ] Order event streaming
  - [ ] Order history and tracking
- **KPI References**:
  - Order placement success rate: ≥99%
  - Order processing time: Target SLA
- **Source**: [`docs/notion-export/04-product-interfaces.md`](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/04-product-interfaces.md)
- **Related Issues**: #12, #13

#### Issue #15: Implement Fulfillment Domain
- **Labels**: `phase:1-foundation`, `type:feature`, `priority:critical`, `domain:fulfillment`
- **Milestone**: PHASE 1
- **Description**: Build fulfillment and picking system
- **Acceptance Criteria**:
  - [ ] Picking workflow implemented
  - [ ] Substitution logic
  - [ ] Order splitting and batching
  - [ ] Quality checks integration
  - [ ] Staging and handoff to delivery
- **KPI References**:
  - Fulfillment SLA: Target pick-to-ready time
  - Substitution acceptance rate: Target %
- **Source**: [`docs/notion-export/04-product-interfaces.md`](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/04-product-interfaces.md), [`docs/notion-export/09-operating-pack-template.md`](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/09-operating-pack-template.md)
- **Related Issues**: #14

#### Issue #16: Implement Routing and Delivery Domain
- **Labels**: `phase:1-foundation`, `type:feature`, `priority:high`, `domain:routing`
- **Milestone**: PHASE 1
- **Description**: Build route optimization and delivery tracking system
- **Acceptance Criteria**:
  - [ ] Zone management
  - [ ] Route optimization algorithms
  - [ ] ETA calculation
  - [ ] Live tracking
  - [ ] Proof of delivery (POD)
- **KPI References**:
  - [On-time delivery ≥95%](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/07-metrics-and-gates.md#L3)
  - Delivery cost per order: Target threshold
  - ETA accuracy: Target %
- **Source**: [`docs/notion-export/04-product-interfaces.md`](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/04-product-interfaces.md), [`docs/notion-export/10-technology-principles.md`](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/10-technology-principles.md)
- **Related Issues**: #15

#### Issue #17: Implement Partner Management Domain
- **Labels**: `phase:1-foundation`, `type:feature`, `priority:high`, `domain:partner`
- **Milestone**: PHASE 1
- **Description**: Build partner onboarding and management system
- **Acceptance Criteria**:
  - [ ] Partner onboarding workflow
  - [ ] KYB (Know Your Business) verification
  - [ ] Partner dashboard foundation
  - [ ] Catalog and inventory integration
  - [ ] Settlement foundation
- **KPI References**:
  - Partner onboarding time: Target days
  - Partner quality score: Minimum threshold
- **Source**: [`docs/notion-export/04-product-interfaces.md`](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/04-product-interfaces.md)
- **Related Issues**: #12, #13

#### Issue #18: Implement Workforce Management Domain
- **Labels**: `phase:1-foundation`, `type:feature`, `priority:high`, `domain:workforce`
- **Milestone**: PHASE 1
- **Description**: Build workforce and driver management system
- **Acceptance Criteria**:
  - [ ] Driver onboarding and verification
  - [ ] Assignment logic
  - [ ] Driver mobile app foundation
  - [ ] Performance tracking
  - [ ] Incentive calculation foundation
- **KPI References**:
  - Driver quality score: Target threshold
  - Assignment efficiency: Target %
- **Source**: [`docs/notion-export/04-product-interfaces.md`](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/04-product-interfaces.md), [`docs/notion-export/11-operations-governance.md`](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/11-operations-governance.md)
- **Related Issues**: #16

### PHASE 2 Issues (MVP Launch)

#### Issue #19: Build Consumer Mobile App (MVP)
- **Labels**: `phase:2-mvp`, `type:feature`, `priority:critical`
- **Milestone**: PHASE 2
- **Description**: Build consumer-facing mobile application for iOS and Android
- **Acceptance Criteria**:
  - [ ] Browse catalog
  - [ ] Search and filter
  - [ ] Shopping cart
  - [ ] Checkout and payment
  - [ ] Order tracking
  - [ ] Support and disputes
- **KPI References**:
  - App rating: Target ≥4.0
  - Conversion rate: Target %
  - [CSAT ≥60](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/07-metrics-and-gates.md#L6)
- **Source**: [`docs/notion-export/04-product-interfaces.md`](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/04-product-interfaces.md)
- **Related Issues**: #12, #14

#### Issue #20: Build Partner Dashboard (MVP)
- **Labels**: `phase:2-mvp`, `type:feature`, `priority:high`, `domain:partner`
- **Milestone**: PHASE 2
- **Description**: Build partner dashboard for catalog, orders, and settlements
- **Acceptance Criteria**:
  - [ ] Catalog management UI
  - [ ] Inventory management UI
  - [ ] Order fulfillment workflow
  - [ ] Settlement reports
  - [ ] Performance metrics dashboard
- **KPI References**:
  - Partner adoption rate: Target %
  - Time to first order: Target hours
- **Source**: [`docs/notion-export/04-product-interfaces.md`](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/04-product-interfaces.md)
- **Related Issues**: #17

#### Issue #21: Build Workforce Mobile App (MVP)
- **Labels**: `phase:2-mvp`, `type:feature`, `priority:high`, `domain:workforce`
- **Milestone**: PHASE 2
- **Description**: Build driver/workforce mobile app for task management
- **Acceptance Criteria**:
  - [ ] Assignment notifications
  - [ ] Route navigation integration
  - [ ] POD capture (photo, signature)
  - [ ] Status updates
  - [ ] Earnings tracking
- **KPI References**:
  - Driver adoption rate: Target %
  - POD capture rate: 100%
- **Source**: [`docs/notion-export/04-product-interfaces.md`](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/04-product-interfaces.md)
- **Related Issues**: #18

#### Issue #22: Implement Payment Integration
- **Labels**: `phase:2-mvp`, `type:feature`, `priority:critical`
- **Milestone**: PHASE 2
- **Description**: Integrate payment gateway and implement payment flows
- **Acceptance Criteria**:
  - [ ] Payment gateway integration (credit/debit cards)
  - [ ] Digital wallet support
  - [ ] Cash on delivery option
  - [ ] Refund handling
  - [ ] Settlement automation for partners
- **KPI References**:
  - [Payment success ≥99%](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/07-metrics-and-gates.md#L4)
  - Refund processing time: Target SLA
- **Source**: [`docs/notion-export/04-product-interfaces.md`](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/04-product-interfaces.md)
- **Related Issues**: #14

#### Issue #23: Implement Notification System
- **Labels**: `phase:2-mvp`, `type:feature`, `priority:medium`
- **Milestone**: PHASE 2
- **Description**: Build multi-channel notification system
- **Acceptance Criteria**:
  - [ ] Email notifications
  - [ ] SMS notifications
  - [ ] Push notifications
  - [ ] Notification preferences
  - [ ] Template management
- **KPI References**:
  - Notification delivery rate: ≥99%
  - Opt-out rate: Below threshold
- **Source**: [`docs/notion-export/04-product-interfaces.md`](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/04-product-interfaces.md)
- **Related Issues**: #19

#### Issue #24: Implement Dispute and Support System
- **Labels**: `phase:2-mvp`, `type:feature`, `priority:high`
- **Milestone**: PHASE 2
- **Description**: Build dispute handling and customer support system
- **Acceptance Criteria**:
  - [ ] Support ticket creation
  - [ ] Dispute workflow with evidence
  - [ ] Refund processing
  - [ ] Support agent dashboard
  - [ ] SLA tracking
- **KPI References**:
  - First response time: Target SLA
  - Resolution time: Target SLA
  - Dispute resolution rate: Target %
- **Source**: [`docs/notion-export/04-product-interfaces.md`](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/04-product-interfaces.md)
- **Related Issues**: #19

#### Issue #25: Launch Pilot in City 1 with 2 Categories
- **Labels**: `phase:2-mvp`, `type:feature`, `priority:critical`, `gate:reliability`, `gate:economics`
- **Milestone**: PHASE 2
- **Description**: Execute pilot launch following 90-day plan
- **Acceptance Criteria**:
  - [ ] Operating zones defined
  - [ ] 2 categories launched (grocery + one other)
  - [ ] Partner network established (minimum 5 partners)
  - [ ] Driver pool recruited (minimum 10 drivers)
  - [ ] Week 7-10 pilot operations completed
  - [ ] All 4 gates validated (reliability, economics, trust, compliance)
- **KPI References**:
  - [On-time delivery ≥95%](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/07-metrics-and-gates.md#L3)
  - [Payment success ≥99%](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/07-metrics-and-gates.md#L4)
  - [Cancellation ≤5%](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/07-metrics-and-gates.md#L5)
  - [CSAT ≥60](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/07-metrics-and-gates.md#L6)
  - Direct contribution margin: Positive
- **Source**: [`docs/notion-export/08-90-day-city-launch-plan.md`](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/08-90-day-city-launch-plan.md)
- **Related Issues**: #5, #19, #20, #21

### PHASE 3 Issues (Scale & Optimize)

#### Issue #26: Expand to 5-7 Categories in City 1
- **Labels**: `phase:3-scale`, `type:feature`, `priority:high`, `category:cold-chain`, `category:regulated`
- **Milestone**: PHASE 3
- **Description**: Expand category coverage following operational pack patterns
- **Acceptance Criteria**:
  - [ ] Cold-chain category pack implemented (sensors, time limits)
  - [ ] Regulated category pack implemented (KYC, age verification, strong POD)
  - [ ] Service category pack implemented (scheduling, service pricing)
  - [ ] 5-7 categories operational
  - [ ] Category-specific KPIs tracked
- **KPI References**:
  - Direct contribution margin per category: Positive
  - Category adoption rate: Target %
- **Source**: [`docs/notion-export/03-platform-scope.md`](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/03-platform-scope.md)
- **Related Issues**: #4, #25

#### Issue #27: Implement Operational Analytics and Dashboards
- **Labels**: `phase:3-scale`, `type:feature`, `priority:high`, `domain:operations`
- **Milestone**: PHASE 3
- **Description**: Build comprehensive analytics and monitoring dashboards
- **Acceptance Criteria**:
  - [ ] Daily operations dashboard
  - [ ] Weekly unit economics dashboard
  - [ ] Monthly partner health dashboard
  - [ ] Real-time alerting system
  - [ ] Executive reporting
- **KPI References**:
  - Dashboard uptime: ≥99.9%
  - Data freshness: Real-time to daily as appropriate
  - Alert accuracy: Low false positive rate
- **Source**: [`docs/notion-export/13-measurement-dictionary.md`](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/13-measurement-dictionary.md)
- **Related Issues**: #6

#### Issue #28: Implement Fraud Detection System
- **Labels**: `phase:3-scale`, `type:security`, `priority:high`, `gate:trust`
- **Milestone**: PHASE 3
- **Description**: Build fraud detection and prevention system
- **Acceptance Criteria**:
  - [ ] Real-time fraud scoring
  - [ ] Anomaly detection
  - [ ] Manual review workflow
  - [ ] Blocklist management
  - [ ] Fraud reporting and analytics
- **KPI References**:
  - Fraud rate: Below threshold
  - False positive rate: Below threshold
- **Source**: [`docs/notion-export/06-risks-and-controls.md`](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/06-risks-and-controls.md)
- **Related Issues**: #7

#### Issue #29: Implement CAPA (Corrective and Preventive Actions) System
- **Labels**: `phase:3-scale`, `type:feature`, `priority:medium`, `domain:operations`
- **Milestone**: PHASE 3
- **Description**: Build CAPA tracking and management system
- **Acceptance Criteria**:
  - [ ] Incident logging
  - [ ] Root cause analysis workflow
  - [ ] Corrective action tracking
  - [ ] Preventive measure implementation
  - [ ] Effectiveness review
- **KPI References**:
  - CAPA closure rate: Target %
  - Recurring incident rate: Decreasing trend
- **Source**: [`docs/notion-export/09-operating-pack-template.md`](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/09-operating-pack-template.md), [`docs/notion-export/11-operations-governance.md`](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/11-operations-governance.md)
- **Related Issues**: #9

#### Issue #30: Launch City 2
- **Labels**: `phase:3-scale`, `type:feature`, `priority:high`, `gate:reliability`, `gate:economics`
- **Milestone**: PHASE 3
- **Description**: Expand to second city in same country
- **Acceptance Criteria**:
  - [ ] City selection criteria applied
  - [ ] Operating zones defined
  - [ ] Partner network established
  - [ ] Pilot execution (2 categories initially)
  - [ ] All 4 gates validated
  - [ ] Expansion to 5-7 categories
- **KPI References**:
  - Time to launch: Target days from decision
  - Same KPIs as City 1 (on-time, payment success, cancellation, CSAT)
- **Source**: [`docs/notion-export/08-90-day-city-launch-plan.md`](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/08-90-day-city-launch-plan.md), [`docs/notion-export/02-target-market.md`](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/02-target-market.md)
- **Related Issues**: #25

### PHASE 4 Issues (Global Expansion)

#### Issue #31: Implement Multi-Country Policy Engine
- **Labels**: `phase:4-global`, `type:feature`, `priority:critical`, `domain:compliance`
- **Milestone**: PHASE 4
- **Description**: Build configurable policy engine for multi-country compliance
- **Acceptance Criteria**:
  - [ ] Policy configuration framework
  - [ ] Country-specific rule engine
  - [ ] Category restrictions by country
  - [ ] Age verification rules
  - [ ] License and permit checking
- **KPI References**:
  - Policy compliance rate: 100%
  - Configuration errors: 0
- **Source**: [`docs/notion-export/06-risks-and-controls.md`](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/06-risks-and-controls.md)
- **Related Issues**: #7

#### Issue #32: Implement Multi-Currency and Tax Engine
- **Labels**: `phase:4-global`, `type:feature`, `priority:high`
- **Milestone**: PHASE 4
- **Description**: Support multiple currencies and tax regimes
- **Acceptance Criteria**:
  - [ ] Multi-currency support
  - [ ] Exchange rate management
  - [ ] Country-specific tax calculation
  - [ ] Invoicing per country regulations
  - [ ] Financial reporting per country
- **KPI References**:
  - Tax calculation accuracy: 100%
  - Invoice compliance: 100%
- **Source**: [`docs/notion-export/12-economics.md`](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/12-economics.md)
- **Related Issues**: #10

#### Issue #33: Implement Localization Framework
- **Labels**: `phase:4-global`, `type:feature`, `priority:high`
- **Milestone**: PHASE 4
- **Description**: Build comprehensive localization support
- **Acceptance Criteria**:
  - [ ] Multi-language UI support
  - [ ] RTL (Right-to-Left) language support
  - [ ] Locale-specific date/time/number formatting
  - [ ] Translation management system
  - [ ] Country-specific content
- **KPI References**:
  - Translation coverage: 100% for supported languages
  - Localization defects: Below threshold
- **Source**: [`docs/notion-export/03-platform-scope.md`](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/03-platform-scope.md)
- **Related Issues**: #12

#### Issue #34: Implement Data Governance and Privacy Framework
- **Labels**: `phase:4-global`, `type:compliance-task`, `priority:critical`, `domain:compliance`
- **Milestone**: PHASE 4
- **Description**: Implement comprehensive data governance for global operations
- **Acceptance Criteria**:
  - [ ] Data classification system
  - [ ] Role-based access control (RBAC)
  - [ ] Data retention policies per country
  - [ ] User consent management
  - [ ] Right to deletion (with regulatory exceptions)
  - [ ] Audit trail for all data access
- **KPI References**:
  - Data breach incidents: 0
  - Privacy compliance audit: Pass
  - GDPR/local privacy law compliance: 100%
- **Source**: [`docs/notion-export/06-risks-and-controls.md`](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/06-risks-and-controls.md)
- **Related Issues**: #7, #31

#### Issue #35: Launch Country 2
- **Labels**: `phase:4-global`, `type:feature`, `priority:critical`, `gate:compliance`
- **Milestone**: PHASE 4
- **Description**: Expand to second country
- **Acceptance Criteria**:
  - [ ] Country selection criteria applied
  - [ ] Policy engine configured for country
  - [ ] Payment and tax integration completed
  - [ ] Localization completed
  - [ ] Compliance documentation ready
  - [ ] City 1 in country 2 launched
  - [ ] All 4 gates validated
- **KPI References**:
  - Time to country launch: Target months
  - Compliance violations: 0 critical
  - Same operational KPIs as previous launches
- **Source**: [`docs/notion-export/08-90-day-city-launch-plan.md`](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/08-90-day-city-launch-plan.md)
- **Related Issues**: #31, #32, #33, #34

#### Issue #36: Implement B2B Module
- **Labels**: `phase:4-global`, `type:feature`, `priority:medium`, `category:b2b`
- **Milestone**: PHASE 4
- **Description**: Build B2B ordering and fulfillment capabilities
- **Acceptance Criteria**:
  - [ ] Corporate account management
  - [ ] Recurring order contracts
  - [ ] SLA agreements
  - [ ] Invoicing and payment terms
  - [ ] B2B analytics dashboard
- **KPI References**:
  - B2B customer acquisition: Target count
  - Contract renewal rate: Target %
  - B2B order volume: Target growth
- **Source**: [`docs/notion-export/03-platform-scope.md`](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/03-platform-scope.md)
- **Related Issues**: #4

### Cross-Cutting Issues

#### Issue #37: Document All ADRs (Architecture Decision Records)
- **Labels**: `phase:1-foundation`, `type:architecture`, `priority:medium`, `domain:platform`
- **Milestone**: PHASE 1
- **Description**: Create ADRs for all major architectural decisions
- **Acceptance Criteria**:
  - [ ] ADR template created
  - [ ] ADRs for: domain boundaries, event system, data storage, API design, security model
  - [ ] ADR review process established
  - [ ] ADRs published and accessible to team
- **KPI References**:
  - ADR coverage: All major decisions documented
- **Source**: [`docs/notion-export/10-technology-principles.md`](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/10-technology-principles.md)
- **Related Issues**: #8

#### Issue #38: Setup Continuous Integration and Testing
- **Labels**: `phase:1-foundation`, `type:infrastructure`, `priority:high`, `domain:platform`
- **Milestone**: PHASE 1
- **Description**: Establish CI/CD pipeline and testing practices
- **Acceptance Criteria**:
  - [ ] CI pipeline for automated testing
  - [ ] Code coverage tracking
  - [ ] Automated security scanning
  - [ ] Performance testing framework
  - [ ] Release train process
- **KPI References**:
  - Test coverage: Target % per domain
  - CI success rate: ≥95%
  - Deployment frequency: Target per week
- **Source**: [`docs/notion-export/10-technology-principles.md`](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/10-technology-principles.md)
- **Related Issues**: #11

#### Issue #39: Implement Improvement Loop Process
- **Labels**: `phase:2-mvp`, `type:documentation`, `priority:medium`, `domain:operations`
- **Milestone**: PHASE 2
- **Description**: Establish continuous improvement process
- **Acceptance Criteria**:
  - [ ] Experiment log template
  - [ ] Decision template
  - [ ] Change log
  - [ ] Weekly cycle: hypothesis → experiment → result → decision
  - [ ] Rollback plan for all changes
- **KPI References**:
  - Experiment success rate: Target %
  - Time from hypothesis to decision: Target days
- **Source**: [`docs/notion-export/15-improvement-loop.md`](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/15-improvement-loop.md)
- **Related Issues**: #9

#### Issue #40: Close Critical Gaps from Gap Analysis
- **Labels**: `phase:2-mvp`, `type:feature`, `priority:high`
- **Milestone**: PHASE 2
- **Description**: Address critical gaps identified in Notion export
- **Acceptance Criteria**:
  - [ ] Gap matrix created
  - [ ] Owners assigned
  - [ ] Target dates set
  - [ ] Gaps closed with measurable KPI impact
- **KPI References**:
  - Gap closure rate: 100% of critical gaps
  - Time to close: Target days
- **Source**: [`docs/notion-export/16-gaps-and-closures.md`](https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/16-gaps-and-closures.md)
- **Related Issues**: #3, #5

---

## 5. Automation Scripts

### scripts/planning/bootstrap_github.sh

Bash script using `gh` CLI to create labels, milestones, and issues.

**Features**:
- Idempotent (checks existence before creating)
- Creates all labels from taxonomy
- Creates all milestones
- Creates all issues with full traceability
- Links issues to milestones and labels
- Prints summary with GitHub URLs

**Usage**:
```bash
export GH_TOKEN=<your-github-token>
export GITHUB_REPOSITORY=Abuzhor/smart-grocery-logistics-platform
./scripts/planning/bootstrap_github.sh
```

### scripts/planning/bootstrap_github.py

Python script using GitHub GraphQL API to create Projects v2 board.

**Features**:
- Creates project board
- Configures custom fields (Phase, Domain, Priority, Gate Criteria, Notion Reference)
- Creates status columns (Backlog, Ready, In Progress, Review, Blocked, Done)
- Adds all created issues to project
- Sets initial status and field values

**Usage**:
```bash
export GH_TOKEN=<your-github-token>
python3 scripts/planning/bootstrap_github.py
```

---

## 6. Traceability Matrix

All issues include:

1. **Direct Notion Export Links**: GitHub blob URLs with line anchors to exact source sections
2. **KPI References**: Links to specific metrics in measurement dictionary and gates document
3. **Acceptance Criteria**: Clear, testable criteria for issue completion
4. **Cross-Links**: Related issues referenced by number
5. **Labels**: Phase, domain, type, priority, and gate labels for filtering
6. **Milestones**: Associated with appropriate phase milestone

**Example Traceability Flow**:
```
Issue #3 (Define Vision and North Star Metrics)
  ↓ References
docs/notion-export/01-vision-and-goals.md
docs/notion-export/07-metrics-and-gates.md (lines 3-6)
  ↓ Defines KPIs
On-time delivery ≥95%
Payment success ≥99%
Cancellation ≤5%
CSAT ≥60
  ↓ Used by
Issue #25 (Launch Pilot) - validates these KPIs
Issue #27 (Analytics Dashboard) - tracks these KPIs
```

---

## 7. Execution Checklist

- [ ] Create all labels via `bootstrap_github.sh`
- [ ] Create all milestones via `bootstrap_github.sh`
- [ ] Create meta issue #1
- [ ] Create all PHASE 0 issues (#2-10)
- [ ] Create all PHASE 1 issues (#11-18)
- [ ] Create all PHASE 2 issues (#19-25)
- [ ] Create all PHASE 3 issues (#26-30)
- [ ] Create all PHASE 4 issues (#31-36)
- [ ] Create cross-cutting issues (#37-40)
- [ ] Create Projects v2 board via `bootstrap_github.py`
- [ ] Add all issues to project board
- [ ] Set initial status to "Backlog" for all issues
- [ ] Set custom field values (Phase, Domain, Priority, etc.)
- [ ] Validate all links are working
- [ ] Verify traceability from issues to Notion export
- [ ] Update meta issue #1 with completion status

---

## 8. Success Criteria

This PHASE 0 execution is complete when:

1. ✅ All 6 label categories (phase, domain, type, priority, category, gate) created
2. ✅ All 5 milestones created (PHASE 0-4)
3. ✅ All 40 issues created with complete traceability
4. ✅ Projects v2 board created with 6 status columns
5. ✅ All issues added to project board
6. ✅ Custom fields configured and populated
7. ✅ All Notion export references are valid GitHub blob URLs
8. ✅ All KPI references link to specific lines in measurement documents
9. ✅ Scripts are idempotent and can be re-run safely
10. ✅ Documentation is clear and maintainable

---

## 9. Maintenance

### Adding New Issues
1. Add issue mapping to this document
2. Run `bootstrap_github.sh` to create the issue
3. Run `bootstrap_github.py` to add to project board
4. Update meta issue #1 checklist

### Updating Labels or Milestones
1. Update taxonomy in this document
2. Modify scripts with new definitions
3. Re-run scripts (idempotent)

### Notion Export Updates
1. Update `docs/notion-export/**` files
2. Review and update issue mappings in this document
3. Update affected issues manually or via script

---

**Document Version**: 1.0  
**Last Updated**: 2026-01-08  
**Maintained By**: PHASE 0 Execution Team

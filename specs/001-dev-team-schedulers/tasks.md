# Tasks: Development Team Automation Tool

**Input**: Design documents from `/specs/001-dev-team-schedulers/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/, research.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize backend and frontend projects.

- [x] T001 [P] Initialize FastAPI backend project in `backend/`
- [x] T002 [P] Initialize React/Vite frontend project in `frontend/`
- [x] T003 [P] Configure backend linting (e.g., ruff, black) in `backend/`
- [x] T004 [P] Configure frontend linting (e.g., ESLint, Prettier) in `frontend/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure needed for all user stories.

### Backend
- [x] T005 Create GCS client service for config management in `backend/src/services/gcs_service.py`
- [x] T006 Write unit tests for GCS client service in `backend/tests/unit/test_gcs_service.py`
- [x] T007 Implement Pydantic models for all entities from `data-model.md` in `backend/src/models/config.py`
- [x] T008 Implement main FastAPI app (`main.py`) with basic error handling middleware in `backend/src/`
- [x] T009 Create a config service to load and access config in `backend/src/services/config_service.py`

### Frontend
- [x] T010 [P] Set up basic project structure (pages, components folders) in `frontend/src/`
- [x] T011 [P] Implement a basic API client service to communicate with the backend in `frontend/src/services/api.ts`
- [x] T012 [P] Set up basic routing (e.g., with React Router) in `frontend/src/App.tsx`
- [x] T013 Set up basic layout/chrome for the admin UI in `frontend/src/components/Layout.tsx`

---

## Phase 3: User Story 1 - Automate Confluence Weekly Report Creation (Priority: P1) 🎯 MVP

**Goal**: Automatically generate the weekly report draft on Confluence every Monday.
**Independent Test**: Trigger the scheduler and verify the Confluence page is created and a Slack message is sent.

### Tests for User Story 1
- [x] T014 [US1] Write contract test for `POST /schedule/confluence-weekly-report` endpoint in `backend/tests/contract/test_schedule_api.py`
- [x] T015 [US1] Write unit test for the Confluence service logic in `backend/tests/unit/test_confluence_service.py`

### Implementation for User Story 1
- [x] T016 [US1] Implement Confluence API client in `backend/src/services/confluence_client.py`
- [x] T017 [US1] Implement Slack notification service in `backend/src/services/slack_service.py`
- [x] T018 [US1] Implement the core logic for the Confluence report creation in `backend/src/services/confluence_service.py`
- [x] T019 [US1] Create the `POST /schedule/confluence-weekly-report` API endpoint in `backend/src/api/schedule.py`

---

## Phase 4: User Story 4 - Web Admin for Configuration (Priority: P1)

**Goal**: Provide a web UI for administrators to manage job configurations.
**Independent Test**: An admin can open the web UI, modify a setting, save it, and see the changes persist on reload.

### Tests for User Story 4
- [x] T020 [P] [US4] Write contract tests for `GET` and `PUT` `/api/config` endpoints in `backend/tests/contract/test_config_api.py`
- [x] T021 [P] [US4] Write component tests for the Confluence config form in `frontend/src/components/ConfluenceForm.test.tsx`
- [x] T022 [P] [US4] Write component tests for the On-Call config form in `frontend/src/components/OnCallForm.test.tsx`
- [x] T023 [P] [US4] Write component tests for the On-Call roster management UI in `frontend/src/components/OnCallRoster.test.tsx`

### Implementation for User Story 4
#### Backend
- [x] T024 [US4] Implement `GET /api/config` endpoint in `backend/src/api/config.py`
- [x] T025 [US4] Implement `PUT /api/config` endpoint in `backend/src/api/config.py`

#### Frontend
- [x] T026 [US4] Create main admin page component in `frontend/src/pages/AdminPage.tsx`
- [x] T027 [P] [US4] Create form component for Confluence settings in `frontend/src/components/ConfluenceForm.tsx`
- [x] T028 [P] [US4] Create form component for On-Call settings in `frontend/src/components/OnCallForm.tsx`
- [x] T029 [P] [US4] Create component for managing the on-call roster list in `frontend/src/components/OnCallRoster.tsx`
- [x] T030 [US4] Implement state management (e.g., React Context or Zustand) for config data in `frontend/src/`

---

## Phase 5: User Story 3 - Automate On-Call Duty Notifications (Priority: P2)

**Goal**: Announce the weekly on-call person in Slack every Friday.
**Independent Test**: Trigger the scheduler and verify the correct user is @-mentioned in Slack and the channel topic is updated.

### Tests for User Story 3
- [x] T031 [P] [US3] Write contract test for `POST /schedule/on-call-notification` endpoint in `backend/tests/contract/test_schedule_api.py`
- [x] T032 [US3] Write unit test for the on-call notification service logic in `backend/tests/unit/test_oncall_service.py`

### Implementation for User Story 3
- [x] T033 [US3] Implement the core logic for determining the on-call person and sending the notification in `backend/src/services/oncall_service.py`
- [x] T034 [US3] Create the `POST /schedule/on-call-notification` API endpoint in `backend/src/api/schedule.py`

---

## Phase N: Polish & Cross-Cutting Concerns

- [x] T035 [P] Add comprehensive README files for both `backend/` and `frontend/`
- [ ] T036 [P] Set up CI/CD pipelines for automated testing and deployment to GCP.
- [ ] T037 [P] Refine error handling and logging across all services.
- [ ] T038 Review and validate all configuration options and UI components for usability.

---

## Dependencies & Execution Order

- **Phase 1 (Setup)** must be complete before any other phase.
- **Phase 2 (Foundational)** must be complete before any user story phases (3, 4, 5).
- **User Stories (Phases 3, 4, 5)** can technically be worked on in parallel after Phase 2 is complete, but the recommended order is by priority: Phase 3 (US1) & Phase 4 (US4) -> Phase 5 (US3).
- **Phase 4 (Admin UI)** is a prerequisite for users to easily manage the other features.

### Implementation Strategy

#### MVP First (User Story 1 & 4)

1.  Complete Phase 1: Setup
2.  Complete Phase 2: Foundational
3.  Complete Phase 3 (US1) and Phase 4 (US4).
4.  **STOP and VALIDATE**: At this point, the core functionality (Confluence automation) and its configuration are complete. This is a deployable MVP.

#### Incremental Delivery

1.  Deploy the MVP (US1 + US4).
2.  Add User Story 3 (On-call notifications).
3.  Deploy the updated version.

# Feature Specification: Development Team Automation Tool

**Feature Branch**: `001-dev-team-schedulers`
**Created**: 2026-01-01
**Status**: Draft
**Input**: User description: "我需要建立一個開發團隊輔助工具，我需要建立三個排程，描述如下 1. 第一個排程：可對 Confluence 上的文件做讀寫，並建立一個排程於每週一早上 10 點做以下兩個動作 a. 讀取指定 Confluence 週報文件，並 clone 一份完整的內容，標題 Pattern 是 「2025 W52 技術部 RD4 團隊週報 (1222-1226)」每次 clone 時要調整為符合當週的週一至週五的日期，年份也要檢查，複製完後放到相同的資料夾下，同時也要考慮西元年份的調整，若跨年就要另開新的年份的資料夾，把 clone 的文件放在該資料夾下 b. 文件建立完成後要發 slack 通知到指定 slack channel 2. 第二個排程：於每週一早上 9:00 對一個指定的 Jira Spce 上的 Sprint 做 complete 以及另一個 Sprint 做 start 的動作 3. 第三個排程：於每週五 18:00 對指定 slack channel 做通知當週的值班人員，且需要 @ 該值班人員的 slack use id，以及更新該 channel 的 Description 欄位 除了排程我還需要建立一個網頁管理後台，管理上述排程的參數管理，例如 1. 第一個排程的參數管理包含要通知的 slack channel 設定以及要 clone 的 Confluence 網址 2. 第二個排程的參數管理包含要通知的 slack channel 以及 Jira URL 3. 第三個排程的參數管理包含要通知的 slack channel，以及需要一個後台讓我儲存管理所有值班人員的排班順序以及他們的 slack user id，確保我可以通知到值班人員"

## User Scenarios & Testing *(mandatory)*

## Clarifications

### Session 2026-01-01
- Q: What is the logic for the on-call rotation? → A: Weekly rotation, shifting Friday 18:00, with 5 personnel.

---



### User Story 1 - Automate Confluence Weekly Report Creation (Priority: P1)

As a team manager, I want to automatically generate the weekly report draft on Confluence every Monday morning so that my team can fill it out without the manual setup.

**Why this priority**: This is a frequent, repetitive task that consumes manual effort every week. Automating it provides immediate time savings.

**Independent Test**: The system can be triggered for a specific date, and it should correctly create a new Confluence page with the right title and content in the specified location, and then send a Slack notification.

**Acceptance Scenarios**:

1.  **Given** it's Monday at 10:00 AM, **When** the scheduler runs, **Then** a new Confluence page is created by cloning the previous week's report.
2.  **Given** the new page is created, **When** the title is generated, **Then** it must follow the pattern "YYYY W## TEAM_NAME 週報 (MMDD-MMDD)" with the correct year, week number, and dates for the current week.
3.  **Given** the scheduler runs on the first week of a new year, **When** the page is created, **Then** a new parent folder for the new year is created in Confluence and the page is placed within it.
4.  **Given** the page is successfully created, **When** the process finishes, **Then** a notification is sent to the configured Slack channel.



---

### User Story 3 - Automate On-Call Duty Notifications (Priority: P2)

As a team lead, I want the system to automatically announce the on-call person for the week in Slack every Friday evening to ensure the team knows who is responsible for weekend support.

**Why this priority**: This keeps the team informed and ensures a smooth hand-off for on-call responsibilities.

**Independent Test**: The system can be triggered for a specific date, and it should correctly identify the on-call person from the schedule, @-mention them in the correct Slack channel, and update the channel description.

**Acceptance Scenarios**:

1.  **Given** it's Friday at 18:00, **When** the scheduler runs, **Then** it identifies the correct on-call person for the upcoming week from the stored rotation schedule.
2.  **Given** the on-call person is identified, **When** the notification is sent, **Then** it must contain an @-mention using the person's Slack User ID.
3.  **Given** the notification is sent, **When** the process continues, **Then** the description of the specified Slack channel is updated to include the name of the current on-call person.

---

### User Story 4 - Web Admin for Configuration (Priority: P1)

As an administrator, I need a web-based backend to manage the settings for all the automated jobs so I can easily update parameters without changing code.

**Why this priority**: The automation is not usable without a way to configure it. This is essential for the operation of all other user stories.

**Independent Test**: The admin can log in, view, update, and save the configuration for each of the three schedulers.

**Acceptance Scenarios**:

1.  **Given** an admin is on the web backend, **When** they navigate to the Confluence scheduler settings, **Then** they can view and update the target Confluence URL and the Slack notification channel.

3.  **Given** an admin is on the web backend, **When** they navigate to the On-call scheduler settings, **Then** they can view and update the Slack notification channel.
4.  **Given** an admin is on the web backend, **When** they navigate to the on-call roster page, **Then** they can add, remove, and re-order the list of on-call personnel and their corresponding Slack User IDs.

### Edge Cases

- **Confluence/Slack APIs are down**: The system must handle API failures gracefully, log the error, and send a failure notification to a designated admin channel.
- **Invalid configuration**: If a URL, channel name, or other parameter is incorrect, the job should fail with a clear error message.
- **Permissions issues**: The tool might lack the necessary permissions in Confluence, Jira, or Slack. These errors must be caught and reported.
- **No on-call person scheduled**: If the on-call rotation is empty, the Friday notification should report this error instead of failing silently.
- **Time zone differences**: All scheduled times must be configurable to a specific time zone to avoid ambiguity.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST provide a mechanism to schedule three distinct jobs at specified times.
- **FR-002**: **Job 1 (Confluence)**: The system MUST be able to connect to a Confluence instance, read a specified page, and create a new page with modified content and title.
- **FR-003**: **Job 1 (Confluence)**: The system MUST correctly calculate the current week's year, week number, and day range for the new page title. It must handle year-end transitions by creating new parent folders.

- **FR-006**: **Job 3 (On-call)**: The system MUST be able to send a message to a Slack channel that includes a user-specific @-mention.
- **FR-007**: **Job 3 (On-call)**: The system MUST be able to update a Slack channel's description field.
- **FR-008**: **Job 3 (On-call)**: The system MUST determine the correct on-call person based on a stored schedule. The rotation is weekly, shifting on Friday at 18:00, among five on-call personnel.
- **FR-009**: **Admin UI**: The system MUST provide a secure web interface for managing job parameters for Confluence and On-call schedulers.
- **FR-010**: **Admin UI**: The system MUST allow administrators to manage a list of personnel, including their names and Slack User IDs, for the on-call rotation.

### Key Entities *(include if feature involves data)*

- **SchedulerJob**: Represents one of the three automated jobs, containing its schedule (cron string), type (Confluence, Jira, On-call), and associated parameters.
- **Configuration**: A set of key-value pairs for job parameters, such as `confluence_url`, `slack_channel_id`.
- **OnCallPerson**: Represents a team member in the on-call schedule, containing their name and `slack_user_id`.
- **OnCallSchedule**: An ordered list or sequence of `OnCallPerson` objects that defines the rotation.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Reduce manual effort for weekly report creation from ~15 minutes to zero.

- **SC-003**: Achieve a 100% notification rate for the correct on-call person each week.
- **SC-004**: An administrator must be able to update any job parameter via the web UI in under 2 minutes.
- **SC-005**: The system's scheduled jobs must have a success rate of over 99%, with failures properly logged and reported.
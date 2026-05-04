# Custom Link Shortener Project

A streamlined URL shortening platform designed for efficient link management, user monetization, and simplified administration.

## 📌 Project Overview
Our goal is to build a new, custom script that leverages existing management logic while introducing a specialized frontend and ad-revenue workflow by modifying existing adlinkfly 

### Core Functions
* **Management:** Use established logic to manage users, links, statistics, and core data features.
* 
## 💰 Monetization Workflow (How it Works)
The platform follows a straightforward path for users to generate revenue:
1.  **Shorten:** User generates a shortened link.
2.  **Share:** User shares the link on their platform.
3.  **Click:** A visitor clicks the link.
4.  **Safe-Link:** The visitor is forwarded to a "SafeLink" blog site where ads are displayed.
5.  **Destination:** The visitor receives the final destination link.
6.  **Payout:** Admin earns revenue; the user who shortened the link is paid based on a **CPM (Cost Per Mille)** model.

---

## 🛠️ UI/UX Redesign Plans

### 1. Member Dashboard (`/member/dashboard`)
We are refining the user experience by simplifying the dashboard:
* **Keep existing core features** to maintain familiarity.
* **Remove Referral Earnings** functionality.
* **Remove Route:** Access to `/member/users/referrals` will be disabled completely

### 2. Public Home Page (site.com/)
The home page will be redesigned to focus on four primary navigation points:
* **Home:** General landing page.
* **Publisher Rates:** Transparent payout information.
* **Portal:** Unified Login/Signup/Dashboard access.

---

## 📊 Payout Structure (Publisher Rates)
Publisher rates represent the amount paid to users for every **1,000 views** generated on their links.

* **Fixed Rates:** Unlike complex scripts with multiple formats, we will implement a **single, unified publisher rate** across the site for clarity.
* **Example:** * **United States:** $2.00 per 1,000 views.

---

# Site Navigation & Routing Map

This document defines the URL structure and the primary navigation menu layout for the frontend.

## 🛣️ Page Routes

The following table maps the site pages to their respective application routes:

| Page Name          | Endpoint Route         |
| :----------------- | :--------------------- |
| **Home** | `/`                    |
| **Dashboard** | `/member/dashboard`    |
| **Login** | `/auth/signin`         |
| **Signup** | `/auth/signup`         |
| **Privacy Policy** | `/pages/privacy`       |
| **Terms of Use** | `/pages/terms`         |
| **DMCA** | `/pages/dmca`          |
| **Publisher Rates**| `/pages/payout-rates`  |

---

## 📱 Menu Structure

The navigation menu is designed to be clean, with essential links visible and legal pages grouped into a dropdown.

### Primary Links
* **Home**
* **Publishers Rates**
* **Dashboard** (Toggle: Show **Login/Signup** if the user is not authenticated)

### "Important Pages" Dropdown
To simplify the UI, the following pages are combined into a single menu button:
* **Terms of Use**
* **Privacy Policy**
* **DMCA**
* *Dynamic Links:* Any additional pages created via the **Admin Panel**.

---

## 🛠️ Development Notes
* **Blog System:** The blog system has been deprecated and should be removed from the code (No longer needed).
* **Route Grouping:** All legal/informational pages are nested under the `/pages/` prefix for better organization.

# Admin Panel & Backend Configuration

This section outlines the refinements for the administrative interface, focusing on core functionality while removing unnecessary complex features.

## 🖥️ Admin Dashboard Refinement (`/admin/dashboard`)

The dashboard is being simplified to prioritize essential platform statistics over secondary data.

### Features to Remove:
* **Owner Earnings:** Hide/Remove tracking for owner-specific revenue.
* **Referral Earnings:** Remove all referral-related data points.

### Statistics Logic:
* Statistics should represent a global view of all users.
* **Combined View:** Integrate **Publisher Earnings** and **Total Views** into a unified statistical overview that covers the entire user base.

---

## 🔗 Link Management (`/admin/links`)

We are maintaining the primary link oversight while keeping the interface clean.

* **Active Links:** Keep `/admin/links` as the primary management hub.
* **Hidden/Inactive Links:** Retain `/admin/links/hidden` and `/admin/links/inactive` for administrative control and moderation.

---

## 💸 Payout & Ad Format Restructuring

We are deprecating the old multi-format payout system in favor of a single, streamlined ad model.

### Route Cleanup:
The following routes are to be **removed**:
* `/admin/options/payout-interstitial`
* `/admin/options/payout-banner`
* `/admin/options/payout-popup`

### New Logic:
* **Single Ad Format:** The platform will utilize only **one single type of ad format**.
* **Fixed Selection:** Ad types will no longer be "selectable" by users; the system will enforce a global format for all.

---

## 👥 User & Withdrawal Management

Streamlining how users are handled and how payments are distributed.

### Withdrawals:
* **Keep as is:** Retain `/admin/withdraws` and `/admin/withdraws/export` for processing payments.

### User Routes:
* **Keep:** `/admin/users` (Primary list) and `/admin/users/add` (or export) for user database management.
* **Remove:** `/admin/users/referrals` — As previously noted, the referral system is entirely removed from the project scope.


# Admin Feature Cleanup & System Settings

This document outlines the final removal of legacy modules and the configuration of the core system options.

## 🚫 Deprecated Modules (To Be Removed)

We are stripping away features that are not required for our current business model to ensure a lightweight and focused admin panel.

### 1. Plans & Invoices
* **Routes to Remove:** `/admin/plans` and `/admin/plans/add`.
* **Reasoning:** Since the platform will not be collecting money directly from publishers, these subscription/plan routes are obsolete.
* **Invoices:** All `/admin/invoices` routes are also unusable and should be removed.

### 2. Content & UI Management
* **Blog/Posts:** Remove `/admin/posts` and `/admin/posts/add` (Blog system deprecated).
* **Testimonials:** Remove the testimonials module.
* **Menu Manager:** Remove the custom menu manager.
* **System Options:** Remove `/admin/options/system`.

---

## 🛠️ Features to Retain

The following core modules will remain active to support site operations:

* **Static Pages:** Keep `/admin/pages` and `/admin/pages/add` to manage the "Important Pages" (Terms, Privacy, DMCA).
* **Announcements:** Keep the announcement system active for user communication.
* **Advanced Stats:** Keep `/admin/advanced/statistics`.

---

## ⚙️ System Options Configuration (`/admin/options/`)

We are simplifying the settings to keep the platform lean and reduce dependencies.

| Option Path | Action | Logic / Reason |
| :--- | :--- | :--- |
| `/admin/options/ads` | **REMOVE** | Ad management on the core script is no longer needed. |
| `/admin/options/social-login` | **REMOVE** | Keep login simple and native; social login is not required. |
| `/admin/options/payment` | **REMOVE** | No payments are being collected from users. |
| `/admin/options/withdraw` | **KEEP** | Necessary for managing publisher payouts. |
| `/admin/options/email` | **KEEP** | Required for system notifications and account recovery. |

---

## 📝 Final Development Note
The goal is a "Social-Free, Plan-Free" environment where the focus is entirely on link shortening and CPM-based payouts through the simplified withdrawal system.





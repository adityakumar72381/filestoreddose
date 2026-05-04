# MODIFICATION GUIDE: MEMBER DASHBOARD & CORE LOGIC

## 1. REMOVE REFERRAL SYSTEM (Member Side)
Goal: Eliminate all traces of referral earnings to keep the dashboard clean.

- FIND FILE: src/Template/Member/Dashboard/index.twig
  - ACTION: Locate the statistics widgets. Remove the <div> or box containing "Referral Earnings".
  - ACTION: Remove any progress bars or charts related to "Referral Views".

- FIND FILE: src/Template/Layout/member.twig (or sidebar.twig)
  - ACTION: Locate the navigation menu. Delete the <li> item for "Referrals" (/member/users/referrals).

- FIND FILE: src/Controller/Member/UsersController.php
  - ACTION: Find the 'referrals' function and comment it out or delete it to disable the route.

## 2. SIMPLIFY PUBLISHER RATES (General)
Goal: Replace complex multi-ad formats with a single fixed-rate system.

- FIND FILE: src/Template/Pages/payout_rates.twig
  - ACTION: Remove columns for "Banner", "Interstitial", and "Popup". 
  - ACTION: Create a single column titled "CPM Rate (per 1000 views)".
  - EXAMPLE: Set a fixed value row (e.g., United States -> $2.00).

- ADMIN PANEL CONFIGURATION:
  - Go to Settings -> Ad Types.
  - Disable all ad types except for the "Native/Direct" one that matches your safelink flow.

## 3. URL STRUCTURE & ROUTING
Goal: Clean up the URL paths for a "compressed" feel.

- HOME PAGE: Should only link to:
  - Home (/)
  - Publisher Rates (/payout-rates)
  - Login/Signup (If not authenticated)
  - Dashboard (/member/dashboard - If authenticated)

- BLOG REMOVAL: 
  - Delete or hide any "Blog" buttons in the navigation. 
  - The script should now only serve as a management tool for the external safelink blog.

## 4. STATISTICS CLEANUP
- ACTION: In the Dashboard Controller, modify the query to sum only "Publisher Earnings" and "Link Views". 
- ACTION: Set the "Referral Earnings" variable to 0 in the controller so no data is pulled from the database for referrals.


# MODIFICATION GUIDE: FRONTEND NAVIGATION & URL STRUCTURE

## 1. MENU RE-ORGANIZATION (Header/Navigation)
Goal: Create a clean, compressed menu with a dropdown for "Important Pages."

- FIND FILE: src/Template/Element/front_header.twig (or header.twig)
  - ACTION: Remove the existing "Blog" list item (<li>).
  - ACTION: Organize the main links as follows:
    1. Home -> /
    2. Publishers Rates -> /pages/payout-rates
    3. Dashboard (if logged in) -> /member/dashboard
    4. Login/Signup (if guest) -> /auth/signin & /auth/signup
  
- ACTION: Create a Dropdown Button titled "Important Pages"
  - Inside the dropdown, add links for:
    - Terms of Use -> /pages/terms
    - Privacy Policy -> /pages/privacy
    - DMCA -> /pages/dmca
    - Dynamic Pages: Ensure the code for "other pages from admin panel" remains inside this dropdown loop.

## 2. BLOG SYSTEM REMOVAL
Goal: Completely disable the internal blog to save resources.

- FIND FOLDER: src/Template/Posts/
  - ACTION: You can delete this folder or keep it but ensure no links point to it.
  
- FIND FILE: config/routes.php
  - ACTION: Search for routes containing '/blog' or 'Posts' and comment them out using '//'. This prevents users from accessing those pages even if they type the URL.

## 3. URL REDIRECTS (Routing)
Goal: Ensure the paths match your requested clean structure.

- PATH: /auth/signin  -> Ensure this points to UsersController::login
- PATH: /auth/signup  -> Ensure this points to UsersController::register
- PATH: /member/dashboard -> Ensure this is the default landing page after login.

## 4. FOOTER SIMPLIFICATION
- FIND FILE: src/Template/Element/front_footer.twig
  - ACTION: Match the footer links to your new "Important Pages" structure. 
  - ACTION: Remove the "Latest Posts" or "Blog" sections from the footer area.

## 5. ADMIN PANEL "PAGES" SECTION
- Goal: Keep the ability to add custom pages, but make sure they automatically appear in the "Important Pages" dropdown you created in Step 1.


# MODIFICATION GUIDE: ADMIN PANEL SIMPLIFICATION

## 1. ADMIN DASHBOARD STATS (/admin/dashboard)
Goal: Simplify the stats to show only combined totals.

- FIND FILE: src/Template/Admin/Dashboard/index.twig
  - ACTION: Remove the widget for "Owner Earnings".
  - ACTION: Remove the widget for "Referral Earnings".
  - ACTION: Create/Modify a central widget that displays "Total Views" and "Total Publisher Earnings" (combined for all users).

## 2. LINK MANAGEMENT (/admin/links)
Goal: Keep management but clean up the view.

- KEEP AS IS: 
  - /admin/links (List all links)
  - /admin/links/hidden (View hidden links)
  - /admin/links/inactive (View inactive links)

## 3. PAYOUT & AD TYPE OVERHAUL
Goal: Remove the "User Choice" for ad formats and consolidate into one system.

- FIND FILE: src/Template/Admin/Options/payout.twig
  - ACTION: Remove the entire "Interstitial", "Banner", and "Popup" selection logic.
  - ACTION: Modify the page to only have a single input for the "Default CPM Rate".
  
- ACTION: REMOVE THE FOLLOWING ROUTES/FILES:
  - /admin/options/payout-interstitial
  - /admin/options/payout-banner
  - /admin/options/payout-popup
  - NOTE: Users should NOT be able to choose their ad type. Force the "Direct" flow globally.

## 4. USER & WITHDRAWAL MANAGEMENT
Goal: Keep the core financial distribution system.

- KEEP AS IS:
  - /admin/withdraws (Manage payments)
  - /admin/withdraws/export (Financial reporting)
  - /admin/users (Manage site members)
  - /admin/users/add (Manually add users)
  - /admin/users/export (Export user data)

- REMOVE/DISABLE:
  - /admin/users/referrals
  - ACTION: Delete any links in the sidebar pointing to "Referral Management".

## 5. REVENUE LOGIC SIMPLIFICATION
Goal: Focus only on what you pay the publishers.

- FIND FILE: src/Controller/Admin/DashboardController.php
  - ACTION: In the data fetching logic, comment out the code that calculates "Referral Profits" or "Owner Net Profit". 
  - ACTION: Ensure the "Total Earnings" variable only reflects the sum of Publisher Earnings to keep the dashboard simple and accurate to your business model.

# MODIFICATION GUIDE: SYSTEM SETTINGS & MODULE REMOVAL

## 1. REMOVE SUBSCRIPTION & BILLING (Advertiser System)
Goal: Delete the "Plans" and "Invoices" logic as users do not pay for services.

- REMOVE/DISABLE ROUTES:
  - /admin/plans and /admin/plans/add
  - /admin/invoices (Not usable since no money comes from publishers)

- FIND FILE: src/Template/Layout/admin.twig
  - ACTION: Locate and delete the sidebar menu items for "Plans" and "Invoices".

## 2. CONTENT & SOCIAL CLEANUP
Goal: Remove extra marketing features and external login bloat.

- REMOVE BLOG/POSTS:
  - /admin/posts and /admin/posts/add
  - ACTION: Delete "Posts" from the sidebar menu.

- REMOVE TESTIMONIALS & MENU MANAGER:
  - /admin/testimonials (No need for reviews)
  - /admin/menu-manager (Menu will be hardcoded/simplified in step 2)

- KEEP: 
  - Announcements (Useful for notifying users of updates)
  - Pages List/Add (/admin/pages) for your Terms/Privacy/DMCA.

## 3. ADVANCED SETTINGS SIMPLIFICATION
Goal: Disable unneeded options and social logins.

- REMOVE FROM ADMIN SETTINGS:
  - /admin/options/ads (Since you don't show ads on the shortener itself)
  - /admin/options/social-login (Keep it simple with standard email login)
  - /admin/options/payment (No payment gateways needed from user to admin)

- KEEP:
  - /admin/advanced/statistics (Core feature)
  - /admin/options/system (Basic site settings)
  - /admin/options/withdraw (To set how you pay users)
  - /admin/options/email (Required for password resets/notifications)

## 4. DASHBOARD CLEANUP (Member & Admin)
- ACTION: Ensure no "Buy Traffic" or "Add Funds" buttons appear in the Member dashboard, as these are now defunct.



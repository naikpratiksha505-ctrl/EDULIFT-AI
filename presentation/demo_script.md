# EduLift AI — Step-by-Step Live Demo Script

This guide outlines the recommended live demonstration path for judges during a 3 to 5-minute hackathon evaluation.

---

### Step 1: Landing Page & Problem Context (30 seconds)
1. **Open the browser** to `http://127.0.0.1:5000/`.
2. **Highlight the heading:** *"Every Student Deserves a Chance to Succeed."*
3. **Key talking point:** Explain that EduLift AI is designed to replace punitive red flags with constructive, actionable guidance for students and faculty.
4. **Click:** The **"Explore Demo as Student"** button.

---

### Step 2: Student Login & Multi-Persona Autofill (30 seconds)
1. Point out the **Quick Hackathon Autofill** grid on `/login`.
2. Notice the **6 distinct student personas**:
   * 🟢 **Priya Patel** (Star Student: 95.7% attendance, 93.5% marks)
   * 🟡 **Aarav Sharma** (Mixed profile: 80% attendance, Math dip)
   * 🔴 **Rohan Verma** (High Support Needed: 63.8% attendance, 55.6% marks)
   * 📈 **Sneha Kulkarni** (Rapid Improver: +30% upward score surge)
   * 🟣 **Vikram Singh** (Transit Gap: 74.8% attendance, 77.1% marks)
   * ⚪ **Ananya Iyer** (Steady On-Track: 88.1% attendance, 82.5% marks)
3. Click any persona button to automatically fill credentials and see a preview summary.
4. Click **"Sign In to Portal"**.

---

### Step 3: Student Overview Dashboard (60 seconds)
1. **Welcome Message & Key Metrics:**
   * Point out Aarav Sharma's profile: Roll No `26AIML042`, B.Tech AIML (Section A).
   * Show the stat cards: Overall Attendance (80.0%), Average Marks (76.8%), Study Goals, and Identified Advisories.
2. **Chart.js Progress Trend:**
   * Showcase the interactive line chart showing assessment scores across the semester.
   * Point out the tooltips when hovering over data points.
3. **Subject Breakdown Table:**
   * Show how attendance and marks are paired per subject.
   * Highlight that *Mathematics for AI* shows 69.0% attendance, triggering a constructive "Focus Area" tag.
4. **Supportive AI Recommendations:**
   * Show the recommendation card: *"Discuss Attendance Support with Faculty Advisor"*.
   * Walk through the four required components:
     * **Title:** Clear topic.
     * **Why this appeared:** Clear root cause.
     * **Academic Evidence:** Attended 29 of 42 classes in Math.
     * **Actionable Step:** Schedule a quick check-in to explore makeup sessions or recorded modules.
5. **Machine Learning Demonstration Card:**
   * Point out the scikit-learn Logistic Regression prediction and probability.
   * Show the factor attribution breakdown (how attendance, marks, and trends contributed).
   * Read the ethical advisory warning: *"This demonstration uses synthetic data and is not validated for real students. Predictions are advisory and must not be used for disciplinary decisions."*

---

### Step 4: Study Goals & Progress Snapshots (40 seconds)
1. **Study Goal Tracker:**
   * In the "Weekly Study Goals" card, type a new goal: `Review Linear Algebra vector spaces`.
   * Click **"+ Add Goal"**. Show that it appears immediately.
   * Click **"Mark Done"** on any existing goal to show real-time persistence.
2. **Progress Snapshots:**
   * Click the **"Save Progress Snapshot"** button at the top.
   * Scroll down to the "Historical Progress Snapshots" table to show the new point-in-time record saved with the current timestamp alongside the fictional seed records.

---

### Step 5: Weekly Study Planner (45 seconds)
1. In the sidebar, click **"Study Planner"** (or `/student/study-planner`).
2. Point out the notice: *"This is a suggested study plan. Adjust it to your needs and available time."*
3. **Automated Timetable Generation:**
   * Set Available Study Time to `10` hours.
   * Select *Mathematics for AI* under "Prioritize Upcoming Assessment".
   * Click **"Generate Suggested Timetable"**.
   * Show how the schedule creates 45-minute focused blocks with 15-minute intervals across weekdays, weighting Math higher.
4. Toggle completion on a task or delete one to show interactive database updates.

---

### Step 6: Faculty Portal & Mentorship Workflow (60 seconds)
1. Click **"Sign Out"** in the top navigation bar.
2. On the login screen, click the **"Faculty Demo"** autofill button (`faculty_demo` / `Password123!`).
3. Click **"Sign In"**.
4. **Cohort Analytics:**
   * Show the cohort overview: 5 students enrolled, Cohort Average Attendance, Cohort Average Marks.
   * View the Cohort Subject Performance bar chart.
5. **Real-Time Student Search:**
   * In the student roster search box, type `Rohan` or `Aarav`. Show that the table filters instantly.
6. **Support Alerts:**
   * Point out the supportive alerts: *"This student may benefit from a check-in because attendance below demo threshold."*
7. **Drill Down to Student Detail:**
   * Click **"View & Support"** for Aarav Sharma.
   * Demonstrate the **Attendance Correction form** (e.g. adjust attended classes and save).
   * Demonstrate the **Assessment Entry form** (e.g. record a Quiz score).
   * Show the **Intervention Lifecycle Tracker**: update an intervention from *In progress* to *Completed* with an outcome note.
8. Point out that permissions are strictly enforced: Faculty can only see their assigned cohort, and students cannot access faculty paths.

---

### Step 7: Conclude (15 seconds)
"EduLift AI is complete, fully tested with 23 passing unit tests, runs offline with zero paid APIs, and is ready for real campus pilots. Thank you!"

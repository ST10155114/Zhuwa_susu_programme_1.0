# Zhuwa Susu Savings Management System 💰

A command-line Python application designed to digitize, manage, and automate traditional **Susu** (rotating savings and credit association) groups. Built with strict domain rules, financial accuracy using fixed decimal precision, and automated verification via unit tests.

---

## 📌 Features

- **Group Setup:** Easily create a Susu group with a custom group name and fixed weekly contribution amount (GHS).
- **Member Registration:** Register members with unique IDs during the initial setup period (Week 1).
- **Strict Registration Lock:** Mid-cycle member additions are blocked once group operations begin to ensure rotation fairness.
- **Contribution Tracking:** Record contributions safely—prevents overpayments, negative values, and contributions for future unreached weeks.
- **Automated Payout Rotations:** Automatically calculates and awards the collective weekly pot to the next scheduled recipient when all members complete their weekly contribution.
- **Reporting & Statements:** Instantly inspect member balances, contribution history, and payout history.

---

## 🛠️ Requirements & Installation

- **Python 3.8+** must be installed on your machine.
- No third-party dependencies required (uses standard Python libraries: `decimal`, `unittest`).

### Clone the Repository

```bash
git clone https://github.com/ST10155114/Zhuwa_susu_programme_1.0.git
cd Zhuwa_susu_programme_1.0
```

---

## 🚀 Running the Application

To start the interactive command-line application, run the main Python script from your terminal:

```bash
python Zhuwa_susu_programme_1_0.py
```

### Usage Flow
1. **Initialize Group:** Set your group name and weekly required contribution (e.g., `50`).
2. **Register Members:** Add members with unique ID numbers (e.g., Name: `Alice`, ID: `A1`).
3. **Record Payments:** Log member contributions week by week.
4. **Close Week:** Once all members have fully paid for the current week, close the week to issue the payout rotation automatically.
5. **View Summary:** Inspect full financial group reports at any time.

---

## 🧪 Running Automated Tests

The application includes an automated test suite covering 10 distinct test cases (validation of payment limits, unknown member handling, registration locking, partial-payment checks, and payout rotations).

To run all automated tests in verbose mode, run:

```bash
python -m unittest -v tests
```

*Or directly executing the test file:*

```bash
python tests.py
```

---

## 📁 Repository Structure

```text
├── Zhuwa_susu_programme_1_0.py   # Main Susu application logic & CLI interactive flow
├── tests.py                     # Automated unit test suite (10 test cases)
└── README.md                    # Project documentation
```

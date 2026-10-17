from decimal import Decimal

class SusuGroup:
    def __init__(self, group_name, weekly_contribution):
        self.group_name = group_name.strip() if group_name.strip() else "Default Group"
        self.weekly_contribution = Decimal(str(weekly_contribution)).quantize(Decimal('0.01'))
        if self.weekly_contribution <= 0:
            raise ValueError("Weekly contribution must be greater than zero.")
            
        self.members = {}
        self.current_week = 1
        self.payout_history = []
        self.closed_weeks = set()
        self.contributions = {1: {}}
        self.registration_open = True

    def add_member(self, name, member_id):
        name = name.strip()
        member_id = member_id.strip()
        if not name or not member_id:
            return "Error: Member name and ID cannot be empty."
        if not self.registration_open:
            return "Error: Cannot add members after Week 1 has started."
        if member_id in self.members:
            return f"Error: Member ID '{member_id}' already exists."
            
        self.members[member_id] = name
        for week in self.contributions:
            self.contributions[week][member_id] = Decimal('0.00')
            
        return f"Success: Added '{name}' (ID: {member_id})."

    def record_contribution(self, member_id, week, amount):
        if week < 1:
            return "Error: Week number cannot be less than 1."
        if week > self.current_week:
            return f"Error: Cannot record for future week {week}."
        if member_id not in self.members:
            return f"Error: Unknown member ID '{member_id}'."
            
        amt_decimal = Decimal(str(amount)).quantize(Decimal('0.01'))
        if amt_decimal <= 0:
            return "Error: Contribution amount must be greater than zero."
            
        if week not in self.contributions:
            self.contributions[week] = {m: Decimal('0.00') for m in self.members}
            
        current_paid = self.contributions[week][member_id]
        allowed_due = self.weekly_contribution - current_paid
        
        if amt_decimal > allowed_due:
            name = self.members[member_id]
            return f"Error: Payment exceeds what is owed. '{name}' owes GHS {allowed_due:.2f} more."
            
        self.contributions[week][member_id] = current_paid + amt_decimal
        return f"Success: Recorded GHS {amt_decimal:.2f} for '{self.members[member_id]}'."

    def close_week(self):
        self.registration_open = False
        
        if not self.members:
            return "Error: No members in the group."
            
        week_data = self.contributions[self.current_week]
        unpaid_members = []
        
        for member_id, name in self.members.items():
            paid = week_data.get(member_id, Decimal('0.00'))
            if paid < self.weekly_contribution:
                due = self.weekly_contribution - paid
                unpaid_members.append((name, member_id, due))
                
        if unpaid_members:
            report_lines = [f"Week {self.current_week} could not be closed. Payout withheld."]
            for name, m_id, due in unpaid_members:
                report_lines.append(f"  - {name} (ID: {m_id}) owes GHS {due:.2f}")
            return "\n".join(report_lines)
            
        member_ids = list(self.members.keys())
        recipient_index = (self.current_week - 1) % len(member_ids)
        recipient_id = member_ids[recipient_index]
        recipient_name = self.members[recipient_id]
        total_pot = self.weekly_contribution * len(self.members)
        
        self.payout_history.append({
            "week": self.current_week,
            "recipient": recipient_name,
            "recipient_id": recipient_id,
            "amount": total_pot
        })
        
        self.closed_weeks.add(self.current_week)
        payout_msg = f"Week {self.current_week} closed! Pot of GHS {total_pot:.2f} paid to {recipient_name} (ID: {recipient_id})."
        
        self.current_week += 1
        self.contributions[self.current_week] = {m: Decimal('0.00') for m in self.members}
        
        return payout_msg

    def get_report(self):
        current_week_data = self.contributions.get(self.current_week, {m: Decimal('0.00') for m in self.members})
        
        report = []
        report.append("====================")
        report.append(f"  {self.group_name.upper()} REPORT")
        report.append("====================")
        report.append(f"Current Week: {self.current_week}")
        report.append(f"Weekly Amount: GHS {self.weekly_contribution:.2f}")
        report.append("--------------------")
        
        report.append("Current Week Contributions:")
        for member_id, name in self.members.items():
            paid = current_week_data.get(member_id, Decimal('0.00'))
            status = f"Paid: GHS {paid:.2f} / GHS {self.weekly_contribution:.2f}"
            if paid >= self.weekly_contribution:
                status += " (Paid in Full)"
            else:
                due = self.weekly_contribution - paid
                status += f" [Owes: GHS {due:.2f}]"
            report.append(f"  - {name} (ID: {member_id}) -> {status}")
            
        report.append("--------------------")
        report.append("Closed Weeks:")
        if self.closed_weeks:
            for w in sorted(self.closed_weeks):
                report.append(f"  - Week {w} (Closed successfully)")
        else:
            report.append("  - No weeks closed yet")
            
        report.append("--------------------")
        report.append("Payout History:")
        if self.payout_history:
            for p in self.payout_history:
                report.append(f"  - Week {p['week']}: GHS {p['amount']:.2f} paid to {p['recipient']} (ID: {p['recipient_id']})")
        else:
            report.append("  - No payouts executed yet")
        report.append("====================")
        
        return "\n".join(report)

def display_user_info():
    info = []
    info.append("====================")
    info.append("    configuration ")
    info.append("====================")
    info.append("Name: Khaarendiwe Yadah Mudimeli")
    info.append("Email: yadahmudimelik@gmail.com")
    info.append("====================")
    return "\n".join(info)

def main():
    print("--- susu Group ---")
    print("--- create group...  ---")
    group_name = input("Enter group name: ")
    amt = input("Enter fixed weekly contribution amount in GHS: ")
    group = SusuGroup(group_name, amt)
    print(f"Group '{group.group_name}' successfully created with a weekly contribution of GHS {group.weekly_contribution:.2f}!")
    
    while True:
        print(f"\n--- {group.group_name} Menu ---")
        print("1. Add Member")
        print("2. Record Contribution")
        print("3. Close Week")
        print("4. Show Report")
        print("5. Programm detais")
        print("6. Exit")
        
        choice = input("Choose an option (1-6): ").strip()
        
        if choice == "1":
            name = input("Enter member name: ")
            member_id = input("Enter member ID: ")
            print(group.add_member(name, member_id))
        elif choice == "2":
            member_id = input("Enter member ID: ")
            try:
                week = int(input("Enter week number: "))
                amount = input("Enter amount paid: ")
                print(group.record_contribution(member_id, week, amount))
            except ValueError:
                print("Error: Invalid number format for week or amount.")
        elif choice == "3":
            print(group.close_week())
        elif choice == "4":
            print(group.get_report())
        elif choice == "5":
            print(display_user_info())
        elif choice == "6":
            print("Exiting program.")
            break
        else:
            print("Invalid option. Please choose between 1 and 6.")

if __name__ == "__main__":
    main()
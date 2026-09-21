import pandas as pd
import csv

def organize_data(filepath):
    with open(filepath, 'r') as file:
        member_file = csv.DictReader(file)  
        members_dict = {}

        for row in member_file:
            member_ID = row['Subscriber_ID']  
            members_dict[member_ID] = {key: row[key] for key in row.keys()}

    return members_dict

def organize_repeatable_data(filepath):
    with open(filepath, 'r') as file:
        enrollment_plan = csv.DictReader(file)  
        enrollment_plan_dict = {}

        for row in enrollment_plan:
            subscriber_ID = row['Subscriber_ID']  

            if subscriber_ID in enrollment_plan_dict:
                for key in row:
                    if key in enrollment_plan_dict[subscriber_ID]:
                        enrollment_plan_dict[subscriber_ID][key].append(row[key])
                    else:
                        enrollment_plan_dict[subscriber_ID][key] = [row[key]]
            else:
                enrollment_plan_dict[subscriber_ID] = {key: [value] for key, value in row.items()}
    return enrollment_plan_dict

members_csv            = organize_repeatable_data("Members.csv")
subscribers_csv        = organize_data("Subscribers.csv")
subenrollment_csv      = organize_repeatable_data("SubEnrollment.csv")
subenrollment_plan_csv = organize_repeatable_data("SubEnrollmentPlan.csv")


# Other fields that can be modified but are currently empty
RECORD_TYPE = 23
member_num_overflow = None
insured_ID_overflow = None
filler_1 = None
alternate_member_num = None
pcp_start_date = None
pcp_end_date = None
medical_group_start_date = None
medical_group = None
reserved_1 = None
reserved_2 = None
miscellaneous_code_1 = None
miscellaneous_code_2 = None
miscellaneous_code_3 = None
miscellaneous_code_4 = None
cob_code = None
pcp_ID_num = None
miscellaneous_code_5 = None
miscellaneous_code_6 = None
miscellaneous_code_7 = None
filler_2 = None
HIC_num = None
id_card_print_date = None
medicare_code = None
term_code = None
force_ID_card = None
credit_card_num = None
expiration_date = None
miscellaneous_code_9 = None
miscellaneous_code_10 = None
miscellaneous_code_11 = None
miscellaneous_code_12 = None
cob_prime_code = None
medicaid_num = None
filler_3 = None
pcp_ID_overflow = None
void_flag = None
conf_communication_flag = None
phone_num = None
phone_num_ext = None
second_phone_num = None
second_phone_num_ext = None
medicare_ID = None
reserved_filler_1 = None
foreign_language = None
ethnicity = None
filler_4 = None
reserved_filler_2 = None



whole_array = []

# Looping over subscriber IDs
for key in subscribers_csv.keys():
    subscriber_ID = key
    if subscriber_ID not in subenrollment_plan_csv:
        continue
    else:
        # Getting important info from subenrollment plan file
        division_ID = subenrollment_plan_csv[subscriber_ID]["Division_ID"][0]
        plan_ID = subenrollment_plan_csv[subscriber_ID]["Plan_ID"][0][:-5]
        group_number = division_ID + str(plan_ID[-1])
        if division_ID[0] == "C":
            headquarters_code = "KPC07"
        elif division_ID[0] == "K":
            headquarters_code = "KPC08"
        else:
            headquarters_code = ""

        # Getting info from the subscriber file
        address = subscribers_csv[subscriber_ID]["Address"]
        city = subscribers_csv[subscriber_ID]["City"]
        state = subscribers_csv[subscriber_ID]["State"]
        zip_code = subscribers_csv[subscriber_ID]["Zip_Code"]
        address_2 = subscribers_csv[subscriber_ID]["Address2"]

        # Using same ID to access member's info
        member_info = members_csv[subscriber_ID]
        num_members = len(member_info["Member_Seq"])
        member_array = []
        for i in range(num_members):
            last_name = member_info["Last_Name"][i]
            first_name = member_info["First_Name"][i]
            relationship = int(member_info["Relationship"][i])
            birth_date = member_info["Birth_Date"][i]
            birth_date = ''.join((birth_date.split()[0]).split("-"))
            sex = member_info["Sex"][i]
            alternate_ID = member_info["Alternate_ID"][i]
            middle_name = member_info["Middle_Name"][i]
            social_sec_num = member_info["SSN"][i]
            if relationship == 1:
                relationship = "I"
            elif relationship == 2:
                relationship = "S"
            elif relationship == 19:
                relationship = "D"
            insured_ID = member_info["Alternate_ID"][i][:-2]
            member_number = member_info["Alternate_ID"][i]
            # Member numbers are unique so the person code is 00 for everyone
            person_code = 0
            term_date = member_info["Disenroll_Date"][i]
            
            if term_date != [] and term_date != "":
                if num_members == 1:
                    term_date = ''.join(term_date.split("-"))
                else:
                    term_date = ''.join((term_date.split()[0]).split("-"))
            date_enrolled = member_info["Date_Enrolled"][i]
            if num_members == 1:
                date_enrolled = ''.join(date_enrolled.split("-"))
            else:
                date_enrolled = ''.join((date_enrolled.split()[0]).split("-"))
            if int(date_enrolled[:4]) < 2024:
                date_enrolled = "20240101"
            # Should be 1 for single, 2 for family, etc (based on Type 23)
            dependent_coverage_code = 0
            reserved_xref_mem_num = insured_ID
            reserved_xref_family_pos = member_number[-2:]

            # Creating an item for the whole_array that will represent a single member with all of its fields
            member_array = [RECORD_TYPE, group_number, division_ID, insured_ID, 
                            member_number, person_code, relationship, last_name, 
                            first_name, middle_name, birth_date, sex, address, 
                            address_2, member_num_overflow, insured_ID_overflow, 
                            filler_1, alternate_member_num, pcp_start_date, 
                            pcp_end_date, medical_group_start_date, medical_group, 
                            reserved_1, reserved_2, miscellaneous_code_1, 
                            miscellaneous_code_2, miscellaneous_code_3, 
                            miscellaneous_code_4, city, state, zip_code, 
                            social_sec_num, dependent_coverage_code, cob_code, 
                            date_enrolled, term_date, headquarters_code, pcp_ID_num, 
                            miscellaneous_code_5, miscellaneous_code_6, miscellaneous_code_7, 
                            filler_2, HIC_num, id_card_print_date, medicare_code, 
                            term_code, force_ID_card, credit_card_num, expiration_date, 
                            miscellaneous_code_9, miscellaneous_code_10, miscellaneous_code_11, 
                            miscellaneous_code_12, reserved_xref_mem_num, reserved_xref_family_pos, 
                            cob_prime_code, medicaid_num, filler_3, pcp_ID_overflow, 
                            void_flag, conf_communication_flag, phone_num, phone_num_ext, 
                            second_phone_num, second_phone_num_ext, medicare_ID, reserved_filler_1, 
                            foreign_language, ethnicity, filler_4, reserved_filler_2]
            whole_array.append(member_array)



headers = ["Record Type", "Group Number", "Division", "Insured I.D.", "Member Number", "Person Code", 
           "Relationship", "Last Name", "First Name", "Middle Name", "Birth Date", "Sex", "Address", 
           "Address 2", "Member Num Overflow", "Insured ID Overflow", "Filler 1", "Alternate Member Num", 
           "PCP Start Date", "PCP End Date", "Medical Group Start Date", "Medical Group", "Reserved 1", 
           "Reserved 2", "Miscellaneous Code 1", "Miscellaneous Code 2", "Miscellaneous Code 3", 
           "Miscellaneous Code 4", "City", "State", "Zip Code", "Social Sec Num", "Dependent Coverage Code", 
           "COB Code", "Date Enrolled", "Term Date", "Headquarters Code", "PCP ID Num", "Miscellaneous Code 5", 
           "Miscellaneous Code 6", "Miscellaneous Code 7", "Filler 2", "HIC Num", "ID Card Print Date", 
           "Medicare Code", "Term Code", "Force ID Card", "Credit Card Num", "Expiration Date", 
           "Miscellaneous Code 9", "Miscellaneous Code 10", "Miscellaneous Code 11", "Miscellaneous Code 12", 
           "Reserved Xref Mem Num", "Reserved Xref Family Pos", "COB Prime Code", "Medicaid Num", "Filler 3", 
           "PCP ID Overflow", "Void Flag", "Conf Communication Flag", "Phone Num", "Phone Num Ext", 
           "Second Phone Num", "Second Phone Num Ext", "Medicare ID", "Reserved Filler 1", "Foreign Language", 
           "Ethnicity", "Filler 4", "Reserved Filler 2"]

# Using pandas to convert the array to the xlsx file
output = pd.DataFrame(whole_array, columns=headers)
# Sorting based on couple of fields
sorted_array = output.sort_values(by=["Group Number", "Division", "Insured I.D."])
xlsx_final_file = "results.xlsx"
sorted_array.to_excel(xlsx_final_file, index=False)

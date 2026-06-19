"""
Seed script — Rich dummy data for all modules.
Run: python seed_data.py
"""
import os, sys, json, uuid
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
UPLOADS_DIR = os.path.join(os.path.dirname(__file__), "uploads")

def gid(p): return f"{p}_{uuid.uuid4().hex[:8]}"
def ts(d=0): return (datetime.now(timezone.utc) - timedelta(days=d)).isoformat()
def save(f, d):
    with open(os.path.join(DATA_DIR, f), "w", encoding="utf-8") as fh:
        json.dump(d, fh, indent=2, ensure_ascii=False)
    print(f"  ✓ {f} — {len(d) if isinstance(d,list) else 'dict'}")

# ========== DRIVES ==========
drives = [
  {"drive_id":"drv_aws2026","name":"AWS Solutions Architect - July 2026",
   "sponsor":"L&D Mavericks","budget":75000,"start_date":"2026-06-15",
   "end_date":"2026-08-15","target_count":40,
   "policy_notes":"Max 2 attempts/year. Training mandatory. Manager approval required.",
   "pass_threshold":72,"status":"active","created_at":ts(30),"created_by":"admin_001"},
  {"drive_id":"drv_azure2026","name":"Azure Administrator AZ-104 - Aug 2026",
   "sponsor":"Cloud COE","budget":50000,"start_date":"2026-07-01",
   "end_date":"2026-09-30","target_count":30,
   "policy_notes":"Min 90 days tenure. Max 2 attempts.",
   "pass_threshold":70,"status":"active","created_at":ts(20),"created_by":"admin_001"},
  {"drive_id":"drv_gcp2026","name":"GCP Cloud Architect - Sep 2026",
   "sponsor":"Engineering L&D","budget":60000,"start_date":"2026-08-01",
   "end_date":"2026-10-31","target_count":25,
   "policy_notes":"Senior engineers with 1+ year tenure.",
   "pass_threshold":75,"status":"active","created_at":ts(10),"created_by":"admin_001"},
]

# ========== REGISTRATIONS ==========
aws_candidates = [
  ("EMP1001","Priya Sharma","priya.sharma@hexaware.com","Digital Engineering","Chennai"),
  ("EMP1002","Rahul Verma","rahul.verma@hexaware.com","Cloud Services","Pune"),
  ("EMP1003","Anita Desai","anita.desai@hexaware.com","Data & AI","Mumbai"),
  ("EMP1004","Vikram Singh","vikram.singh@hexaware.com","Digital Engineering","Bangalore"),
  ("EMP1005","Sneha Patel","sneha.patel@hexaware.com","Cloud Services","Chennai"),
  ("EMP1006","Arjun Nair","arjun.nair@hexaware.com","Platform Engineering","Hyderabad"),
  ("EMP1007","Deepika Rao","deepika.rao@hexaware.com","Digital Engineering","Pune"),
  ("EMP1008","Karthik Kumar","karthik.kumar@hexaware.com","Cloud Services","Chennai"),
  ("EMP1009","Meera Iyer","meera.iyer@hexaware.com","Data & AI","Bangalore"),
  ("EMP1010","Suresh Reddy","suresh.reddy@hexaware.com","Platform Engineering","Hyderabad"),
  ("EMP1011","Kavya Menon","kavya.menon@hexaware.com","Digital Engineering","Chennai"),
  ("EMP1012","Arun Krishnan","arun.krishnan@hexaware.com","Cloud Services","Pune"),
  ("EMP1013","Divya Gupta","divya.gupta@hexaware.com","Data & AI","Mumbai"),
  ("EMP1014","Rajesh Pillai","rajesh.pillai@hexaware.com","Digital Engineering","Bangalore"),
  ("EMP1015","Lakshmi Venkat","lakshmi.venkat@hexaware.com","Cloud Services","Chennai"),
  ("EMP1016","Manish Tiwari","manish.tiwari@hexaware.com","Platform Engineering","Pune"),
  ("EMP1017","Nisha Agarwal","nisha.agarwal@hexaware.com","Data & AI","Mumbai"),
  ("EMP1018","Rohan Jha","rohan.jha@hexaware.com","Cloud Services","Bangalore"),
  ("EMP1019","Tanvi Bhatt","tanvi.bhatt@hexaware.com","Digital Engineering","Hyderabad"),
  ("EMP1020","Sameer Khan","sameer.khan@hexaware.com","Platform Engineering","Chennai"),
]
azure_candidates = [
  ("EMP2001","Amit Joshi","amit.joshi@hexaware.com","Cloud Services","Pune"),
  ("EMP2002","Riya Saxena","riya.saxena@hexaware.com","Platform Engineering","Chennai"),
  ("EMP2003","Nikhil Das","nikhil.das@hexaware.com","Digital Engineering","Bangalore"),
  ("EMP2004","Pooja Mehta","pooja.mehta@hexaware.com","Cloud Services","Mumbai"),
  ("EMP2005","Sanjay Yadav","sanjay.yadav@hexaware.com","Data & AI","Hyderabad"),
  ("EMP2006","Shruti Kapoor","shruti.kapoor@hexaware.com","Platform Engineering","Pune"),
  ("EMP2007","Varun Malhotra","varun.malhotra@hexaware.com","Cloud Services","Chennai"),
  ("EMP2008","Neha Srivastava","neha.srivastava@hexaware.com","Digital Engineering","Mumbai"),
  ("EMP2009","Abhishek Roy","abhishek.roy@hexaware.com","Data & AI","Bangalore"),
  ("EMP2010","Pallavi Mishra","pallavi.mishra@hexaware.com","Cloud Services","Hyderabad"),
]
gcp_candidates = [
  ("EMP3001","Siddharth Nath","siddharth.nath@hexaware.com","Platform Engineering","Chennai"),
  ("EMP3002","Aditi Banerjee","aditi.banerjee@hexaware.com","Cloud Services","Pune"),
  ("EMP3003","Gaurav Saxena","gaurav.saxena@hexaware.com","Digital Engineering","Bangalore"),
  ("EMP3004","Swati Kulkarni","swati.kulkarni@hexaware.com","Data & AI","Mumbai"),
  ("EMP3005","Harish Menon","harish.menon@hexaware.com","Platform Engineering","Hyderabad"),
]

# Build registrations
registrations = []
# AWS: 20 candidates, varied statuses
aws_statuses = ["passed"]*8 + ["failed"]*3 + ["eligible"]*4 + ["registered"]*3 + ["ineligible"]*2
for i,(eid,name,email,bu,loc) in enumerate(aws_candidates):
    registrations.append({
        "reg_id":f"reg_{eid.lower()}","drive_id":"drv_aws2026",
        "emp_id":eid,"name":name,"email":email,"bu":bu,"location":loc,
        "manager_email":f"mgr.{name.split()[1].lower()}@hexaware.com",
        "exam_track":"AWS Solutions Architect","slot":"2026-07-20",
        "prior_attempts": 2 if aws_statuses[i]=="ineligible" else 0,
        "status":aws_statuses[i],
        "registered_at":ts(28-i),"ack_timestamp":ts(28-i),
    })
# Azure: 10 candidates
az_statuses = ["passed"]*4 + ["failed"]*2 + ["eligible"]*2 + ["registered"]*2
for i,(eid,name,email,bu,loc) in enumerate(azure_candidates):
    registrations.append({
        "reg_id":f"reg_{eid.lower()}","drive_id":"drv_azure2026",
        "emp_id":eid,"name":name,"email":email,"bu":bu,"location":loc,
        "manager_email":f"mgr.{name.split()[1].lower()}@hexaware.com",
        "exam_track":"Azure AZ-104","slot":"2026-08-10",
        "prior_attempts":0,"status":az_statuses[i],
        "registered_at":ts(18-i),"ack_timestamp":ts(18-i),
    })
# GCP: 5 candidates
gcp_statuses = ["eligible"]*3 + ["registered"]*2
for i,(eid,name,email,bu,loc) in enumerate(gcp_candidates):
    registrations.append({
        "reg_id":f"reg_{eid.lower()}","drive_id":"drv_gcp2026",
        "emp_id":eid,"name":name,"email":email,"bu":bu,"location":loc,
        "manager_email":f"mgr.{name.split()[1].lower()}@hexaware.com",
        "exam_track":"GCP Cloud Architect","slot":"2026-09-15",
        "prior_attempts":0,"status":gcp_statuses[i],
        "registered_at":ts(8-i),"ack_timestamp":ts(8-i),
    })

# ========== ELIGIBILITY ==========
eligibility = []
for r in registrations:
    if r["status"] in ("eligible","passed","failed"):
        eligibility.append({
            "elig_id":gid("elig"),"reg_id":r["reg_id"],"drive_id":r["drive_id"],
            "criteria":{"tenure_days":180,"tenure_check":True,"training_complete":True,
                        "prior_attempts":r["prior_attempts"],"prior_attempts_check":True,"budget_check":True},
            "decision":"eligible","approver":"admin_001","decision_date":ts(20),"notes":"",
        })
    elif r["status"]=="ineligible":
        eligibility.append({
            "elig_id":gid("elig"),"reg_id":r["reg_id"],"drive_id":r["drive_id"],
            "criteria":{"tenure_days":200,"tenure_check":True,"training_complete":True,
                        "prior_attempts":2,"prior_attempts_check":False,"budget_check":True},
            "decision":"ineligible","approver":"admin_001","decision_date":ts(20),
            "notes":"Prior attempts (2) exceed limit",
        })

# ========== RESULTS ==========
results = []
scores_pass = [78,82,85,91,76,88,79,84]
scores_fail = [55,62,68,58,65]
pi = 0; fi = 0
for r in registrations:
    if r["status"]=="passed":
        s = scores_pass[pi % len(scores_pass)]; pi += 1
        drv = next(d for d in drives if d["drive_id"]==r["drive_id"])
        results.append({
            "result_id":gid("res"),"reg_id":r["reg_id"],"drive_id":r["drive_id"],
            "score":s,"pass_threshold":drv["pass_threshold"],"outcome":"passed",
            "exam_date":r["slot"],"evidence_filename":f"{r['emp_id']}_cert.pdf","uploaded_at":ts(10),
        })
    elif r["status"]=="failed":
        s = scores_fail[fi % len(scores_fail)]; fi += 1
        drv = next(d for d in drives if d["drive_id"]==r["drive_id"])
        results.append({
            "result_id":gid("res"),"reg_id":r["reg_id"],"drive_id":r["drive_id"],
            "score":s,"pass_threshold":drv["pass_threshold"],"outcome":"failed",
            "exam_date":r["slot"],"evidence_filename":"","uploaded_at":ts(10),
        })

# ========== VOUCHERS ==========
vouchers = []
aws_codes = ["AWS-PRO-7K4M-X9QW","AWS-PRO-2N8J-L5VT","AWS-PRO-4D6H-R3YP",
             "AWS-PRO-8F1C-W7ZA","AWS-PRO-5G9B-M2KE","AWS-PRO-3J7N-T6XS",
             "AWS-PRO-6L2D-Q4HV","AWS-PRO-1P5R-Y8FC","AWS-PRO-9W3A-K7NB",
             "AWS-PRO-7T4E-S1GM","AWS-PRO-2R6F-P8WC","AWS-PRO-4K9H-N3XD"]
az_codes = ["AZ104-VCH-A1B2-C3D4","AZ104-VCH-E5F6-G7H8","AZ104-VCH-I9J0-K1L2",
            "AZ104-VCH-M3N4-O5P6","AZ104-VCH-Q7R8-S9T0","AZ104-VCH-U1V2-W3X4"]

passed_aws = [r for r in registrations if r["drive_id"]=="drv_aws2026" and r["status"]=="passed"]
passed_az = [r for r in registrations if r["drive_id"]=="drv_azure2026" and r["status"]=="passed"]

for i,code in enumerate(aws_codes):
    v = {"voucher_id":gid("vch"),"drive_id":"drv_aws2026","vendor":"AWS",
         "code":code,"masked_code":"****-****-"+code[-4:],"value":300,
         "expiry_date":"2026-12-31","status":"available","assigned_to":None,
         "allocated_date":None,"delivery_status":"pending","redeemed_date":None,"reminder_sent":[]}
    if i < len(passed_aws):
        v["status"]="allocated"; v["assigned_to"]=passed_aws[i]["reg_id"]
        v["allocated_date"]=ts(7); v["delivery_status"]="delivered"
        if i < 4:  # first 4 redeemed
            v["status"]="redeemed"; v["redeemed_date"]=ts(2)
    vouchers.append(v)

for i,code in enumerate(az_codes):
    v = {"voucher_id":gid("vch"),"drive_id":"drv_azure2026","vendor":"Microsoft",
         "code":code,"masked_code":"****-****-"+code[-4:],"value":250,
         "expiry_date":"2027-01-31","status":"available","assigned_to":None,
         "allocated_date":None,"delivery_status":"pending","redeemed_date":None,"reminder_sent":[]}
    if i < len(passed_az):
        v["status"]="allocated"; v["assigned_to"]=passed_az[i]["reg_id"]
        v["allocated_date"]=ts(5); v["delivery_status"]="delivered"
        if i < 2:
            v["status"]="redeemed"; v["redeemed_date"]=ts(1)
    vouchers.append(v)

# ========== AUDIT LOGS ==========
audit_logs = [
  {"log_id":gid("log"),"entity":"Drive","entity_id":"drv_aws2026","action":"created",
   "actor":"admin_001","timestamp":ts(30),"before":None,"after":{"name":"AWS Solutions Architect - July 2026","status":"active"}},
  {"log_id":gid("log"),"entity":"Drive","entity_id":"drv_azure2026","action":"created",
   "actor":"admin_001","timestamp":ts(20),"before":None,"after":{"name":"Azure Administrator AZ-104","status":"active"}},
  {"log_id":gid("log"),"entity":"Drive","entity_id":"drv_gcp2026","action":"created",
   "actor":"admin_001","timestamp":ts(10),"before":None,"after":{"name":"GCP Cloud Architect","status":"active"}},
  {"log_id":gid("log"),"entity":"Registration","entity_id":"drv_aws2026","action":"bulk_imported",
   "actor":"admin_001","timestamp":ts(28),"before":None,"after":{"success":20,"errors":0}},
  {"log_id":gid("log"),"entity":"Registration","entity_id":"drv_azure2026","action":"bulk_imported",
   "actor":"admin_001","timestamp":ts(18),"before":None,"after":{"success":10,"errors":0}},
  {"log_id":gid("log"),"entity":"Eligibility","entity_id":"drv_aws2026","action":"evaluated",
   "actor":"admin_001","timestamp":ts(22),"before":None,"after":{"eligible":15,"ineligible":2,"total":17}},
  {"log_id":gid("log"),"entity":"Eligibility","entity_id":"drv_azure2026","action":"evaluated",
   "actor":"admin_001","timestamp":ts(15),"before":None,"after":{"eligible":8,"ineligible":0,"total":8}},
  {"log_id":gid("log"),"entity":"Result","entity_id":"drv_aws2026","action":"bulk_imported",
   "actor":"admin_001","timestamp":ts(12),"before":None,"after":{"passed":8,"failed":3,"total":11}},
  {"log_id":gid("log"),"entity":"Result","entity_id":"drv_azure2026","action":"bulk_imported",
   "actor":"admin_001","timestamp":ts(9),"before":None,"after":{"passed":4,"failed":2,"total":6}},
  {"log_id":gid("log"),"entity":"Voucher","entity_id":"drv_aws2026","action":"pool_added",
   "actor":"admin_001","timestamp":ts(8),"before":None,"after":{"count":12,"vendor":"AWS","value":300}},
  {"log_id":gid("log"),"entity":"Voucher","entity_id":"drv_azure2026","action":"pool_added",
   "actor":"admin_001","timestamp":ts(6),"before":None,"after":{"count":6,"vendor":"Microsoft","value":250}},
  {"log_id":gid("log"),"entity":"Voucher","entity_id":"drv_aws2026","action":"allocated",
   "actor":"admin_001","timestamp":ts(7),"before":{"available":12},"after":{"allocated":8,"available":4}},
  {"log_id":gid("log"),"entity":"Voucher","entity_id":"drv_azure2026","action":"allocated",
   "actor":"admin_001","timestamp":ts(5),"before":{"available":6},"after":{"allocated":4,"available":2}},
  {"log_id":gid("log"),"entity":"Voucher","entity_id":"drv_aws2026","action":"redeemed",
   "actor":"user_001","timestamp":ts(2),"before":{"status":"allocated","count":8},"after":{"status":"redeemed","redeemed":4}},
  {"log_id":gid("log"),"entity":"Voucher","entity_id":"drv_azure2026","action":"redeemed",
   "actor":"user_001","timestamp":ts(1),"before":{"status":"allocated","count":4},"after":{"status":"redeemed","redeemed":2}},
  {"log_id":gid("log"),"entity":"Drive","entity_id":"drv_aws2026","action":"updated",
   "actor":"admin_001","timestamp":ts(15),"before":{"target_count":30},"after":{"target_count":40}},
]

# ========== COMMUNICATIONS ==========
communications = []
# Ack for all registrations
for r in registrations:
    drv = next(d for d in drives if d["drive_id"]==r["drive_id"])
    communications.append({
        "comm_id":gid("comm"),"reg_id":r["reg_id"],"template_key":"registration_ack",
        "rendered_content":f"Dear {r['name']}, your registration for {drv['name']} has been received. Registration ID: {r['reg_id']}.",
        "simulated_sent_at":r["registered_at"],"status":"sent",
    })
# Eligibility notifications
for e in eligibility:
    reg = next((r for r in registrations if r["reg_id"]==e["reg_id"]),None)
    if not reg: continue
    drv = next(d for d in drives if d["drive_id"]==e["drive_id"])
    tpl = "eligibility_approved" if e["decision"]=="eligible" else "eligibility_rejected"
    msg = f"Dear {reg['name']}, you have been {'approved as eligible' if e['decision']=='eligible' else 'found ineligible'} for {drv['name']}."
    if e["notes"]: msg += f" Reason: {e['notes']}"
    communications.append({
        "comm_id":gid("comm"),"reg_id":reg["reg_id"],"template_key":tpl,
        "rendered_content":msg,"simulated_sent_at":ts(20),"status":"sent",
    })
# Result notifications
for res in results:
    reg = next((r for r in registrations if r["reg_id"]==res["reg_id"]),None)
    if not reg: continue
    drv = next(d for d in drives if d["drive_id"]==res["drive_id"])
    if res["outcome"]=="passed":
        msg = f"Dear {reg['name']}, congratulations! You passed {drv['name']} with score {res['score']}%. Your voucher will be issued shortly."
    else:
        msg = f"Dear {reg['name']}, you scored {res['score']}% on {drv['name']} (threshold: {res['pass_threshold']}%). Please check retake policies."
    communications.append({
        "comm_id":gid("comm"),"reg_id":reg["reg_id"],
        "template_key":"result_passed" if res["outcome"]=="passed" else "result_failed",
        "rendered_content":msg,"simulated_sent_at":ts(10),"status":"sent",
    })
# Voucher issued notifications
for v in vouchers:
    if v["assigned_to"]:
        reg = next((r for r in registrations if r["reg_id"]==v["assigned_to"]),None)
        if not reg: continue
        drv = next(d for d in drives if d["drive_id"]==v["drive_id"])
        communications.append({
            "comm_id":gid("comm"),"reg_id":reg["reg_id"],"template_key":"voucher_issued",
            "rendered_content":f"Dear {reg['name']}, your voucher for {drv['name']} has been issued. Code: {v['masked_code']}, Expiry: {v['expiry_date']}.",
            "simulated_sent_at":ts(7),"status":"sent",
        })

# ========== SAVE ==========
print("Seeding rich dummy data...")
save("drives.json", drives)
save("registrations.json", registrations)
save("eligibility.json", eligibility)
save("results.json", results)
save("vouchers.json", vouchers)
save("audit_logs.json", audit_logs)
save("communications.json", communications)

# Upload folders
for d in drives:
    for f in ["01_Registrations","02_Attendance","03_Assessments","04_Vouchers","99_Audit"]:
        os.makedirs(os.path.join(UPLOADS_DIR, d["drive_id"], f), exist_ok=True)
print(f"  ✓ Upload folders for {len(drives)} drives")
print("\n✅ Seed complete!")

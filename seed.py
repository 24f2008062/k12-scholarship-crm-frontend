"""
Seed data script for K12 Hunar Scholarship Management CRM.
Populates the required 9 assessment scholarship records idempotently.
"""
from models import db, Scholarship

SEED_SCHOLARSHIPS = [
    # Bihar Records
    {
        "state": "Bihar",
        "name": "Post-Matric Scholarship BC EBC",
        "applicable_class": "Class 11-12",
        "deadline": "30 Sep 2026",
        "status": "Published",
        "provider_name": "Backward & Extremely Backward Classes Welfare Department, Govt. of Bihar",
        "eligibility_criteria": "Must be a permanent resident of Bihar belonging to BC or EBC category, enrolled in recognized Class 11-12 courses with family annual income within prescribed government limits.",
        "benefit": "Tuition fee reimbursement and monthly maintenance allowance based on government rate slabs.",
        "application_link": "http://pmsonline.bih.nic.in"
    },
    {
        "state": "Bihar",
        "name": "Post-Matric Scholarship SC ST",
        "applicable_class": "Class 11-12",
        "deadline": "30 Sep 2026",
        "status": "Draft",
        "provider_name": "Scheduled Caste & Scheduled Tribe Welfare Department, Govt. of Bihar",
        "eligibility_criteria": "Must be a permanent resident of Bihar belonging to SC or ST community, studying in recognized higher secondary schools (Class 11 or 12).",
        "benefit": "Full mandatory fee reimbursement and annual study allowance.",
        "application_link": "http://pmsonline.bih.nic.in"
    },
    {
        "state": "Bihar",
        "name": "Mukhyamantri Balak Balika Protsahan Yojana",
        "applicable_class": "Class 9-10",
        "deadline": "Not stated",
        "status": "Expired",
        "provider_name": "Education Department, Govt. of Bihar",
        "eligibility_criteria": "Students who have passed the 10th board examination with 1st division (or 2nd division for eligible reserved categories) from Bihar School Examination Board (BSEB).",
        "benefit": "One-time direct bank transfer incentive of up to ₹10,000 for academic encouragement.",
        "application_link": "http://medhasoft.bih.nic.in"
    },

    # Haryana Records
    {
        "state": "Haryana",
        "name": "Pre-Matric Scholarship for SC Students",
        "applicable_class": "Class 9-10",
        "deadline": "31 Dec 2026",
        "status": "Published",
        "provider_name": "Welfare of Scheduled Castes and Backward Classes Department, Haryana",
        "eligibility_criteria": "Domicile of Haryana belonging to Scheduled Castes, enrolled as regular students in Class 9 or 10 in recognized schools.",
        "benefit": "Academic grant and book maintenance allowance deposited directly to student account.",
        "application_link": "https://harchhatravratti.highereduhry.ac.in"
    },
    {
        "state": "Haryana",
        "name": "Pre-Matric Scholarship for BC Students",
        "applicable_class": "Class 9-10",
        "deadline": "31 Dec 2026",
        "status": "Draft",
        "provider_name": "Welfare of Scheduled Castes and Backward Classes Department, Haryana",
        "eligibility_criteria": "Haryana resident belonging to Backward Classes (Block A / Block B) with family annual income under the state eligibility threshold.",
        "benefit": "Financial support for tuition fees and school educational supplies.",
        "application_link": "https://harchhatravratti.highereduhry.ac.in"
    },
    {
        "state": "Haryana",
        "name": "Post-Matric Scholarship for SC Students",
        "applicable_class": "Class 11-12",
        "deadline": "31 Dec 2026",
        "status": "Expired",
        "provider_name": "Department of Higher Education, Haryana",
        "eligibility_criteria": "Permanent resident of Haryana belonging to SC category enrolled in Class 11 or 12 post-matric education with valid Parivar Pehchan Patra (PPP).",
        "benefit": "Comprehensive tuition fee waiver plus monthly hosteller/day-scholar allowance.",
        "application_link": "https://harchhatravratti.highereduhry.ac.in"
    },

    # Jharkhand Records
    {
        "state": "Jharkhand",
        "name": "Pre-Matric Scholarship for SC Students",
        "applicable_class": "Class 1-10",
        "deadline": "20 Nov 2026",
        "status": "Published",
        "provider_name": "Scheduled Tribe, Scheduled Caste, Minority and Backward Class Welfare Department, Jharkhand",
        "eligibility_criteria": "Resident of Jharkhand state belonging to Scheduled Caste category studying in Class 1 to 10 in recognized government/aided schools.",
        "benefit": "Direct benefit transfer for uniform, school stationary, and educational support.",
        "application_link": "https://ekalyan.cgg.gov.in"
    },
    {
        "state": "Jharkhand",
        "name": "Pre-Matric Scholarship for ST Students",
        "applicable_class": "Class 1-10",
        "deadline": "20 Nov 2026",
        "status": "Draft",
        "provider_name": "Scheduled Tribe, Scheduled Caste, Minority and Backward Class Welfare Department, Jharkhand",
        "eligibility_criteria": "Resident of Jharkhand state belonging to Scheduled Tribe category studying in Class 1 to 10 in recognized institutions.",
        "benefit": "Stipend and educational allowance distributed through e-Kalyan portal.",
        "application_link": "https://ekalyan.cgg.gov.in"
    },
    {
        "state": "Jharkhand",
        "name": "Pre-Matric Scholarship for BC OBC Students",
        "applicable_class": "Class 1-10",
        "deadline": "20 Nov 2026",
        "status": "Expired",
        "provider_name": "Scheduled Tribe, Scheduled Caste, Minority and Backward Class Welfare Department, Jharkhand",
        "eligibility_criteria": "Resident of Jharkhand state belonging to Backward Classes / OBC category studying in Class 1 to 10 with verified income certificate.",
        "benefit": "Annual educational assistance allowance credited via DBT.",
        "application_link": "https://ekalyan.cgg.gov.in"
    }
]


def seed_database(force=False):
    """
    Seed the database with the 9 assessment scholarship records.
    Idempotent: Only seeds if the database is currently empty (unless force=True).
    """
    count = Scholarship.query.count()
    if count == 0 or force:
        if force and count > 0:
            Scholarship.query.delete()
            db.session.commit()

        for item in SEED_SCHOLARSHIPS:
            scholarship = Scholarship(
                name=item["name"],
                state=item["state"],
                provider_name=item["provider_name"],
                applicable_class=item["applicable_class"],
                eligibility_criteria=item["eligibility_criteria"],
                benefit=item["benefit"],
                deadline=item["deadline"],
                application_link=item["application_link"],
                status=item["status"]
            )
            db.session.add(scholarship)
        db.session.commit()
        print(f"Successfully seeded {len(SEED_SCHOLARSHIPS)} assessment scholarship records.")
        return True
    else:
        print(f"Database already contains {count} records. Skipping seed.")
        return False


if __name__ == "__main__":
    from app import app
    with app.app_context():
        db.create_all()
        seed_database()

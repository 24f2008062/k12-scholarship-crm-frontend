"""
Simple, comprehensive unit and integration tests for K12 Hunar Scholarship CRM.
"""
import unittest
from app import app, db, Scholarship


class ScholarshipCRMTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.client = app.test_client()
        with app.app_context():
            db.create_all()
            from seed import seed_database
            seed_database(force=True)

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_initial_seed_and_counts(self):
        """Verify 9 initial records and dynamic counts."""
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        with app.app_context():
            self.assertEqual(Scholarship.query.count(), 9)
            self.assertEqual(Scholarship.query.filter_by(status="Published").count(), 3)
            self.assertEqual(Scholarship.query.filter_by(status="Draft").count(), 3)
            self.assertEqual(Scholarship.query.filter_by(status="Expired").count(), 3)

    def test_state_and_status_filtering(self):
        """Verify filtering by state and status."""
        res_bihar = self.client.get("/?state=Bihar")
        self.assertEqual(res_bihar.status_code, 200)
        self.assertIn("Post-Matric Scholarship BC EBC", res_bihar.get_data(as_text=True))

        res_haryana = self.client.get("/?state=Haryana")
        self.assertEqual(res_haryana.status_code, 200)
        self.assertIn("Pre-Matric Scholarship for SC Students", res_haryana.get_data(as_text=True))

        res_combined = self.client.get("/?state=Bihar&status=Draft")
        self.assertEqual(res_combined.status_code, 200)
        self.assertIn("Post-Matric Scholarship SC ST", res_combined.get_data(as_text=True))

    def test_add_scholarship_valid_and_invalid(self):
        """Verify adding scholarship validation and persistence."""
        # Invalid (missing required fields)
        res_bad = self.client.post("/scholarships/new", data={"name": ""})
        self.assertEqual(res_bad.status_code, 400)

        # Valid
        payload = {
            "name": "New State Talent Scholarship",
            "state": "Bihar",
            "provider_name": "Education Department",
            "applicable_class": "Class 11-12",
            "eligibility_criteria": "Merit score above 85%",
            "benefit": "₹20,000 allowance",
            "deadline": "31 Dec 2026",
            "application_link": "https://scholarships.gov.in",
            "status": "Published"
        }
        res_good = self.client.post("/scholarships/new", data=payload, follow_redirects=True)
        self.assertEqual(res_good.status_code, 200)
        self.assertIn("Scholarship added successfully.", res_good.get_data(as_text=True))
        with app.app_context():
            self.assertEqual(Scholarship.query.count(), 10)

    def test_edit_scholarship(self):
        """Verify editing a scholarship."""
        payload = {
            "name": "Updated Mukhyamantri Balak Balika",
            "state": "Bihar",
            "provider_name": "Education Dept, Bihar",
            "applicable_class": "Class 9-10",
            "eligibility_criteria": "First division passed",
            "benefit": "₹15,000",
            "deadline": "31 Dec 2026",
            "application_link": "http://medhasoft.bih.nic.in",
            "status": "Published"
        }
        res = self.client.post("/scholarships/3/edit", data=payload, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn("Scholarship updated successfully.", res.get_data(as_text=True))
        with app.app_context():
            s = db.session.get(Scholarship, 3)
            self.assertEqual(s.name, "Updated Mukhyamantri Balak Balika")
            self.assertEqual(s.status, "Published")

    def test_status_update(self):
        """Verify inline status update."""
        res = self.client.post("/scholarships/1/status", data={"status": "Draft"}, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn("Scholarship status updated successfully.", res.get_data(as_text=True))
        with app.app_context():
            s = db.session.get(Scholarship, 1)
            self.assertEqual(s.status, "Draft")

    def test_student_preview_and_404(self):
        """Verify preview and 404 behavior."""
        res = self.client.get("/scholarships/1/preview")
        self.assertEqual(res.status_code, 200)
        self.assertIn("Post-Matric Scholarship BC EBC", res.get_data(as_text=True))
        self.assertIn("Financial Grant & Benefits", res.get_data(as_text=True))

        res_404 = self.client.get("/scholarships/9999/preview")
        self.assertEqual(res_404.status_code, 404)


if __name__ == "__main__":
    unittest.main()

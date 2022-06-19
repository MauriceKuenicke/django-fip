from django.test import TestCase
from .models import PLAN, USER
from django.utils import timezone
from django.urls import reverse
import datetime

class UserModelTests(TestCase):
    
    def test_was_published_recently_with_future_plan(self):
        """
        was_published_recently() returns False for plan whose created_at CREATED_AT
        is in the future.
        """
        u = USER(USERNAME="TestCaseUser", USERPASSWORD='12345678')
        time = timezone.now() + datetime.timedelta(days=30)
        future_plan = PLAN(PLANNAME='TestPlan', USERID=u, CREATED_AT=time)
        self.assertIs(future_plan.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose CREATED_AT date
        is older than 7 day.
        """
        u = USER(USERNAME="TestCaseUser", USERPASSWORD='12345678')
        time = timezone.now() - datetime.timedelta(days=7, seconds=1)
        old_plan =PLAN(PLANNAME='TestPlan', USERID=u, CREATED_AT=time)
        self.assertIs(old_plan.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose CREATED_AT date
        is within the last day.
        """
        u = USER(USERNAME="TestCaseUser", USERPASSWORD='12345678')
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = PLAN(PLANNAME='TestPlan', USERID=u, CREATED_AT=time)
        self.assertIs(recent_question.was_published_recently(), True)


class PlanViewTests(TestCase):
    def test_no_user(self):
        """
        Display 404 if no user exists.
        """
        response = self.client.get(reverse('financial_planner:plan', args=('TestUser', 1)))
        self.assertEqual(response.status_code, 404)

    def test_no_plan(self):
        """
        Display 404 if no plan exists for a given user.
        """
        u = USER(USERNAME="TestUser", USERPASSWORD='12345678')
        u.save()
        response = self.client.get(reverse('financial_planner:plan', args=(u.USERNAME, 1)))
        self.assertEqual(response.status_code, 404)

    def test_view_loads_successfully(self):
        """
        Checks if the plan view can be loaded successfully.
        """
        u = USER(USERNAME="TestUser", USERPASSWORD='12345678')
        u.save()
        p = PLAN(PLANNAME='TestPlan', USERID=u, CREATED_AT=timezone.now())
        p.save()
        response = self.client.get(reverse('financial_planner:plan', args=(u.USERNAME, p.PLANID)))
        self.assertEqual(response.status_code, 200)
        
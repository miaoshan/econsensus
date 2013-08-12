from selenium.webdriver.common.by import By
from django_dynamic_fixture import G
from organizations.models import Organization
from publicweb.models import Decision
from guardian.shortcuts import assign_perm
from selenium.webdriver.support.wait import WebDriverWait
from publicweb.tests.selenium.selenium_testcase import SeleniumTestCase 
from actionitems.models import ActionItem
        
class AddActionItemsTest(SeleniumTestCase):
    def setUp(self):
        self.login()
        self.organization = G(Organization)
        self.organization.add_user(self.user)
        assign_perm('edit_decisions_feedback',
               self.user, self.organization)
            
    def test_action_item_form_replaces_add_action_item_button(self):
        # self.selenium is the name of the web driver for the class
        decision = G(Decision, organization=self.organization, 
              author=self.user, editor=self.user)
        driver = self.selenium
        driver.get("%s/item/detail/%d/" % (
           self.live_server_url, decision.id))
        
        driver.find_element_by_css_selector("a.button.add_actionitem").click()
        
        WebDriverWait(driver, 10).until(
            lambda x: x.find_element_by_id("id_deadline"))
        
        self.assertTrue(
            self.is_element_present(
                By.CSS_SELECTOR, "#actionitem_add_anchor > form"))
        self.assertFalse(
             self.is_element_present(
                 By.CSS_SELECTOR, "#actionitem_add_anchor > .add_actionitem"))
    
    def test_action_item_form_cancel_recreates_button_without_adding_new_item(self):
        expected_action_items = list(ActionItem.objects.all())
        
        decision = G(Decision, organization=self.organization, 
              author=self.user, editor=self.user)
        driver = self.selenium
        driver.get("%s/item/detail/%d/" % (
           self.live_server_url, decision.id))
        
        driver.find_element_by_css_selector("a.button.add_actionitem").click()
        
        WebDriverWait(driver, 10).until(
            lambda x: x.find_element_by_id("id_deadline"))
        
        driver.find_element_by_css_selector(".actionitem_cancel").click()

        WebDriverWait(driver, 10).until(
            lambda x: x.find_element_by_css_selector("a.button.add_actionitem"))
        
        actual_action_items = list(ActionItem.objects.all())
        self.assertTrue(
             self.is_element_present(
                 By.CSS_SELECTOR, "#actionitem_add_anchor > .add_actionitem"))
        self.assertFalse(
            self.is_element_present(
                By.CSS_SELECTOR, "#actionitem_add_anchor > form"))
        self.assertListEqual(expected_action_items, actual_action_items)
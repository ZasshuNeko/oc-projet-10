from django.test import TestCase, Client
from django.urls import reverse
import unittest
import os
from django.contrib.auth.models import User

from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By


# Create your tests here.
class TestAuth(TestCase):
	""" Mise en place des tests """

	def setUp(self):
		""" Mise en place des bases de données """
		test_user1 = User.objects.create_user(
			username="testuser1", password='testtest')
		test_user2 = User.objects.create_user(
			username="testuser2", password='testtest')

		test_user1.save()
		test_user2.save()

	def test_log_in(self):
		''' Test de la connexion
		Connection test '''
		default_data = {"log_id": "testuser1", "pwd": "testtest"}
		test_login = self.client.post('/auth_app/log_in/', default_data)
		self.assertEqual(test_login.status_code, 302)
		self.assertRedirects(test_login, '/polls/')

	def test_log_out(self):
		''' Test la deconnexion
		Test the disconnection '''
		login = self.client.login(username="testuser2", password='testtest')
		response = self.client.get(reverse('logout'))
		self.assertIsNone(response.context)
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, '/polls/')

	def test_signeit(self):
		''' Test la possibilité de s'inscrire
		Test the possibility of registering '''
		default_data = {
			"username": "testuser3",
			"email": "unittest@test.com",
			"pass_first": "1234testtest",
			"pass_second": "1234testtest"}
		test_signit = self.client.post('/auth_app/signe_it/', default_data)
		self.assertEqual(test_signit.status_code, 200)
		self.assertTemplateUsed(test_signit, 'signe_it.html')

	def test_signeiterror(self):
		''' Test si une erreur est renseigné
		Test if an error is entered '''
		default_data = {
			"username": "testuser1",
			"email": "unittest@test.com",
			"pass_first": "1234testtest",
			"pass_second": "1234testtest"}
		test_signit = self.client.post('/auth_app/signe_it/', default_data)
		self.assertEqual(test_signit.status_code, 200)
		self.assertTemplateUsed(test_signit, 'signe_it.html')


class AccountTestCase(LiveServerTestCase):
	''' Test Selenium '''

	def setUp(self):
            ''' Mise en place des paramètres
            Setting parameters BROWSER '''
            browserstack_local_identifier = os.getenv("BROWSERSTACK_LOCAL_IDENTIFIER")
            BROWSERSTACK_URL = 'https://nicolasmazaleyra1:tt8A68XfsXBeJxgMrpB5@hub-cloud.browserstack.com/wd/hub'

            desired_cap = {
                'browserstack.local': 'true',
                'browserstack.localIdentifier': browserstack_local_identifier,
                'os' : 'Windows',
                'os_version' : '10',
                'browser' : 'Chrome',
                'browser_version' : '80',
                'name' : "nicolasmazaleyra1's First Test"
            }

            self.selenium = webdriver.Remote(
                command_executor=BROWSERSTACK_URL,
                desired_capabilities=desired_cap
            )
            super(AccountTestCase, self).setUp()

	def tearDown(self):

		self.selenium.quit()
		super(AccountTestCase, self).tearDown()

	def test_register(self):

		''' Appel la page d'enregistrement
		Call up the registration page '''
		selenium = self.selenium
		# Opening the link we want to test
		selenium.get('http://35.180.208.255/auth_app/signe_it/')
		# find the form element
		username = selenium.find_element_by_id('id_username')
		email = selenium.find_element_by_id('id_email')
		password1 = selenium.find_element_by_id('id_pass_first')
		password2 = selenium.find_element_by_id('id_pass_second')

		submit = selenium.find_element_by_name('register')

		# Fill the form with data
		username.send_keys('TestSelenium')
		email.send_keys('yusuf@qawba.com')
		password1.send_keys('test123456')
		password2.send_keys('test123456')

		# submitting the form
		submit.send_keys(Keys.RETURN)
		selenium.implicitly_wait(20)

		# check the returned result
		self.assertEqual(selenium.find_element_by_css_selector("p#information").get_attribute(
			"innerHTML").splitlines()[0], "Vous avez maintenant un compte sur notre site")

	def test_signeUp(self):
		''' Test de connexion
		Connection test '''
		selenium = self.selenium
		# Opening the link we want to test
		selenium.get('http://35.180.208.255/auth_app/log_in/')
		# find the form element
		username = selenium.find_element_by_id('id_log_id')
		password = selenium.find_element_by_id('id_pwd')

		submit = selenium.find_element_by_name('login')

		# Fill the form with data
		username.send_keys('TestSelenium')
		password.send_keys('test123456')

		# submitting the form
		submit.send_keys(Keys.RETURN)
		selenium.implicitly_wait(20)
		name_index = "Bonjour TestSelenium"
		# check the returned result
		self.assertEqual(selenium.find_element_by_css_selector(
			"h1#info_login").get_attribute("innerHTML").splitlines()[0], name_index)

import requests
import unittest
from menus import getMod, putMod, postMod, deleteMod

class TestRESTMethods(unittest.TestCase):
    def test_getMod_api_status(self):
        self.assertEqual(200,getMod('tech_pack').status)
    
    def test_getMod_invalid_mod_id(self):
        self.assertEqual(404,getMod('oejgweojgowpeg').status)

    def test_postMod_success(self):
        mod_metadata = {
            "mod_id": "tech_pack",
            "username": "TechEnthusiast88",
            "json": "{}",
            "version": "1.0.5",
            "mod_name": "Tech Gadgets Mod"
        }
        self.assertEqual(200,postMod(mod_metadata).status)
    
    def test_putMod_invalid_mod_id(self):
        mod_metadata = {
            "mod_id": "oejgweojgowpeg",
            "username": "ThatRobin3001",
            "json": "{}",
            "version": "1.0.0",
            "mod_name": "Random Test Mod"
        }
        self.assertEqual(400,putMod('oejgweojgowpeg', {}).status)

    def test_deleteMod_invalid_mod_id(self):
        self.assertEqual(404,deleteMod('oejgweojgowpeg').status)

    

    
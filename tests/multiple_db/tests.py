from django.test import TestCase
from haystack.exceptions import NotRegistered, AlreadyRegistered

class AutoSiteRegistrationTestCase(TestCase):
    def setUp(self):
        super(AutoSiteRegistrationTestCase, self).setUp()
        
        # Stow.
        import haystack
        self.old_site = haystack.site
        test_site = haystack.sites.SearchSite()
        haystack.site = test_site
        
        haystack.autodiscover()
    
    def test_registrations(self):
        from haystack import backend
        sb = backend.SearchBackend()
        self.assertEqual(len(sb.site.get_indexed_models()), 2)
        
        from haystack import site
        self.assertEqual(len(site.get_indexed_models()), 2)

        from multiple_db.models import Foo, Bar
        self.assertEqual(len(site.get_model_databases(Foo)), 0)
        self.assertEqual(len(site.get_model_databases(Bar)), 2)

class ManualSiteRegistrationTestCase(TestCase):
    def test_registrations(self):
        from haystack import backend
        sb = backend.SearchBackend()
        self.assertEqual(len(sb.site.get_indexed_models()), 2)
        
        from haystack import site
        self.assertEqual(len(site.get_indexed_models()), 2)
        
        from multiple_db.models import Foo, Bar
        
        # Number of databases per model.
        self.assertEqual(len(site.get_model_databases(Foo)), 0)
        self.assertEqual(len(site.get_model_databases(Bar)), 2)
        
        # Repeated registration with default db after non-default db.
        self.assertRaises(AlreadyRegistered, site.register, Bar)
        site.unregister(Bar)
        self.assertEqual(len(sb.site.get_indexed_models()), 1)
        self.assertRaises(NotRegistered, site.get_model_databases, Bar)
        
        # Repeated registration with non-default db after default db.
        site.register(Foo, db='db1')
        self.assertEqual(len(sb.site.get_model_databases(Foo)), 1)
        site.register(Foo, db='db1')
        self.assertEqual(len(sb.site.get_model_databases(Foo)), 1)
        
        # Unregistering with non-registered db.
        self.assertRaises(NotRegistered, site.unregister, Foo, db='db2')
        
        # Unregister a model completely.
        site.unregister(Foo)
        
        # Unregister a non-registered model with db parameter.
        self.assertRaises(NotRegistered, site.unregister, Foo, db='db1')
        
        # Unregister a non-registered model.
        self.assertRaises(NotRegistered, site.unregister, Foo)
        
        # No models left
        self.assertEqual(len(sb.site.get_indexed_models()), 0)
        self.assertEqual(len(site.get_indexed_models()), 0)
        
        # Registration with non-existing database.
        self.assertRaises(ValueError, site.register, Bar, db='non-existing-db')
        site.register(Bar, db='db1')
        site.register(Bar, db='db2')
        
        # Drain databases to completely unregister the model.
        self.assertEqual(len(site.get_model_databases(Bar)), 2)
        site.unregister(Bar, db='db1')
        self.assertEqual(len(site.get_model_databases(Bar)), 1)
        site.unregister(Bar, db='db2')
        self.assertRaises(NotRegistered, site.get_model_databases, Bar)


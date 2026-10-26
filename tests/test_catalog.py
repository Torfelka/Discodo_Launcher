import json,tempfile,unittest
from pathlib import Path
from catalog import Catalog,POPULAR_GAMES,MIN_CATALOG_SIZE,FEATURED_LIMIT
class CatalogTests(unittest.TestCase):
 def test_catalog_target_is_at_least_50000(self):self.assertEqual(MIN_CATALOG_SIZE,50000);self.assertEqual(FEATURED_LIMIT,500)
 def test_featured_ids_are_unique(self):self.assertGreaterEqual(len(POPULAR_GAMES),40);self.assertEqual(len(POPULAR_GAMES),len(set(POPULAR_GAMES)))
 def test_cache_reads_60000_entries(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/"apps.json";p.write_text(json.dumps([{"appid":i+1,"name":f"Game {i+1}"} for i in range(60000)]),encoding="utf-8");self.assertEqual(len(Catalog(p).load_cached()),60000)
 def test_blank_names_are_skipped(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/"apps.json";p.write_text('[{"appid":1,"name":"Valid"},{"appid":2,"name":""}]',encoding="utf-8");self.assertEqual([g.name for g in Catalog(p).load_cached()],["Valid"])
if __name__=="__main__":unittest.main()

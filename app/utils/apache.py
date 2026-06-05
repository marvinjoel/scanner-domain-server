import os
import re


class ApacheExtractor:
    
    @staticmethod
    def get_domains(conf_dir: str) -> list:
        domains = set()
        pattern = re.compile(r'^\s*(ServerName|ServerAlias)\s+(.+)$', re.IGNORECASE)
        
        if not os.path.exists(conf_dir):
            print(f"[WARN] El directorio de Apache {conf_dir} no existe.")
            return []

        for root, _, files in os.walk(conf_dir):
            for file in files:
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        for line in f:
                            match = pattern.search(line)
                            if match:
                                raw_line = match.group(2).split('#')[0].strip()
                                raw_domains = raw_line.split()
                                for d in raw_domains:
                                    d = d.strip()
                                    if d and d != 'localhost' and not d.startswith('_'):
                                        domains.add(d)
                except (IOError, UnicodeDecodeError):
                    continue
                    
        return sorted(list(domains))
import os
import re


class NginxExtractor:
    
    @staticmethod
    def get_domains(conf_dir: str) -> list:
        domains = set()
        pattern = re.compile(r'^\s*server_name\s+(.+);')
        
        if not os.path.exists(conf_dir):
            return []

        for root, _, files in os.walk(conf_dir):
            for file in files:
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        for line in f:
                            match = pattern.search(line)
                            if match:
                                raw_domains = match.group(1).replace(';', '').split()
                                for d in raw_domains:
                                    d = d.strip()
                                    if d and d != 'localhost' and not d.startswith('_'):
                                        domains.add(d)
                except (IOError, UnicodeDecodeError):
                    continue
        return sorted(list(domains))